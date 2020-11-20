"""Prediction of Users based on Tweet embeddings."""

import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorize_tweet


def predict_user(user1_name, user2_name, hypo_tweet_text):
    """Determine and return which user is more likely to say a given Tweet."""
    user1 = User.query.filter(User.name == user1_name).one()
    user2 = User.query.filter(User.name == user2_name).one()
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])
    user2_vects = np.array([tweet.vect for tweet in user2.tweets])
    vects = np.vstack([user1_vects, user2_vects])
    labels = np.concatenate([np.ones(len(user1.tweets)),
                             np.zeros(len(user2.tweets))])
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text)

    log_reg = LogisticRegression().fit(vects, labels)

    return log_reg.predict(hypo_tweet_vect.reshape(1, -1))


'''
Things to consider doing for a better model: (1) collect more tweets,
(4) play with reduced dimensionality techniques, (2) use a more powerful model
like random forests or trees, (3) reshuffle your data (reshuffle embedings and
labels in a way where labels and embeddings are still aligned)
'''

'''
If you really want to experiment fire up a jupyter notebook, and work there
with some data tuning etc.
'''
