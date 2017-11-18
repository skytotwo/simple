import unittest
from flask import url_for
from simple import create_app, db
from simple.models import User


class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # 插入一个用户
    def insert_user(self):
        user = User()
        user.email = 'user@example.com'
        user.username = 'test'
        user.avatar = 'default.jpg'
        user.set_password('123456')
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        return user

    # 测试主页
    def test_index(self):
        user = self.insert_user()

        # 先登录
        response = self.client.post(
            url_for('auth.login'),
            data={'email': 'user@example.com',
                  'password': '123456'},
            follow_redirects=True)
        self.assertIn('写博客', response.get_data(as_text=True))

        # 测试关注
        response = self.client.get(url_for('main.followed_posts'))
        self.assertIn('关注', response.get_data(as_text=True))
