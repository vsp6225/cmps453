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

from tmpl import BaseHandler

cgitb.enable()

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

class MainPage(BaseHandler):
	@login_required
	def get(self):
		self.render('html/index.html', {})
		
class LapTrackerHandler(BaseHandler):
	@login_required
	def get(self):
		self.render('html/tracker.html')
		
# assigns a web address to a handler
application = webapp2.WSGIApplication([
	('/', MainPage),
	('/import', ImportHandler),
	('/export', ExportHandler),
	('/track', LapTrackerHandler),
], debug=True)