import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'
DEFAULT_GUESTBOOK_NAME1= 'default_guestbook1'
DEFAULT_GUESTBOOK_NAME2= 'default_guestbook2'

# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('Guestbook', guestbook_name)


class Greeting(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

class MemberOnePage(webapp2.RequestHandler):
    def get(self):

        guestbook_name = self.request.get('guestbook_name1',
                                          DEFAULT_GUESTBOOK_NAME1)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user_name': users.get_current_user(),
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }
        
        template = JINJA_ENVIRONMENT.get_template('member_one.html')
        self.response.write(template.render(template_values))
        

class MemberTwoPage(webapp2.RequestHandler):
    def get(self):
    
        guestbook_name = self.request.get('guestbook_name2',
                                          DEFAULT_GUESTBOOK_NAME2)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user_name': users.get_current_user(),
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('member_two.html')
        self.response.write(template.render(template_values))


class Home(webapp2.RequestHandler):

     def get(self):

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user_name': users.get_current_user(),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('home.html')
        self.response.write(template.render(template_values))


class Dashboard(webapp2.RequestHandler):

    def get(self):
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user_name': users.get_current_user(),
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


class Guestbook(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/guestbook?' + urllib.urlencode(query_params))


class Guestbook1(webapp2.RequestHandler):
    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        guestbook_name = self.request.get('guestbook_name1',
                                          DEFAULT_GUESTBOOK_NAME1)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/module-1/1?' + urllib.urlencode(query_params))

class Guestbook2(webapp2.RequestHandler):
    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        guestbook_name = self.request.get('guestbook_name2',
                                          DEFAULT_GUESTBOOK_NAME2)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/module-1/2?' + urllib.urlencode(query_params))

class Thesis(ndb.Model):
    thesis_title = ndb.StringProperty(indexed=False)
    thesis_sy = ndb.StringProperty(indexed=False)
    descrip = ndb.StringProperty(indexed=False)
    status = ndb.StringProperty(indexed=False)
    proponents = ndb.StringProperty(indexed=False)
    adviser = ndb.StringProperty(indexed=False)

class SuccessPageHandler(webapp2.RequestHandler):
    def get(self):

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user_name': users.get_current_user(),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('success_1.html')
        self.response.write(template.render(template_values))


class ThesisViewHandler(webapp2.RequestHandler):
    def get(self, thesis_id):

        thesis = Thesis.query().fetch()
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        
        template_values = {
            "all_thesis": thesis,
            "id"        : int(thesis_id),
            'user_name' : users.get_current_user(),
            'url'       : url,
            'url_linktext': url_linktext
        }
        template = JINJA_ENVIRONMENT.get_template('thesis_view.html')
        self.response.write(template.render(template_values))


class ThesisListHandler(webapp2.RequestHandler):
    def get(self):

        thesis = Thesis.query().fetch()
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        template_values = {
            "all_thesis": thesis,
            'user_name' : users.get_current_user(),
            'url'       : url,
            'url_linktext': url_linktext
        }
        template = JINJA_ENVIRONMENT.get_template('thesis_list.html')
        self.response.write(template.render(template_values))


class ThesisNewHandler(webapp2.RequestHandler):
    def get(self):

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user_name': users.get_current_user(),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('thesis_new.html')
        self.response.write(template.render(template_values))

    def post(self):
        thesis = Thesis()
        thesis.thesis_title = self.request.get('thesis_title')
        thesis.thesis_sy= self.request.get('thesis_sy')
        thesis.descrip = self.request.get('descrip')
        thesis.status = self.request.get ('status')
        thesis.proponents = self.request.get('proponents')
        thesis.adviser = self.request.get('adviser')
        thesis.put()
        self.redirect('/thesis/success')



class Adviser(ndb.Model):
    adviser_title = ndb.StringProperty(indexed=False)
    adviser_fname = ndb.StringProperty(indexed=False)
    adviser_lname = ndb.StringProperty(indexed=False)
    email2 = ndb.StringProperty(indexed=False)
    pnumber = ndb.StringProperty(indexed=False)
    dept = ndb.StringProperty(indexed=False)

class SuccessPageHandler2(webapp2.RequestHandler):
    
    def get(self):

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user_name': users.get_current_user(),
            'url': url,
            'url_linktext': url_linktext,
        }
        template = JINJA_ENVIRONMENT.get_template('success_2.html')
        self.response.write(template.render(template_values))


