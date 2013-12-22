import tornado.ioloop
import tornado.web
import os
import handler
import signal

path = os.path.normpath(os.path.dirname(__file__) + "/../../../")
# os.environ['DOCUMENT_ROOT'] = path

settings = {
    "static_path": os.path.join(path, "static"),
}

application = tornado.web.Application([
    (r"/.*", handler.MainHandler),
], **settings)


is_closing = False

def signal_handler(signum, frame):
    global is_closing
    print 'exiting...'
    is_closing = True

def try_exit(): 
    global is_closing
    if is_closing:
        tornado.ioloop.IOLoop.instance().stop()
        print 'exit success'

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    application.listen(8888)
    tornado.ioloop.PeriodicCallback(try_exit, 100).start() 
    loop= tornado.ioloop.IOLoop.instance()
    print 'fis server started'
    loop.start()

