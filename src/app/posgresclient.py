import psycopg2
from .configDB import *

class pgDB :

    def __init__(self) :
        self.schema = CONNEXION_DB['schema']
        self.database = CONNEXION_DB['database']
        self.user = CONNEXION_DB['user']
        self.password = CONNEXION_DB['password']
        self.host = CONNEXION_DB['host']
        self.port = CONNEXION_DB['port']
        self.connect()

    def connect(self) :
        con =  psycopg2.connect(database=self.database,
        user = self.user,
        password = self.password,
        host = self.host,
        port = self.port)

        self.connexion = con

    def create_cursor(self) :
        self.cursor = self.connexion.cursor()
        return self.cursor

    def get_cursor(self) :
        return self.cursor

    def execute_query(self,query) : 
        try :
            return self.create_cursor().execute(query)
        except :
            raise('DB error')

    def commit_query(self,query) :
        try : 
            self.execute_query(query)
            self.connexion.commit()
        except :
            self.connect()
            raise('Commit query error')
        finally :
            self.connect()

    def fetch_query(self,query) :
        self.execute_query(query)
        for element in self.cursor.fetchall():
            yield element

    def create_table(self,table) : 
        self.commit_query(DATABASES[table])

    def drop_table(self,table_name) :
        query = ''' DROP TABLE {}."{}" '''.format(self.schema , table_name)
        self.commit_query(query)

    def show(self) : 
        query = '''SELECT table_name FROM information_schema.tables WHERE table_schema = '{}' '''.format(self.schema)
        return self.fetch_query(query)

    def __select(self,table,*args) :
        if len(args) :
            query = ''' SELECT "{}" FROM {}."{}"'''.format('","'.join(args),self.schema,table)
        else : 
            query = ''' SELECT * FROM {}."{}"'''.format(self.schema,table)
        
        return(query)

    def select(self,table,*args) :
        query = self.__select(table,*args)
        return self.fetch_query(query)

    def insert(self,table,**kwargs) :
        query = ''' INSERT INTO {}."{}" ("{}") VALUES ({})'''.format(self.schema,table,'","'.join(list(kwargs.keys())),",".join(list(kwargs.values())))
        self.commit_query(query)

    def select_where(self,table,where,*args) : 
        query = self.__select(table,*args) + """ WHERE "{}" = {} """.format(''.join(list(where.keys())),''.join(where.values()))
        return self.fetch_query(query)