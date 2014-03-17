#coding: utf-8
import tornado.web
import logging
log = logging.getLogger("result")
log.setLevel(logging.DEBUG)
class ResultHandler(tornado.web.RequestHandler):
	def __init__(self, application, request, **kwargs):
		self.res_method = {
							"user": {
										"add": self._user_add,
										"delete": self._user_delete
									},
							"notice": {
										"add": self._notice_add,
										"delete": self._notice_delete
									}
						}
		super(ResultHandler, self).__init__(application, request, **kwargs)

	def get(self):
		log.debug("get")
		res_type_str = self.get_argument("type")
		res_type = self.res_method.get(res_type_str)
		if not res_type:
			raise tornado.web.HTTPError(404)
		op_type_str= self.get_argument("operating")
		op_method = res_type.get(op_type_str)
		if not op_method:
			raise tornado.web.HTTPError(404)
		return op_method()
	
	def _user_add(self):
		user_id = self.get_argument("id")
		if not user_id:
			return self.write(u"用户已存在")
		return self.write(u"添加成功")

	def _notice_add(self):
		return self.write(u"添加通知成功")

	def _user_delete(self):
		return self.write(u"删除成功")

	def _notice_delete(self):
		return self.write(u"删除通知成功")
