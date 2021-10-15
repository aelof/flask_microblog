from datetime import datetime, timedelta
import unittest
from test_app import create_app, db
from test_app.models import User, Post
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='dasha')
        u.set_password('dog')
        self.assertFalse(u.check_password('cat'))
        self.assertTrue(u.check_password('dog'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_follow(self):
        u1 = User(username='glasha', email='glasha@gnail.urus')
        u2 = User(username='yasha', email='yasha@gnail.urus')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'yasha')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'glasha')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_post(self):
        # create 4 users
        u1 = User(username='sasha', email='sasha@gnail.urus')
        u2 = User(username='pasha', email='pasha@gnail.urus')
        u3 = User(username='masha', email='masha@gnail.urus')
        u4 = User(username='dasha', email='dasha@gnail.urus')
        db.session.add_all([u1, u2, u3, u4])

        # create 4 posts
        now = datetime.utcnow()
        p1 = Post(body='post from sasha', author=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(body='post from pasha', author=u2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Post(body='post from masha', author=u3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Post(body='post from dasha', author=u4,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        u1.follow(u2)  # sasha follows pasha
        u1.follow(u4)  # sasha follows dasha
        u2.follow(u3)  # pasha follows masha
        u3.follow(u4)  # masha follows dasha
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])


if __name__ == '__main__':
    unittest.main(verbosity=2)
