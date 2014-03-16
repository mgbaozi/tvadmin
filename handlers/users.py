#coding: utf-8
import tornado.web
from base.session_tools import SessionTools
from models import UserModel
import json
from functools import wraps

class UserHandler(tornado.web.RequestHandler):
	def __init__(self, application, request, **kwargs):
		self.session = SessionTools()
		self.users = UserModel()
		super(UserHandler, self).__init__(application, request, **kwargs)

	def get(self):
		user_id = get_body_argument("user_id")
		if not user_id:
			return self.write(json.dumps(self.users.get_all()))
		return self.write(json.dumps(self.users.get_one(user_id)))

	def post(self):
		account = get_body_argument("account")
		passwd = get_body_argument("passwd")
		if not account or not passwd:
			return self.write(json.dumps({
						u"error": 1,
						u"content": u"请输入用户名或密码！"
						}))
		user_id = self.users.login(account, passwd)
		if not user_id:
			return self.write(json.dumps({
						u"error": 2,
						u"content": u"用户名或密码错误"
						}))
		self.session.login(self.set_cookie, user_id)
		self.redirect(r'/')
	
	def admin_required(fn):
		@wraps(fn)
		def func(self):
			user_id = self.session.logged_user(self.get_cookie)
			if not user_id:
				return self.write(json.dumps({
							u"error": 3,
							u"content": u"请先登录"
							}))
			user_limits = self.users.get_limits()
			if user_limits != "admin" and user_limits != "root":
				return self.write(json.dumps({
							u"error": 4,
							u"content": u"权限不足"
							}))
			return fn(self)
		return func
	@admin_required
	def put(self):
		account = get_body_argument("account")
		passwd = get_body_argument("passwd")
		name = get_body_argument("name")
		limits = get_body_argument("limits")
		self.users.add_user({
				u"account": account,
				u"passwd": passwd,
				u"name": name,
				u"limits": limits})
		self.redirect("/results?type=user&operating=add&account={0}&name={1}&limits={2}".format(account, name, limits))
	
	@admin_required
	def delete(self):
		user_id = get_body_argument("user_id")
		self.users.remove(user_id)
		self.redirect("/results?type=user&operating=delete")
		
