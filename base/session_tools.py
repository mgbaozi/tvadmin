import memcache
from singleton import Singleton
import uuid
import logging
log = logging.getLogger("session")

class SessionTools(object):
	__metaclass__ = Singleton
	def __init__(self):
		self.cache = memcache.Client(['127.0.0.1:12333'])
	
	def login(self, set_cookie, user_id):
		session_id = uuid.uuid4().get_hex()
		self.cache.set(session_id, user_id)
		set_cookie("session_id", session_id, 20 * 60)

	def logged_user(self, get_cookie):
		session_id = get_cookie("session_id")
		if session_id:
			user_id = self.cache.get(session_id)
			return user_id if user_id else None
		return None

