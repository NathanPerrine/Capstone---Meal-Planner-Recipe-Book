from flask import render_template, redirect, url_for, flash 
from flask_login import login_user, logout_user, login_required, current_user
from . import auth 
from .forms import SignUpForm, LogInForm, ChangePasswordForm
from .models import User

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    title = "Sign Up"
    form = SignUpForm()

    if form.validate_on_submit():
        email = form.email.data.strip()
        username = form.username.data.strip()
        password = form.password.data 

        # Check if user already exists 
        # .ilike() is case insensitive 
        user_already_exists = User.query.filter((User.username.ilike(username)) | (User.email.ilike(email))).all()
        if user_already_exists:
            # If taken, flash warning message, redirect
            flash("That username or email is already in use, please try again.", "danger")
            return render_template('signup.html', title=title, form=form)
        
        new_user = User(email = email, username = username, password = password)
        flash(f"{new_user} has been created!", "success")
        login_user(new_user)
        return redirect(url_for('index'))
    return render_template('signup.html', title = title, form = form)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    title = "Log In"
    form = LogInForm()

    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data
        #Check for a user with that name 
        user = User.query.filter(User.username.ilike(username)).first()
        if user and user.check_password(password):
            login_user(user)
            flash(f"{user} has successfully logged in.", "success")
            return redirect(url_for('home.index'))
        else:
            flash("Username and/or password is incorrect.", 'warning')
    return render_template('login.html', title = title, form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out.", "success")
    return redirect(url_for('home.index'))

@auth.route('/userProfile/<user_Id>', methods=['GET', 'POST'])
@login_required
def userProfile(user_Id):
    if int(user_Id) != current_user.id:
        flash('You do not have access to this profile.', 'danger')
        return redirect(url_for('home.index'))

    title = f'User Profile for {current_user.username}'
    date_created = str(current_user.date_created).split()[0]
    change_pass_form = ChangePasswordForm()

    # Change password form validated
    if change_pass_form.validate_on_submit():
        old_password = change_pass_form.old_password.data
        new_password = change_pass_form.new_password.data
        confirm_new_password = change_pass_form.confirm_new_password.data

        # Check if password is correct
        if current_user.check_password(old_password):
            current_user.change_password(confirm_new_password)
            flash('Password has been changed.', 'success')

        # print(f'Old Password: {old_password}')
        # print(f'New password: {new_password}')
        # print(f'Confirm New Pass: {confirm_new_password}')

    return render_template('userProfile.html', title=title, date_created=date_created, change_pass_form=change_pass_form)