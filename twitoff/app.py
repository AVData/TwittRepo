from decouple import config
# from dotenv import load_dotenv
from flask import Flask, render_template, request
from .models import DB, User
from .twitter import add_or_update_user
from .predict import predict_user

# the following code is all from the Bruno lecture

# load_dotenv()
#
# def create_app():
#     app = Flask(__name__)
#     app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
#     DB.init_app(app)
#
#     @app.route('/')
#     def root():
#         return render_template('base.html', title='the Space Jam!', users=User.query.all())
#
#     return app

# The following code comes from the Alex Kim lecture

def create_app():
    """Create and configure an instance of the Flask application"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)

    @app.route('/')
    def root():
        DB.create_all()
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
            tweets = User.query.filter(User.name==name).one().tweets
        except Exception as e:
            message = f'Error while trying to add user {name}: {e}'
            tweets = []
        return render_template('user.html',
                                title=name,
                                message=message,
                                tweets=tweets)


    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset database!')

    # @app.route('/predict')
    # def predict_user():


    return app