class AdviserViewHandler(webapp2.RequestHandler):
    def get(self, adviser_id):
        adviser = Adviser.query().fetch()

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            "all_adviser": adviser,
            "id"        : int(adviser_id),
            'user_name' : users.get_current_user(),
            'url'       : url,
            'url_linktext': url_linktext
        }
        template = JINJA_ENVIRONMENT.get_template('adviser_view.html')
        self.response.write(template.render(template_values))


class AdviserListHandler(webapp2.RequestHandler):
    def get(self):

        adviser = Adviser.query().fetch()
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        template_values = {
            "all_adviser": adviser,
            'user_name'  : users.get_current_user(),
            'url'        : url,
            'url_linktext': url_linktext
        }
        template = JINJA_ENVIRONMENT.get_template('adviser_list.html')
        self.response.write(template.render(template_values))


class AdviserNewHandler(webapp2.RequestHandler):
    def get(self):

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user_name': users.get_current_user(),
            'url': url,
            'url_linktext': url_linktext,
        }
        template = JINJA_ENVIRONMENT.get_template('adviser_new.html')
        self.response.write(template.render(template_values))

    def post(self):
        adviser = Adviser()
        adviser.adviser_title = self.request.get('adviser_title')
        adviser.adviser_fname= self.request.get('adviser_fname')
        adviser.adviser_lname = self.request.get('adviser_lname')
        adviser.email2 = self.request.get ('email2')
        adviser.pnumber = self.request.get('pnumber')
        adviser.dept = self.request.get('dept')
        adviser.put()
        self.redirect('/adviser/success')



class Student(ndb.Model):
    student_fname = ndb.StringProperty(indexed=False)
    student_lname = ndb.StringProperty(indexed=False)
    email2 = ndb.StringProperty(indexed=False)
    student_no = ndb.StringProperty(indexed=False)


class SuccessPageHandler3(webapp2.RequestHandler):
    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user_name': users.get_current_user(),
            'url': url,
            'url_linktext': url_linktext,
        }
        template = JINJA_ENVIRONMENT.get_template('success_3.html')
        self.response.write(template.render(template_values))


class StudentViewHandler(webapp2.RequestHandler):
    def get(self, student_id):
        student = Student.query().fetch()
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        
        template_values = {
            "all_student": student,
            "id"        : int(student_id),
            'user_name' : users.get_current_user(),
            'url'       : url,
            'url_linktext': url_linktext
        }
        template = JINJA_ENVIRONMENT.get_template('student_view.html')
        self.response.write(template.render(template_values))


class StudentListHandler(webapp2.RequestHandler):
    def get(self):
        student = Student.query().fetch()

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        template_values = {
            "all_student": student,
            'user_name' : users.get_current_user(),
            'url'       : url,
            'url_linktext': url_linktext
        }
        template = JINJA_ENVIRONMENT.get_template('student_list.html')
        self.response.write(template.render(template_values))


class StudentNewHandler(webapp2.RequestHandler):
    def get(self):

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user_name': users.get_current_user(),
            'url': url,
            'url_linktext': url_linktext,
        }
        template = JINJA_ENVIRONMENT.get_template('student_new.html')
        self.response.write(template.render(template_values))

    def post(self):
        student = Student()
        student.student_fname= self.request.get('student_fname')
        student.student_lname = self.request.get('student_lname')
        student.email2 = self.request.get ('email2')
        student.student_no = self.request.get('student_no')
        student.put()
        self.redirect('/student/success')

