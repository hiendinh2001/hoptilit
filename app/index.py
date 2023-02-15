import math
from flask import render_template, request, redirect, url_for, session, jsonify
from app import app, login
from app import utils
import cloudinary.uploader
from flask_login import login_user, logout_user, current_user
from flask_login import login_required 
from app.models import UserRole

@app.route("/")
def home(): #index.html

    return render_template('index.html')

@app.route('/patient')
@login_required
def patient():
    service_id = request.args.get('service_id')
    status_id = request.args.get('status_id')
    kw = request.args.get("keyword")
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    patients = utils.load_patients(service_id=service_id, status_id=status_id, kw=kw, from_date=from_date, to_date=to_date)  

    return render_template('patient.html',
                           patients=patients)

@app.route('/status')
@login_required
def status():

    return render_template('status.html',
                           status=utils.status_stats())

@app.route('/register', methods=['get', 'post']) 
def user_register():
    err_msg = "" 
    if request.method.__eq__('POST'): 
        name = request.form.get('name') 
        username = request.form.get('username') 
        password = request.form.get('password')
        email = request.form.get('email')
        confirm = request.form.get('confirm')
        fonction = request.form.get('fonction')
        service = request.form.get('service')
        avatar_path = None

        try: 
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']

                utils.add_user(name=name,
                               username=username,
                               password=password,
                               email=email,
                               avatar=avatar_path,
                               fonction=fonction,
                               service=service)
                return redirect(url_for('user_signin')) 
            else:
                err_msg = 'Le mot de passe ressaisi est incorrect'
        except Exception as ex: 
            err_msg = 'Le système a une erreur' + str(ex)

    return render_template('register.html',
                           err_msg=err_msg)

@app.route('/user-login', methods=['get', 'post']) 
def user_signin():
    err_msg = "" 
    if request.method.__eq__('POST'):  
        username = request.form.get('username')  
        password = request.form.get('password')

        user = utils.check_login(username=username,
                                 password=password)
        if user: 
            login_user(user=user)
            if 'product_id' in request.args:
                return redirect(url_for(request.args.get('next', 'home'), product_id=request.args['product_id']))

            return redirect(url_for(request.args.get('next', 'home')))
        else:
            err_msg = "Identifiant ou mot de passe incorrect!!!"

    return render_template('login.html',
                           err_msg=err_msg)

@app.route('/admin-login', methods=['post']) 
def signin_admin():
    err_msg = "" 
    username = request.form['username']  
    password = request.form['password']

    user = utils.check_login(username=username,
                             password=password,
                             role=UserRole.ADMIN)
    if user: 
        login_user(user=user) 

    return redirect('/admin')

@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('user_signin'))

@login.user_loader 
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id) 

@app.route('/info-perso') 
@login_required
def info_perso():
    return render_template('info_perso.html')

if __name__ == '__main__':
    from app.admin import *
    app.run(debug=True)