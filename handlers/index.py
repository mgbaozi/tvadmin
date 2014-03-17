import tornado.web
from base.session_tools import SessionTools

class IndexHandler(tornado.web.RequestHandler):

	def __init__(self, application, request, **kwargs):
		self.session = SessionTools()
		super(IndexHandler, self).__init__(application, request, **kwargs)
	def get(self):
		user_id = self.session.logged_user(self.get_cookie)
		if not user_id:
			return self.render('login.html')
		add_type = self.get_argument("add", None)
		if not add_type:
			return self.render('index.html')
		return self.render("add{0}.html".format(add_type))
