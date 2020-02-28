
from app.posgresclient import pgDB

db = pgDB()

db.drop_all_table()
db.create_all_table()

db.insert('Partner',nom = "'Lunghi'", prenom = "'Bruno'", email = "'bruno.lunghi@pwcavocats.com'")