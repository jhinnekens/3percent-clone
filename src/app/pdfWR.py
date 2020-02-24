
from config import *

#import pdfrw
import time
import os

from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject

class PDF :

    def __init__(self,path = None) :
        """[summary]
        
        Arguments:
            template_id {[type]} -- [description]
        
        Keyword Arguments:
            path {[type]} -- [description] (default: {None})
        """

        self.template_id = '2746-sd_2589'
        if path is None :
            self.path = 'app/data/cerfa/'
        else :
            self.path = path

        self.inputStream = open(self.path + self.template_id + '.pdf', "rb")
        self.outputStream = open(self.path + self.template_id + time.ctime().replace(' ','_').replace(':','_') + '.pdf', "wb")

        self.pdf_reader = PdfFileReader(self.inputStream, strict=False)
        if "/AcroForm" in self.pdf_reader.trailer["/Root"]:
            self.pdf_reader.trailer["/Root"]["/AcroForm"].update(
                {NameObject("/NeedAppearances"): BooleanObject(True)})


        self.pdf_writer = PdfFileWriter()
        self.set_need_appearances_writer(self.pdf_writer)
        if "/AcroForm" in self.pdf_writer._root_object:
            self.pdf_writer._root_object["/AcroForm"].update(
                {NameObject("/NeedAppearances"): BooleanObject(True)})

        
    def set_need_appearances_writer(self,writer):
        # See 12.7.2 and 7.7.2 for more information:
        # http://www.adobe.com/content/dam/acom/en/devnet/acrobat/pdfs/PDF32000_2008.pdf
        try:
            catalog = writer._root_object
            # get the AcroForm tree and add "/NeedAppearances attribute
            if "/AcroForm" not in catalog:
                writer._root_object.update({
                    NameObject("/AcroForm"): IndirectObject(len(writer._objects), 0, writer)})

            need_appearances = NameObject("/NeedAppearances")
            writer._root_object["/AcroForm"][need_appearances] = BooleanObject(True)
            return writer

        except Exception as e:
            print('set_need_appearances_writer() catch : ', repr(e))
            return writer

    def update(self,field_dictionary) :

        self.pdf_writer.addPage(self.pdf_reader.getPage(0))
        self.pdf_writer.addPage(self.pdf_reader.getPage(1))
        self.pdf_writer.updatePageFormFieldValues(self.pdf_writer.getPage(0), field_dictionary)

    def add_page(self,name) :
        self.annexe_input = open(UPLOAD_FOLDER + str(name) + '.pdf', "rb")
        self.pdf_writer.addPage(PdfFileReader(self.annexe_input, strict = False).getPage(0))

    def write_pdf(self) :

       self.pdf_writer.write(self.outputStream)

       self.inputStream.close()
       self.outputStream.close()
       self.annexe_input.close()
       os.remove(os.path.join(UPLOAD_FOLDER,'annexe_shareolders.pdf'))
