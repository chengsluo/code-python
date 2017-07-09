import tornado.ioloop
import tornado.web

class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello Tornado!")


app=tornado.web.Application([
    (r"/",HelloHandler),
        ])


if __name__=="__main__":
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()