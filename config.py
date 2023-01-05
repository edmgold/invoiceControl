import databases
import sqlalchemy
import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite')

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
