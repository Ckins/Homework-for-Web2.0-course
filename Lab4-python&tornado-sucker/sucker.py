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

class FormHandler(tornado.web.RequestHandler):
    """This is the key part!"""
    def get(self):
        self.render('buyagrade.html')

    def post(self):
        name = self.get_argument('name', '')
        section = self.get_argument('section', '')
        card = self.get_argument('card', '')
        card_type = self.get_argument('card_type', '')

        if not self.isfill(name, section, card, card_type):
            self.render('sorry.html',\
                tips="You didn't fill out the form completely.")

        else:
            card = self.valid(card, card_type)
            if card == '':
                self.render('sorry.html',\
                    tips="You didn't provide a valid card number.")
            else:
                filepath = os.path.dirname(__name__)         
                txt = self.text_operate(filepath, name, section, card, card_type)

                self.render('sucker.html', name=name, cc=card, section=section, ct=card_type, txt=txt)

    def isfill(self, name, section, card, card_type):
        if name != '' and section != '' and card != '' and card_type != '':
            return True
        return False

    def text_operate(self, filepath, name, section, card, cc):

        txt = open(os.path.join(filepath, 'static/suckers.txt'), 'a')
        content=''
        content=name+';'+section+';'+card+';'+cc+'\n'
        txt.write(content)
        txt.close()
            
        txt = open(os.path.join(filepath, 'static/suckers.txt'))
        text = ''
        for line in txt.readlines():
            text += line
        txt.close()
        return text

    def valid(self, card, card_type):

        if card_type == 'visa':
            flag1 = re.match(r'^4\d{3}(-?\d{4}){3}$', card)
        else:
            flag1 = re.match(r'^5\d{3}(-?\d{4}){3}$', card)

        card = card.replace('-', '')
        if not flag1:
            return ''

        result=0

        for i in range(16):
            if i%2 != 0:
                result+=(int(card[i]))
            else:
                tmp=2*(int(card[i]))
                if tmp>=10:
                    dig1= int(tmp/10)
                    dig2=tmp%10
                    print tmp,dig1, '+', dig2
                    result+=(dig1+dig2)
                else:
                    result+=tmp

        if result%10 != 0:
            return ''

        return card


if __name__ == '__main__':
    tornado.options.parse_command_line()
    _APP = tornado.web.Application(
        handlers=[(r'/', FormHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    HTTPS = tornado.httpserver.HTTPServer(_APP)
    HTTPS.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    