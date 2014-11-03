import webapp2
from lapTracker import BACK_BUTTON

class ImportHandler(webapp2.RequestHandler):
	def post(self):
		self.response.write('<html><body>Import data to be handled here')
		self.response.write(BACK_BUTTON)
		
class ExportHandler(webapp2.RequestHandler):
	def post(self):
		self.response.write('<html><body>Export data to be handled here')
		self.response.write(BACK_BUTTON)
