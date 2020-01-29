from decouple import config
from dotenv import load_dotenv
from flask import Flask, render_template
from .models import DB, User

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    DB.init_app(app)

    @app.route('/')
    def root():
        return render_template('base.html', title='the Space Jam!', users=User.query.all())

    return app
#     @app.route('/welcome')
#     def root():
#         return render_template('base.html', title='the Space Jam!')
#
#     @app.route('/user/<username>')
#     def show_user_profile(username):
#         # show the user profile for that user
#         return f'{username}'
#     return app
#
# if __name__ == "__main__":
#     app.run(debug=True, port=8080)
