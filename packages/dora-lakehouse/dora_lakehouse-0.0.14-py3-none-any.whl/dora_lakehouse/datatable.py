# -*- coding: utf-8 -*-
#
# Copyright 2021 Compasso UOL
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Lakehouse Data Table"""
import os
import re
from pathlib import Path
from time import sleep
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import concat_ws
from pyspark.sql.functions import lit as spark_lit
from pyspark.sql.functions import expr as spark_expr
from pyspark.sql.functions import col as spark_col
from dora_lakehouse.catalog import Table, Column
from dora_lakehouse.utils import logger, sanitize

class PseudoColumn(Column):
    """Data table pseudo columns. Used to data control"""
    def representation(self) -> dict:
        return dict(name=self.name,type=self.data_type)

class DataTable(DataFrame):
    """Table data representation. Extends Spark Dataframe"""
    # List of pseudo columns
    PSEUDO_COLUMNS={
        'UPDT_COL':PseudoColumn(os.environ.get('UPDT_COL','__dora_last_update__'),"timestamp",nulable=False),
        'HASH_COL':PseudoColumn(os.environ.get('HASH_COL','__dora_file_hash__'),"string",nulable=False),
        'DEL_COL' :PseudoColumn(os.environ.get('DEL_COL' ,'__dora_delete__'),"bool",nulable=False),
        'IDX_COL' :PseudoColumn(os.environ.get('IDX_COL' ,'__index_level_0__'),"string",nulable=False)}

    @classmethod
    def _group_names_(cls, names:list, regex:str=r"(max|min)\((.+)\)"):
        """ After using agregation functions Spark change the column original name
        This function receives the list of names and by regular expression get the original column name
        :param names: data frame column names
        :param regex: regular expression
        :return: list of names
        """
        for _col in names:
            try:
                match = re.finditer(regex, _col, re.IGNORECASE)
                yield next(match).group(2)
            except StopIteration:
                yield _col
    @classmethod
    def empty_df(cls, context, table:Table):
        """Create an table compatible empty data frame"""
        _columns = table.columns + [_col for _, _col in cls.PSEUDO_COLUMNS.items()]
        _schema = Table.create_schema(_columns)
        return context.createDataFrame(context.spark_context.emptyRDD(), _schema)

    @classmethod
    def _update_sequence_(cls, dirpath:Path, increment) -> int:
        """Update table sequence"""
        seq_file = os.path.join(dirpath, "sequence")
        Path(seq_file).touch() # Create file if not exists
        with open(seq_file, 'r') as reader:
            try:
                value = int(reader.read())
            except ValueError:
                value = 0
                logger.info("SEQUENCE:CREATED")
            finally:
                if increment > 0:
                    with open(seq_file, 'w') as writer:
                        writer.write(str(increment+value))
            logger.info("SEQUENCE:VALUE:%s",value)
            return value
    
    @classmethod
    def _sequence_(cls, table:Table, increment:int=-1, attempts:int=10) -> int:
        """Get and update table sequence metadata
        :param table: table where the sequence will be apply
        :param increment: sequence increment to update, if greater then 0.
        :param attempts: max number of attempts to get the sequence value
        :return: sequence value before update
        """
        dirpath = Path(f"{os.environ['METADIR']}/{table.database.name}/{table.name}")
        lock = os.path.join(dirpath, ".lock")
        for attempt in range(attempts):
            try:
                os.makedirs(lock, exist_ok=False)
                logger.debug("SEQUENCE:LOCK:%s",lock)
                try:
                    return cls._update_sequence_(dirpath, increment)
                finally:
                    os.rmdir(lock)
                    logger.debug("SEQUENCE:UNLOCK:%s",lock)
            except FileExistsError:
                logger.debug("SEQUENCE:ATTEMPT:%s",attempt)
                sleep(1)
        raise ValueError(f"Sequece Unreachable after {attempts} attempts")
    
    @classmethod
    def _indexing_(cls, dataframe:DataFrame, table:Table) -> DataFrame:
        """Apply index to the dataframe"""
        index_column = cls.PSEUDO_COLUMNS['IDX_COL']
        idx = [spark_col(i.name) for i in table.indexes]
        if table.update == 'append':
            _expr = f"(row_number() OVER (PARTITION BY 1 ORDER BY 1))+{cls._sequence_(table,dataframe.count())}"
            return dataframe.withColumn(index_column.name, spark_expr(_expr))
        if len(idx)>0:
            return dataframe.withColumn(index_column.name, concat_ws('##', *idx))
        return dataframe.withColumn(index_column.name, spark_expr("uuid()"))
    
    @classmethod
    def _filter_(cls, rdf:DataFrame, table:Table) -> DataFrame:
        """Filter dataframe by table definitions"""
        # Name of all columns used to filter
        att = [i.name for i in table.indexes]
        # If the data frame has no index
        if len(att)==0:
            return [rdf, None]
        # Create an dataframe grouped by index to filter the original by tiebreacks
        gdf = rdf.where('1=1')
        for tbk in table.tiebreaks:
            gdf = gdf.groupBy(att).agg({tbk.name:tbk.tiebreak[1]})
            gdf = gdf.toDF(*DataTable._group_names_(gdf.columns))
            att.append(tbk.name)
            # Create the WHERE clausule
            whr = [rdf[att[i]]==gdf[att[i]] for i in range(len(att))]
            # Filter by tiebreack dataframe
            fdf = rdf.join(gdf,on=whr,how='inner')
            gdf = fdf.select([rdf[c] for c in rdf.columns])
        sdf = gdf.alias('s')
        # Remove duplicate rows
        col_idx = [i.name for i in table.indexes]
        edf = sdf.groupBy(col_idx).count().filter('count>1').alias('r')
        if edf.count()>0:
            logger.error(f"Index contraint violation. Check table configurations")
            whr = [sdf[col_idx[i]]==edf[col_idx[i]] for i in range(len(col_idx))]
            return [
                sdf.join(edf,on=whr,how='anti').select('s.*'),
                edf.join(sdf,on=whr,how='inner').select('s.*')]
        return [sdf.select('s.*'), None]
    
    @classmethod
    def column_equalization(cls, data_frame:DataFrame, table:Table) -> DataFrame:
        """Compare the columns (by name) in the table definition of loaded dataframe.
        1. Add all the missing columns on the data frame, with None values
        2. Remove all columns not related with the table definition
        :param rdf: raw data frame
        :return: equalized data frame
        """
        col_df = [sanitize(_col) for _col in data_frame.columns]
        for _col in table.columns:
            if _col.name not in col_df: # If this column not in the dataframe
                data_frame = data_frame.withColumn(_col.name, spark_lit(None).cast(_col.sparktype))
            else: # apply the type constraint
                data_frame = data_frame.withColumn(_col.name,data_frame[_col.name].cast(_col.sparktype))
        dataframe, dataframe_e = cls._filter_(data_frame.dropDuplicates(), table)
        # Verify pseudo columns
        if table.hash_def is None:
            raise ValueError(f'Cant find data hash function on table "{table.full_name}".\n{table.representation()}')
        _hash_def=f"lpad(abs(ceil({table.hash_def})),{os.environ.get('NAME_SIZE','18')},'0')"
        logger.debug("HASH:DEFINITION:%s", _hash_def)
        #TODO:Create an process to anonimization when the row is marked as deleted
        dataframe = cls._indexing_(dataframe\
            .withColumn(cls.PSEUDO_COLUMNS['HASH_COL'].name, spark_expr(_hash_def))\
            .withColumn(cls.PSEUDO_COLUMNS['UPDT_COL'].name, spark_expr("now()"))\
            .withColumn(cls.PSEUDO_COLUMNS['DEL_COL'].name, spark_expr(f"ifnull(({table.delete}),False)")),table)
        # Apply the same function used on table creation for all df columns
        col_ps = [cls.PSEUDO_COLUMNS[_key] for _key in cls.PSEUDO_COLUMNS]
        col_tb = [_col.name for _col in table.columns+col_ps]
        for _col in col_df: # For each column of the raw dataframe
            if _col not in col_tb: # if someone are not in the table definition
                logger.warning("DROP:COL:%s", _col)
                dataframe = dataframe.drop(_col) # Remove the column
        return [
            dataframe.select(col_tb),
            dataframe_e
        ]

    def __init__(self, sparkContext, dataFrame, table:Table, **kwargs):
        sdf, edf = self.column_equalization(dataFrame, table)
        _columns = table.columns + [_col for _, _col in DataTable.PSEUDO_COLUMNS.items()]
        super().__init__(sparkContext.createDataFrame(sdf.rdd, Table.create_schema(_columns))._jdf, sparkContext)
        self.table = table
        self.context = sparkContext
        self.master_dataframe = kwargs.get('master')
        self.error_dataframe = edf
        self.hash_list = kwargs.get('hash')
    
    @property
    def keys(self):
        """Return an list of keys, used for join or ordering"""
        _keys = [_col.name for _col in self.table.indexes]
        if len(_keys)==0: #If table dont have index
            _keys = [DataTable.PSEUDO_COLUMNS['IDX_COL'].name] # Use meta column
        return _keys
    @property
    def hashs(self):
        """List of hash IDs"""
        hash_col=DataTable.PSEUDO_COLUMNS['HASH_COL'].name
        if self.hash_list is None:
            self.hash_list = [_hk[hash_col] for _hk in self.select(hash_col).distinct().collect()]
        return self.hash_list
    @property
    def master(self):
        """Master dataframe"""
        return self.context.load_master(self.hashs, self.table)
    @property
    def errors(self):
        """Errors dataframe"""
        if self.error_dataframe is None:
            return DataTable.empty_df(self.context,self.table)
        return self.error_dataframe
    
    def update(self, data_table:DataFrame=None):
        """Merge data and write the updates"""
        idx_col = DataTable.PSEUDO_COLUMNS['IDX_COL'].name
        # Master data frame
        if data_table is None:
            data_table = self.master
        else:
            if data_table.table.checksum() != self.table.checksum():
                logger.error("Expected:%s\nReceives:%s",self.table, data_table.table)
                raise ValueError("Incompatible table definitions")
        mdf = data_table.alias('r') # right table on join
        # Staged data frame
        sdf = self.alias('l') # left table on join
        # Full outer join data frame
        join_condition = [(spark_col(f'r.{idx}')==spark_col(f'l.{idx}')) for idx in self.keys]
        if self.table.update == 'append': # IDX_COL have the sequence
            join_condition.append((spark_col(f'r.{idx_col}')==spark_col(f'l.{idx_col}')))
        fdf = mdf.join( sdf, on=join_condition, how='full_outer')
        # Out of scope
        offset = fdf.where(" AND ".join([f'l.{idx} IS NULL' for idx in self.keys])).select('r.*')
        if self.table.update == 'overwrite': # If table update mode is 'overwrite'
            offset = offset.withColumn(DataTable.PSEUDO_COLUMNS['DEL_COL'].name, spark_lit(True)) # Mark all lines as Deleted
        # New lines
        inserts = fdf.where(" AND ".join([f'r.{idx} IS NULL' for idx in self.keys])).select('l.*')
        # Update common data
        unchange_filter = ['1=2'] # List of filters, starts with False
        update_filter = ['1=1'] # List of filters, starts with True
        for _col in self.table.tiebreaks: # If there is some criteria
            if str(_col.tiebreak[1]).lower()=='max':
                unchange_filter.append(f"""r.{_col.name} > l.{_col.name}""")
                update_filter.append(f"""r.{_col.name} <= l.{_col.name}""")
            elif str(_col.tiebreak[1]).lower()=='min':
                unchange_filter.append(f"""r.{_col.name} < l.{_col.name}""")
                update_filter.append(f"""r.{_col.name} >= l.{_col.name}""")
            else:
                logger.error("Tiebreack option '%s' not implemented.", _col.tiebreak)
                raise NotImplementedError
        unchange = fdf.filter(spark_col(f'l.{idx_col}').isNotNull()).where(" OR ".join(unchange_filter)).select('r.*')
        updates  = fdf.filter(spark_col(f'l.{idx_col}').isNotNull()).where(" AND ".join(update_filter)).select('l.*')
        # Update dataframe
        self._jdf = offset.union(inserts).union(unchange.union(updates)).dropDuplicates()._jdf
        return self
    def stage(self) -> list:
        """Save Datatable on lake
        :return: hash keys"""
        return self.context.write_stage(self)
    def save(self):
        """Save Datatable on lake"""
        if not self.table.save():
            raise ValueError(f"Cant save table {self.table.full_name}")
        return self.context.write_refined(self)
        