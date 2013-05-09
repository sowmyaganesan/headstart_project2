from django.conf.urls import patterns, include, url


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    # Examples:
    url(r'^$', 'registeruser.views.frontpage', name='frontpage'),
    url(r'^frontpage', 'registeruser.views.frontpage', name='frontpage'),
    url(r'^$', 'registeruser.views.frontpage', name='frontpage'),
    
    #Course Related Views
    url(r'^add-course/$', 'registeruser.views.addcourse', name='addcourse'),
    url(r'^update-course/$', 'registeruser.views.updatecourse', name='updatecourse'),
    url(r'^delete-course/$', 'registeruser.views.deletecourse', name='deletecourse'),
    url(r'^search-form/$', 'registeruser.views.search_form', name='search_form'),
    url(r'^search/$','registeruser.views.search',name='search'),

    #Announcement Related Views
    url(r'^add-announce/$','registeruser.views.addannounce',name='addanounce'),
    #url(r'^search-announce/$', 'registeruser.views.search_announce', name='search_announce'),
    #url(r'^searchannouncement/$','registeruser.views.searchannouncement',name='searchanouncement'),
    url(r'^update-announce/$', 'registeruser.views.updateannouncement', name='updateannouncement'),
    url(r'^delete-announce/$', 'registeruser.views.deleteannounce', name='deleteannounce'),
    url(r'^all-announce/$', 'registeruser.views.displayannounce', name='displayannounce'),

    #Category Related Views
    url(r'^add-category/$','registeruser.views.addcategory',name='addcategory'),
    url(r'^search-category/$', 'registeruser.views.search_category', name='search_category'),
    url(r'^searchcategory/$','registeruser.views.searchcategory',name='searchcategory'),
    url(r'^all-category/$','registeruser.views.displaycategory',name='displaycategory'),

    #Quiz Related Views
    url(r'^delete-quiz/$', 'registeruser.views.deletequiz', name='deletequiz'),
    url(r'^search_quiz/$', 'registeruser.views.search_quiz', name='search_quiz'),
    url(r'^searchquiz/$','registeruser.views.searchquiz',name='searchquiz'),
    url(r'^update-quiz/$', 'registeruser.views.updatequiz', name='updatequiz'),
    url(r'^add-quiz/$', 'registeruser.views.addquiz', name='addquiz'),


    #Discussion Related Views
    url(r'^discussion_list/$', 'registeruser.views.displaydiscussion', name='displaydiscussion'),
    url(r'^discussion_detail/(?P<id>[a-zA-Z0-9-]+)/$', 'registeruser.views.displaymessage', name='displaymessage'),
    url(r'^discussion_detail/(?P<id>[a-zA-Z0-9-]+)/add/$', 'registeruser.views.displaymessage', name='displaymessage'),
    #url(r'^addmessage/$', 'registeruser.views.addmessage', name='addmessage'),
    url(r'^add-discuss/$','registeruser.views.adddiscuss',name='adddiscuss'),
    url(r'^delete-discuss/$', 'registeruser.views.deletediscuss', name='deletediscuss'),

    #User Account Related Views
    url(r'^signup/$', 'registeruser.views.signup'), 
    url(r'^signin/$', 'registeruser.views.signin'),
    url(r'^add_user$', 'registeruser.views.add_user'),
    url(r'^login$', 'registeruser.views.login_user', name='signin'), 
    url(r'^logout/$', 'registeruser.views.logout_user'),
    url(r'^update_user/$', 'registeruser.views.update_user'),
    url(r'^enroll_course/$', 'registeruser.views.enroll_course'),
    url(r'^drop_course/$', 'registeruser.views.drop_course'),
    url(r'^my_course/$', 'registeruser.views.my_course'),

    # url(r'^MOOCClient/', include('MOOCClient.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)



