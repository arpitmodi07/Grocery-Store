from flask import render_template, redirect, session, request, url_for, flash
from grocerystore import app
from .forms import LoginForm
from grocerystore.products.models import Addproduct, Category
from flask_login import logout_user,login_required


@app.route('/admin')
def admin():
    if 'username' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    products = Addproduct.query.all()
    categories= Category.query.all()
    return render_template('index.html',title='Admin Page',products=products,categories=categories)



@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method=="POST" and form.validate():
        username = form.username.data
        password = form.password.data
        if username == 'admin' and password == 'admin':
            session['username'] = username
            session['password'] = password
            flash('Welcome Admin! You are now logged in.', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('Wrong Password try again','danger')
    return render_template('login.html',form=form,title="Login Page")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
