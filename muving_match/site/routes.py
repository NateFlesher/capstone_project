from flask import Blueprint, render_template,  request, redirect, url_for, flash, current_app
from muving_match.forms import UserSignupForm, UserSigninForm, UpdateProfileForm, PostAJobForm
from muving_match.models import User, db, CustomerProfile, MuvingJobs
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from geopy.geocoders import Nominatim
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
#from muving_match.helpers import get_user_location
from datetime import datetime

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')
# def home():
#     # Get the user's zip code from the database
#     if current_user.is_authenticated:
#         user_zipcode = get_user_zipcode(current_user.id)
#     else:
#         return render_template('home.html', mymap=mymap, GOOGLEMAPS_APIKEY=current_app.config['GOOGLEMAPS_API_KEY'])
#     # handle unauthenticated users
    
#     # Create a Map object centered on the user's zip code
#     mymap = Map(
#         identifier="mymap",
#         lat=user_zipcode.lat,
#         lng=user_zipcode.lng,
#         markers=[(user_zipcode.lat, user_zipcode.lng)]
#     )

#     # Render the template with the map
#     return render_template('home.html', mymap=mymap, GOOGLEMAPS_APIKEY=current_app.config['GOOGLEMAPS_API_KEY'])
    


@site.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = UpdateProfileForm()
    customer_profile = CustomerProfile.query.filter_by(user_id=current_user.id).first()
    try:
        if form.validate_on_submit() and request.method == 'POST':
            # Update the existing customer profile object
            customer_profile.first_name = form.first_name.data
            customer_profile.last_name = form.last_name.data
            customer_profile.current_address = form.current_address.data
            customer_profile.city = form.city.data
            customer_profile.state = form.state.data
            customer_profile.zip_code = form.zip_code.data
            customer_profile.phone_number = form.phone_number.data
            db.session.commit()
            flash('Your profile has been updated', 'success')
            return redirect(url_for('site.settings'))
    except:
            raise Exception('Invalid Form Data: Please Check and try again')
    
    return render_template('settings.html', form=form, customer_profile=customer_profile)


@site.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    print(current_user.id)
    form = UpdateProfileForm()
    try:
        if form.validate_on_submit() and request.method=='POST':
            # Create a new customer profile object and add it to the database
            
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            current_address=form.current_address.data,
            city=form.city.data,
            state=form.state.data,
            zip_code=form.zip_code.data,
            phone_number=form.phone_number.data,
            user_id = current_user.id
            customer_profile = CustomerProfile(first_name, last_name, current_address, city, state, zip_code, phone_number, user_id)
            db.session.add(customer_profile)
            db.session.commit()

            flash('Your profile has been updated', 'success')
            return redirect(url_for('site.home'))
        
    except:
        raise Exception('Invalid Form Data: Please Check and try again')

    return render_template('profile.html', form=form)


@site.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = UpdateProfileForm()
    customer_profile = CustomerProfile.query.filter_by(user_id=current_user.id).first()
    if request.method == 'GET' and customer_profile:
        form.first_name.data = customer_profile.first_name
        form.last_name.data = customer_profile.last_name
        form.current_address.data = customer_profile.current_address
        form.city.data = customer_profile.city
        form.state.data = customer_profile.state
        form.zip_code.data = customer_profile.zip_code
        form.phone_number.data = customer_profile.phone_number

    try:
        if form.validate_on_submit():
            if not customer_profile:
                customer_profile = CustomerProfile(user_id=current_user.id)
            customer_profile.first_name = form.first_name.data
            customer_profile.last_name = form.last_name.data
            customer_profile.current_address = form.current_address.data
            customer_profile.city = form.city.data
            customer_profile.state = form.state.data
            customer_profile.zip_code = form.zip_code.data
            customer_profile.phone_number = form.phone_number.data
            db.session.add(customer_profile)
            db.session.commit()
            flash('Your profile has been updated', 'success')
            return redirect(url_for('site.settings'))
    except:
        raise Exception('Invalid Form Data: Please Check and try again')

    return render_template('edit_profile.html', form=form)



# @site.route('/post_a_job', methods=['GET', 'POST'])
# @login_required
# def post_a_job():
#     form = PostAJobForm()
#     muving_jobs = Muving_Jobs(
#         customer_id=current_user.id,
#         title=form.title.data,
#         description=form.description.data,
#         start_add=form.start_add.data,
#         end_add=form.end_add.data,
#         extra_add=form.extra_add.data,
#         moving_date=form.moving_date.data
#     )
#     print('moving post attempt')
#     try:
#         if form.validate_on_submit():
#             muving_jobs.title = form.title.data
#             muving_jobs.description = form.description.data
#             muving_jobs.start_add = form.start_add.data
#             muving_jobs.start_housing_type = form.start_housing_type.data
#             muving_jobs.start_floor_num = form.start_floor_num.data
#             muving_jobs.start_beds = form.start_beds.data
#             muving_jobs.start_baths = form.start_baths.data
#             muving_jobs.end_add = form.end_add.data
#             muving_jobs.end_housing_type = form.end_housing_type.data
#             muving_jobs.end_floor_num = form.end_floor_num.data
#             muving_jobs.end_beds = form.end_beds.data
#             muving_jobs.end_baths = form.end_baths.data
#             muving_jobs.extra_add = form.extra_add.data
#             muving_jobs.moving_date = datetime.strptime(form.moving_date.data, '%m/%d/%Y')

#             db.session.add(muving_jobs)
#             db.session.commit()
#             flash('Your Move has been Posted', 'success')
#             return redirect(url_for('site.index'))
#     except:
#         raise Exception('Invalid Form Data: Please Check and try again')

#     return render_template('post_a_job.html', form=form)





@site.route('/post_a_job', methods=['GET', 'POST'])
@login_required
def post_a_job():
    form = PostAJobForm()
    try:
        if form.validate_on_submit() and request.method== "POST":
            title = form.title.data
            description = form.description.data
            start_add = form.start_add.data
            start_housing_type = form.start_housing_type.data
            start_floor_num = form.start_floor_num.data
            start_beds = form.start_beds.data
            start_baths = form.start_baths.data
            end_add = form.end_add.data
            end_housing_type = form.end_housing_type.data
            end_floor_num = form.end_floor_num.data
            end_beds = form.end_beds.data
            end_baths = form.end_baths.data
            extra_add = form.extra_add.data
            moving_date_str = form.moving_date.data.strftime('%m/%d/%Y')
            moving_date = datetime.strptime(moving_date_str, '%m/%d/%Y')
            customer_profile = CustomerProfile.query.filter_by(user_id=current_user.id).first()
            customer_id = customer_profile.customer_id
            print(form.errors)
            muving_jobs = MuvingJobs(title, description, start_add, start_housing_type, start_floor_num, start_beds, start_baths, end_add, end_housing_type, end_floor_num, end_beds, end_baths, extra_add, moving_date, customer_id)
            print(form.errors)
            db.session.add(muving_jobs)
            db.session.commit()
            flash('Your Move has been Posted', 'success')
            return redirect(url_for('site.home'))
    except:
        raise Exception('Invalid Form Data: Please Check and try again')

    return render_template('post_a_job.html', form=form)



# <div class="container-fluid">
#     {{ googlemap(map_options) }}
# </div>
