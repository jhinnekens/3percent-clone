import psycopg2

def connect() :
    return psycopg2.connect(database="3percent",
    user="postgres",
    password="",
    host="127.0.0.1",
    port="5432")


cur = con.cursor()

cur.execute('''
SELECT "ID" , "NAME" FROM public."CLIENT"
 ''')

rows = cur.fetchall()

for row in rows :
    print(row)  

### INSERT ####

postgres_insert_query = ''' INSERT INTO public."CLIENT" ("NAME") VALUES ('TEST python 2')'''
cur.execute(postgres_insert_query)
con.commit()
