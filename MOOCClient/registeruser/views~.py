from django.shortcuts import render_to_response
import json,requests
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect, HttpResponse
import simplejson
from django.http import Http404
import uuid
import urllib2
from time import gmtime, strftime
from django.core.context_processors import csrf
from django.core.context_processors import csrf
import urlparse
from django.contrib.auth import authenticate, login, logout
import sys
from django.contrib.auth.models import User
from django.db import IntegrityError

def home(request):
	r =  requests.get('http://localhost:8080/rest/course/doc1')
        courses=r.json()
	print(r.json())
	return render_to_response('courselist.html',{'courses': courses})

def search_form(request):
    return render(request, 'search_form.html')

def frontpage(request):
    return render_to_response('frontpage.html',context_instance=RequestContext(request))

# Search Course by id

def search(request):
    if 'id' in request.GET:
	
           r =  requests.get('http://localhost:8080/course/%s' % request.GET['id'])
	   if r.status_code == 404:
		return render(request, 'search_form.html',{'errors': ' 404 Document not found'},context_instance=RequestContext(request))
	   else:
	   	courses=r.json()
	   	return render_to_response('courselist.html',{'courses': courses})


# ADD course
def addcourse(request):
    errors = []
    if request.method != 'POST':
        r =  requests.get('http://localhost:8080/course/list')
        result = r.json()
        print(result)
            
        return render(request, 'add-course.html',{'result': result},context_instance=RequestContext(request)) 

    if request.method == 'POST':
        if not request.POST.get('title', ''):
            errors.append('Enter the Title')
        if not request.POST.get('section', ''):
            errors.append('Enter the Section.')
	if not request.POST.get('department', ''):
            errors.append('Enter the Department.')
	if not request.POST.get('instructorname', ''):
            errors.append('Enter the instructorname')
	if not request.POST.get('instructorid', ''):
            errors.append('Enter the instructorid')


        if not errors:
            if not request.POST.get('id', ''):
	        id1 = str(uuid.uuid4())[:6]
            else:
                id1 = request.POST['id']
            print(id1)
	    term= request.POST['term']
	    title= request.POST['title']
	    section = request.POST['section']
	    category = request.POST['category']
	    department = request.POST['department']
   	    name= request.POST['instructorname']
	    tid = request.POST['instructorid']
	    days = request.POST['days']
	    time = request.POST['time1']
	    Description = request.POST['Description']
	    version = request.POST['version']
            addstr = {"id": id1,"category": category,"term": term,"title": title,"section": section ,"dept":department,"instructor": [name,tid],"days": days,"hours": time,"Description":Description,"version":version}
	    coursejson=simplejson.dumps(addstr)

	    print(coursejson)
	    addurl = "http://localhost:8080/course"
	    r = requests.post(addurl, data=coursejson, allow_redirects=True)
	    print r.content
	    # response = urllib2.urlopen(addurl, coursejson)
	    return render(request, 'add-course.html',{'sucess': 'Success'},context_instance=RequestContext(request))
    return render(request, 'add-course.html',{'errors': errors},context_instance=RequestContext(request))




