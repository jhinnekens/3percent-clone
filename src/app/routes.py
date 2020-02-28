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


#app.config['UPLOAD_FOLDER'] = 'app/temp/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','xlsx'])

db = pgDB()

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/ping')
def ping():
    return {'status' : 'OK' , 'time' : datetime.now()}

@app.route('/julien')
def julien():
    return jsonify([{"id": 1, "firstname": "EtienneS", "name": "Secking"},{"id": 2,"firstname": "Jane","name": "Doe"}])

@app.route('/download' , methods=['GET', 'POST'])
def download():
    return send_from_directory(directory = UPLOAD_FOLDER , filename = 'cerfa.pdf' , cache_timeout = 2)

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/python-flask-files-upload', methods=['POST'])
def upload_file():
	# check if the post request has the file part
	if 'files[]' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	
	files = request.files.getlist('files[]')
	
	errors = {}
	success = False

	for file in files:
		if file and allowed_file(file.filename):
			
    		## Upload file :
			filename = secure_filename(file.filename)
			if os.path.exists(os.path.join(UPLOAD_FOLDER, 'cerfa.pdf')) :
				os.remove(os.path.join(UPLOAD_FOLDER, 'cerfa.pdf'))
			file.save(os.path.join(UPLOAD_FOLDER, filename))

			## Store in database
	
			with open(os.path.join(UPLOAD_FOLDER, filename), "rb") as f:
				db.insert('Fichier_collecte',Active = True, Date_creation = 'NOW()' , ID_Client = 122,
				 ID_Partner = 3, ID_Creator = 1, Fichier_Excel = ps2.Binary(f.read()))


			ID_Collecte = db.get_max_id('Fichier_collecte','ID')
			## Read file
			input_file = InputFile(os.path.join(UPLOAD_FOLDER, filename))

			## Check error
			input_file.process()

			## Build Organigramme
			organigramme = Organigramme()
			organigramme.build(input_file)

			#a = organigramme.jsonify()


			## Construct and Store Cerfas

			for entitie in organigramme.get_entities() :
				cerfa = CerfaWriter(entitie,orga = organigramme)
				writer = cerfa.fill_pdf()
				tmp = io.BytesIO()
				writer.write(tmp)
				db.insert('Cerfa',ID_Collecte = ID_Collecte , Pdf = ps2.Binary(tmp.getvalue()))

			## Remove uploaded file
			os.remove(os.path.join(UPLOAD_FOLDER, filename))
			success = True
		else:
			errors[file.filename] = 'File type is not allowed'
	
	if success and errors:
		errors['message'] = 'File(s) successfully uploaded'
		resp = jsonify(errors)
		resp.status_code = 206
		return resp
		
	if success:
		resp = jsonify({'message' : 'Files successfully uploaded'})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify(errors)
		resp.status_code = 400
		return resp


@app.route('/declarations')
def declarations():
	fichiers_collecte = db.select_where('Fichier_collecte',{'ID_Creator' : 1})
	resp = []

	for f in fichiers_collecte :
		declarations = db.select_where('Cerfa',{'ID_Collecte' : f['ID']})
		#declarations = [{key:value for key,value in [('Cerfa' + str(e['ID_Cerfa']),request.host_url + 'download_cerfa/' + str(e['ID_Cerfa'])) for e in declarations]}]
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

@app.route('/upload2' , methods=['POST'])
def upload2():
	### READ UPLOAD REQUEST
	files = request.form
	excel = files['file'].split(',')[1]
	excel = base64.b64decode(excel)
	partner = files['email']
	partner = next(db.select_where('Partner',{'email':"'" + partner + "'" }))
	Nom_Client = files['groupe']


	### PROCESS INPUT FILE
	input_file = InputFile(excel)
	input_file.process()

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