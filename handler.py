import tornado.web
import os
import traceback
import sys
import StringIO

lib_path = os.path.normpath(os.path.join(os.path.dirname(__file__) + '/../'))
sys.path.append(lib_path)

from rewrite import rewrite

class MainHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        self.rewrite = rewrite.Rewrite(self)
        tornado.web.RequestHandler.__init__(self, *args, **kwargs)

    def get(self):
        url = self.request.uri
        self.rewrite.match(url)

    def write_error(self, status, **kwargs):
        info = sys.exc_info()
        for file, lineno, function, text in traceback.extract_tb(info[2]):
            fp = StringIO.StringIO()
            traceback.print_exc(file=fp)
            message = fp.getvalue()
            message = message.replace("\n","<br/>")
            self.write(message)
