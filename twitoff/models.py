"""SQLAlchemy models for twitoff."""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class User(DB.Model):
    """Class used to set up User DB objects."""

    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String(20), unique=True, nullable=False)
    newest_tweet_id = DB.Column(DB.BigInteger, nullable=False)

    def __repr__(self):
        """Printable representation method of User object."""
        return '<User %r>' % self.name


class Tweet(DB.Model):
    """Class used to set up Tweet objects."""

    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(500), nullable=False)
    vect = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(
                    DB.BigInteger,
                    DB.ForeignKey('user.id'),
                    nullable=False
                    )
    user = DB.relationship("User", backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        """Printable representation method of Tweet object."""
        return '<Tweet %r>' % self.text
