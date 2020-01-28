import uuid
from flask import Flask
from .models import DB, User, Tweet

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_db.sqlite'
    DB.init_app(app)

    @app.route('/')
    def index():
        rand_name = str(uuid.uuid4())
        rand_u = User(name=rand_name)
        DB.session.add(rand_u)
        DB.session.commit()
        return 'The Index Page'

    @app.route('/hello')
    def hello():
        return 'Hello, World'

    @app.route('/user/<username>')
    def show_user_profile(username):
        # show the user profile for that user
        return f'{username}'
    return app

# if __name__ == "__main__":
#     app.run(debug=True, port=8080)