# Update Course
def updatecourse(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('courseid', ''):
            errors.append('Enter the courseid')
        if not request.POST.get('ufield', ''):
            errors.append('Enter the Update Value')
        if not errors:
	    courseid= request.POST['courseid']
	    print(courseid)
	    field1 = request.POST['field']
	    value =  request.POST['ufield'] 
                 
	    if value == 'all':
	       return render(request, 'add-course.html',{'id1':courseid},context_instance=RequestContext(request))
	    if value != 'all':

	       r =  requests.get('http://localhost:8080/course/%s' % request.POST['courseid'])
	       if r.status_code == 404:
		  return render(request, 'update-course.html',{'errors': ' 404 Document not found'},context_instance=RequestContext(request))
	       else:
	   	  updateurl = "http://localhost:8080/course/"+ courseid + "?" + field1 + "=" + value
	          print(updateurl)
		  r = requests.put(updateurl, ' ' , allow_redirects=True)
	          return render(request, 'update-course.html',{'values': 'Field Updated'},context_instance=RequestContext(request))
    return render(request, 'update-course.html',{'errors': errors},context_instance=RequestContext(request))


# DELETE Course
def deletecourse(request):
    errors = []
    if request.method != 'POST':
        r =  requests.get('http://localhost:8080/course/list')
        result = r.json()
        print(result)
            
        return render(request, 'delete-course.html',{'result': result},context_instance=RequestContext(request)) 

    ann_status = 'yes'
    dis_status = 'yes'
    if request.method == 'POST':
        if not request.POST.get('courseid', ''):
            errors.append('Enter the courseid')
        if not errors:
	    courseid= request.POST['courseid']
	    r =  requests.get('http://localhost:8080/course/%s' % request.POST['courseid'])
	    if r.status_code == 404:
		return render(request, 'delete-course.html',{'errors': ' 404 Document not found'},context_instance=RequestContext(request))
	    if r.status_code == 200:
	        r =  requests.get('http://localhost:8080/announcement/findcourse/%s' % request.POST['courseid'])
	        if r.status_code == 200:
		   # delete all announcement under the course id
		   re =  requests.delete('http://localhost:8080/announcement/course/%s' % request.POST['courseid']) 
		   ann_status='yes'
		   print(ann_status)
		
		r =  requests.get('http://localhost:8080/discussion/%s' % request.POST['courseid'])
	        if r.status_code == 200:
	           r =  requests.delete('http://localhost:8080/discussion/course/%s' % request.POST['courseid'])
	           dis_status='yes'
		   print(dis_status)

	      		
			
		if (ann_status == 'yes' and dis_status == 'yes'):
		   	re =  requests.delete('http://localhost:8080/course/%s' % request.POST['courseid'])   
		        return render(request, 'delete-course.html',{'success': 'Success'},context_instance=RequestContext(request))

    return render(request, 'delete-course.html',{'errors': errors},context_instance=RequestContext(request))



######################

#announcement - add

def addannounce(request):
    errors = []
    if request.method == 'POST':
	if not request.POST.get('title',' '):
	    errors.append('Enter the Title')
	if not request.POST.get('courseId',' '):
	    errors.append('Enter the CourseId')
	if not request.POST.get('description',' '):
	    errors.append('Enter the description')
	if not request.POST.get('postDate',' '):
	    errors.append('Enter the postDate')
	if not request.POST.get('status',' '):
	    errors.append('Enter the status')


	if not errors:
            print ('here1')
	    id1 = str(uuid.uuid4())[:6]
	    title= request.POST['title']
	    courseId = request.POST['courseId']
	    description = request.POST['description']
	    postDate = request.POST['postDate']
	    status = request.POST['status']
	    print (courseId)
	    for courseId in request.POST:
                    r = requests.get('http://localhost:8080/announcement/findcourse/%s' % request.POST[courseId])
                    print('here2')
                    print('_______________')
                    print(r.status_code)
                    if r.status_code == 200:
                         addstr = {"id": id1, "courseId":courseId,"title": title,"description": description,"postDate": postDate,"status": status}
                         announcejson=simplejson.dumps(addstr)
                         print(announcejson)
                         addurl = "http://localhost:8080/announcements"
                         r = requests.post(addurl, data= announcejson, allow_redirects=True)
                         print r.content
                         return render(request, 'add-announce.html',{'success':'successfully added'},context_instance=RequestContext(request))
                    else:
                         errors.append('Course Id not found')
                         return render(request,'add-announce.html',{'errors': errors},context_instance=RequestContext(request))
                                       
    return render(request,'add-announce.html',{'errors': errors},context_instance=RequestContext(request))

#search announcement by id
def search_announce(request):
    return render(request, 'search-announce.html')

def searchannouncement(request):
    announce=''
    if 'id' in request.GET:
	
           r =  requests.get('http://localhost:8080/announcement/%s' % request.GET['id'])
	   if r.status_code == 404:
		return render(request,'search-announce.html',{'errors': ' 404 Document not found'},context_instance=RequestContext(request))
	   else:
	   	announce=r.json()
    return render_to_response('announcelist.html',{'announce':announce})

# Update Announcement
def updateannouncement(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('announceid', ''):
            errors.append('Enter the announcement id')
        if not request.POST.get('ufield', ''):
            errors.append('Enter the Update Value')
        if not errors:
                announceid= request.POST['announceid']
                print(announceid)
                field1 = request.POST['field']
                value =  request.POST['ufield'] 
                 
        if value == 'all':
           return render(request, 'add-announce.html',{'id1':announceid},context_instance=RequestContext(request))
        if value != 'all':

           r =  requests.get('http://localhost:8080/announcement/%s' % request.POST['announceid'])
           if r.status_code == 404:
                   return render(request, 'update-announce.html',{'errors': ' 404 Document not found'},context_instance=RequestContext(request))
           else:
              updateurl = "http://localhost:8080/announcement/"+ announceid + "?" + field1 + "=" + value
              print(updateurl)
              r = requests.put(updateurl, ' ' , allow_redirects=True)
              return render(request, 'update-announce.html',{'values': 'Field Updated'},context_instance=RequestContext(request))
    return render(request, 'update-announce.html',{'errors': errors},context_instance=RequestContext(request))

# DELETE Announcement
def deleteannounce(request):
    errors = []
    if request.method != 'POST':
        r =  requests.get('http://localhost:8080/announcement/list')
        result = r.json()
        print(result)
            
        return render(request, 'delete-announce.html',{'result': result},context_instance=RequestContext(request)) 

    if request.method == 'POST':
        if not request.POST.get('announceid', ''):
            errors.append('Enter the announcementId')
        if not errors:
                announceid= request.POST['announceid']
                r =  requests.get('http://localhost:8080/announcement/%s' % request.POST['announceid'])
                if r.status_code == 404:
                        return render(request, 'delete-announce.html',{'errors': ' 404 Document not found'},context_instance=RequestContext(request))
                if r.status_code == 200:
                        re =  requests.delete('http://localhost:8080/announcement/%s' % request.POST['announceid'])   
                        return render(request, 'delete-announce.html',{'success': 'success'},context_instance=RequestContext(request))

    return render(request, 'delete-announce.html',{'errors': errors},context_instance=RequestContext(request))

#display all announcements
def displayannounce(request):
	r=  requests.get('http://localhost:8080/announcement/list')
	if r.status_code == 404:
                return render(request, 'all-announce.html',{'errors': ' 404 Document not found'},context_instance=RequestContext(request))
	if r.status_code == 200:
                announce=r.json()
                print(announce)
                return render_to_response('all-announce.html',{'announce': announce})

##############################  

# add category

def addcategory(request):
    errors = []
    if request.method == 'POST':
	if not request.POST.get('name',' '):
	    errors.append('Enter the Name')
	if not request.POST.get('description',' '):
	    errors.append('Enter the description')
	if not request.POST.get('createDate',' '):
	    errors.append('Enter the createDate')
	if not request.POST.get('status',' '):
	    errors.append('Enter the status')


	if not errors:
	    id1 = str(uuid.uuid4())[:6]
	    name = request.POST['name']
	    description = request.POST['description']
	    createDate = request.POST['createDate']
	    status = request.POST['status']
	    addstr = {"id": id1, "name":name,"description": description,"createDate": createDate,"status": status}
	    categoryjson=simplejson.dumps(addstr)
	    
	    print(categoryjson)
	    
	    addurl = "http://localhost:8080/categories"
	    r = requests.post(addurl, data= categoryjson, allow_redirects=True)
	    print r.content
            return render(request, 'add-category.html',{'success':'successfully added'},context_instance=RequestContext(request))
    return render(request, 'add-category.html',{'errors': errors},context_instance=RequestContext(request))

#search category by id

def search_category(request):
    print ('helo')
    if request.method != 'POST':
        	r =  requests.get('http://localhost:8080/category/list')
       		result = r.json()
        	print(result)
            
        	return render(request, 'search-category.html',{'result': result},context_instance=RequestContext(request)) 


def searchcategory(request):
           print ('here')
	           if request.method == 'POST':
                  	 r =  requests.get('http://localhost:8080/course/findcategory/%s' % request.POST['category'])
                   if r.status_code == 404:
                           return render(request,'search-category.html',{'errors': 'No courses in that category'},context_instance=RequestContext(request))
                   if r.status_code == 200:
                        category = r.json()
                        return render_to_response('categorylist.html',{'category':category})

#display all category
                
def displaycategory(request):
	r=  requests.get('http://localhost:8080/category/list')
	
	if r.status_code == 404:
                return render(request, 'all-category.html',{'errors': '404 Document not found'},context_instance=RequestContext(request))
        
	if r.status_code == 200:
                category=r.json()
                return render_to_response('all-category.html',{'category': category})

# add Discussion

def adddiscuss(request):
    errors = []
    if request.method == 'POST':
	if not request.POST.get('title',' '):
	    errors.append('Enter the Title')
	if not request.POST.get('created_by',' '):
	    errors.append('Enter the Created by')
	if not request.POST.get('created_at',' '):
	    errors.append('Enter the created at')
	if not request.POST.get('updated_at',' '):
	    errors.append('Enter the updated date')


	if not errors:
	    id1 = str(uuid.uuid4())[:6]
	    title = request.POST['title']
	    created_by = request.POST['created_by']
	    created_at = request.POST['created_at']
	    updated_at = request.POST['updated_at']
	    addstr = {"id": id1, "title":title,"created_by": created_by,"created_at": created_at,"updated_at": updated_at}
	    discussjson=simplejson.dumps(addstr)
	    
	    print(discussjson)
	    
	    addurl = "http://localhost:8080/discussion"
	    r = requests.post(addurl, data= discussjson, allow_redirects=True)
	    print r.content
            return render(request, 'add-discuss.html',{'success':'successfully added'},context_instance=RequestContext(request))
    return render(request, 'add-discuss.html',{'errors': errors},context_instance=RequestContext(request))

# DELETE Discussion
def deletediscuss(request):
    errors = []
    if request.method != 'POST':
        r =  requests.get('http://localhost:8080/discussion/list')
        result = r.json()
        print(result)
            
        return render(request, 'delete-discuss.html',{'result': result},context_instance=RequestContext(request)) 
    if request.method == 'POST':
        if not request.POST.get('discussid', ''):
            errors.append('Enter the DiscussionId')
        if not errors:
                discussid= request.POST['discussid']
                r =  requests.get('http://localhost:8080/discussion/%s' % request.POST['discussid'])
                if r.status_code == 404:
                        return render(request, 'delete-discuss.html',{'errors': ' 404 Document not found'},context_instance=RequestContext(request))
                if r.status_code == 200:
                        re =  requests.delete('http://localhost:8080/discussion/%s' % request.POST['discussid'])   
                        return render(request, 'delete-discuss.html',{'success': 'success'},context_instance=RequestContext(request))

    return render(request, 'delete-discuss.html',{'errors': errors},context_instance=RequestContext(request))


# DELETE Quiz
def deletequiz(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('quizid', ''):
            errors.append('Enter the quizId')
        if not errors:
                quizid= request.POST['quizid']
                r =  requests.get('http://localhost:8080/quiz/%s' % request.POST['quizid'])
                if r.status_code == 404:
                        return render(request, 'delete-quiz.html',{'errors': ' 404 Document not found'},context_instance=RequestContext(request))
                if r.status_code == 200:
                        re =  requests.delete('http://localhost:8080/quiz/%s' % request.POST['quizid'])   
                        return render(request, 'delete-quiz.html',{'success': 'success'},context_instance=RequestContext(request))

    return render(request, 'delete-quiz.html',{'errors': errors},context_instance=RequestContext(request))



#############################################################

def search_quiz(request):
    return render(request, 'search_quiz.html')
 
def searchquiz(request):
    quiz = ''
    if 'id' in request.GET:
        r =  requests.get('http://localhost:8080/quiz/course/%s' % request.GET['id'])
        if r.status_code == 404:
            return render(request, 'search_quiz.html',{'errors': ' 404 Document not found'},context_instance=RequestContext(request))
        else:
            quiz = r.json()
            print(quiz)
            return render_to_response('quizlist.html',{'quiz': quiz})
 
 
 
def addquiz(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('courseId', ''):
            errors.append('Enter course id')
        if not request.POST.get('question', ''):
            errors.append('Enter question')
        if not request.POST.get('opt1', ''):
            errors.append('Enter Option1')
        if not request.POST.get('opt2', ''):
            errors.append('Enter Option2')
        if not request.POST.get('opt3', ''):
            errors.append('Enter Option3')
        if not request.POST.get('a1', ''):
            errors.append('Enter Answer')
        if not request.POST.get('p1', ''):
            errors.append('Enter points')
       
 
        #search for course id
        x = search_course_id(request.POST['courseId'])
        if not x:
            if not errors:
                errors.append('course id not found!')
        if not errors and x:
            id1 = str(uuid.uuid4())[:6]
            cid = request.POST['courseId']
            ques = request.POST['question']
            opt1 = request.POST['opt1']
            opt2 = request.POST['opt2']
            opt3 = request.POST['opt3']
            a1 = request.POST['a1']
            p1 = request.POST['p1']
 
            ques = ques.strip()
            opt1 = opt1.strip()
            opt2 = opt2.strip()
            opt3 = opt3.strip()
            a1 = a1.strip()
            p1 = p1.strip()
            list1 = [opt1,opt2,opt3]
           
            quizjson=simplejson.dumps({"id": id1, "courseId": cid, "questions":([{"question":"%s" %ques,"options":list1,"answer":a1,"point": p1}])})
            print(quizjson)
            addurl = "http://localhost:8080/quizzes"
            r = requests.post(addurl, data=quizjson, allow_redirects=True)
            print r.content
            # response = urllib2.urlopen(addurl, coursejson)
            return render(request,'add-quiz.html',{'success':'Sucessfully added'},context_instance=RequestContext(request))
    return render(request, 'add-quiz.html',{'errors': errors},context_instance=RequestContext(request))
 
def search_course_id(id):
    addurl = "http://localhost:8080/course/list"
    r = requests.get(addurl, data="", allow_redirects=True)
    if(r.status_code==200):
   	 return True
   # line = r.content
  #  data = json.loads(line)
   # for k, v in data.items():
       # for a, b in v.iteritems():
           # if(a== "id"):
             #  print a, b
             #  if( b == id):
                 #  return True
    else:
       return False
 
# Update Quiz
def updatequiz(request):
    value = []
    errors = []
    if request.method == 'POST':
        if not request.POST.get('quizid', ''):
            errors.append('Enter the quizid')
        if not request.POST.get('questions', ''):
            errors.append('Enter question')
        if not request.POST.get('opt1', ''):
            errors.append('Enter update options')
        if not request.POST.get('an1', ''):
            errors.append('Enter Answer')
        if not request.POST.get('pt1', ''):
            errors.append('Enter Points')
           
        if not errors:
            quizid = request.POST['quizid']
            ques   = request.POST['questions']
            opt1   = request.POST['opt1']
            an1    = request.POST['an1']
            pt1    = request.POST['pt1']
            r =  requests.get('http://localhost:8080/quiz/%s' % quizid)
            if r.status_code == 404:
                errors.append(' 404 Document not found')
                return render(request, 'update-quiz.html',{'errors': errors},context_instance=RequestContext(request))
            else:
                updateurl = "http://localhost:8080/quiz/" + quizid+ "?" + "answer" + "=" + an1 + "&point=" + pt1
                r = requests.put(updateurl, ' ' , allow_redirects=True)
                return render(request, 'update-quiz.html',{'values': 'Field Updated'},context_instance=RequestContext(request))
 
       
            
    return render(request, 'update-quiz.html',{'errors': errors},context_instance=RequestContext(request))

##############################

##############


#display all discussion
def displaydiscussion(request):
	r=  requests.get('http://localhost:8080/discussion/list')
	if r.status_code == 404:
                return render(request, 'discussion_list.html',{'errors': ' 404 Document not found'},context_instance=RequestContext(request))
	if r.status_code == 200:
                discussion=r.json()
                print(discussion)
                return render_to_response('discussion_list.html',{'discussion_list': discussion})


#display all message
def displaymessage(request,*args, **kwargs):
	
	
        discussionurl = request.get_full_path()
	print(discussionurl)	
	
        v = kwargs	
	
        
	
	errors = []
	
        if "add" in discussionurl:
                print("in ssssss")
		if not request.GET.get('content',' '):
		    errors.append('Enter the content')
		if not request.GET.get('created_by',' '):
		    errors.append('Enter your email address')
                print(errors)
		if not errors:
		    
		    disid = request.GET['disid']
		    
		    content= request.GET['content']
		    created_by = request.GET['created_by']
		    created_at = strftime("%Y-%m-%d", gmtime())
		    updated_at = created_at
		    addstr = {"discussion_id": disid, "content":content,"created_by": created_by,"created_at": created_at,"updated_at":updated_at}
		    messagejson=simplejson.dumps(addstr)
		    print("helllllllllllllllllllllllo")
		    print(messagejson)
		    addurl = "http://localhost:8080/message"
		    r = requests.post(addurl, data= messagejson, allow_redirects=True)
	            return render_to_response('discussion_detail.html',{'messages_list': messagejson, 'disid' : v['id']})
            
                return render(request, 'discussion_detail.html',{'errors': errors},context_instance=RequestContext(request))
	else:
		r=  requests.get('http://localhost:8080/message/%s' % v['id'])
		if r.status_code == 200:
		        message=r.json()
		        return render_to_response('discussion_detail.html',{'messages_list': message, 'disid' : v['id']})
	
   
            
        


#Add - message to particular discussion

def addcomment(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('discussion_detail.html',c, context_instance=RequestContext(request))

def addmessage(request):
        errors = []
        if request.method == 'GET':
                
		if not request.GET.get('content',' '):
		    errors.append('Enter the content')
		if not request.GET.get('created_by',' '):
		    errors.append('Enter your email address')

		if not errors:
		    
		    disid = request.GET['disid']
		    
		    content= request.GET['content']
		    created_by = request.GET['created_by']
		    created_at = strftime("%Y-%m-%d", gmtime())
		    updated_at = created_at
		    addstr = {"discussion_id": disid, "content":content,"created_by": created_by,"created_at": created_at,"updated_at":updated_at}
		    messagejson=simplejson.dumps(addstr)
		    print("helllllllllllllllllllllllo")
		    print(messagejson)
		    addurl = "http://localhost:8080/message"
		    r = requests.post(addurl, data= messagejson, allow_redirects=True)
	            return render_to_response('discussion_detail.html',{'messages_list': message, 'disid' : v['id']})
            
        return render(request, 'discussion_detail.html',{'errors': errors},context_instance=RequestContext(request))



##################

#display all message
def displaymessage(request,*args, **kwargs):
    
    
        discussionurl = request.get_full_path()
        v = kwargs    
        errors = []
    
        if "add" in discussionurl:
   
                if not request.GET.get('content',' '):
                    errors.append('Enter the content')
                if not request.GET.get('created_by',' '):
                    errors.append('Enter your email address')
                        
                if not errors:
                    
                    disid = request.GET['disid']
                    
                    content= request.GET['content']
                    created_by = request.GET['created_by']
                    created_at = strftime("%Y-%m-%d", gmtime())
                    updated_at = created_at
                    addstr = {"discussion_id": disid, "content":content,"created_by": created_by,"created_at": created_at,"updated_at":updated_at}
                    messagejson=simplejson.dumps(addstr)
                    print('hello')
                    print (messagejson)
                   
                    addurl = "http://localhost:8080/message"
                    r = requests.post(addurl, data= messagejson, allow_redirects=True)
                    r=  requests.get('http://localhost:8080/message/%s' % v['id'])
                    message=r.json()
                    return render_to_response('discussion_detail.html',{'messages_list': message, 'disid' : v['id']})
                    
                return render(request, 'discussion_detail.html',{'errors': errors},context_instance=RequestContext(request))
        else:
                r=  requests.get('http://localhost:8080/message/%s' % v['id'])
                if r.status_code == 200:
                        message=r.json()
                        return render_to_response('discussion_detail.html',{'messages_list': message, 'disid' : v['id']})
		if r.status_code == 404:
			return render_to_response('discussion_detail.html')

#Login Related Functions

#Login - Signup
def signup(request):
   return render_to_response("signup.html")

#Login - Signin
def signin(request):
	ctx = {}
	if request.user.is_authenticated():
		return render_to_response("home.html",ctx,context_instance=RequestContext(request))
	else:
		return render_to_response("login.html")

#Login - Login
def login_user(request):
    ctx = {}
    if request.user.is_authenticated():
        return render_to_response("home.html",ctx,context_instance=RequestContext(request))
    if request.method != 'POST':
    	ctx={"message":"You are not logged in."}
    	return render_to_response("login.html",ctx,context_instance=RequestContext(request))
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(username=email, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            print user.first_name
            ctx = {"fName": user.first_name, "lName": user.last_name }
            return render_to_response("home.html",ctx,context_instance=RequestContext(request))
        else:
            ctx = {"message" :"Login Failed. Please try Again"}
            return render_to_response("login.html",ctx,context_instance=RequestContext(request))
    else:
        ctx = {"message" :"Login Failed. Please try Again"}
        return render_to_response("login.html",ctx,context_instance=RequestContext(request))

#Login - Logout
def logout_user(request):
    logout(request)
    return render_to_response('login.html')

#Login - Register
def add_user(request):
	ctx = {}
	if request.method == "POST" :
		email = request.POST.get("email")
		password = request.POST.get("password")
		firstname = request.POST.get("firstname")
		lastname = request.POST.get("lastname")
	try:
		djangouser = User.objects.create_user(email,email,password)
		djangouser.first_name = firstname
		djangouser.last_name = lastname
		djangouser.save()
		#ctx = {"message" : "User successfully registered, please login to continue."}
		#return render_to_response("login.html",ctx,context_instance=RequestContext(request))
	except NameError(" error"):
		print "Unexpected error:", sys.exc_info()[0]
		ctx = {'message':'User ID already exists.'}
		return render_to_response("signup.html",ctx,context_instance=RequestContext(request))
	except IntegrityError:
		print "Unexpected error:", sys.exc_info()[0]
		ctx = {'message':'User ID already exists.'}
		return render_to_response("signup.html",ctx,context_instance=RequestContext(request))
	payload = {"email":email, "own":[], "enrolled":[], "quizzes":[]} 
	response = requests.post("http://127.0.0.1:8080/user", data=json.dumps(payload), headers={'content-type': 'application/json', 'charset': 'utf-8'})
	if response.status_code == 200:
		ctx = {"message" : "User successfully registered, please login to continue."}
		return render_to_response("login.html",ctx)
	ctx = {"message":"Failed to register"}
	return render_to_response("signup.html",ctx)

def update_user(request):
	ctx={}
	if not(request.user.is_authenticated()):
		ctx={"message":"You are not logged in."}
		return render_to_response("login.html",ctx,context_instance=RequestContext(request))
	if request.method != 'POST':
		return render_to_response("updateprofile.html",ctx,context_instance=RequestContext(request))
	password = request.POST['password']
	firstname = request.POST.get('firstname')
	lastname = request.POST.get('lastname')
	if len(password.strip())>0:
		print len(password)
		request.user.set_password(password)
	if firstname is not None:
		request.user.first_name = firstname
	if lastname is not None:
		request.user.last_name = lastname
	request.user.save()

	return render_to_response('home.html',ctx,context_instance=RequestContext(request))

def enroll_course(request):
	ctx={}
	if not(request.user.is_authenticated()):
		ctx={"message":"You are not logged in."}
		return render_to_response("login.html",ctx,context_instance=RequestContext(request))
	
	courseid = request.GET.get('id')
	updateurl = "http://127.0.0.1:8080/course/enroll?email="+request.user.username+"&courseid="+courseid
	responsecode = requests.put(updateurl, headers={'content-type': 'application/json', 'charset': 'utf-8'})
	ctx={"message":"You Have Been enrolled"}
	#TODO: Redirect to home page
	return render_to_response('home.html',ctx,context_instance=RequestContext(request))

def drop_course(request):
	ctx={}
	if not(request.user.is_authenticated()):
		ctx={"message":"You are not logged in."}
		return render_to_response("login.html",ctx,context_instance=RequestContext(request))
	courseid = request.GET.get('id')
	dropurl = "http://127.0.0.1:8080/course/drop?email="+request.user.username+"&courseid="+courseid
	responsecode = requests.put(dropurl, headers={'content-type': 'application/json', 'charset': 'utf-8'})
	ctx={"message":"Course Dropped"}
	#TODO: Redirect to home page
	return render_to_response('home.html',ctx,context_instance=RequestContext(request))
