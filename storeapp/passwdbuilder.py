
import os, base64
import flask_bcrypt as Bcrypt

class PassBuilder:

	def HashBuilder(self, password):

		return Bcrypt.generate_password_hash(password).decode('utf-8')
	

	def SaltBuilder(self):

		return base64.b64encode(os.urandom(15)).decode('utf-8')
		

