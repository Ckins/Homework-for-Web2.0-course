# -*- coding: utf-8 -*-
"""this is a docstring"""
import os
import re
import json
import datetime

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import HTMLParser
import urlparse
import urllib
import urllib2
import cookielib
import string

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")


class IndexHandler(BaseHandler):
    """ handle Index"""
    def get(self):
        if self.get_current_user():
            self.render('index.html', loged=self.get_current_user())
        else:
            self.render('index.html', loged='')

    def data_received(self, chunk):
        pass


class LoginHandler(BaseHandler):
    """ handle Login"""
    def get(self):
        self.render("login.html", state=0, content='')

    def post(self):
        goto = self.get_argument('goto', '/')
        name = self.get_argument('name')
        password = self.get_argument("password")
        self.checkValid(name, password, goto)

    def checkValid(self, name, password, goto):
        hosturl = 'http://insysu.com' 
        posturl = 'http://insysu.com/sign_in' 
        cj = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)  
        h = urllib2.urlopen(hosturl)
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                   'Referer' : 'http://insysu.com/'}
        postData = {'username': name,
                    'password': password}
        postData = urllib.urlencode(postData)
        request = urllib2.Request(posturl, postData, headers)
        response = urllib2.urlopen(request)
        text = response.read()
        count = text.find('data-toggle="dropdown">')
        if count == -1:
            self.render("login.html", state=-1, content=goto)
        else:
            the_name = ''
            count += 23
            while text[count] != ' ':
                the_name += text[count]
                count += 1
            self.set_secure_cookie("username", the_name)
            self.redirect(goto)

    def data_received(self, chunk):
        pass


class GradeHandler(BaseHandler):
    """handle grade"""
    def get(self, grade):
        judge = self.get_argument("suibian", None)
        if judge:
            if grade == 'back':
                the_dict = dict(state=1, contents="Grade1|Grade2|Grade3|Public_Courses")
                self.write(json.dumps(the_dict))
            else:
                f_path = os.path.join(os.path.dirname(__file__), "static/data/menu_data")
                grade_path = os.path.join(f_path, grade)
                all_file = os.listdir(grade_path)
                toWtite = "|".join(all_file)
                the_dict = dict(state=1, contents=toWtite)
                self.write(json.dumps(the_dict))
        else:
            self.redirect('/')

    def data_received(self, chunk):
        pass


class CourseHandler(BaseHandler):
    """handle courses"""
    def get(self, grade, course):
        judge = self.get_argument("suibian", None)
        if judge:
            f_path = os.path.join(os.path.dirname(__file__), "static/data/menu_data")
            grade_path = os.path.join(f_path, grade)
            course_path = os.path.join(grade_path, course)
            all_file = os.listdir(course_path)
            toWtite = "|".join(all_file)
            the_dict = dict(state=8, contents=toWtite)
            self.write(json.dumps(the_dict))
        else:
            self.redirect('/')

    def data_received(self, chunk):
        pass


