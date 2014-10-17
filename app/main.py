import webapp2
from model import ParserDemo

class HomePage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Hello, World")


app = webapp2.WSGIApplication([
	('/', HomePage),
	('/demo', ParserDemo),
])

