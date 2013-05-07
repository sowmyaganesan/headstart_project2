import json
import bottle
from bottle import route, run, request, response, abort
from pymongo import Connection
from json import JSONEncoder
from bson.objectid import ObjectId
from bson import json_util
import urlparse
from dao.mongo import Storage

 
connection = Connection('localhost', 27017)
db = connection.mooc1

class MongoEncoder(JSONEncoder):
    def default(self,obj,**kwargs):
        if isinstance(obj,ObjectId):
            return str(obj)
        else:
            return JSONEncoder.default(obj,**kwargs)
"""
Add quiz
"""
        
@route('/quizzes', method='POST')
def add_document():
    data = request.body.readline()
    entity = json.loads(data)
    if not entity.has_key('id'):
        abort(400, 'No id specified')
    try:
       db['quizcollection'].save(entity)
    except ValidationError as ve:
        abort(400, str(ve))


"""
Delete quiz by id
"""
@route('/quiz/:id', method='DELETE')
def del_document(id):
    try:
       db['quizcollection'].remove({'id':id})
    except ValidationError as ve:
        abort(400, str(ve))
        
"""
Get Quiz by ID
"""
@route('/quiz/:id', method='GET')
def get_document(id):
    cursor = db['quizcollection'].find({"id":id})
    json_docs=[]
    for doc in cursor:
        json_doc=json.dumps(doc,default = json_util.default)
        json_docs.append(json_doc)
        json_docs.append("")

    if not json_docs:
        abort(404,'No document')
    return json_docs

"""
Update the quiz details
"""
@route('/quiz/:id',method='PUT')
def update_document(id):
    url_to_parse = request.url
    parsed_url = urlparse.urlparse(url_to_parse)
    query_as_dict = urlparse.parse_qs(parsed_url.query)
    for k,v in query_as_dict.items():
        try:
            if(k== "courseId"):
                db['quizcollection'].update({"id":id},{"$set":{k:v[0]}})
            if(k == "answer"):
                db['quizcollection'].update({"id":id}, {"$set":{ 'questions.0.answer' : v[0] }})
            if(k == "point"):
                db['quizcollection'].update({"id":id}, {"$set":{ 'questions.0.point' : v[0] }})
        except ValidationError as ve:
            abort(400,str(ve))
 
"""
List quiz by courseid
"""
@route('/quiz/course/:id', method='GET')
def get_document(id):
    print (id)
    cursor = db['quizcollection'].find({"courseId":id})
    json_docs=[]
    json_docs.append("[")
    for doc in cursor:
        json_doc=json.dumps(doc,default = json_util.default)
        json_docs.append(json_doc)
        json_docs.append(",")
  
    json_docs = json_docs[:-1]
    json_docs.append("]")
    if not json_docs:
        abort(404,'No document')
    return json_docs

"""
List quiz
"""
@route('/quiz/list', method='GET')
def get_document():
    cursor = db['quizcollection'].find()
    json_docs=[]
    for doc in cursor:
        json_doc=json.dumps(doc,default = json_util.default)
        json_docs.append(json_doc)
        json_docs.append("")

    if not json_docs:
        abort(404,'No document')
    return json_docs

"""
Add Discussion
"""
@route('/discussion', method='POST')
def add_discussion():
    data = request.body.readline()
    entity = json.loads(data)
    if not entity.has_key('id'):
        abort(400, 'No id specified')
    try:
       db['discussioncollection'].save(entity)
    except ValidationError as ve:
        abort(400, str(ve))

"""
List Discussion
"""
@route('/discussion/list', method='GET')
def get_document():
    cursor = db['discussioncollection'].find()
    json_docs=[]
    json_docs.append("[")
    for doc in cursor:
        json_doc=json.dumps(doc,default = json_util.default)
        json_docs.append(json_doc)
        json_docs.append(",")
  
    json_docs = json_docs[:-1]
    json_docs.append("]")
    if not json_docs:
        abort(404,'No document')
    return json_docs
"""
Get Discussion by ID
"""
@route('/discussion/:id', method='GET')
def get_document(id):
   cursor = db['discussioncollection'].find({"id":id})
   json_docs=[]
   for doc in cursor:
        json_doc=json.dumps(doc,default = json_util.default)
        json_docs.append(json_doc)
        json_docs.append("")

   if not json_docs:
       abort(404,'No document')
   return json_docs

