from modelbase import ModelBase
from datetime import datetime, timedelta
from users import UserModel

class NoticeModel(ModelBase):
	def __init__(self):
		self.name = "notices"
		self.users = UserModel()
		super(NoticeModel, self).__init__()

	def add_notice(self, data):
		notice = {
					"content": data["content"],
					"publisher": ModelBase.get_oid(data["publisher"]),
					"create_date": datetime.utcnow(),
					"invalid_date": datetime.utcnow() + timedelta(days = int(data["life"]))
				}	
		return str(self.collection.insert(notice))
	
	def to_user(self, notice):
		user_id = str(notice["publisher"])
		user = self.users.get_one(user_id)
		notice["publisher"] = user["name"]
		notice["create_date"] = notice["create_date"].strftime('%Y-%m-%d')
		notice["invalid_date"] = notice["invalid_date"].strftime('%Y-%m-%d')
		return notice

	def get_one(self, notice_id):
		notice = self.collection.find_one(ModelBase.get_oid(notice_id))
		notice = self.to_user(notice)
		return ModelBase.transform_id(notice)

	def get_all(self):
		cursor = self.collection.find()
		notice_list = ModelBase.cursor2list(cursor)
		return [self.to_user(notice) for notice in notice_list]

	def get_effective(self):
		cursor = self.collection.find({'$gte': datetime.utcnow()})
		notice_list = ModelBase.cursor2list(cursor)
		return [self.to_user(notice) for notice in notice_list]
