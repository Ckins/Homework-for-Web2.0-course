#! coding: utf-8

import os
import random
import re
import math

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        name = tornado.escape.xhtml_escape(self.current_user)

        questionList=[]
        replyList=[]
        questionDict={}
        filepath = os.path.dirname(__file__)
        questions = open(os.path.join(filepath, 'static/data/questionData.txt'))
        for line in questions.readlines():
            line = line.rstrip().split(';')
            questionDict={}
            questionDict["title"] = line[0]
            questionDict["time"] = line[1]
            questionDict["author"] = line[2]
            questionDict["text"] = line[3]
            replyList=[]
            reply = open(os.path.join(filepath, 'static/data/replyData.txt'))
            for one in reply.readlines():
                print one
                replyDict={}
                one = one.rstrip().split(';')
                if one[0] == line[2]:
                    replyDict={}
                    replyDict["work"]=(one[0])
                    replyDict["time"]=(one[1])
                    replyDict["author"]=(one[2])
                    replyDict["text"]=(one[3])
                    replyList.append(replyDict)
            reply.close()

            questionDict["reply"] = replyList
            questionList.append(questionDict)
        questions.close()

        self.render('index.html', questionList=questionList)

class LoginHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.render('login.html')
            return
        else:
            self.redirect("/")

    def post(self):
        name = self.get_argument('name', None)
        password = self.get_argument('password', None)
        if  self.Validlogin(name, password):
            self.set_secure_cookie("user", self.get_argument("name"))
            self.redirect("/")
        else:
            self.redirect("/login")

    def Validlogin(self, name, password):
        if not name:
            return False
        if not password:
            return False
        Flag = False
        filepath = os.path.dirname(__file__)
        users = open(os.path.join(filepath, 'static/data/userData.txt'))
        for line in users.readlines():
            line = line.rstrip().split(',')
            if line[0] == name:
                if line[1] == password:
                    Flag = True
        users.close()
        return Flag


class SignupHandler(BaseHandler):
    def get(self):
        if  self.current_user:
            self.redirect("/")
            return
        else:
            self.render('signup.html')

    def post(self):
        name = self.get_argument('name', None)
        password = self.get_argument('password', None)
        if  self.Validsign(name, password):
            filepath = os.path.dirname(__file__)
            users = open(os.path.join(filepath, 'static/data/userData.txt'), 'a')
            content = ''
            content='\n'+name+','+password
            users.write(content)
            users.close()
            self.set_secure_cookie("user", self.get_argument("name"))
            self.redirect("/")
        else:
            self.redirect("/signup")

    def Validsign(self, name, password):
        if not name:
            return False
        if not password:
            return False
        if not (re.match(r'[0-9a-zA-Z]{6,12}', name)):
            return False
        if not re.match(r'^[A-Z][0-9a-zA-Z]{5,12}', password):
            return False
        Flag = True
        filepath = os.path.dirname(__file__)
        users = open(os.path.join(filepath, 'static/data/userData.txt'))
        for line in users.readlines():
            line = line.rstrip().split(',')
            if line[0] == name:
                Flag = False
        users.close()
        return Flag

class questionHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/")
            return
        else:
            self.render('question.html')

    def post(self):
          name = self.get_argument("title", None)
          content = self.get_argument("content", None)
          time = self.get_argument("time", None)
          author = tornado.escape.xhtml_escape(self.current_user)
          filepath = os.path.dirname(__file__)
          reply = open(os.path.join(filepath, 'static/data/replyData.txt'), 'a')
          cc=''
          cc = '\n'+str(name)+';'+str(time)+';'+str(author)+';'+str(content)
          reply.write(cc)
          reply.close()
          self.redirect("/")

if __name__ == '__main__':
    tornado.options.parse_command_line()
    _APP = tornado.web.Application(
        handlers=[(r'/', MainHandler), (r"/login", LoginHandler), (r"/signup", SignupHandler), (r"/question", questionHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "template"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        debug=True
    )
    HTTPS = tornado.httpserver.HTTPServer(_APP)
    HTTPS.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
