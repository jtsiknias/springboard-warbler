"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


from app import app
import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        user1 = User.signup("user1", "user@example.com", "password", None)
        uid1 = 1000
        user1.id = uid1

        user2 = User.signup("user2", "user2@example.com", "password", None)
        uid2 = 1234
        user2.id = uid2

        db.session.add(user1, user2)
        db.session.commit()

        user1 = User.query.get(uid1)
        user2 = User.query.get(uid2)

        self.user1 = user1
        self.uid1 = uid1

        self.user2 = user2
        self.uid2 = uid2

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_follow_user(self):
        """Does 'following' feature work"""
        self.user2.followers.append(self.user1)
        db.session.commit()

        self.assertEqual(len(self.user2.followers), 1)
        self.assertEqual(len(self.user1.followers), 0)
        self.assertEqual(len(self.user2.following), 0)
        self.assertEqual(len(self.user1.following), 1)

    def test_repr(self):
        self.assertIn(f"<User #1000", self.user1.__repr__())

    def test_valid_user(self):
        valid_user = User.signup(
            "validuser", "validuser@example.com", "password", None)
        db.session.add(valid_user)
        db.session.commit()

        self.assertIsNotNone(valid_user)
        self.assertEqual(valid_user.email, "validuser@example.com")
        self.assertEqual(valid_user.username, "validuser")
        self.assertNotEqual(valid_user.password, "password")

    def test_invalid_username_signup(self):
        """Test invalid email at signup"""
        invalid_user = User.signup(None, "example@email.com", "password", None)

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_email_signup(self):
        """Test invalid email at signup"""
        invalid_user = User.signup("invaliduser", None, "password", None)

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_password_signup(self):
        """Test invalid password at signup"""
        with self.assertRaises(ValueError) as context:
            User.signup("invaliduser", "invaliduser@example.com", None, None)

        with self.assertRaises(ValueError) as context:
            User.signup("invaliduser", "invaliduser@example.com", "", None)
