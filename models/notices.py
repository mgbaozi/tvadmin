from modelbase import ModelBase
from datetime import datetime, timedelta

class NoticeModel(ModelBase):
	def __init__(self):
		self.name = "notices"
		super(NoticeModel, self).__init__()

	def add_notice(self, data):
		notice = {
					"contents": data["contents"],
					"publisher": ModelBase.get_oid(data["user_id"]),
					"create_date": datetime.utcnow(),
					"invalid_date": datetime.utcnow() + timedelta(days = int(data["life"]))
				}	
		return str(self.collection.insert(notice))

	def get_all(self):
		cursor = self.collection.find()
		return ModelBase.cursor2list(cursor)

	def get_effective(self):
		cursor = self.collection.find({'$gte': datetime.utcnow()})
		return ModelBase.cursor2list(cursor)
