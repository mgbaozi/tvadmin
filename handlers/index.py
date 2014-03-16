import tornado.web

class IndexHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		self.write("It works")
		self.finish()
