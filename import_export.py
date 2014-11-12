import webapp2
from xl2model import parseWorkbook
from xlrd import open_workbook
import tmpl
import json

class ImportHandler(tmpl.BaseHandler):
	def get(self):
		self.render('html/import.html', {})
	def post(self):
		upload = self.request.get('file')
		wb = open_workbook(file_contents=upload)
		classes, errors = parseWorkbook(wb)
		self.render('html/view_all.html', {
			'classes': classes,
			'errors': errors,
		})

class ExportHandler(webapp2.RequestHandler):
	def post(self):
		self.response.write('<html><body>Export data to be handled here')
		self.response.write(BACK_BUTTON)
