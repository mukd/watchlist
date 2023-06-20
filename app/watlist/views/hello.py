from flask import render_template, Blueprint, request, flash, redirect, url_for
import click
from app.watlist.models import User, Movie
from realproject import db
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from realproject import app

login_manage = LoginManager(app) #实例化扩展类
login_manage.login_view = 'watlist.login'
bg = Blueprint('watlist',__name__,url_prefix='/watlist',template_folder='../templates',static_folder='../static')

@login_manage.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id)) #用 ID 作为 User 模型的主键查询对应的用户
    return user  #返回用户对象

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

#生成管理员账户
@bg.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username,password):
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('updating user...')
        user.username = username
        user.set_password(password) #设置密码
    else:
        click.echo('Creating user...')
        user = User(username=username,name="Admin")
        user.set_password(password)
        db.session.add(user)
    db.session.commit()
    click.echo('Done')

@bg.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('Invald input...')
            return redirect(url_for('watlist.login'))
        user = User.query.first()
        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success...')
            return redirect(url_for('watlist.index'))
        flash('Invalid username or password...')
        return redirect(url_for('watlist.login'))
    return render_template('login.html')

@bg.route('/settings',methods=['GET','POST'])
@login_required
def settings():
    if request.method=='POST':
        name = request.form['name']
        if not name or len(name) > 20:
            flash('Invalid input...')
            return redirect(url_for('watlist.settings'))
        current_user.name = name
        db.session.commit()
        return redirect(url_for('watlist.index'))
    return render_template('settings.html')

@bg.route('/logout')
@login_required
def logout():
    logout_user() #登出用户
    flash('Goodbye...')
    return redirect(url_for('watlist.index'))

@bg.context_processor #上下文处理函数
def inject_user():
    user = User.query.first()
    return dict(user=user)

@bg.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@bg.route('/')
def index():
    #user = User.query.first() #读取用用户记录
    movies = Movie.query.all() #读取所有电影记录
    return render_template('index.html', movies=movies)

@bg.route('/movie/add',methods=['GET','POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input...')
            return redirect(url_for('watlist.create'))
        movie = Movie(title=title,year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created success...')
        return redirect(url_for('watlist.index'))
    movies = Movie.query.all()
    return render_template('create.html',movies=movies)

@bg.route('/movie/edit/<int:movie_id>',methods=['GET','POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year) !=4 or len(title) > 60:
            flash('Invalid input...')
            return redirect(url_for('edit',movie_id=movie_id)) #重定向回对应的编辑页面
        movie.title=title #更新标题
        movie.year=year   #更新年份
        db.session.commit()
        flash('Item update success...')
        return redirect(url_for('watlist.index'))#重定向到主页
    return render_template('edit.html',movie=movie)

@bg.route('/movie/delete/<int:movie_id>',methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted...')
    return redirect(url_for('watlist.index'))

