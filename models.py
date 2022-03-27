from flask import Flask, render_template, url_for, flash, abort, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, Session
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user, login_url
from forms import LoginForm, RegisterForm
import boto3
from werkzeug.utils import secure_filename

application = Flask(__name__)
app = application

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///UserUs.db'
app.config['SECRET_KEY'] = 'RockWorld'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)

client = boto3.client(
    's3',
    aws_access_key_id = 'AKIAWWCN26J3O5VNI5EL',
    aws_secret_access_key = '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',
    region_name = 'us-east-2'
)
# clientResponse = client.list_buckets()

