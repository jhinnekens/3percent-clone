
from config import *

import pdfrw
import time
import os

class PDF :

    def __init__(self,path = None) :
        """[summary]
        
        Arguments:
            template_id {[type]} -- [description]
        
        Keyword Arguments:
            path {[type]} -- [description] (default: {None})
        """

        self.writer = pdfrw.PdfWriter()
        self.annexes = []
        self.template_id = '2746-sd_2589'
        if path is None :
            self.path = 'app/data/cerfa/'
        else :
            self.path = path

    def read_template(self) :
        template_pdf = pdfrw.PdfReader(self.path + self.template_id + '.pdf')

        try : 
            template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
        except : 
            self.template_pdf = template_pdf
        self.template_pdf = template_pdf

    def get_at(self,form_id) : 
        return self.template_pdf.Root.AcroForm.Fields[form_id]

    def update(self,field,value) :
        update_value = str(value)
        if field['type'] == 'seq' :
            update_value = '(' + str(value) + ')'
        
        #self.template_pdf.Root.AcroForm.Fields[field['index']].update(pdfrw.PdfDict(V = pdfrw.PdfString(update_value)))
        next(item for item in self.template_pdf.Root.AcroForm.Fields if item['/T'] == field['index']).update(pdfrw.PdfDict(V = pdfrw.PdfString(update_value)))

    def fill_at(self,form_id,value) :
        field = FIELDS_PDF[form_id]
        value = str(value)
        if len(value) <= field['length'] : 
            self.update(field,value)
        else : 
            print('error')

    def add_pages(self) :
        self.writer.addpages(self.template_pdf.pages)

    def add_annexes(annexes) :
        return

    def write_pdf(self) :
        self.writer.write(self.path + self.template_id + time.ctime().replace(' ','_').replace(':','_') + '.pdf',self.template_pdf)

