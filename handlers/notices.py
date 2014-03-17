#coding: utf-8
import tornado.web
from base.session_tools import SessionTools
from models import NoticeModel
import json
from functools import wraps

from base.singleton import Singleton
class NoticePusher(object):
	__metaclas__ = Singleton
	def __init__(self):
		self._callbacks = []
		self.notices = NoticeModel()

	def register(self, callback):
		self._callbacks.append(callback)
	
	def unregister(self, callback):
		self._callbacks.remove(callback)
	
	def notify_all(self, notice_id):
		notice = self.notices.get_one(notice_id)
		for callback in self._callbacks:
			callback(notice)
		self._callbacks = []

class NoticeHandler(tornado.web.RequestHandler):
	def __init__(self, application, request, **kwargs):
		self.session = SessionTools()
		self.notices = NoticeModel()
		self.pusher = NoticePusher()
		super(NoticeHandler, self).__init__(application, request, **kwargs)

	def get(self):
		return self.write(json.dumps(self.notices.get_all()))
	
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
		notice_id = self.notices.add_notice({
				u"contents": contents,
				u"life": life,
				u"publisher": user_id
				})
		if not notice_id:
			notice_id = ""
		else:
			self.pusher.notify_all(notice_id)
		self.redirect("/results?type=notice&operating=add&id={0}".format(notice_id))
	
	@login_required
	def delete(self, user_id):
		notice_id = self.get_body_argument("notice_id")
		self.notices.remove(notice_id)
		self.redirect("/results?type=notice&operating=delete")

class NewNoticeHandler(tornado.web.RequestHandler):
	def __init__(self, application, request, **kwargs):
		self.session = SessionTools()
		self.notices = NoticeModel()
		self.pusher = NoticePusher()
		super(NewNoticeHandler, self).__init__(application, request, **kwargs)
	@tornado.web.asynchronous
	def get(self):
		self.pusher.register(self.notify)

	def notify(self, notice):
		self.write(json.dumps(notice))
		self.finish()
	
	def on_close(self):
		self.pusher.unregister(self.notify)

