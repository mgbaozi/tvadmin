from handlers import IndexHandler, UserHandler, NoticeHandler

views = [
	(r'/', IndexHandler),
	(r'/user', UserHandler),
	(r'/notice', NoticeHandler),
]
