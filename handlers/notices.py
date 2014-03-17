#coding: utf-8
import tornado.web
from base.session_tools import SessionTools
from models import NoticeModel
import json
from functools import wraps

class NoticeHandler(tornado.web.RequestHandler):
	def __init__(self, application, request, **kwargs):
		self.session = SessionTools()
		self.notices = NoticeModel()
		super(NoticeHandler, self).__init__(application, request, **kwargs)

	def get(self):
		return self.write(json.dumps(self.notices.get_all()))

	def post(self):
		account = self.get_body_argument("account")
		passwd = self.get_body_argument("passwd")
		if not account or not passwd:
			return self.write(json.dumps({
						u"error": 1,
						u"content": u"请输入用户名或密码！"
						}))
		notice_id = self.notices.login(account, passwd)
		if not notice_id:
			return self.write(json.dumps({
						u"error": 2,
						u"content": u"用户名或密码错误"
						}))
		self.session.login(self.set_cookie, notice_id)
		self.redirect(r'/')
	
	def login_required(fn):
		@wraps(fn)
		def func(self):
			user_id = self.session.logged_user(self.get_cookie)
			if not user_id:
				return self.write(json.dumps({
							u"error": 3,
							u"content": u"请先登录"
							}))
			return fn(self, user_id)
		return func
	@login_required
	def put(self, user_id):
		contents = self.get_body_argument("contents")
		life = self.get_body_argument("life")
		self.notices.add_notice({
				u"contents": contents,
				u"life": life,
				u"publisher": user_id
				})
		user_id = self.session.logged_user(self.get_cookie)
		self.redirect("/results?type=notice&operating=add&account={0}&name={1}&limits={2}".format(account, name, limits))
	
	@login_required
	def delete(self, user_id):
		notice_id = self.get_body_argument("notice_id")
		self.notices.remove(notice_id)
		self.redirect("/results?type=notice&operating=delete")
		
