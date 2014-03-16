from modelbase import ModelBase

class UserModel(ModelBase):
	def __init__(self):
		self.name = "users"
		super(UserModel, self).__init__()
	
	def add_user(self, user):
		return str(self.collection.insert(user))

	def get_all(self):
		cursor = self.collection.find()
		return ModelBase.cursor2list(cursor)
	
	def get_one(self, user_id):
		result = self.collection.find_one(ModelBase.get_oid(user_id))
		return ModelBase.transform_id(result)
