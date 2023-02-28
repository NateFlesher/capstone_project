from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, Length, NumberRange


class UserSigninForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField()

class UserSignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password', validators=[DataRequired()])
    is_muver = BooleanField('Are you Signing up as a Muver?', default=False)
    submit_button = SubmitField()

class UpdateProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=100)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=100)])
    current_address = StringField('Current Address', validators=[DataRequired(), Length(max=100)])
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    state = StringField('State', validators=[DataRequired(), Length(max=100)])
    zip_code = IntegerField('Zip Code', validators=[
        DataRequired(),
        NumberRange(min=10000, max=99999, message='Zip code must be a 5-digit number'),
    ])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(max=12)])
    submit_button = SubmitField()

class PostAJobForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = StringField('Description', validators=[DataRequired(), Length(max=500)])
    start_add = StringField('Starting/Loading Address', validators=[DataRequired(), Length(max=100)])
    start_housing_type = StringField('Starting House Type', validators=[DataRequired(), Length(max=100)])
    start_floor_num = IntegerField('Starting Floor Number')
    start_beds = IntegerField('Starting Bedrooms', validators=[DataRequired()])
    start_baths = IntegerField('Starting Bathrooms', validators=[DataRequired()])
    end_add = StringField('Ending/Unloading Address', validators=[DataRequired(), Length(max=100)])
    end_housing_type = StringField('Ending House Type', validators=[DataRequired(), Length(max=100)])
    end_floor_num = IntegerField('Ending Floor Number')
    end_beds = IntegerField('Ending Bedrooms', validators=[DataRequired()])
    end_baths = IntegerField('Ending Bathrooms', validators=[DataRequired()])
    extra_add = StringField('Additional Addresses', validators=[Length(max=100)])
    moving_date = DateField('Estimated Moving Date', validators=[DataRequired()])
    submit_button = SubmitField()