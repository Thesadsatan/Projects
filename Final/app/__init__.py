import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from flask_session import Session
from flask_login import LoginManager, UserMixin
from flask_mail import Mail, Message



app = Flask(__name__)

app.config['SECRET_KEY'] = 'e617a03888caff57272b73f114e07701'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

async_engine = create_async_engine('postgresql+asyncpg://user:password@host/dbname', echo=True)
async_session = sessionmaker(async_engine, class_=AsyncSession)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('Quodophile_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('Quodophile_SMTP_PASS')

mail = Mail(app)



from app import routes