class TeacherHandler(BaseHandler):
    """handle teachers"""
    def get(self, grade, course, teacher):
        f_path = os.path.join(os.path.dirname(__file__), "static/data/menu_data")
        grade_path = os.path.join(f_path, grade)
        course_path = os.path.join(grade_path, course)
        teacher_path = os.path.join(course_path, teacher)

        new_path1 = os.path.join("static/data/menu_data", grade)
        new_path2 = os.path.join(new_path1, course)
        new_path3 = os.path.join(new_path2, teacher)

        isValid = 1
        if os.path.exists(grade_path):
            if os.path.exists(course_path):
                if os.path.exists(teacher_path):
                    pass
                else:
                    isValid = 0
            else:
                isValid = 0
        else:
            isValid = 0

        if isValid:
            teacher_head = ''
            if 'teacher.jpg' in os.listdir(teacher_path):
                teacher_head = os.path.join(new_path3, 'teacher.jpg')
            else:
                teacher_head = 'static/images/default.jpg'

            teacher_info = dict()

            the_file = open(os.path.join(teacher_path, 'info.txt'))
            for the_line in the_file:
                the_line = the_line.rstrip()
                info = the_line.split('|')
                teacher_info[info[0]] = info[1]
            the_file.close()

            materials = dict()
            the_file = open(os.path.join(teacher_path, 'materials.txt'))
            for the_line in the_file:
                the_line = the_line.rstrip()
                info = the_line.split('|')
                materials[info[0]] = info[1]
            the_file.close()

            points = list()
            the_file = open(os.path.join(teacher_path, 'points.txt'))
            for the_line in the_file:
                the_line = the_line.rstrip()
                points.append(the_line)
            the_file.close()

            comments = list()
            the_file = open(os.path.join(teacher_path, 'comments.txt'))
            for the_line in the_file:
                the_line = the_line.rstrip()
                info = the_line.split('|')

                if len(info) > 1:
                    tem = dict()
                    tem['content'] = info[0]
                    tem['author'] = info[1]
                    tem['time'] = info[2]
                    comments.append(tem)
            the_file.close()

            new_dict = dict()
            new_dict['teacher_head'] = teacher_head
            new_dict['teacher_info'] = teacher_info
            new_dict['materials'] = materials
            new_dict['points'] = points
            new_dict['comments'] = comments
            new_dict['state'] = 0

            judge = self.get_argument("suibian", None)
            if judge:
                self.write(json.dumps(new_dict))
            else:
                if self.get_current_user():
                    print self.get_current_user()
                    self.render("teacher.html", username=self.get_current_user(), teacher_head=teacher_head, teacher_info=teacher_info, materials=materials, points=points, comments=comments)
                else:
                    self.render("login.html", state=5, content='/'+grade+'/'+course+'/'+teacher)
                    
        else:
            self.set_status(404)

    def data_received(self, chunk):
        pass


class CommentHandler(BaseHandler):
    def get(self):
        pass

    def post(self, grade, course, teacher):
        f_path = os.path.join(os.path.dirname(__file__), "static/data/menu_data")
        grade_path = os.path.join(f_path, grade)
        course_path = os.path.join(grade_path, course)
        teacher_path = os.path.join(course_path, teacher)
        the_file = open(os.path.join(teacher_path, 'comments.txt'), 'a')
        time = datetime.datetime.now()
        time = time.strftime("%Y-%m-%d")
        user = self.get_current_user()
        content = self.get_argument('remark_text', None)
        content = content.encode('utf-8')
        new_comment = [content, user, time]
        the_file.write('|'.join(new_comment)+'\n')
        the_file.close()
        self.write('|'.join(new_comment))

    def data_received(self, chunk):
        pass


class PointHandler(BaseHandler):
    def get(self):
        pass

    def post(self, grade, course, teacher):
        f_path = os.path.join(os.path.dirname(__file__), "static/data/menu_data")
        grade_path = os.path.join(f_path, grade)
        course_path = os.path.join(grade_path, course)
        teacher_path = os.path.join(course_path, teacher)
        the_file = open(os.path.join(teacher_path, 'points.txt'), 'a')
        content = self.get_argument('point_form', None)
        content = content.encode('utf-8')
        the_file.write(content+'\n')
        the_file.close()
        self.write(content)

    def data_received(self, chunk):
        pass
                


class LogoutHandler(BaseHandler):
    """handle logout"""
    def get(self):
        self.clear_cookie("username")
        self.redirect("/")


if __name__ == "__main__":
    tornado.options.parse_command_line()
    APP = tornado.web.Application(
        handlers=[(r"/", IndexHandler),
                  (r"/login", LoginHandler),
                  (r"/logout", LogoutHandler),
                  (r"/(\w+)", GradeHandler),
                  (r"/(\w+)/(\w+)", CourseHandler),
                  (r"/(\w+)/(\w+)/(\w+)", TeacherHandler),
                  (r"/comment/(\w+)/(\w+)/(\w+)", CommentHandler),
                  (r"/point/(\w+)/(\w+)/(\w+)", PointHandler)
                  ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        cookie_secret="TVoFesPDQC+saNw1W6oewgPqS+6C7098mK/ngZ/Mmy0=",
        debug=True
    )
    HTTP_SERVER = tornado.httpserver.HTTPServer(APP)
    HTTP_SERVER.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()



