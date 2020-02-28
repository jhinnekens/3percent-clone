import psycopg2
from configDB import *
from psycopg2.extras import RealDictCursor

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
        self.cursor = self.connexion.cursor(cursor_factory=RealDictCursor)
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
            #print(query)
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

    def create_all_table(self) : 
        for key,value in DATABASES.items() :
            self.create_table(key)

    def drop_table(self,table_name) :
        query = ''' DROP TABLE {}."{}" '''.format(self.schema , table_name)
        self.commit_query(query)

    def drop_all_table(self) :
        for table in [row['table_name'] for row in self.show()] : 
            self.drop_table(table)

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
        query = ''' INSERT INTO {}."{}" ("{}") VALUES ({})'''.format(
            self.schema,table,'","'.join(list(kwargs.keys())),",".join(str(e) for e in list(kwargs.values())))
        self.commit_query(query)

    def select_where(self,table,where,*args) : 
        query = self.__select(table,*args) + """ WHERE "{}" = {} """.format(''.join(list(where.keys())),''.join(str(e) for e in where.values()))
        return self.fetch_query(query)

    def get_max_id(self,table,id) : 
        query = ''' SELECT MAX("{}") FROM {}."{}" '''.format(id,self.schema,table)
        return next(self.fetch_query(query))['max']