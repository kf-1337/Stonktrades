from flask import render_template, redirect, request, flash
from flask_login import login_required, current_user
from . import admin
from ..extensions import db, scheduler
from ..api import api_to_db
from ..models import User
from .forms import DeleteUserForm, UserRoleChangeForm
from sqlalchemy import and_, or_, not_


@admin.route('/admindashboard')
@login_required
def admindashboard():
    if current_user.role == 'Admin':
        return render_template('admindashboard.html', pageTitle='Admin Dashboard', name=current_user.username)
    else:
        return redirect('/')
    
@admin.route('/admindashboard/api')
@login_required
def admindashboardapi():
    if current_user.role == 'Admin':
        return render_template('admindashboard_api.html', pageTitle='Admin Dashboard', name=current_user.username)
    else:
        return redirect('/')


@admin.route('/admindashboard/usermgmt', methods=['GET','POST'])
@login_required
def usermgmt():
    if current_user.role == 'Admin':
        formdelete = DeleteUserForm()
        formrolechange = UserRoleChangeForm()
        users_header = ['ID', 'Username','Role', 'Password']
        result = User.query.all()
        if request.method == 'GET':
            return render_template('admindashboard_usermgmt.html', pageTitle = 'User Management', name=current_user.username, users_header=users_header, result = result, formrolechange = formrolechange, formdelete = formdelete)
        
        elif request.method == 'POST':
            if formdelete.submit1.data and formdelete.validate_on_submit():
                print("Trigger: Form user deletion")
                try:
                    User.query.filter(and_(User.id == formdelete.userid1.data, User.username == formdelete.username1.data)).delete()
                    db.session.commit()
                    flash("User Deleted.")
                    return redirect ('/admindashboard/usermgmt')
                except:
                    return render_template('admindashboard_usermgmt.html', pageTitle = 'User Management', name=current_user.username, users_header=users_header, result = result, formrolechange = formrolechange, formdelete = formdelete, formInvalidError = '')
                    return redirect ('/admindashboard/usermgmt')
            elif formrolechange.submit2.data and formrolechange.validate_on_submit():
                print("Trigger: Form role change")
                try:
                    print("Try")
                    user_to_update = User.query.filter(and_(User.id == formrolechange.userid2.data, User.username == formrolechange.username2.data)).first()
                    user_to_update.role = formrolechange.role2.data
                    db.session.commit(user_to_update)
                    flash(" Role changed.")
                    return redirect ('/admindashboard/usermgmt')
                except:
                    return render_template('admindashboard_usermgmt.html', pageTitle = 'User Management', name=current_user.username, users_header=users_header, result = result, formrolechange = formrolechange, formdelete = formdelete, formInvalidError = '')
                    
                    return redirect ('/admindashboard/usermgmt')
            else:
                return render_template('admindashboard_usermgmt.html', pageTitle = 'User Management', name=current_user.username, users_header=users_header, result = result)
        else:
            return render_template('admindashboard_usermgmt.html', pageTitle = 'User Management', name=current_user.username, users_header=users_header, result = result, formrolechange = formrolechange, formdelete = formdelete, formInvalidError='The form was not filled out correctly. Please try again.')
            
    else:
        return redirect('/')













@admin.route('/api/startup')
@login_required
def api_startup():
    if current_user.role == 'Admin':
        scheduler.start()
        return redirect('/admindashboard/api')
    else:
        redirect('/dashboard')

@admin.route('/api/shutdown')
@login_required
def api_shutdown():
    if current_user.role == 'Admin':
        scheduler.shutdown(wait=False)
        return redirect('/admindashboard/api')
    else:
        return redirect('/dashboard')



@admin.route('/api/runtickerlist')
@login_required
def runtickerlist():
    if current_user.role == 'Admin':
        api_to_db.job_ticker_list()
        return redirect('/admindashboard/api')
    else:
        return redirect('/dashboard')


@admin.route('/api/runtickerdetails')
@login_required
def runtickerdetails():
    if current_user.role == 'Admin':
        api_to_db.temp_job()
        return redirect('/admindashboard/api')
    else:
        return redirect('/dashboard')

@admin.route('/api/runtickeraggs')
@login_required
def runtickeraggs():
    if current_user.role == 'Admin':
        api_to_db.job_ticker_aggs()
        return redirect('/admindashboard/api')
    else:
        return redirect('/dashboard')


@admin.route('/api/runtickergroupeddaily')
@login_required
def runtickergroupeddaily():
    if current_user.role == 'Admin':
        api_to_db.job_ticker_grouped_daily()
        return redirect('/admindashboard/api')
    else:
        return redirect('/dashboard')



@admin.route('/admin/gtcs')
def gtcs_admin():
    if current_user.role == 'Admin':
        return render_template('gtcs_admin.html', pageTitle="GTCs", name=current_user.username)
    else:
        return redirect('/dashboard')

@admin.route('/admin/imprint')
def imprint_admin():
    if current_user.role == 'Admin':
        return render_template('imprint_admin.html', pageTitle="Imprint", name=current_user.username)
    else:
        return redirect('/dashboard')

@admin.route('/admin/gdpr')
def gdpr_admin():
    if current_user.role == 'Admin':
        return render_template('gdpr_admin.html', pageTitle="GDPR", name=current_user.username)
    else:
        return redirect('/dashboard')