from realproject import create_app,db
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

app = create_app()
manage = Manager(app) #实例化管理器
Migrate(app,db) #注入框架实例和数据实例
manage.add_command('db',MigrateCommand)#添加迁移命令

if __name__ == '__main__':
    manage.run()

