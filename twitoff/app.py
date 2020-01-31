from decouple import config
from dotenv import load_dotenv
from flask import Flask, render_template, request
from .models import DB, User
from .twitter import add_or_update_user, update_all_users, add_default_users
from .predict import predict_user

# the following code is all from the Bruno lecture

load_dotenv()

# The following code comes from the Alex Kim lecture

def create_app():
    """Create and configure an instance of the Flask application"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)

    @app.route('/')
    def root():
        return render_template('base.html',
                                title='Home',
                                users=User.query.all())

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        name = name or request.values['username']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = f'User {name} successfully added!'
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = f'Error while trying to add user {name}: {e}'
            tweets = []
        return render_template('user.html',
                                title=name,
                                message=message,
                                tweets=tweets)

    @app.route('/compare', methods=['POST'])
    def compare(messages=''):
        user1 = request.values['user1']
        user2 = request.values['user2']
        tweet_text = request.values['tweet_text']

        if user1 == user2:
            message = 'Error: Compare two different users!'
            return render_template('predict.html',
                                    title='Prediction',
                                    message=message)
        else:
            prediction = predict_user(user1, user2, tweet_text)
            message = '"{}" is more likely to be said by {} than {}'.format(
                request.values['tweet_text'], user1 if prediction else user2,
                user2 if prediction else user1)
            return render_template('predict.html',
                                    title='Prediction',
                                    message=message)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset database!')

    @app.route('/update')
    def update():
        update_all_users()
        return render_template('base.html',
                                users=User.query.all(),
                                title='All Tweets updated!!')

    @app.route('/add_default')
    def add_default():
        add_default_users()
        return render_template('base.html',
                                users=User.query.all(),
                                title='Added all default users to database')


    return app
