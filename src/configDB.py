
##### CONF POSTGRES SQL DATABASE


#### CONNEXION 

CONNEXION_DB = {
    'schema' : 'public',
    'database' : 'postgres',
    'user' : 'postgres',
    'password' : 'Poklm9222',
    'host' : "127.0.0.1",
    'port' : '5432'
}


####  DATABASE 

DATABASES = {
    
    'Fichier_collecte' : ''' 

        -- Table: public."Fichier_collecte"

        -- DROP TABLE public."Fichier_collecte";

        CREATE TABLE public."Fichier_collecte"
        (
        "ID" SERIAL,
        "Date_creation" timestamp without time zone,
        "Active" boolean,
        "Nom_Client" character(50),
        "ID_Partner" bigint,
        "ID_Creator" bigint,
        "Fichier_Excel" bytea,
        "Organigramme" json,
        CONSTRAINT "ID" PRIMARY KEY ("ID")
        )
        WITH (
        OIDS=FALSE
        );
        ALTER TABLE public."Fichier_collecte"
        OWNER TO postgres;
                        ''',
    'Cerfa' : 
    '''
        -- Table: public."Cerfa"

        -- DROP TABLE public."Cerfa";

        CREATE TABLE public."Cerfa"
        (
        "ID_Cerfa" SERIAL,
        "ID_Collecte" bigint,
        "Nom_Entite" character(50),
        "Pdf" bytea,
        CONSTRAINT "ID_Cerfa" PRIMARY KEY ("ID_Cerfa")
        )
        WITH (
        OIDS=FALSE
        );
        ALTER TABLE public."Cerfa"
        OWNER TO postgres;
                        ''',
    'Partner' : 
    '''
        -- Table: public."Partner"

        -- DROP TABLE public."Partner";

        CREATE TABLE public."Partner"
        (
        "ID_Partner" SERIAL,
        "nom" character(50),
        "prenom" character(50),
        "email" character(50),
        CONSTRAINT "ID_Partner" PRIMARY KEY ("ID_Partner")
        )
        WITH (
        OIDS=FALSE
        );
        ALTER TABLE public."Partner"
        OWNER TO postgres;
                        '''
}