class ThesisEditHandler(webapp2.RequestHandler):
    def get(self, thesis_id):
        thesis = Thesis.query().fetch()
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        template_values = {
            "all_thesis": thesis,
            "id"        : int(thesis_id),
            'user_name' : users.get_current_user(),
            'url'       : url,
            'url_linktext': url_linktext

        }
        template = JINJA_ENVIRONMENT.get_template('thesis_edit.html')
        self.response.write(template.render(template_values))

    def post(self,thesis_id):
        thesis_id=int(thesis_id)
        thesis = Thesis.get_by_id(thesis_id)
        thesis.thesis_title = self.request.get('thesis_title')
        thesis.thesis_sy= self.request.get('thesis_sy')
        thesis.descrip = self.request.get('descrip')
        thesis.status = self.request.get ('status')
        thesis.proponents = self.request.get('proponents')
        thesis.adviser = self.request.get('adviser')
        thesis.put()
        self.redirect('/thesis/success')

class StudentEditHandler(webapp2.RequestHandler):
    def get(self, student_id):
        student = Student.query().fetch()
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            "all_student": student,
            "id"        : int(student_id),
            'user_name' : users.get_current_user(),
            'url'       : url,
            'url_linktext': url_linktext
        }
        template = JINJA_ENVIRONMENT.get_template('student_edit.html')
        self.response.write(template.render(template_values))

    def post(self, student_id):
        student_id=int(student_id)
        student = Student.get_by_id(student_id)
        student.student_fname= self.request.get('student_fname')
        student.student_lname = self.request.get('student_lname')
        student.email2 = self.request.get ('email2')
        student.student_no = self.request.get('student_no')
        student.put()
        self.redirect('/student/success')

class AdviserEditHandler(webapp2.RequestHandler):
    def get(self, adviser_id):
        adviser = Adviser.query().fetch()
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            "all_adviser": adviser,
            "id"        : int(adviser_id),
            'user_name' : users.get_current_user(),
            'url'       : url,
            'url_linktext': url_linktext

        }
        template = JINJA_ENVIRONMENT.get_template('adviser_edit.html')
        self.response.write(template.render(template_values))

    def post(self,adviser_id):
        adviser_id=int(adviser_id)
        adviser = Adviser.get_by_id(adviser_id)
        adviser.adviser_title = self.request.get('adviser_title')
        adviser.adviser_fname= self.request.get('adviser_fname')
        adviser.adviser_lname = self.request.get('adviser_lname')
        adviser.email2 = self.request.get ('email2')
        adviser.pnumber = self.request.get('pnumber')
        adviser.dept = self.request.get('dept')
        adviser.put()
        self.redirect('/adviser/success')

application = webapp2.WSGIApplication([
    ('/', Home),
    ('/guestbook', Dashboard),
    ('/sign', Guestbook),
    ('/sign1', Guestbook1),
    ('/sign2', Guestbook2),
    ('/module-1/1', MemberOnePage),
    ('/module-1/2', MemberTwoPage),
    ('/thesis/new', ThesisNewHandler),
    ('/thesis/edit/(\d+)', ThesisEditHandler),
    ('/thesis/success', SuccessPageHandler),
    ('/thesis/list', ThesisListHandler),
    ('/thesis/view/(\d+)', ThesisViewHandler),
    ('/adviser/new', AdviserNewHandler),
    ('/adviser/success', SuccessPageHandler2),
    ('/adviser/list', AdviserListHandler),
    ('/adviser/view/(\d+)', AdviserViewHandler),
    ('/adviser/edit/(\d+)', AdviserEditHandler),
    ('/student/new', StudentNewHandler),
    ('/student/success', SuccessPageHandler3),
    ('/student/list', StudentListHandler),
    ('/student/view/(\d+)', StudentViewHandler),
    ('/student/edit/(\d+)', StudentEditHandler),

], debug=True)
