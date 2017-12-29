from pymongo import MongoClient

def get_db():
	conn = MongoClient()['site']
	return conn
