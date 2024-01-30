from flask import redirect, render_template, url_for, flash, request,session
from flask_login import login_required, current_user,logout_user,login_user
from grocerystore import db, app
from .forms import CustomerRegisterForm, CustomerLoginForm
from .models import User
from grocerystore.products.models import Addproduct

@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.name.data}, Thank you for registering', 'success')
        return redirect(url_for('customerlogin'))

    return render_template('customer_register.html', form=form)

@app.route('/customer/login', methods=['GET', 'POST'])
def customerlogin():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:  # Simple password comparison
            login_user(user)
            flash('You are logged in now!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash('Incorrect email and password', 'danger')
        return redirect(url_for('customerlogin'))

    return render_template('customer_login.html', form=form)


@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        try:
            # Update the stock of products in the shopping cart
            for product_id, product in session['Shoppingcart'].items():
                product_obj = Addproduct.query.get(product_id)
                if product_obj:
                    # Reduce the stock by the quantity in the shopping cart
                    product_obj.stock -= int(product['quantity'])
                    db.session.commit()

            session.pop('Shoppingcart')
            flash('Your order has been sent successfully', 'success')
            return render_template("order.html")
            
            
        except Exception as e:
            print(e)
            flash('Something went wrong while placing the order', 'danger')
            return redirect(url_for('getCart'))
    else:
        return redirect(url_for('customerlogin'))




