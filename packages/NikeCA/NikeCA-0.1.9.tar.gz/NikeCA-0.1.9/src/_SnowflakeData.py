class SnowflakeData:
    import pandas

    def build_search_query(self, inp_db=None, schema=None, table=None, column_name=None, like_flag=False,
                           col_and_or='AND'):
        """
        Constructs a SQL query for searching tables and columns in a database based on specified search criteria.

        Parameters:
        -----------
        inp_db: str, optional
            The database name to search in. If not specified, searches all databases.
        schema: str, optional
            The schema name to search in. If not specified, searches all schemas.
        table: str, optional
            The table name to search for. If not specified, searches all tables.
        column_name: str or list of str, optional
            The column name(s) to search for. If not specified, searches all columns.
            If a list is provided, searches for any columns that match any of the names in the list.
        like_flag: bool, optional
            If True, uses a SQL LIKE statement to search for columns that contain the specified column name(s).
            If False, searches for exact matches to the specified column name(s).
            If not specified, defaults to False.
        col_and_or: str, optional
            If specified and column_name is a list, determines whether to search for columns that match all or any of
            the names in the list. Must be one of the following values: 'AND', 'and', 'OR', 'or'.
            If not specified, defaults to 'AND'.

        Returns:
        --------
        str
            The constructed SQL query string.
        """

        # ie. always TRUE --> allows us to search for tables/cols/etc. even without knowing the db
        where_stmt = "WHERE 1=1 "
        where_stmt = where_stmt + f"AND table_catalog = '{inp_db}' " if inp_db else where_stmt
        where_stmt = where_stmt + f"AND table_schema = '{schema}' " if schema else where_stmt
        where_stmt = where_stmt + f"AND table_name = '{table}' " if table else where_stmt

        # add column(s) search criteria -->
        # if like_flag = false then column name equals
        # if column_name is a list add an AND statement for each search value in the list
        if column_name is not None:
            if type(column_name) == str:
                where_stmt = where_stmt + f"AND column_name like '{column_name}' " \
                    if like_flag else where_stmt + f"AND column_name = '{column_name}' "

            # OR statement where value matches multiple
            elif (type(column_name) == list) & (not like_flag):
                where_stmt = where_stmt + f"""AND column_name in ({' ,'.join(f"'{str(x)}'" for x in column_name)})"""

            # --> user input list of search criteria
            elif type(column_name) == list:
                for idx, x in enumerate(column_name):

                    # col contains all column_name search criteria
                    if col_and_or.lower() == 'and':
                        where_stmt = where_stmt + f"AND column_name like '{x}' " \
                            if like_flag else where_stmt + f"AND column_name = '{x}' "

                    # col contains any of the column_name search criteria
                    elif col_and_or.lower() == 'or':
                        where_stmt = where_stmt + f"AND (column_name like '{x}' " \
                            if idx == 0 else where_stmt + f"OR column_name like '{x}' "

                    # non-matching input value
                    else:
                        raise ValueError('col_and_or input must match: AND/And/and, OR/Or/or')
                where_stmt = where_stmt + ')' if (type(column_name) == list) & (col_and_or == 'or') else where_stmt

            # --> invalid format
            else:
                raise ValueError(f'ERROR: column_name={column_name} does not match required input of list/string')

        # final search-schema query
        query = f'''        
        SELECT 
            DISTINCT
            TABLE_CATALOG
            ,TABLE_SCHEMA
            ,TABLE_NAME
            ,COLUMN_NAME
            ,IS_NULLABLE
            ,DATA_TYPE
        FROM 
            INFORMATION_SCHEMA.COLUMNS
        {where_stmt}
        ORDER BY 
            TABLE_CATALOG
            , TABLE_SCHEMA
            , TABLE_NAME
            , COLUMN_NAME
        '''

        return query

    def snowflake_pull(self, query: str | dict | None, un, wh, db, role, schema=None, table=None,
                       sample_table: bool = False, sample_val: bool = False, table_sample: dict = None,
                       dtypes_conv=None, separate_dataframes: bool = True) -> pandas.DataFrame:

        """
        function: pulls snowflake data

        dependencies: [
            pandas,
            snowflake.connector,
            time,
            datetime.datetime
        ]

        :param separate_dataframes:
        :param table:
        :param schema:
        :param query: str | dict
            SQL query to run on Snowflake
                    E.G. query = "SELECT * FROM  NGP_DA_PROD.POS.TO_DATE_AGG_CHANNEL_CY"
            Can also be multiple queries in the form of a dictionary
                    E.G. query = {"df1": "SELECT * FROM  NGP_DA_PROD.POS.TO_DATE_AGG_CHANNEL_CY", "df "SELECT TOP 2 * \
                    FROM  NGP_DA_PROD.POS.TO_DATE_AGG_CHANNEL_CY"}

        :param un: str
            Nike Snowflake Username
                "USERNAME"

        :param db: str, default 'NA'
            Name of the Database

        :param wh: str
            Name of the Wharehouse
            e.g. "DA_DSM_SCANALYTICS_REPORTING_PROD"

        :param role: str
            Name of the role under which you are running Snowflake
                "DF_######"

        :param sample_table: bool, default: False

        :param sample_val: bool, default: False

        :param table_sample: dict, default: None
            later
                if table_sample = None
                    table_sample = {'db': None, 'schema': None, 'table': None, 'col': None}

        :param dtypes_conv: default: None

        :return: pandas.DataFrame
        """

            # snowflake connection packages:
        import pandas as pd
        import snowflake.connector
        import time

        if table_sample is not None:
            table_sample = {'db': None, 'schema': None, 'table': None, 'col': None}

        # --> take a random sample from a table in snowflake
        query = f'''SELECT * FROM {table_sample['db']}.{table_sample['schema']}.{table_sample['table']} LIMIT 100''' \
            if sample_table else query

        # --> take a random sample of a column from a table in snowflake
        query = f'''SELECT DISTINCT 
                {table_sample['col']} 
            FROM 
                {table_sample['db']}.{table_sample['schema']}.{table_sample['table']} 
            ORDER BY 1 LIMIT 10''' \
            if sample_val else query

        recs = False

        if type(query) == dict:

            df = pd.DataFrame([query]).T
            df_index = df.index

            df_return = pd.DataFrame(index=df.index)
            df_return['sfqid'] = ''

            queries = len(df)
            print('Pulling ' + str(queries) + ' queries')

            query_list = []
            db_list = []
            complete = []

            for item in range(queries):
                query_list.append(item)
                db_list.append(item)
                complete.append(0)

            print('opening snowflake connection...')

            try:
                cnn = snowflake.connector.connect(
                    user=un,
                    account='nike',
                    authenticator='externalbrowser',
                    role=role,
                    warehouse='POS_REPORT_PROD'
                )

                cs = cnn.cursor()
                process_complete = 0
                process_pass = 0
                counter = 0

                for k, v in df.iterrows():
                    sql = v[0]
                    cs.execute_async(sql)
                    query_list[counter] = cs.sfqid
                    df_return['sfqid'][k] = cs.sfqid
                    counter += 1
                dfs = {}
                while process_complete == 0:
                    item = -1
                    process_pass += 1
                    if sum(complete) == queries or process_pass == 10:
                        process_complete = 1
                    for result in query_list:
                        item += 1
                        if complete[item] == 0:
                            status = cnn.get_query_status_throw_if_error(result)
                            print('the status for ' + df_return[df_return['sfqid'] == result].index[0] + ' is ' +
                                  str(status))
                            if str(status) == 'QueryStatus.SUCCESS':
                                complete[item] = 1
                                cs.get_results_from_sfqid(result)
                                if separate_dataframes:

                                    recs = True
                                    dfs[df_return[df_return['sfqid'] == result].index[0]] = cs.fetch_pandas_all()

                                else:
                                    df = pd.concat([df, cs.fetch_pandas_all()])
                            else:
                                time.sleep(.25)
            except Exception as e:
                print(e)
            finally:
                cnn.close()
                print('process complete')
        else:
            # connection settings
            conn = snowflake.connector.connect(
                user=un,
                account='nike',

                # opens separate browser window to confirm authentication
                authenticator='externalbrowser',
                warehouse=wh,
                database=db,
                role=role
            )

            # connect to snowflake using conn variables
            cur = conn.cursor()

            cur.execute(query)  # execute sql, store into-->

            try:
                # final data pull --> allows datatype-memory optimization
                df = cur.fetch_pandas_all() if dtypes_conv is None else cur.fetch_pandas_all().astype(
                    dtypes_conv)

            # --> allows metadata querying
            except:
                temp_df = cur.fetchall()  # return data
                cols = [x.name for x in cur.description]  # get column names
                df = pd.DataFrame(temp_df, columns=cols)  # create dataset

            conn.close()
            cur.close()
        if recs:
            return [dfs[k] for k in df_index]

        return df

    def search_schema(self, un, wh, db, role, sample_table: bool = False, sample_val: bool = False,
                      table_sample: dict = None, dtypes_conv=None, schema=None, table=None, column_name=None,
                      col_and_or='and', get_ex_val=False, like_flag=True):

        import pandas as pd

        # --> pull data, filter out exclusions
        results = pd.DataFrame()
        if type(db) == list:
            queries = {}

            for k in db:
                queries[k] = SnowflakeData.build_search_query(self, inp_db=k, schema=schema, table=table,
                                                              column_name=column_name, like_flag=like_flag,
                                                              col_and_or=col_and_or)
                queries[k] = queries[k][:queries[k].find("INFORMATION_SCHEMA.COLUMNS")] + k + '.' + \
                             queries[k][queries[k].find("INFORMATION_SCHEMA.COLUMNS"):]

            df = SnowflakeData.snowflake_pull(self, queries, un=un, wh=wh, role=role, db=None,
                                              sample_table=sample_table, sample_val=sample_val,
                                              table_sample=table_sample, dtypes_conv=dtypes_conv,
                                              separate_dataframes=False)

            results = pd.concat([results, df], axis=0)

        elif db is None:
            # --> check user's database access for list of dbs to check
            get_dbs = SnowflakeData.snowflake_pull(self, query='''SHOW DATABASES''', un=un, db=db, wh=wh, role=role)

            # list of user's db names
            db_names = list(get_dbs['name'].values)

            print(f"No input database --> checking all of databases in user's access: {len(db_names)} total databases")
            queries = {}
            for db in db_names:
                queries[db] = SnowflakeData.build_search_query(self, inp_db=db, schema=schema, table=table,
                                                               column_name=column_name, like_flag=like_flag,
                                                               col_and_or=col_and_or)
                queries[db] = queries[db][:queries[db].find("INFORMATION_SCHEMA.COLUMNS")] + db + '.' + \
                              queries[db][queries[db].find("INFORMATION_SCHEMA.COLUMNS"):]

            temp_results = SnowflakeData.snowflake_pull(self, query=queries, un=un, wh=wh, role=role, db=None,
                                                        sample_table=sample_table, sample_val=sample_val,
                                                        table_sample=table_sample, dtypes_conv=dtypes_conv,
                                                        separate_dataframes=False)

            results = pd.concat([results, temp_results], axis=0)
        else:
            results = SnowflakeData.snowflake_pull(
                self,
                query=SnowflakeData.build_search_query(self, inp_db=db, schema=schema, table=table,
                                                       column_name=column_name, like_flag=like_flag,
                                                       col_and_or=col_and_or),
                un=un, db=db, wh=wh, role=role)

        # exclude from table results
        exclusions = ['TEST', 'BACKUP', 'BKUP', 'BCKUP', 'BCKP', '_OLD', 'UPDT', 'DELETED', 'FIX']
        # # drop exclusion rows
        results_fin = results # [~results['TABLE_NAME'].str.contains('|'.join(exclusions))].copy().reset_index(drop=True)

        # --> print result statement
        print(f'''
    Total table-columns found: {len(results_fin)}    

    Unique column names found: {list(results_fin['COLUMN_NAME'].unique())}
    Total = {len(list(results_fin['COLUMN_NAME'].unique()))}
        ''')

        # --> flagged to retrieve a sample value for each column
        if get_ex_val:
            results_fin['EX_VALS'] = None
            # --> loop through each row & retrieve values
            for indx, row in results_fin.iterrows():
                try:
                    row_res = SnowflakeData.snowflake_pull(self, '', un=un, db=None, wh=wh, role=role, sample_val=True,
                                                           table_sample={'db': row['TABLE_CATALOG'],
                                                                         'schema': row['TABLE_SCHEMA'],
                                                                         'table': row['TABLE_NAME'],
                                                                         'col': row['COLUMN_NAME']})  # row results
                    # set row example values equal to unique column value list
                    row['EX_VALS'] = list(row_res[row['COLUMN_NAME']].unique())
                except:
                    print(f"Could not pull {row['COLUMN_NAME']} for table: {row['TABLE_NAME']}")
                    continue

        return results_fin

    import pandas

    def snowflake_dependencies(self, tables: str | list, username: str, warehouse: str, role: str,
                               database: str | None = None, schema: str | list | None = None) -> pandas.DataFrame:

        # snowflake connection packages:
        import pandas as pd
        import snowflake.connector
        import time

        if type(tables) == str:
            tables = [tables]

        print('opening snowflake connection...')

        cnn = snowflake.connector.connect(
            user=username,
            account='nike',
            authenticator='externalbrowser',
            role=role,
            warehouse=warehouse,
        )
        cs = cnn.cursor()
        process_complete = 0
        process_pass = 0
        counter = 0

        # fetch schema and table names
        query = 'SELECT * FROM ' + database + '.INFORMATION_SCHEMA.TABLES'
        if schema is not None:
            if type(schema) == str:
                schema = [schema]
            query = query + " WHERE TABLE_SCHEMA IN ('" + schema[0] + "'"
            if len(schema) > 1:
                for i in schema[1:]:
                    query = query + ", '" + i + "'"
            query = query + ')'

        cs.execute(query)
        df_tables = cs.fetch_pandas_all()

        query_ddl = {}

        for k, i in df_tables.iterrows():
            if i['TABLE_TYPE'] == 'VIEW':
                query_ddl[i['TABLE_CATALOG'] + '.' + i['TABLE_SCHEMA'] + '.' + i['TABLE_NAME']] = \
                    "SELECT GET_DDL('" + i['TABLE_TYPE'] + "', '" + i['TABLE_CATALOG'] + '.' + i[
                        'TABLE_SCHEMA'] + '.' \
                    + i['TABLE_NAME'] + "')"
            elif i['TABLE_TYPE'] == 'BASE TABLE':
                query_ddl[i['TABLE_CATALOG'] + '.' + i['TABLE_SCHEMA'] + '.' + i['TABLE_NAME']] = \
                    "SELECT GET_DDL('TABLE', '" + i['TABLE_CATALOG'] + '.' + i['TABLE_SCHEMA'] + '.' + \
                    i['TABLE_NAME'] + "')"

        df = pd.DataFrame([query_ddl]).T

        searchfor = ['NGP_DA_PROD.ODM_EMOPS.PG2NTABLE_EXT_SEC',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_STG_T.KEY_ACCNTS_snpsht_2020_02_04',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_STG_T.raju_temp_20200604',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_STG_T.KEY_ACCNTS_snpsht_2020_06_15',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_T.MCB_BOOKING_NDDC_DF_cv',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_T.FRNCH_SILH_4SEASONS_Test',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_T.MCB_BOOKING_NDDC_EMEA_DF_cv',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_T.MCB_STYLE_COLOR_DF_NDDC_EMEA_temp1',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_T.test_pv',
                     'NGP_DA_PROD.POS_STG_T.ACCESS_HISTORY_TEST_0801_new',
                     'NGP_DA_PROD.POS_STG_T.Test_Table',
                     'NGP_DA_PROD.POS_STG_T.Test_Table',
                     '.INFORMATION_SCHEMA.',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC.PE_V5.2_JAN2020_2021MARCH23_APLA',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_STG_T.KEY_ACCNTS_snpsht_2020_03_02',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_STG_T.raju_temp_20200602_fw_corefocus',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_STG_T.test_STOCKOUT_FLGS',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_T.MCB_STYLE_COLOR_DF_NDDC_EMEA_temp',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_T.PYTHIA_PE_ETL_CV',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_T.MCB_STYLE_COLOR_DF_CV',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_T.raju_temp_20200602_fw_corefocus',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_T.MCB_STYLE_COLOR_DF_NDDC_temp1',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_T.MCB_STYLE_COLOR_DF_NDDC_temp2',
                     'NGP_DA_PROD.POS_STG_T.pos_rtlr_sc_trend_agg_0331']

        df = df[~df.index.str.contains('|'.join(searchfor), case=False)]

        df_index = df.index

        df_return = pd.DataFrame(index=df_index)
        df_return['sfqid'] = ''

        queries = len(df)
        print('Pulling ' + str(queries) + ' queries')

        query_list = []
        db_list = []
        complete = []

        for item in range(queries):
            query_list.append(item)
            db_list.append(item)
            complete.append(0)

        for k, v in df.iterrows():
            sql = v[0]
            cs.execute_async(sql)
            query_list[counter] = cs.sfqid
            df_return['sfqid'][k] = cs.sfqid
            counter += 1
        df = pd.DataFrame()
        counter = 1
        while process_complete == 0:
            item = -1
            process_pass += 1
            if sum(complete) == queries or process_pass == 10:
                process_complete = 1
            for result in query_list:
                item += 1
                if complete[item] == 0:
                    print('Running ' + df_return[df_return['sfqid'] == result].index[0])
                    status = cnn.get_query_status_throw_if_error(result)
                    print('the status for ' + df_return[df_return['sfqid'] == result].index[0] + ' is ' +
                          str(status) + ' ' + str(counter))
                    if str(status) == 'QueryStatus.SUCCESS':
                        complete[item] = 1
                        cs.get_results_from_sfqid(result)
                        data = cs.fetch_pandas_all()
                        for table in tables:
                            if table.upper() in data.iloc[0, 0].upper():
                                df[df_return[df_return['sfqid'] == result].index[0]] = data
                    else:
                        time.sleep(.25)
                counter += 1
        df = df.T
        if len(df) == 0:
            return pd.DataFrame()
        df.columns = ['ddl']
        cnn.close()
        print('process complete')

        return df

    def optimize_tbl_mem(self, username: str, warehouse: str, role: str, database: str = None, schema: str = None,
                         table_name: str = None, pull_all_cols=True, run_debugging: bool = False,
                         query=None):

        import pandas as pd
        import numpy as np
        from NikeQA import QA

        from datetime import datetime

        if query is not None:
            query = str(query) + ' LIMIT 5' if query[-1] != ';' else str(
                query[:-1]) + ' LIMIT 5'  # add limit if user inputs a query (checking for semicolon at end of query)
            print(query)

        # --> DEBUGGING CODE: Return data profile if run for debugging purposes
        if run_debugging:
            t_sample = self.snowflake_pull(query=None, un=username, wh=warehouse, role=role, db=database,
                                           sample_table=True,
                                           table_sample={'db': database, 'schema': schema, 'table': table_name}
                                           if query is None else query)

            sample_prfl = QA(t_sample).data_prfl_analysis(ds_name='Table Sample', print_analysis=False)  # --> run data profiling function to get table info
            return sample_prfl

        # ======================================================================================================
        # --> DYNAMICALLY DETERMINE HOW TO CONVERT COLUMN DATA TYPES TO OPTIMIZE PYTHON-PANDAS MEMORY
        t_sample = self.snowflake_pull(query=None, un=username, wh=warehouse, role=role, db=database, sample_table=True,
                                       table_sample={'db': database, 'schema': schema, 'table': table_name}) \
            if query is None else self.snowflake_pull(query, username, warehouse, database, role=role)  # --> input table information from function inputs & sample table

        # --> determine column datatype conversions to make:
        sample_prfl = QA(t_sample).data_prfl_analysis(ds_name='Table Sample', print_analysis=False)  # --> run data profiling function to get table info

        sample_prfl['UNIQUE_PCT'] = (sample_prfl['UNIQUE_VALUES'] / (sample_prfl['NON_NULL_ROWS'])) * 100  # --> determine 0-100 percentage of unique values in the column

        for index, row in sample_prfl.iterrows():  # --> get the min/max values for all our integer columns
            sample_prfl.loc[index, 'INT_MIN'] = min(t_sample[row['COLUMN']]) if row['COL_DATA_TYPE'] == int else None
            sample_prfl.loc[index, 'INT_MAX'] = max(t_sample[row['COLUMN']]) if row['COL_DATA_TYPE'] == int else None

        # drop unneeded columns
        sample_prfl = sample_prfl[['COLUMN', 'COL_DATA_TYPE', 'UNIQUE_PCT', 'INT_MIN', 'INT_MAX']].copy()

        # --> run conversion rules to replace data types
        #    strings/keys/anything <> int w/ a distinct record on each row (>7% for our logic) = pd.StringDtype()
        #    integers = int64 (error handling), except 'int8' = 'int8'
        #    any float or decimals = float32
        #    any string/object that is not distinct on each row = 'category'
        #    any True/False fields = bool ('category' may also work)
        sample_prfl['DTYPE_CONV'] = np.where(
            ((sample_prfl['COL_DATA_TYPE'] == object) & (sample_prfl['UNIQUE_PCT'] <= 66)) | (
                        (sample_prfl['COL_DATA_TYPE'] == object) & (sample_prfl['UNIQUE_PCT'].isna())), 'category',
            # default string/object value
            np.where((sample_prfl['COL_DATA_TYPE'] == object) & (sample_prfl['UNIQUE_PCT'] > 66), str, #, pd.StringDtype(),
                     # objects w/ a distinct record on each row (>80% for our logic) = pd.StringDtype()
                     np.where(sample_prfl['COL_DATA_TYPE'] == int, 'int64',
                              # handles dtype error (makes other INT criteria irrelevant)
                              np.where(sample_prfl['COL_DATA_TYPE'] == 'int8', 'int8',  # default for any integer value
                                       np.where(sample_prfl['COL_DATA_TYPE'] == float, 'float32',  # float columns
                                                np.where(sample_prfl['COL_DATA_TYPE'] == bool, 'bool',
                                                         'ERROR'))))))  # True/False boolean columns

        # --> QA/ERROR checking
        error_flag = sample_prfl.loc[sample_prfl['DTYPE_CONV'] == 'ERROR'].copy().reset_index(drop=True)
        if len(error_flag) > 0:
            raise ValueError(f'''ERROR: the following columns have no data type conversion rule: {
                list(error_flag['COLUMN'].unique())}''')  # raise error if we're missing any conversion rules

        sample_prfl.index = sample_prfl['COLUMN']  # reset index to column name
        sample_prfl.drop(columns=['COLUMN', 'COL_DATA_TYPE', 'UNIQUE_PCT', 'INT_MIN', 'INT_MAX'],
                         inplace=True)  # drop unneeded columns

        dtypes = sample_prfl.to_dict()['DTYPE_CONV']  # convert to dictionary --> use for final query

        # ======================================================================================================
        # --> ANALYZE MEMORY OPTIMIZATION: get sample after memory conversion
        t_test = self.snowflake_pull(None, un=username, wh=warehouse, role=role, db=database, sample_table=True,
                                     table_sample={'db': database, 'schema': schema, 'table': table_name},
                                     dtypes_conv=dtypes) if query is None else self.snowflake_pull(
            query=query, un=username, wh=warehouse, role=role, db=database, dtypes_conv=dtypes)

        before_memory = t_sample.memory_usage(deep=True).sum()  # sample table memory usage (before conversion)
        after_memory = t_test.memory_usage(deep=True).sum()  # sample table memory usage (after conversion)

        print(f'''
        Sample table memory usage -->
        Before memory conversion: {before_memory / 1000000000} GB
        After memory conversion: {after_memory / 1000000000} GB
        Memory reduction percentage: {"{:.2%}".format((before_memory - after_memory) / before_memory)}

        Finished running! {datetime.now().strftime("%H:%M:%S")}
        ''')  # convert to GB & print total memory usage before & after conversion

        return dtypes  # --> return the datatypes to convert each column in the table to


