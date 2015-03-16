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

class Singler(object):
    """docstring for Singler"""
    def __init__(self, name, gender, age, personality, system, seeking, age_start, age_end):
        self.name = name
        self.gender = gender
        self.system = system
        self.age = age
        self.seeking = seeking
        self.age_start = age_start
        self.age_end = age_end
        self.personality = personality
        self.image_path=''


        self.image_path=None
        self.match_rate=0
        if len(seeking) > 1:
            self.seek = seeking[0]+seeking[1]
        else:
            self.seek = seeking[0]

    def match(self, one):
        if self.seek.find(one.gender) != -1 and one.seek.find(self.gender) != -1:
            match_rate = 0
            if one.system == self.system:
                match_rate += 2
            for each in str(one.personality):
                if self.personality.find(each):
                    match_rate += 1
            if one.age <= self.age_end and one.age >= self.age_start and \
               self.age <= one.age_end and self.age >= one.age_start:
                match_rate += 1
            return match_rate
        else:
            return False

    @staticmethod
    def Match_list(per):
        """to match singles"""
        filepath = os.path.dirname(__file__)
        matchlist = []
        singles = open(os.path.join(filepath, 'static/singles.txt'))
        for line in singles.readlines():
            line = line.rstrip().split(',')
            old_singler = Singler(line[0], line[1], int(line[2]), line[3], line[4], \
                line[5], int(line[6]), int(line[7]))
            if per.match(old_singler) >= 3:
                old_singler.match_rate = per.match(old_singler)
                name_path = line[0].lower().replace(' ', '_')
                filepath = os.path.dirname(__file__)
                old_singler.image_path = (os.path.join(filepath, 'static/images/'+name_path+'.jpg'))
                matchlist.append(old_singler)
        return matchlist



class FormHandler(tornado.web.RequestHandler):
    """This is the key part!"""
    def get(self):
        self.render('index.html')

    def post(self):
        name = self.get_argument('name', None)
        gender = self.get_argument('gender', None)
        system = self.get_argument('section', None)
        age = self.get_argument('age', None)
        seeking = self.get_arguments("seeking", None)
        age_start = self.get_argument('ageleft', None)
        age_end = self.get_argument('ageright', None)
        personality = self.get_argument('personality', None)

        new_singler = Singler(name, gender, age, personality, system, seeking, age_start, age_end)

        filepath = os.path.dirname(__file__)

        self.render('results.html', singlers=Singler.Match_list(new_singler))

if __name__ == '__main__':
    tornado.options.parse_command_line()
    _APP = tornado.web.Application(
        handlers=[(r'/', FormHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    HTTPS = tornado.httpserver.HTTPServer(_APP)
    HTTPS.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