"""
Update discussion
"""
@route('/discussion/:id',method='PUT')
def update_document(id):
    url_to_parse = request.url
    parsed_url = urlparse.urlparse(url_to_parse)
    query_as_dict = urlparse.parse_qs(parsed_url.query)
    print query_as_dict
    for k,v in query_as_dict.items():
        try:
            if(k=="messages"):
                db['discussioncollection'].update({"id":id},{"$set":{k:v}})
            else:
                db['discussioncollection'].update({"id":id},{"$set":{k:v[0]}})
        except ValidationError as ve:
            abort(400,str(ve))
"""
Delete Discussion
"""
@route('/discussion/:id', method='DELETE')
def del_document(id):
    try:
       db['discussioncollection'].remove({'id':id})
    except ValidationError as ve:
        abort(400, str(ve))

"""
Add Course
"""
@route('/course', method='POST')
def add_course():
    data = request.body.readline()
    entity = json.loads(data)
    if not entity.has_key('id'):
        abort(400, 'No id specified')
    try:
       db['coursecollection'].save(entity)
    except ValidationError as ve:
        abort(400, str(ve))

"""
List course
"""
@route('/course/list', method='GET')
def get_document():
    cursor = db['coursecollection'].find()
    json_docs=[]
    for doc in cursor:
        json_doc=json.dumps(doc,default = json_util.default)
        json_docs.append(json_doc)
        json_docs.append("")

    if not json_docs:
        abort(404,'No document')
    return json_docs
"""
Get course by ID
"""
@route('/course/:id', method='GET')
def get_document(id):
    cursor = db['coursecollection'].find({"id":id})
    json_docs=[]
    for doc in cursor:
        json_doc=json.dumps(doc,default = json_util.default)
        json_docs.append(json_doc)
        json_docs.append("")

    if not json_docs:
        abort(404,'No document')
    return json_docs
"""
Update course
"""
@route('/course/:id',method='PUT')
def update_document(id):
    url_to_parse = request.url
    parsed_url = urlparse.urlparse(url_to_parse)
    query_as_dict = urlparse.parse_qs(parsed_url.query)
    print query_as_dict
    for k,v in query_as_dict.items():
        try:
            if(k=="instructor" or k=="days" or k=="hours"):
                db['coursecollection'].update({"id":id},{"$set":{k:v}})
            else:
                db['coursecollection'].update({"id":id},{"$set":{k:v[0]}})
        except ValidationError as ve:
            abort(400,str(ve))
"""
Delete course
"""
@route('/course/:id', method='DELETE')
def del_document(id):
    try:
       db['coursecollection'].remove({'id':id})
    except ValidationError as ve:
        abort(400, str(ve))

"""
Add Announcement
"""
@route('/announcements', method='POST')
def add_course():
    data = request.body.readline()
    entity = json.loads(data)
    if not entity.has_key('id'):
        abort(400, 'No id specified')
    try:
       db['announcementcollection'].save(entity)
    except ValidationError as ve:
        abort(400, str(ve))

"""
List announcement
"""
@route('/announcement/list', method='GET')
def get_document():
    cursor = db['announcementcollection'].find()
    json_docs=[]
    json_docs.append("[")
    for doc in cursor:
        json_doc=json.dumps(doc,default = json_util.default)
        json_docs.append(json_doc)
        json_docs.append(",")
    
    json_docs = json_docs[:-1]
    json_docs.append("]")
    if not json_docs:
        abort(404,'No document')
    return json_docs

"""
Get announcement by ID
"""
@route('/announcement/:id', method='GET')
def get_documents(id):
    print (id)
    cursor = db['announcementcollection'].find({'id':id})
    json_docs=[]
    for doc in cursor:
        json_doc=json.dumps(doc,default = json_util.default)
        json_docs.append(json_doc)
        json_docs.append("")

    if not json_docs:
        abort(404,'No document')
    return json_docs


"""
Update announcement
"""
@route('/announcement/:id',method='PUT')
def update_document(id):
    url_to_parse = request.url
    parsed_url = urlparse.urlparse(url_to_parse)
    query_as_dict = urlparse.parse_qs(parsed_url.query)
    print query_as_dict
    for k,v in query_as_dict.items():
        try:
            db['announcementcollection'].update({"id":id},{"$set":{k:v[0]}})
        except ValidationError as ve:
            abort(400,str(ve))
"""
Delete announcement
"""
@route('/announcement/:id', method='DELETE')
def del_document(id):
    try:
       db['announcementcollection'].remove({'id':id})
    except ValidationError as ve:
        abort(400, str(ve))

"""
Get announcement by courseID
"""

