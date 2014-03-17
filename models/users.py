from modelbase import ModelBase

class UserModel(ModelBase):
	def __init__(self):
		self.name = "users"
		super(UserModel, self).__init__()
	
	def add_user(self, user):
		if self.collection.find({"account":user["account"]}):
				return None
		return str(self.collection.insert(user))

	def login(self, account, passwd):
		user_msg = self.collection.find_one({"account": account, "passwd": passwd})
		return str(user_msg["_id"]) if user_msg else None

	def get_all(self):
		cursor = self.collection.find()
		return ModelBase.cursor2list(cursor)
	
	def get_one(self, user_id):
		result = self.collection.find_one(ModelBase.get_oid(user_id))
		return ModelBase.transform_id(result)
