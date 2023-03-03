from flask import Blueprint, render_template,  request, redirect, url_for, flash
from muving_match.forms import UserSignupForm, UserSigninForm, UpdateProfileForm
from muving_match.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required


auth =  Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserSignupForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            is_muver = form.is_muver.data

            user = User(email, password, is_muver)
            db.session.add(user)
            db.session.commit()
            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                if logged_user.is_muver:
                    flash("Please complete your muver profile", 'auth-success')
                    return redirect(url_for('site.muver_profile'))
                else:
                    flash("You have successfully logged in", 'auth-success')
                    return redirect(url_for('site.profile'))


            #flash("You have successfully create a user account")

            #return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid Form Data: Please Check and try again')

    return render_template('signup.html', form=form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserSigninForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
            
            flash("You have successfully logged in", 'auth-success')
            return redirect(url_for('site.home'))
    
    except:
        raise Exception('Invalid Form Data: Please check and try again')

    return render_template('signin.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))



