import os
from simple import create_app, db
from simple.models import User, Role, Post

# 创建simpleblog实例
app = create_app(os.getenv('FLASK_CONFIG') or 'development')


# shell上下文
@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post)


# 测试的命令
@app.cli.command()
def test():
    """测试代码"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
