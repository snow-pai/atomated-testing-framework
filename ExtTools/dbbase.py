import pymysql
import sqlite3



class MySqlHelp(object):
    '''mysql数据库操作类'''

    def __init__(self, host, user, password, database, port):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = int(port)
        self.connetcion = None

    def create_connection(self):
        '''连接数据库'''
        self.connetcion = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, port=self.port)

    def mysql_db_select(self, sql):
        '''查询数据库'''
        try:
            self.create_connection()
            with self.connetcion.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"查询数据库失败: {e}")
        finally:
            self.connetcion.close()
    def mysql_db_operate(self, sql):
         '''操作数据库'''
         try:
             self.create_connection()
             with self.connetcion.cursor() as cursor:
                 cursor.execute(sql)
             self.connetcion.commit()
         except Exception as e:
             print(f"操作数据库失败: {e}")
             self.connetcion.rollback()
         finally:
             self.connetcion.close()


class SqliteHelp(object):
    '''sqlite数据库操作类'''

    def __init__(self, db_path=' '):
        self.db_path = db_path
        self.connection = None

    def dict_factory(self, cursor, row):
        '''将查询结果转换为字典'''
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def create_connection(self):
        '''连接数据库'''
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = self.dict_factory  # 设置行工厂，使查询结果以字典形式返回

    def sqlite_db_select(self, sql):
        '''查询数据库'''
        try:
            self.create_connection()
            cursor = self.connection.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"查询数据库失败: {e}")
        finally:
            self.connection.close()

    def sqlite_db_operate(self, sql):
        '''操作数据库'''
        try:
            self.create_connection()
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            print(f"操作数据库失败: {e}")
            self.connection.rollback()
        finally:
            self.connection.close()















