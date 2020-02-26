import psycopg2

def connect() :
    return psycopg2.connect(database="postgres",
    user="postgres",
    password="Poklm9222",
    host="127.0.0.1",
    port="5432")


con = connect()
cur = con.cursor()

req = ''' 

-- Table: public."Fichier_collecte"

-- DROP TABLE public."Fichier_collecte";

CREATE TABLE public."Fichier_collecte"
(
  "ID" SERIAL,
  "Date_creation" timestamp without time zone,
  "Active" boolean,
  "ID_Client" bigint,
  "ID_Associe" bigint,
  "ID_Creator" bigint,
  "Fichier_Excel" bytea,
  CONSTRAINT "ID" PRIMARY KEY ("ID")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public."Fichier_collecte"
  OWNER TO postgres;

'''

### INSERT ####

postgres_insert_query = """ DROP TABLE public."Fichier_collecte";"""
cur.execute(postgres_insert_query)
con.commit()
