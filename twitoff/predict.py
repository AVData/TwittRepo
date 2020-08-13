'''
Prediction of Users based on Tweet embeddings.
'''
import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import BASILICA


def predict_user(user1_name, user2_name, tweet_text):
    """Determine and return which user is more likely to say a given Tweet."""

    user1 = User.query.filter(User.name == user1_name).one()
    user2 = User.query.filter(User.name == user2_name).one()
    user1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])

    # combine embeddings and create labels
    user2_embeddings = np.array([tweet.embedding for tweet in user2.tweets])
    embeddings = np.vstack([user1_embeddings, user2_embeddings])
    labels = np.concatenate([np.ones(len(user1.tweets)),
                             np.zeros(len(user2.tweets))])

    # Train model
    log_reg = LogisticRegression(1000).fit(embeddings, labels)

    tweet_embedding = BASILICA.embed_sentence(tweet_text, model='twitter')
    return log_reg.predict(np.array(tweet_embedding).reshape(1, -1))


'''
things to consider doing for a better model: (1) collect more tweets,
(4) play with reduced dimensionality techniques, (2) use a more powerful model
like random forests or trees, (3) reshuffle your data (reshuffle embedings and
labels in a way where labels and embeddings are still aligned)
'''

'''
If you really want to experiment fire up a jupyter notebook, and work there
with some data tuning etc.
'''
