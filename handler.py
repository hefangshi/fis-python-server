import tornado.web
import os
import traceback
import sys
import StringIO
import urlparse

lib_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(lib_path)

from rewrite.rewrite import Rewrite
from fisdata.manager import FisDataManager

class MainHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        self.rewrite = Rewrite(self)
        self.root = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../'))
        tornado.web.RequestHandler.__init__(self, *args, **kwargs)

    def get(self):
        url = self.request.uri
        if self.rewrite.match(url) is False:
            self.render_template(url)

    def post(self):
        url = self.request.uri
        if self.rewrite.match(url) is False:
            self.render_template(url)

    def render_template(self, url):
        result = urlparse.urlparse(url)
        if result.path == '' or result.path == '/' or result.path.find('/') != 0:
            path = os.path.normpath(os.path.join(self.root, 'template', 'index.tpl'))
        elif len(result.path.split('/')) == 2:
            #shortcut for module
            path = os.path.normpath(os.path.join(self.root, 'template', result.path[1:], 'index.tpl'))
        else:
            path = os.path.normpath(os.path.join(self.root, 'template', result.path[1:] + ".tpl"))
        data = FisDataManager.get_data(self.get_cookie('FIS_DEBUG_DATATYPE'), path)
        print data

    def write_error(self, status, **kwargs):
        info = sys.exc_info()
        for file, lineno, function, text in traceback.extract_tb(info[2]):
            fp = StringIO.StringIO()
            traceback.print_exc(file=fp)
            message = fp.getvalue()
            message = message.replace("\n","<br/>")
            self.write(message)
