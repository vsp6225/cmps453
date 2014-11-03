import cgi
import cgitb
import urllib

from google.appengine.ext import ndb
from webapp2_extras.appengine.users import login_required, admin_required
from google.appengine.api import users
import webapp2
from import_export import ImportHandler, ExportHandler

import json
from string import Template

cgitb.enable()

LOGIN_PAGE_HTML = """
<html>
	<body>
		<form action="/Main" method="post">
			<div>Username:<textarea name="username" rows="1" cols="60"></textarea></div>
			<div>Password: <textarea name="password" rows="1" cols="60"></textarea></div>
			<div><input type="submit" value="Login"></div>
		</form>
	</body>
</html>
"""

MAIN_PAGE_HTML = """
<html>
	<body>
		<form action="/import" method="post">
			<div><input type="submit" value="Import Student Data"></div>
		</form>
		<form action="/export" method="post">
			<div><input type="submit" value="Export Student Data"></div>
		</form>
		<form action="/track" method="post">
			<div><input type="submit" value="Track Labs"></div>
		</form>
	</body>
</html>
"""

BACK_BUTTON = """
		<form action="/Main" method="post">
			<div><input type="submit" value="Back to Main Page"></div>
		</form>
	</body>
</html>
"""

USERNAME = 'dmeche520@gmail.com'
PASSWORD = 'password'


# JSON object template
jTemp = Template('{ "name" : "$name", "numLaps" : $numLaps, "teacherName" : "$teacherName", "barcodeID" : $barcodeID }')
# entry = jTemp.substitute("name='student_name', numLaps=1234, teacherName='teacher_Name', barcodeID=1111111")

# Data structure: Student Data
class studentData(ndb.Model):
	name = ndb.StringProperty(indexed=True)
	numLaps = ndb.IntegerProperty()
	teacherName = ndb.StringProperty(indexed=False)
	teacherName_lower = ndb.ComputedProperty(lambda self: self.teacherName.lower())
	barcodeID = ndb.IntegerProperty()

class MainPage(webapp2.RequestHandler):
	@login_required
	def get(self):
		self.response.write(MAIN_PAGE_HTML)
		
	def post(self):
		# THIS IS WHERE THE AUTHENTICATION WILL TAKE PLACE
		# get the username and password from the previous page
		user = cgi.escape(self.request.get('username'))
		passwd = cgi.escape(self.request.get('password'))
		
		# must use bcrypt
		# FOR NOW
		if (user != USERNAME and passwd != PASSWORD):
			self.redirect('/')
			
		self.response.write(MAIN_PAGE_HTML)
		
class LapTrackerHandler(webapp2.RequestHandler):
	def post(self):
		self.response.write('<html><body>Lap tracking to be handled here')
		self.response.write(BACK_BUTTON)
		
# assigns a web address to a handler
application = webapp2.WSGIApplication([
	('/', MainPage),
	('/import', ImportHandler),
	('/export', ExportHandler),
	('/track', LapTrackerHandler),
], debug=True)