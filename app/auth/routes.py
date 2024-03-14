from flask import render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from .forms import *
from ..models import User
from ..extensions import db

@auth.route('/')
def logincheck():
    if current_user is not None:
        return redirect('/dashboard')
    else:
        return redirect("/login")

@auth.route('/login', methods=['GET','POST'])
def login():
    formlogin = LoginForm()
    if request.method == 'GET':
        if False:
            return redirect("/dashboard")
        else:
            return render_template('login.html', pageTitle='Login', form=formlogin)

    elif request.method == 'POST':
        if formlogin.validate_on_submit():
            print(formlogin.data)
            username = formlogin.username.data
            password = formlogin.password.data

            user = User.query.filter_by(username=username).first()
            print(user)
            # none will be returned if the user doesnt exist
            if user == None:
                return render_template('login.html', pageTitle='Login', form=formlogin, loginerror='Username or Password is wrong.')
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect('/dashboard')
            else:
                return render_template('login.html', pageTitle='Login', form=formlogin, loginerror='Username or Password is wrong.')
        else:
            return render_template('login.html', pageTitle='Login', form=formlogin, loginerror='Username or Password is wrong.')
    else:
        return render_template('login.html', pageTitle='Login', form=formlogin)


@auth.route('/register', methods=['GET','POST'])
def register():
    formregister = RegistrationForm()
    if request.method == 'GET':
        if False:
            return redirect("/dashboard")
        else:
            return render_template('register.html', pageTitle='Register', form=formregister)
        
    elif request.method == 'POST':
        if formregister.validate_on_submit():
            print("Form is valid")
            print(formregister.username.data)
            print(formregister.password.data)
            print(formregister.confirm_password.data)

            username = formregister.username.data
            password = formregister.password.data

            user = User.query.filter_by(username=username).first()

            if user:
                flash('Account already exists:')
                return redirect('/register')
            
            new_user = User(username=username, password=generate_password_hash(password, method='pbkdf2', salt_length=16), role='User')
            db.session.add(new_user)
            db.session.commit()

            return redirect('/login')

        else:
            return render_template('register.html', pageTitle='Register', form=formregister, registererror='Enter valid data please.')
    else:
        return render_template('register.html', pageTitle='Register', form=formregister)
    


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@auth.route('/settings', methods=['GET','POST'])
@login_required
def settings():
    formchangepw = SettingsForm()
    if request.method == 'POST':
        if formchangepw.validate_on_submit():
            print("Password before change: ", current_user.password)
            current_user.password = generate_password_hash(formchangepw.new_password.data, method='pbkdf2', salt_length=16)
            db.session.commit()
            print("Password change: ", current_user.password)
        else:
            return render_template('settings.html', pageTitle='Register', form=formchangepw, settingserror='Enter valid data please.')
    
    return render_template('settings.html', pageTitle='Settings', name=current_user.username, form=formchangepw)


@auth.route('/gtcs')
def gtcs_auth():
    return render_template('gtcs_auth.html', pageTitle="GTCs")


@auth.route('/imprint')
def imprint_auth():
    return render_template('imprint_auth.html', pageTitle="Imprint")

@auth.route('/gdpr')
def gdpr_auth():
    return render_template('gdpr_auth.html', pageTitle="GDPR")
