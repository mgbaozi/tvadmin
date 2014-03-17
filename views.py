from handlers import IndexHandler, UserHandler, NoticeHandler, ResultHandler

views = [
	(r'/', IndexHandler),
	(r'/user', UserHandler),
	(r'/notice', NoticeHandler),
	(r'/results', ResultHandler),
]
