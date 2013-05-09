import sys
import traceback
from bson.objectid import ObjectId
import simplejson
from json import JSONEncoder

from pymongo import Connection

class MongoEncoder(JSONEncoder):
    def default(self,obj,**kwargs):
        if isinstance(obj,ObjectId):
            return str(obj)
        else:
            return JSONEncoder.default(obj,**kwargs)

class Storage(object):
	def __init__(self):
		connection = Connection()
		db=connection['test']
		self.user = db['user']
	def insert(self,json):
		response_code=200
		obj_id=None
		try:
			query={"email":json["email"]}
			total = self.user.find(query).count()
			if(total==0):
				obj_id = self.user.insert(json)
				obj_id = json["email"]
			else:
				response_code = 409
			return {'res_code':response_code,"id":obj_id}
		except:
			traceback.print_exec()
			return {'res_code':500,"id":obj_id}
	def enroll_course(self,email, course_id):
		try:
			self.user.update({"email":email}, {'$push': {'enrolled': course_id}})
			return 200
		except:
			return 500
	def drop_course(self,email, course_id):
		try:
			self.user.update({"email":email}, {'$pull': {'enrolled': course_id}})
			return 200
		except:
			return 500
	def my_enrolled_courses(self,email):
		try:
			response = self.user.find({"email":email},{'enrolled':1,'own':1})
			if not response:
				abort(404, 'No document with id %s' % id)
			response.content_type = 'application/json'
			entries = [entry for entry in response]
			return MongoEncoder().encode(entries)
		except NameError(" error"):
			return "Exception"
