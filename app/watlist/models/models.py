from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from realproject import db
class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True) #主键
    name = db.Column(db.String(20)) #名字
    username = db.Column(db.String(20))
    password = db.Column(db.String(128))
    def set_password(self,password_hash):# 用来设置密码的方法，接受密码作为参数
        self.password = generate_password_hash(password_hash) # 将生成的密码保持到对应字段
    def validate_password(self,password_hash): # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password,password_hash)

class Movie(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(60)) #电影标题
    year = db.Column(db.String(4))   #电影年份
