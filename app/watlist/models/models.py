from realproject import db
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True) #主键
    name = db.Column(db.String(20)) #名字

class Movie(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(60)) #电影标题
    year = db.Column(db.String(4))   #电影年份
