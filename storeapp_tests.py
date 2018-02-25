import os 
import storeapp 
import unittest 
import tempfile 

class StoreappTestCase(unittest.TestCase):

	def setUp(self):
		self.db_fd, storeapp.app.config['DATABASE'] = tempfile.mkstemp()
		storeapp.app.testing = True 
		self.app = storeapp.app.test_client()
		with storeapp.app.app_context():
			storeapp.views.init_db()

	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(storeapp.app.config['DATABASE'])

	def test_empty_db(self):
		rv = self.app.get('/')
		assert b'No books' in rv.data 

if __name__ == '__main__':
	unittest.main()


