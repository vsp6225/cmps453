import webapp2
import json
import csv
import xlrd
from google.appengine.ext import ndb

class Teacher(ndb.Model):
	name = ndb.StringProperty()

	def getTotalMiles(self):
		students = Student.all().filter("teacher=", self).fetch(100)
		return sum([s.getTotalMiles() for s in students])

class Student(ndb.Model):
	ID = ndb.IntegerProperty()
	name = ndb.StringProperty()
	grade = ndb.StringProperty()
	teacher = ndb.KeyProperty(Teacher)
	track_1_laps = ndb.IntegerProperty()
	track_2_laps = ndb.IntegerProperty()

	def getTotalMiles(self):
		return self.track_2_laps * 0.25 + self.track_1_laps * 0.1


class ParserDemo(webapp2.RequestHandler):
	def get(self):
		book = xlrd.open_workbook("sample-data/Laps.xlsx")
		self.response.out.write("%d sheets<br>" % book.nsheets)
		self.response.out.write("sheet names: <br>%s<br>" % "<br>".join(book.sheet_names()))

		# id, name, teacher, grade
		teachers = {}
		students = {}
		id_sheet = book.sheet_by_name("IDs")
		for i in xrange(id_sheet.nrows-2):
			ID, name, teacherName, grade = map(lambda X: X.value, id_sheet.row(i+2))

			teacherName = " ".join(teacherName.strip().split())
			if teacherName in teachers:
				teacher = teachers[teacherName]
			else:
				teacher = Teacher(id=teacherName, name=teacherName)
				teachers[teacherName] = teacher
				teacher.put()

			student = Student(name=name, id=int(ID), ID=int(ID), grade=str(grade), teacher=teacher.key, track_1_laps=0, track_2_laps=0)
			students[name] = student

		# read other sheets to assign lap counts

		ndb.put_multi(students.values())
