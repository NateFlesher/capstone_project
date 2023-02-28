from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import uuid

# Adding Flask security for passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Flask login to check for an authenticated user
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow


# Create an instance of SQLAlchemy
db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True, default=str(uuid.uuid4()))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False, default='')
    is_muver = db.Column(db.Boolean, nullable=False)

    def __init__(self, email, password='', is_muver=False):
        self.id = str(uuid.uuid4())
        self.password = generate_password_hash(password)
        self.email = email
        self.is_muver = is_muver

    def __repr__(self):
        return f"User {self.email} has been created"


class CustomerProfile(db.Model):
    __tablename__ = 'customer_profile'
    customer_id = db.Column(db.String, primary_key=True, default=str(uuid.uuid4()))
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    current_address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(12), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    #user = db.relationship('User', backref=db.backref('customer_profile', uselist=False))

    def __init__(self, first_name, last_name, current_address, city, state, zip_code, phone_number, user_id):
        self.customer_id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.current_address = current_address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.phone_number = phone_number
        self.user_id = user_id


class MuverProfile(db.Model):
    muver_id = db.Column(db.String, primary_key=True, default=str(uuid.uuid4()))
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    current_address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(12), nullable=False)
    tokens_available = db.Column(db.Integer, default=25)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    #user = db.relationship('User', backref=db.backref('muver_profile', uselist=False))

    def __init__(self, first_name, last_name, current_address, city, state, zip_code, phone_number, user_id):
        self.muver_id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.current_address = current_address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.phone_number = phone_number
        self.user_id = user_id




class MuvingJobs(db.Model):
    job_id = db.Column(db.String, primary_key=True, default=str(uuid.uuid4()))
    title=db.Column(db.String(100), nullable=False)
    description=db.Column(db.String(500), nullable=False)
    start_add=db.Column(db.String(100), nullable=False)
    start_housing_type=db.Column(db.String(100), nullable=False)
    start_floor_num=db.Column(db.Integer, nullable=True)
    start_beds=db.Column(db.Integer, nullable=False)
    start_baths=db.Column(db.Integer, nullable=False)
    end_add=db.Column(db.String(100), nullable=False)
    end_housing_type=db.Column(db.String(100))
    end_floor_num=db.Column(db.Integer, nullable=True)
    end_beds=db.Column(db.Integer, nullable=False)
    end_baths=db.Column(db.Integer, nullable=False)
    extra_add=db.Column(db.String(100), nullable=True)
    moving_date=db.Column(db.DateTime, nullable=False)
    job_posted_time=db.Column(db.DateTime, default=datetime.utcnow)
    customer_id = db.Column(db.String, db.ForeignKey('customer_profile.customer_id'), nullable=False)

    def __init__(self, title, description, start_add, start_housing_type, start_floor_num, start_beds, start_baths, end_add, end_housing_type, end_floor_num, end_beds, end_baths, extra_add, moving_date, customer_id = ''):
        self.job_id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.start_add = start_add
        self.start_housing_type = start_housing_type
        self.start_floor_num = start_floor_num
        self.start_beds = start_beds
        self.start_baths = start_baths
        self.end_add = end_add
        self.end_housing_type = end_housing_type
        self.end_floor_num = end_floor_num
        self.end_beds = end_beds
        self.end_baths = end_baths
        self.extra_add = extra_add
        self.moving_date = moving_date
        self.customer_id = customer_id

    def __repr__(self):
        return "Your job has been posted!"



# class MuvingJobSchema(ma.Schema):
#     class Meta:
#         fields = ['job_id', 'title', 'description', 'start_add', 'end_add', 'extra_add', 'moving_date', 'housing_type', 'num_beds', 'num_baths', "floor_num", 'job_posted_time', 'job_status', 'job_type', 'customer_id', 'photos']


# muving_Job_schema=MuvingJobSchema()



# class Photos(db.Model):
#     photo_id = db.Column(db.String, primary_key=True, default=str(uuid.uuid4()))
#     filename = db.Column(db.String(100), nullable=False)
#     job_id = db.Column(db.String, db.ForeignKey(MuvingJobs.job_id), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     def __init__(self, filename, job_id, created_at=None):
#         self.filename = filename
#         self.job_id = job_id
#         self.created_at = created_at if created_at else datetime.utcnow()

# class PhotosSchema(ma.Schema):
#     class Meta:
#         fields = ('photo_id', 'filename', 'created_at')



# self __init__(self):
#         self.user = self.y()
#     def y(self):
#         x = User.query.filter_by(user_id = self.user_id).first()
#         return x
        
        