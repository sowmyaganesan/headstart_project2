import sys
import traceback
from bson.objectid import ObjectId

from pymongo import Connection

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