from app import db, login_manager, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(500), nullable=False, unique=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    book = db.relationship('Book', backref='reader', lazy=True)
    word = db.relationship('Word', backref='reader', lazy=True)


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}')"
 
class Book(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(1000), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Book('{self.title}', '{self.content}', '{self.author}')"

class Word(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(20000), nullable=False)
    part_of_speech = db.Column(db.String(500), nullable=False)
    synonym = db.Column(db.String(20000), nullable=False)
    definition = db.Column(db.Text, nullable=False)
    example = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Word('{self.word}', '{self.definition}')"