@route('/announcement/findcourse/:id', method='GET')
def get_document(id):
    cursor = db['announcementcollection'].find({'courseId':id})
    json_docs=[]
    for doc in cursor:
        json_doc=json.dumps(doc,default = json_util.default)
        json_docs.append(json_doc)
        json_docs.append("")

    if not json_docs:
        abort(404,'No document')
    return json_docs


"""
Add Category
"""
@route('/categories', method='POST')
def add_course():
    data = request.body.readline()
    entity = json.loads(data)
    if not entity.has_key('id'):
        abort(400, 'No id specified')
    try:
       db['categorycollection'].save(entity)
    except ValidationError as ve:
        abort(400, str(ve))

"""
List category
"""
@route('/category/list', method='GET')
def get_document():
    cursor = db['categorycollection'].find()
    json_docs=[]
    json_docs.append("[")
    for doc in cursor:
        json_doc=json.dumps(doc,default = json_util.default)
        json_docs.append(json_doc)
        json_docs.append(",")
   
    json_docs = json_docs[:-1]
    json_docs.append("]")
    if not json_docs:
        abort(404,'No document')
    return json_docs

"""
Get category by ID
"""
@route('/category/:id', method='GET')
def get_document(id):
    print (id)
    cursor = db['categorycollection'].find({'id':id})
    json_docs=[]
    for doc in cursor:
        json_doc=json.dumps(doc,default = json_util.default)
        json_docs.append(json_doc)
        json_docs.append("")

    if not json_docs:
        abort(404,'No document')
    return json_docs

"""
Get category by name
"""
@route('/course/findcategory/:id', method='GET')
def get_document(id):
    print (id)
    cursor = db['coursecollection'].find({'category':id})
    json_docs=[]
    json_docs.append("[")
    for doc in cursor:
        json_doc=json.dumps(doc,default = json_util.default)
        json_docs.append(json_doc)
        json_docs.append(",")
   
    json_docs = json_docs[:-1]
    json_docs.append("]")
    if not json_docs:
        abort(404,'No document')
    return json_docs


"""
Add Discussion
"""
@route('/discussion', method='POST')
def add_discussion():
    data = request.body.readline()
    entity = json.loads(data)
    if not entity.has_key('id'):
        abort(400, 'No id specified')
    try:
       db['discussioncollection'].save(entity)
    except ValidationError as ve:
        abort(400, str(ve))


"""
Delete discussion
"""
@route('/discussion/:id', method='DELETE')
def del_document(id):
    try:
       db['discussioncollection'].remove({'id':id})
    except ValidationError as ve:
        abort(400, str(ve))


"""
Delete quiz by courseId
"""
@route('/quiz/deletecourse/:id', method='DELETE')
def delete_quiz(id):
	try:
		db['quizcollection'].remove({'courseId':id})
	except ValidationError as ve:
		abort (400,str(ve))

"""
Get message by discussion id
"""
@route('/message/:id', method='GET')
def get_message(id):
    cursor = db['messagecollection'].find({'discussion_id':id})
    json_docs=[]
    json_docs.append("[")
    for doc in cursor:
        json_doc=json.dumps(doc,default = json_util.default)
        json_docs.append(json_doc)
        json_docs.append(",")
    
    json_docs = json_docs[:-1]
    json_docs.append("]")
    if not json_docs:
        abort(404,'No document')
    return json_docs


"""
Add Message
"""
@route('/message', method='POST')
def add_discussion():
    data = request.body.readline()
    entity = json.loads(data)
    if not entity.has_key('discussion_id'):
        abort(400, 'No discussion_id specified')
    try:
       db['messagecollection'].save(entity)
    except ValidationError as ve:
        abort(400, str(ve))

"""
Fred
"""

@route('/courses/list', method='GET')
def get_document():
    cursor = db['coursecollection'].find()
    json_docs=["{"]
    x = 0
    for doc in cursor:
        x += 1
        json_doc=json.dumps(doc,default = json_util.default)
        json_docs.append('"(%d)":' % x)

        json_docs.append(json_doc)
        json_docs.append(",")
 
    json_docs = json_docs[:-1]
    json_docs.append("}")
    
    if not json_docs:
        abort(404,'No document')
    return json_docs


"""
User Related - Vaishak
"""
@route('/user', method='POST')
def user_add():
    output = None
    result = Storage().insert(request.json,)
    print result
    if result["res_code"] == 200:
      output = {"success" : True, "id":result["id"]}
    else:
      output = {"success" : False}
    response.status = result["res_code"]    
    response.add_header("Content-Type", "application/json")   
    return output
run(host='localhost', port=8080)
 
