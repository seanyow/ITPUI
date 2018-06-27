from pymysql import connect, Error

import dbconfig as dbconf
from dataframe import *


class SQL:
    def __init__(self, host=dbconf.host, user=dbconf.user, password=dbconf.password, db=dbconf.db,
                 encoding=dbconf.encoding):
        # Connection Settings
        self.__host = host
        self.__user = user
        self.__password = password
        self.__db = db

        self.__connection = None
        self.__cursor = None
        self.__encoding = encoding
        self.__filter_limit = 100
        # FOR TESTING/DEBUGGING TODO:remove when deemed unnecessary
        self.__default_table = "vomsii_data"

    def __del__(self):
        self.__close()

    def destroy(self):
        self.__del__()

    # FOR TESTING/DEBUGGING TODO:remove when deemed unnecessary
    def connection(self):
        return self.__connection

    # FOR TESTING/DEBUGGING TODO:remove when deemed unnecessary
    def query(self, statement, expect_result=False):
        return self.__query(statement, expect_result)

    def get_table(self, table=None):
        if table is None:
            return None

        query = "SELECT * FROM `" + table + "`"

        self.__reconnect()
        return pd.read_sql(sql=query, con=self.__connection)

    # Method to obtain all column names in a table
    def get_column_names(self, table=None):
        # TODO: # TODO: Better 'default table' handling
        if table is None:
            table = self.__default_table

        # Get Column Names from Database
        condition = "table_name = '" + table + "'"
        result = self.__select(columns="COLUMN_NAME", table="INFORMATION_SCHEMA.COLUMNS", condition=condition)

        # Clean Data before returning
        column_names = []
        for name in result:
            column_names.append(name[0])

        # Return Data
        return column_names

    # Method to obtain the datatype and size of each column in a table
    def get_column_datatypes(self, table=None, distinct=False, column=None, singular=False):
        # TODO: Invalid argument handling
        # TODO: Better 'default table' handling
        if table is None:
            table = self.__default_table

        if singular and column is not None:
            # Get Column datatypes from Database TODO: Use SQL 'DISTINCT'
            condition = ("table_name = '%s' AND column_name = '%s'" % (table, column))
            result = self.__select(columns="DATA_TYPE", table="INFORMATION_SCHEMA.COLUMNS", condition=condition)

            # Clean and Return Data
            return result[0][0]
        else:
            # Get Column datatypes from Database TODO: Use SQL 'DISTINCT'
            condition = ("table_name = '%s'" % table)
            result = self.__select(columns="DATA_TYPE, CHARACTER_MAXIMUM_LENGTH", table="INFORMATION_SCHEMA.COLUMNS",
                                   condition=condition)

            # Clean Data before returning
            column_datatypes = []
            for col_name, col_type in result:
                column_datatypes.append([col_name, col_type])

            # Return Data
            if distinct:
                return [list(x) for x in set(tuple(x) for x in column_datatypes)]
            return column_datatypes

    # Method to obtain distinct vessel codes/names TODO: Too reliant on hardcode. Possible redesign required
    def get_vessel_names(self, table=None, column=None):
        # TODO: Better 'default table' handling
        if table is None:
            table = self.__default_table

        # TODO: Better handle 'No column given' condition
        if column is None:
            column = 'DISTINCT `Vessel Name`'
            # column = 'DISTINCT `Vessel Code`'

        return [i[0] for i in (self.__select(columns=column))]

    # Method to obtain filter options
    def get_filter_options(self, table=None):
        # TODO: Better 'default table' handling
        if table is None:
            table = self.__default_table

        # Get Column Info from Database TODO: Use SQL 'DISTINCT'
        condition = "table_name = '" + table + "'"
        info = self.__select(columns="COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH",
                             table="INFORMATION_SCHEMA.COLUMNS", condition=condition)

        # Filter
        filtered_info = []
        for item in info:
            if item[2] <= self.__filter_limit:
                filtered_info.append(item)

        return filtered_info

    # Method to obtain data for a particular vessel
    def get_vessel(self, table=None, vessel=None):
        # TODO: # TODO: Better 'default table' handling
        if table is None:
            table = self.__default_table

        query = "SELECT * FROM vomsii_data"
        if vessel is not None:
            query += " WHERE `Vessel Name`='" + vessel + "'"

        self.__reconnect()
        df = pd.read_sql(sql=query, con=self.__connection)
        return DataFrame(df)

    # Excel-to-SQL Function
    def xlsx_to_sql(self, table_name, xlsx, filetype=FileType.VOMSII, ):
        df = DataFrame(xlsx, filetype)
        columns = df.get_columns()

        # Create empty table in database
        self.__create(table=table_name, columns=columns, datatype=df.get_column_datatypes())

        # Populate table with xlsx data
        for i in range(df.len()):
            row = df.get_row(i + 1)

            col = ""
            val = ""
            valid_rows = len(columns)

            for j in range(len(columns) - 1, -1, -1):
                if not pd.isnull(row[j]):
                    break
                valid_rows -= 1

            for j in range(valid_rows):
                if not pd.isnull(row[j]):
                    col += "`" + columns[j] + "`"
                    val += '"' + unicode(row[j]).replace('"', '\\"') + '"'

                    if j is not (valid_rows - 1):
                        col += ","
                        val += ","

            insert_query = "INSERT INTO `" + table_name + "` (" + col + ") VALUES (" + val + ")"
            err = self.__query(insert_query)
            if err is not None:
                print(err)

    # SQL Select Method
    def __select(self, columns="*", table=None, condition=None):
        # TODO: Handle 404

        # TODO: Better 'default table' handling
        if table is None:
            table = self.__default_table

        # Construct SELECT Query
        sql = "SELECT " + columns + " FROM " + table

        # If condition given
        if condition is not None:
            sql += " WHERE " + condition

        # Run Query
        return self.__query(sql, expect_result=True)
        # self.__reconnect()
        # return pd.read_sql(sql=sql, con=self.__connection)

    # SQL Insert Method
    def __insert(self, columns=[], table=None, data=[]):
        # TODO: Handle error where 'columns' and 'data' do not match(i.e different number of elements)
        # TODO: Handle event where 'row' already exists in Database(i.e Replace or Combine?)

        # TODO: Better 'default table' handling
        if table is None:
            table = self.__default_table

        # Construct INSERT Query
        sql_columns = ""
        sql_data = ""
        for i in range(len(columns)):
            if i is not 0:
                sql_columns += ","
                sql_data += ","

            sql_columns += columns[i]
            sql_data += '"' + unicode(str(data[i])).replace('"', '\\"') + '"'

        sql = "INSERT INTO `" + table + "`(" + sql_columns + ") VALUES (" + sql_data + ")"
        # Run Query
        self.__query(statement=sql, expect_result=False)

    # SQL Create Table Method
    def __create(self, table=None, columns=[], datatype=[]):
        # TODO: Handle invalid arguments(i.e 'id' in 'columns')
        # TODO: Handle error where 'columns' and 'data' do not match(i.e different number of elements)
        # TODO: Handle event where 'table' already exists in Database(i.e Replace or Combine?). Currently replacing

        # TODO: Better 'default table' handling
        if table is None:
            table = self.__default_table

        # Drop table if it already exist in Database
        sql_drop = "DROP TABLE IF EXISTS `" + table + "`"
        self.__query(sql_drop)

        # First part of query, with 'id' as an auto incrementing index
        sql = "CREATE TABLE `" + table + "` (`id` int(11) NOT NULL AUTO_INCREMENT,"

        # Add each column name with its data type to statement
        for i in range(len(columns)):
            line = "`" + columns[i] + "`"

            # Check data type of column and add accordingly TODO: Reconsider hardcoded data sizes
            if datatype[i] == 'datetime64[ns]':
                line += " DATETIME"
            elif datatype[i] == 'object':
                if "Remarks" in columns[i] or "Reason" in columns[i]:
                    line += " VARCHAR(512)"
                elif "Email" in columns[i]:
                    line += " VARCHAR(100)"
                else:
                    line += " VARCHAR(50)"
            elif datatype[i] == 'int64':
                line += " INT"
            elif datatype[i] == 'float64':
                line += " FLOAT"

            # Include comma and add portion to query
            line += ","
            sql += line

        # End part of query
        sql += "PRIMARY KEY (`id`)) ENGINE=InnoDB CHARACTER SET utf8 COLLATE utf8_bin"

        # Run Query
        self.__query(sql)

    # Basic Query Function
    def __query(self, statement, expect_result=False):
        self.__reconnect()

        result = None
        try:
            with self.__cursor as cursor:
                # Run SQL Query
                cursor.execute(statement.encode(self.__encoding))
                self.__connection.commit()

                # If result is expected
                if expect_result:
                    result = cursor.fetchall()
        except Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
        finally:
            return result

    # Open Connection Method
    def __reconnect(self):
        self.__close()

        self.__connection = connect(host=self.__host, user=self.__user, password=self.__password, db=self.__db)
        self.__cursor = self.__connection.cursor()

    # Close Connection Method
    def __close(self):
        if self.__connection is not None:
            self.__connection.close()
