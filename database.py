from peewee import *

db = SqliteDatabase('db.sqlite3')



class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    name = CharField()
    user_id = CharField(primary_key=True)


class Tasks(BaseModel):
    user =  ForeignKeyField(User, backref='tasks')
    title = CharField()
    description = CharField()
    datetime = DateTimeField()
    is_done = BooleanField(default=False)

db.connect()
db.create_tables([User, Tasks])