from flask import Blueprint, render_template,  request, redirect, url_for, flash
from muving_match.forms import UpdateProfileForm, PostAJobForm, PostJobIntroForm
from muving_match.models import User, db, CustomerProfile, MuvingJobs, MuverProfile
from flask_login import login_user, logout_user, login_required, current_user
from muving_match.helpers import get_user_location
from datetime import datetime

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/', methods=['GET', 'POST'])
def home():
    form = PostJobIntroForm()
    muver_jobs = []
    muvers = []
    if current_user.is_authenticated and current_user.is_muver:
        # Get the muver's location based on their zip code
        location = get_user_location(current_user.id, is_muver=True)
        latitude = float(location['latitude'])
        longitude = float(location['longitude'])
        print(latitude, longitude)
        zip_code = location['zip_code']
        # Get jobs available for muvers
        muver_jobs = MuvingJobs.query.all()
    elif current_user.is_authenticated and not current_user.is_muver:
        # Get the customer's location based on their zip code
        location = get_user_location(current_user.id, is_muver=False)
        latitude = float(location['latitude'])
        longitude = float(location['longitude'])
        zip_code = location['zip_code']
         # Get the list of muvers from the database
        muvers = MuverProfile.query.all()
    else:
        # Redirect the user to the sign in page
        return redirect(url_for('auth.signin'))

    if request.method == "POST" and form.validate_on_submit():
        # Construct URL with form data as query parameters
        url = url_for('site.post_a_job',
                      title=form.title.data,
                      description=form.description.data,
                      start_add=form.start_add.data,
                      start_housing_type=form.start_housing_type.data,
                      start_floor_num=form.start_floor_num.data,
                      start_beds=form.start_beds.data,
                      start_baths=form.start_baths.data)
        
        # Redirect to post job page with the constructed URL
        return redirect(url)

    return render_template('index.html', latitude=latitude, longitude=longitude, zip_code=zip_code, form=form, muver_jobs=muver_jobs, muvers=muvers)




@site.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    user = User.query.filter_by(id=current_user.id).first()
    if user.is_muver:
        return redirect(url_for('site.muver_settings'))
    else:
        form = UpdateProfileForm()
        customer_profile = CustomerProfile.query.filter_by(user_id=current_user.id).first()
        job_history = MuvingJobs.query.filter_by(customer_id=customer_profile.customer_id).all()
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
    
    return render_template('settings.html', form=form, customer_profile=customer_profile, job_history=job_history)


@site.route('/muver_settings', methods=['GET', 'POST'])
@login_required
def muver_settings():
    form = UpdateProfileForm()
    muver_profile = MuverProfile.query.filter_by(user_id=current_user.id).first()
    
    return render_template('muver_settings.html', form=form, muver_profile=muver_profile)


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



@site.route('/muver_profile', methods=['GET', 'POST'])
@login_required
def muver_profile():
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
            muver_profile = MuverProfile(first_name, last_name, current_address, city, state, zip_code, phone_number, user_id)
            db.session.add(muver_profile)
            db.session.commit()

            flash('Your profile has been updated', 'success')
            return redirect(url_for('site.home'))
        
    except:
        raise Exception('Invalid Form Data: Please Check and try again')

    return render_template('muver_profile.html', form=form)


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



@site.route('/edit_muver_profile', methods=['GET', 'POST'])
@login_required
def edit_muver_profile():
    form = UpdateProfileForm()
    muver_profile = MuverProfile.query.filter_by(user_id=current_user.id).first()
    if request.method == 'GET' and muver_profile:
        form.first_name.data = muver_profile.first_name
        form.last_name.data = muver_profile.last_name
        form.current_address.data = muver_profile.current_address
        form.city.data = muver_profile.city
        form.state.data = muver_profile.state
        form.zip_code.data = muver_profile.zip_code
        form.phone_number.data = muver_profile.phone_number

    try:
        if form.validate_on_submit():
            if not muver_profile:
                muver_profile = MuverProfile(user_id=current_user.id)
                
            muver_profile.first_name = form.first_name.data
            muver_profile.last_name = form.last_name.data
            muver_profile.current_address = form.current_address.data
            muver_profile.city = form.city.data
            muver_profile.state = form.state.data
            muver_profile.zip_code = form.zip_code.data
            muver_profile.phone_number = form.phone_number.data
            db.session.add(muver_profile)
            db.session.commit()
            flash('Your profile has been updated', 'success')
            return redirect(url_for('site.muver_settings'))
    except:
        raise Exception('Invalid Form Data: Please Check and try again')

    if not muver_profile:
        # If no MuverProfile instance exists, create one
        muver_profile = MuverProfile(user_id=current_user.id)
        db.session.add(muver_profile)
        db.session.commit()
        
    return render_template('edit_muver_profile.html', form=form)


# @site.route('/change_email', methods=['POST'])
# def change_email():
#     new_email = request.form['email']
#     user = User.query.filter_by(id=current_user.id).first()
#     user.email = new_email
#     db.session.commit()
#     flash('Your email has been updated.')
#     return redirect(url_for('site.settings'))

# @site.route('/change_password', methods=['POST'])
# def change_password():
#     new_password = request.form['password']
#     confirm_password = request.form['confirm_password']
#     user = User.query.filter_by(id=current_user.id).first()
#     if new_password != confirm_password:
#         flash('Passwords do not match.')
#         return redirect(url_for('site.settings'))
    
#     user.set_password(new_password)
#     db.session.commit()
#     flash('Password changed successfully.')
#     return redirect(url_for('site.settings')) 





@site.route('/post_a_job', methods=['GET', 'POST'])
@login_required
def post_a_job():
    form = PostAJobForm()

    if form.validate_on_submit() and request.method == 'POST':
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

        muving_jobs = MuvingJobs(title, description, start_add, start_housing_type, start_floor_num, start_beds, start_baths, end_add, end_housing_type, end_floor_num, end_beds, end_baths, extra_add, moving_date, customer_id)
        db.session.add(muving_jobs)
        db.session.commit()

        flash('Your Move has been Posted', 'success')
        return redirect(url_for('site.home'))

    if request.method == 'GET' or form.errors:
        # Pre-populate form fields with query parameters
        form.title.data = request.args.get('title')
        form.description.data = request.args.get('description')
        form.start_add.data = request.args.get('start_add')
        form.start_housing_type.data = request.args.get('start_housing_type')
        form.start_floor_num.data = request.args.get('start_floor_num')
        form.start_beds.data = request.args.get('start_beds')
        form.start_baths.data = request.args.get('start_baths')

    return render_template('post_a_job.html', form=form)



@site.route('/delete_job/<job_id>', methods=['POST'])
@login_required
def delete_job(job_id):
    job = MuvingJobs.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash('The job has been deleted', 'success')
    return redirect(url_for('site.settings'))



@site.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    try:
        # Get the current user's ID
        user_id = current_user.id
        
        # Delete the user's account from the database
        db.session.query(User).filter_by(id=user_id).delete()
        db.session.commit()

        # Log the user out
        logout_user()
        
        # Redirect the user to the homepage
        flash('Your account has been deleted.', 'success')
        return redirect(url_for('site.home'))
    except:
        flash('An error occurred. Your account has not been deleted.', 'danger')
        return redirect(url_for('site.settings'))



# <div class="container-fluid">
#     {{ googlemap(map_options) }}
# </div>
