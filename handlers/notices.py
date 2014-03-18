#coding: utf-8
import tornado.web
from base.session_tools import SessionTools
from models import NoticeModel
import json
from functools import wraps
import logging
log = logging.getLogger("notice")
log.setLevel(logging.DEBUG)

from base.singleton import Singleton
class NoticePusher(object):
	__metaclass__ = Singleton
	def __init__(self):
		self._callbacks = []
		self.notices = NoticeModel()

	def register(self, callback):
		log.debug("register callback")
		self._callbacks.append(callback)
	
	def unregister(self, callback):
		log.debug("unregister callback")
		self._callbacks.remove(callback)
	
	def notify_all(self, notice_id):
		notice = self.notices.get_one(notice_id)
		log.debug("notify {0}".format(self._callbacks))
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
		notices = self.notices.get_effective()
		return self.write(json.dumps(notices))
	
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
	def post(self, user_id):
		log.debug("on_post")
		content = self.get_body_argument("content")
		life = self.get_body_argument("life")
		notice_id = self.notices.add_notice({
				u"content": content,
				u"life": life,
				u"publisher": user_id
				})
		log.debug("add notice id:{0}".format(notice_id))
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
		log.debug("notify{0}".format(notice))
		self.write(json.dumps(notice))
		self.finish()
	
	def on_connection_close(self):
		self.pusher.unregister(self.notify)

