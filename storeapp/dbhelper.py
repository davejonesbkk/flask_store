MOCKUSERS=[{'username': 'foobar', 'email': 'foo@bar.com', 
	'salt': 'zijthwLh396p8bTqMvHAGbRfbAYfQYtYx2K2f6DS',
	'hashed': 'dMwhoi97qQ73fuoQ6C1+AETuWzxOns7AYb6ztr8bIj16xZ8Qmmn/NihaiOKR194oXb/+3sLRWSuwRCO8('
	}]

class DBHelper:

	def get_users(self, username):
		user = [x for x in MOCKUSERS if x.get("username")==username]
		if user:
			return user[0]
		return None 

	def add_user(self, username, email, salt, hashed_pw):
		MOCKUSERS.append({'username': username, 'email': email, 'salt':salt, 'hashed_pw':hashed_pw})