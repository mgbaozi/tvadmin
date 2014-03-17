import tornado.web

class ShowHandler(tornado.web.RequestHandler):
	def get(self):
		return self.render("tv.html")
