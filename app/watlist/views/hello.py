from flask import render_template,Blueprint
import click
from app.watlist.models import User, Movie
from realproject import db

bg = Blueprint('watlist',__name__,url_prefix='/watlist',template_folder='../templates',static_folder='../static')

@bg.cli.command() #注册成为命令
def forge():
    name = 'Kanding Mu'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'],year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done...')

@bg.route('/')
def index():
    user = User.query.first() #读取用用户记录
    movies = Movie.query.all() #读取所有电影记录
    return render_template('index.html', user=user, movies=movies)