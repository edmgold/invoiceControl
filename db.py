import databases
import ormar
import sqlalchemy

from config import database, metadata


class BaseMeta(ormar.ModelMeta):
    database = database
    metadata = metadata
