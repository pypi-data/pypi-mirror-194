





import datetime
import os
from typing import Iterable, Union,TYPE_CHECKING
from dataclasses import dataclass

import colemen_utils as c
from apricity.objects.Database import management_database,content_database,meta_database,business_database
# from apricity.objects.Column import Column
import apricity.objects.Log as log
from apricity.settings.master_control import default_get_limit,default_get_offset
# import apricity.susurrus.CacheFile as _cache_file
_ebase = None
# from apricity.objects.EntityBase import EntityBase as _ebase
# if TYPE_CHECKING:

@dataclass
class SusurrusBase:
    table_name:str = None
    '''The name of the table that this susurrus represents'''

    schema_name:str = None
    '''The name of the schema that the table belongs to.'''

    primary_column_name:str = None
    '''The name of the primary index for this table'''

    hash_id_column_name:str = "hash_id"
    '''The name of the hash_id index for this table'''
    hash_id_prefix:str = None
    '''The string prepended to the hash_id when it is generated.'''

    private_keys = []
    '''A list of column names that should not be shared'''

    required_create_keys = []
    '''A list of column names that must be provided to create a new record.'''

    # table_columns = None
    # column_names = None

    # columns = None
    # '''A list of column instances for the table this susurrus represents.'''

    _cache = None
    '''This susurrus's cache file instance'''

    has_deleted_column:bool = None
    has_timestamp_column:bool = None
    has_modified_column:bool = None
    _sql_table_string:str = None

    cache_dir_path:str = f"{os.getcwd()}/susurrus_cache"
    '''The file path to the susurrus cache directory.'''

    cache_path:str = f"{os.getcwd()}/susurrus_cache"
    '''The file path to this susurrus's cache file.'''

    def __init__(self):
        self.data = {}
        self.__database = None
        self._table = None
        
        # self.__database = management_database()

    def _connect_to_database(self):
        '''
            Connect to the appropriate database for this susurrus.
            ----------

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-05-2022 09:53:56
            `memberOf`: SusurrusBase
            `version`: 1.0
            `method_name`: _connect_to_database
            * @TODO []: documentation for _connect_to_database
        '''
        if "management" in self.schema_name.lower():
            self.__database = management_database()
        if "content_database" in self.schema_name.lower():
            self.__database = content_database()
        if "meta" in self.schema_name.lower():
            self.__database = meta_database()
        if "business_database" in self.schema_name.lower():
            self.__database = business_database()

    def timestamp(self):
        return int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())

    def filter_dict_by_columns(self,data:dict):
        columns = [x.name for x in self._table.columns]
        output = {}
        data = c.obj.keys_to_snake_case(data)
        for k,v in data.items():
            if k in columns:
                output[k] = v
        return output

    def gen_hash_id(self)->str:
        '''
            Generate a hash_id specific to this susurrus's table.

            ----------

            Return {str}
            ----------------------
            A new hash_id for this table.

            user_KlMO8NB1i2tJ

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-05-2022 09:50:53
            `memberOf`: SusurrusBase
            `version`: 1.0
            `method_name`: gen_hash_id
            * @TODO []: documentation for gen_hash_id
        '''
        return f"{self.hash_id_prefix}_{c.rand.rand(24)}"

    def submitDB(self,data:Union[dict,_ebase])->Union[dict,bool]:
        '''
            Insert a new row to this susurrus's table.

            ----------

            Arguments
            -------------------------
            `data` {dict,Entity}
                A dictionary of data to submit to the table.
                This can also be an entity which extends the EntityBase Class.


            Return {dict,bool}
            ----------------------
            The submitted data if successful, False otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-05-2022 09:30:25
            `memberOf`: SusurrusBase
            `version`: 1.0
            `method_name`: submitDB
            * @xxx [12-05-2022 09:31:50]: documentation for submitDB
        '''
        # @Mstep [IF] if an entity is provided.
        if isinstance(data,_ebase):
            # @Mstep [] retrieve the entity's data dictionary
            data = data.data

        inq = self._table.insert_query()
        inq.add_column(data)
        inq.correlate_to_table = True
        inq.return_row=True
        log.add("Submitting to database","info")
        return inq.execute()

        # data = self.__database.correlate_to_table(self.table_name,data,crud="create",cerberus_validate=True)
        # # data = self.__database.correlate_to_table(self.table_name,data,crud="create")
        # # # data = self.filter_dict_by_columns(data)
        # # # @Mstep [IF] if this susurrus has a timestamp column
        # # if self.has_timestamp_column:
        # #     # @Mstep [IF] if the timestamp is not set in the data dictionary.
        # #     if 'timestamp' not in data:
        # #         # @Mstep [] set the timestamp key on the data dictionary.
        # #         data['timestamp'] = int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())

        # # # @Mstep [IF] if this susurrus has a modified_timestamp column
        # # if self.has_modified_column:
        # #     # @Mstep [IF] if the modified_timestamp is not set in the data dictionary.
        # #     if 'modified_timestamp' not in data:
        # #         # @Mstep [] set the modified_timestamp key on the data dictionary.
        # #         data['modified_timestamp'] = int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())


        # # if self.has_create_keys(data) is False:
        # #     return False
        # result = self._table.insert(data,return_row=True)
        # # @Mstep [] execute the submission.
        # # result = self.__database.insert_to_table(,self.table_name)
        # # if isinstance(result,(int)):
        # #     data[self.primary_column_name] = result
        # #     result = data
        # # @Mstep [RETURN] return the submission result.
        # return result

    def selectDB(self,data:dict):
        # @Mstep [] instantiate a new select query
        selq = self._table.select_query()
        # @Mstep [] set the limit and offset on the query.
        selq.limit = c.obj.get_arg(data,["limit"],default_get_limit,(int))
        selq.offset = c.obj.get_arg(data,["offset"],default_get_offset,(int))

        # @Mstep [IF] if no data is provided
        if isinstance(data,(dict)) is False:
            # @Mstep [RETURN] execute the query (select everything up to the limit & offset)
            return selq.execute()

        # @Mstep [] convert the data keys to snake case.
        data = c.obj.keys_to_snake_case(data)

        # @Mstep [IF] if the table has a deleted column
        if self._table.has_deleted_column:
            # @Mstep [] set the include_deleted option on the query.
            selq.include_deleted = c.obj.get_arg(data,["include_deleted"],False,(bool,int))
        # @Mstep [IF] if the table has a timestamp column
        if self._table.has_timestamp_column:
            # @Mstep [] get the start_timestamp and end_timestamp from the data
            start_time = c.obj.get_arg(data,["start_time","start_timestamp"],None,(int))
            end_time = c.obj.get_arg(data,["end_time","end_timestamp"],None,(int))

            # @Mstep [IF] if the start_time and end_time are provided.
            if start_time is not None and end_time is not None:
                if start_time == end_time:
                    pass
                if start_time > 0 and end_time > 0:
                    if end_time < start_time:
                        tmp = end_time
                        end_time = start_time
                        start_time = tmp
                # @Mstep [] add WHERE timestamp between start_time and end_time
                selq.add_where("timestamp",[start_time,end_time],"between")
            # @Mstep [IF] if the start_time is provided and end_time is not.
            if start_time is not None and end_time is None:
                # @Mstep [] add WHERE timestamp >= start_time
                selq.add_where("timestamp",start_time,">=")
            # @Mstep [IF] if the start_time is not provided and end_time is.
            if start_time is None and end_time is not None:
                # @Mstep [] add WHERE timestamp <= start_time
                selq.add_where("timestamp",end_time,"<=")

        # @Mstep [LOOP] iterate the table's columns
        for col in self._table.columns:
            # @Mstep [IF] if the column name is in the data
            if col.data.column_name in data:
                # @Mstep [] add WHERE column_name = data[column_name]
                selq.add_where(col.data.column_name,data[col.data.column_name],"=")
        return selq.execute()


    def updateDB(self,data:Union[dict,_ebase]):
        log.add("update database.")
        if isinstance(data,_ebase):
            return self.update_db_from_entity(data)
        if isinstance(data,(dict)):
        

            primary_name = self.primary_column_name
            primary_id = None
            if self.primary_column_name in data:
                primary_id = data[self.primary_column_name]
            else:
                if 'hash_id' in data:
                    primary_id = data['hash_id']
                    primary_name = 'hash_id'

            if primary_id is None:
                log.add(f"Failed update - Data does not have {self.primary_column_name} or a hash_id","error")
                return False

            upq = self._table.update_query()
            upq.add_where(primary_name,primary_id,"=")
            data = c.obj.remove_keys(data,[self.primary_column_name,"hash_id"])
            for k,v in data.items():
                upq.add_column(k,v)
            return upq.execute()

    # def updateDB(self,data:dict):
    #     upq = self._table.update_query()
    #     upq.add_where('hash_id',data[self.primary_column_name],"=")
    #     for k,v in data.items():
    #         upq.add_column(k,v)
    #     return upq.execute()

    def update_db_from_entity(self,entity:_ebase):
        log.add("   update_db_from_entity","info")
        primary_name = self.primary_column_name
        primary_id = entity.has_primary_column

        if primary_id is None:
            primary_id = entity.has_hash_id
            primary_name = "hash_id"

        if primary_id is None:
            log.add(f"Failed update - Entity does not have {self.primary_column_name} or a hash_id","error")
            return False

        log.add(f"       primary_name:{primary_name}","info")
        log.add(f"       primary_id:{primary_id}","info")
        upq = self._table.update_query()
        upq.add_where(primary_name,primary_id,"=")
        data = entity.data
        data = c.obj.remove_keys(data,[self.primary_column_name,"hash_id"])
        for k,v in data.items():
            upq.add_column(k,v)
        return upq.execute()

    def deleteDB(self,data:dict):
        delq = self._table.delete_query()
        delq.soft_delete = c.obj.get_arg(data,["soft_delete"],True,(bool))
        delq.add_where('hash_id',data[self.primary_column_name],"=")

        return delq.execute()

    def _get_by_primary(self,id_value):
        id_value = self.convert_id(id_value,return_row=True)
        if isinstance(id_value,(dict)):
            return id_value

    def _get_all(self,limit,offset):
        sql = f'''SELECT * FROM {self.sql_table_string} LIMIT %s'''
        args = [limit]
        if offset > 0:
            sql = f"{sql} OFFSET %s"
            args.append(offset)
        return self.__database.run_select(sql,args)

    def _dangerously_run_select(self,sql,args):
        return self.__database.run_select(sql,args)




    def prep(self):
        self._connect_to_database()

        self._table:c.db.MySQL.Table.Table = self.__database.get_table(self.table_name)
        self.primary_column_name = self._table.primary_column_name
        self.hash_id_prefix = self.hash_id_prefix
        # self.__confirm_cache()


    @property
    def column_names(self)->Iterable[str]:
        '''
            Get a list of all column names for this Susurruses table.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-23-2022 11:42:36
            `@memberOf`: SusurrusBase
            `@property`: column_names
        '''
        return self._table.column_names

    @property
    def table_columns(self):
        '''
            Get this SusurrusBase's table_columns

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-23-2022 12:08:23
            `@memberOf`: SusurrusBase
            `@property`: table_columns
        '''
        return self._table.columns


    def get_column_by_name(self,name:str)->c.db.MySQL._db_column_type:
        for col in self.table_columns:
            if col.data.column_name == name:
                return col


    def validate_and_correlate(self,data:dict):
        data = self.filter_dict_by_columns(data)
        for k,v in data.items():
            column = self.get_column_by_name(k)


    # def _gen_column_data(self):
    #     # @Mstep [] get the column data from the database
    #     self.table_columns = self.__database.get_column_data(self.table_name)
    #     parse_column_data(self.table_columns,self)
    #     # @Mstep [] save the data to the cache.
    #     save_cache(self)

    # def save_cache(sus:SusurrusBase):
    #     data = {
    #         "timestamp":sus.timestamp(),
    #         "column_data":sus.table_columns,
    #     }
    #     c.file.writer.to_json(sus.cache_path,data)
    def filter_private_keys(self,data:Union[dict,list]):
        '''
            Filter a dictionary or list of dictionaries to remove keys that are in self.private_keys
            ----------

            Arguments
            -------------------------
            `data` {dict,list}
                The dict or list of dictionaries to filter keys from.

            Return {dict,list}
            ----------------------
            The dictionary or list of dicitonaries with the keys filtered.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-15-2022 10:22:40
            `memberOf`: SusurrusBase
            `version`: 1.0
            `method_name`: filter_private_keys
            * @xxx [12-15-2022 10:27:44]: documentation for filter_private_keys
        '''
        if isinstance(data,(dict,list)) is False:
            return data

        orig_dict = True if isinstance(data,(dict)) else False
        data = c.arr.force_list(data)
        output = []
        for row in data:
            filtered = c.obj.remove_keys(row,self.private_keys)
            output.append(filtered)
        if orig_dict is True and len(output) > 0:
            output = output[0]
        return output

    def has_create_keys(self,data):
        for ckey in self.required_create_keys:
            if ckey not in data:
                return False
        return True


    def convert_id(self,id_value:Union[int,str],**kwargs):
        return_row = c.obj.get_kwarg(['return_row'],False,(bool),**kwargs)
        if isinstance(id_value,(str)):
            if self.hash_id_prefix in id_value:

                # sql = f'''SELECT %s FROM `{self.schema_name}`.`{self.table_name}` WHERE hash_id=%s'''
                # args = [self.primary_column_name,id_value]
                sql = f'''SELECT * FROM {self.sql_table_string} WHERE hash_id=%s;'''
                args = [id_value]
                result = self.__database.run_select(sql,args)
                if isinstance(result,(list)):
                    if len(result)> 0:
                        if return_row is False:
                            return result[0][self.primary_column_name]
                        else:
                            return result[0]
                # return result
        if isinstance(id_value,(int)):
            if return_row is False:
                return id_value
            else:
                sql = f'''SELECT * FROM {self.sql_table_string} WHERE {self.primary_column_name}=%s;'''
                args = [id_value]
                result = self.__database.run_select(sql,args)
                if isinstance(result,(list)):
                    return result[0]
                return None
            # return id_value
        return None

    @property
    def sql_table_string(self):
        '''
            Get this SusurrusBase's sql_table_string

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-05-2022 14:53:55
            `@memberOf`: SusurrusBase
            `@property`: sql_table_string
        '''
        value = self._sql_table_string
        if value is None:
            value = f"`{self.table_name}`"
            if isinstance(self.schema_name,(str)):
                value = f"`{self.schema_name}`.`{self.table_name}`"
            self._sql_table_string = value
        return value


