from config import *
from flask import render_template , jsonify, request , send_from_directory , send_file
from app import app
from werkzeug.utils import secure_filename
from .pdfWR import PDF
from .inputFile import InputFile
from .organigramme import Organigramme
from .cerfawriter import CerfaWriter
from .posgresclient import pgDB
from flask import jsonify

from datetime import datetime
import json
import os
import sys
import pandas as pd
import psycopg2 as ps2
import io
import base64
import json



try :
	db = pgDB()
except Exception as e:
	app.logger.info(str(sys.exc_info()[1]))


@app.route('/ping')
def ping():
    return {'status' : 'OK' , 'time' : datetime.now()}

@app.route('/connectDB')
def connectDB():
	try :
		db = pgDB()
	except Exception as e:
		error = errorHandler("Error in connecting database",str(sys.exc_info()[1]))
		return error,401
	return 200

@app.route('/declarations')
def declarations():
	fichiers_collecte = db.select_where('Fichier_collecte',{'ID_Creator' : 1})
	resp = []

	for f in fichiers_collecte :
		declarations = db.select_where('Cerfa',{'ID_Collecte' : f['ID']})
		declarations = [(link,id) for link,id in [(request.host_url + 'download_cerfa/' + str(e['ID_Cerfa']),e['Nom_Entite']) for e in declarations]]
		dec = []
		for e1,e2 in declarations :
			dec.append({'link':e1 , 'filename' : str(e2)})
		
		resp.append(
			{"id" : f['ID'], 'groupe' : f['Nom_Client'] , 'fichier_collecte' : {
				'filename' : "Fichier de collecte d'information.xlsx",
				'link' : request.host_url + 'download_collecte/' + str(f['ID'])},
				'declarationFiles' : dec,
				'organigramme' : 'organigramme',
				'createdBy' : f['ID_Creator'],
				'created' : datetime.now()
			}
		)
	return jsonify(resp)

@app.route('/download_cerfa/<string:ID>' , methods=['GET', 'POST'])
def download_cerfa(ID):
	cerfa = db.select_where('Cerfa',{'ID_Cerfa':ID},'Pdf')
	cerfa = bytes(next(cerfa)['Pdf'])
	mem = io.BytesIO()
	mem.write(cerfa)
	mem.seek(0)

	return send_file(mem , as_attachment = True ,
	 attachment_filename = 'Cerfa_{}.pdf'.format(str(ID)),
	 mimetype='application/pdf',
	 cache_timeout = 2)

@app.route('/download_collecte/<string:ID>' , methods=['GET', 'POST'])
def download_collecte(ID):
	fichier = db.select_where('Fichier_collecte',{'ID':ID},'Fichier_Excel')
	fichier = bytes(next(fichier)['Fichier_Excel'])
	mem = io.BytesIO()
	mem.write(fichier)
	mem.seek(0)

	return send_file(mem , as_attachment = True ,
	 attachment_filename = 'Fichier_Collecte_{}.xlsx'.format(str(ID)) ,
	  mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
	  cache_timeout = 2)

@app.route('/upload' , methods=['POST'])
def upload():
	### READ UPLOAD REQUEST
	error = {}

	files = request.form
	excel = files['file'].split(',')[1]


	excel = base64.b64decode(excel)
	partner = files['email']
	partner = next(db.select_where('Partner',{'email':"'" + partner + "'" }))
	Nom_Client = files['groupe']


	### PROCESS INPUT FILE
	try :
		input_file = InputFile(excel)
		input_file.process()
	except Exception as e:
		error = errorHandler('Error in reading Input File',str(sys.exc_info()[1]))
		return error , 401
	

	### Build Organigramme
	organigramme = Organigramme()
	organigramme.build(input_file)

	### INSERT FILE IN DATABASE
	db.insert('Fichier_collecte',Active = True ,Date_creation = 'NOW()' ,
	 Nom_Client = "'"+Nom_Client+"'", ID_Partner = partner['ID_Partner'], ID_Creator = 1,
	Fichier_Excel = ps2.Binary(excel) , Organigramme = ps2.extras.Json(organigramme.jsonify()))
	
	ID_Collecte = db.get_max_id('Fichier_collecte','ID')
	### Create Cerfas
	for entitie in organigramme.get_entities() :
		
		cerfa = CerfaWriter(entitie,organigramme,partner['nom'],partner['prenom'],partner['email'])
		writer = cerfa.fill_pdf()
		tmp = io.BytesIO()
		writer.write(tmp)
		db.insert('Cerfa',ID_Collecte = ID_Collecte ,Nom_Entite = "'"+entitie+"'" ,Pdf = ps2.Binary(tmp.getvalue()))

	return '200'

@app.route('/organigramme/<string:ID>')
def draw_orga(ID):
	orga = next(db.select_where('Fichier_collecte',{'ID_Creator' : 1},'Organigramme'))['Organigramme']
	return jsonify(orga)

def errorHandler(message,value):
	error = {'message': message  , 'value': value }
	app.logger.info(error)
	return error