"""web2.0 : homework3 Kin_sang"""
"""The address is localhost:8000/film?=tmnt or princessbride or..."""

import os
import random
import re

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class MovieHandler(tornado.web.RequestHandler):
    """This is the key part!"""
    def get(self):
    	movie_path = os.path.join(os.path.dirname(__file__), "static/moviefiles")
    	name = self.get_argument("film", "tmnt")
    	movie_info = {}
    	bar_view={}
    	Left_comments=[]
    	Right_comments=[]

    	for page in os.listdir(movie_path):
    		if name == page:
    			movie_further_path = os.path.join(movie_path, name)
    			break
    		else:
    			pass
    	#bar comment
    	bar = open(os.path.join(movie_further_path, 'generaloverview.txt'))
        for line in bar.readlines():
            content = (line.rstrip()).split(':')
            bar_view[content[0]] = content[-1]
        bar.close()

        #movie
    	movie_info['image'] = os.path.join(movie_further_path, 'generaloverview.png')
        info = open(os.path.join(movie_further_path, 'info.txt'))
        info_list = info.readlines()
        movie_info["name"] = str(info_list[0].rstrip())
        movie_info["time"] = str(info_list[1].rstrip())
        movie_info["score"] = int(info_list[2].rstrip())
        movie_info["reviews"] = str(info_list[3].rstrip())
        info.close()

        count = 0
        for obj in os.listdir(movie_further_path):
            flag = re.match(r'^review(\d*)\.txt$', obj)
            if flag:
            	comment = {}
            	count += 1
                review_path = open(os.path.join(movie_further_path, obj))
                line_list = review_path.readlines()
                comment["phrase"] = line_list[0].rstrip()
                comment["mark"] = line_list[1].rstrip()
                comment["author"] = line_list[2].rstrip()
                comment["src"] = line_list[3].rstrip()
                if ((count%2) == 0):
                	Right_comments.append(comment)
                else:
                	Left_comments.append(comment)
            else:
            	pass

        self.render("skeleton.html", movie_info=movie_info, bar_view=bar_view, \
        	Right_comments=Right_comments, Left_comments=Left_comments, count=count)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    _APP = tornado.web.Application(
        handlers=[(r'/', MovieHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    HTTPS = tornado.httpserver.HTTPServer(_APP)
    HTTPS.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
