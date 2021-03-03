import psycopg2
from psycopg2 import Error
import sqlalchemy
import json
with open("_cert_.json", "r") as write_file:
    lock_dict = json.load(write_file)


class Db_Connection:
    
    def __init__(self):
        self.connection_string = None
        pass
    
    def makeConnection(self):
        """
        """
        self.connection = sqlalchemy.create_engine(self.connection_string)
        pass
    
    def closeConnection(self):
        """
        """
        self.close()
        pass
    
    def runQuery(self, query):
        """
        """
        self.makeConnection()
#         self.connection.execute(query)
        self.result = [i for i in self.connection.execute(query)]
        
        return self.result

class Training_Db(Db_Connection):

    def __init__(self):
        self.connection_string = lock_dict['training_database_string']
        pass

    def pullBCItems(self, brand = None, table= 'bc_item'):
        """
        """
        query = f"""
                select * 
                from {table} bi 
                """
        if brand:
            query = query + f"where product_code like '%%{brand}'"

        self.columns = [i[0] for i in self.runQuery(f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}'")]
        self.runQuery(query)
        return self.columns, self.result

class wb_Db(Db_Connection):

    def __init__(self):
        self.connection_string = lock_dict['wb_database_string']
        pass

    def pullBCItems(self, brand = None, table= 'bc_item'):
        """
        """
        query = f"""
                select * 
                from {table} bi 
                """
        if brand:
            query = query + f"where product_code like '%%{brand}'"

        self.columns = [i[0] for i in self.runQuery(f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}'")]
        self.runQuery(query)
        return self.columns, self.result



      