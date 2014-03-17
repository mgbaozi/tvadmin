from handlers import IndexHandler, UserHandler, NoticeHandler, ResultHandler, ShowHandler, NewNoticeHandler

views = [
	(r'/', IndexHandler),
	(r'/user', UserHandler),
	(r'/notice', NoticeHandler),
	(r'/results', ResultHandler),
	(r'/show', ShowHandler),
	(r'/getnew', NewNoticeHandler),
]
