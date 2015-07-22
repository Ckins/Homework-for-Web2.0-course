"""web2.0 : lab3 Kin_sang"""
"""Have finished part of Excerise 5 , available for Back and m3u"""

import os

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class MusicHandler(tornado.web.RequestHandler):
    """This is the key part!"""
    def get(self):
        musiclist = self.get_argument("playlist", "none")
        musicdir = []
        textdir = []
        srclist = os.listdir("static/songs/")

        for src in srclist:
            if src.endswith(".mp3"):
                musicdir.append(src)
            else:
                textdir.append(src)

        js_old = {}
        for music in musicdir:
            size = os.path.getsize("static/songs/"+music)
            if size < 1048576:
                js_old[music] = str(size)+"b"
            else:
                js_old[music] = str(round(size/1048576.0, 2))+"Mb"

        if musiclist != "none":
            js_new = {}

            fp_1 = open("static/songs/"+musiclist)
            for line in fp_1.readlines():
                if line.startswith("#"):
                    pass
                else:
                    size_2 = os.path.getsize("static/songs/"+line.strip())
                    transtr(js_new, size_2, line)

            self.render('music.html', musics=js_new, textdir={})
            fp_1.close()

        else:
            self.render('music.html', musics=js_old, textdir=textdir)

def transtr(js_new, size_2, line):
    if size_2 < 1048576:
        js_new[line.strip()] = str(size_2)+"b"
    else:
        js_new[line.strip()] = str(round(size_2/1048576.0, 2)) +"Mb"


if __name__ == '__main__':
    tornado.options.parse_command_line()
    _APP = tornado.web.Application(
        handlers=[(r'/', MusicHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    HTTPS = tornado.httpserver.HTTPServer(_APP)
    HTTPS.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

