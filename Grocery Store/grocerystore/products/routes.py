from flask import redirect, render_template, url_for, flash, request,session
from grocerystore import db, app 
from .models import Category,Addproduct
from .forms import Addproducts,UpdateProduct
from grocerystore.admin.routes import login
from grocerystore.admin.forms import LoginForm

@app.route('/')
def home():
    categories = Category.query.all()
    print("Categories are it is a list", categories)
    category_products = {}
    
    for category in categories:
        products = Addproduct.query.filter_by(category_id=category.id).limit(4).all()
        category_products[category.id] = products
    print("Categories_products are it is a dictionary",category_products)
    products_out_of_stock = Addproduct.query.filter(Addproduct.stock <= 0).order_by(Addproduct.id.desc()).all()
    return render_template('home.html', categories=categories, category_products=category_products, products_out_of_stock=products_out_of_stock)



@app.route('/result')
def result():
    search_query = request.args.get('q')
    category_id = Category.query.filter(Category.name.ilike(f'%{search_query}%')).first()
    print(category_id)
    category_id = category_id.id if category_id else -1
    print(category_id)
    products = Addproduct.query.filter(
        (Addproduct.name.ilike(f'%{search_query}%')) |
        (Addproduct.price.ilike(f'%{search_query}%')) |
        (Addproduct.manufacturing.ilike(f'%{search_query}%')) |
        (Addproduct.category_id == category_id)
    ).all()
    return render_template('search.html', products=products)



@app.route('/product/<int:id>')
def details(id):
    product = Addproduct.query.get(id)
    print(product)
    return render_template('details.html',product=product)
   

@app.route('/add_product_to_category/<int:id>', methods=['GET', 'POST'])
def add_product_to_category(id):
    category = Category.query.get_or_404(id)
    form = Addproducts(request.form)  # Pass the selected category to the form

    if request.method == "POST":
        # Extract the category_id from the 'id' parameter passed in the URL
        category_id = id

        name = form.name.data
        price = form.price.data
        unit = form.unit.data
        manufacturing = form.manufacturing_date.data
        discount = form.discount.data
        stock = form.stock.data
        desc = form.discription.data

        unit = 'Rs/'+unit
        new_product = Addproduct(
            name=name, price=price,unit=unit,manufacturing=manufacturing, discount=discount, stock=stock, desc=desc, category_id=category_id
        )

        db.session.add(new_product)
        flash(f'The product {name} was added to the category {category.name}', 'success')
        db.session.commit()
        return redirect(url_for('get_category', id=id))

    return render_template('addproduct.html', category=category, form=form)



@app.route('/category/<int:id>')
def get_category(id):
    if login in session:
        category = Category.query.get_or_404(id)
        products = Addproduct.query.filter_by(category_id=id).all()
    
        return render_template('category.html', category=category, products=products)
    form = LoginForm(request.form)
    return render_template("login.html", form=form)


@app.route('/categories/<int:id>')
def get_cat_prod(id):
    category = Category.query.get_or_404(id)
    products = Addproduct.query.filter_by(category_id=id).all()
    return render_template('category_products.html', category=category, products=products)


@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    if 'username' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        newcategory = request.form.get('category')
        cat = Category(name=newcategory)
        db.session.add(cat)
        flash(f'The New Category {newcategory} is created successfully', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('addcategory.html')


@app.route('/updatecat/<int:id>',methods=['GET','POST'])
def updatecat(id):
    if 'username' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method=="POST":
        updatecat.name = category
        flash(f'Your category {category} has been updated','success')
        db.session.commit()
        return redirect(url_for('admin'))
        
    return render_template('updatecategory.html',title="Update Category Page",updatecat=updatecat)



@app.route('/deletecategory/<int:id>', methods=['GET', 'POST'])
def deletecategory(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        confirm = request.form.get('confirm_delete')
        if confirm == 'yes':
            products = Addproduct.query.filter_by(category_id=id).all()
            for product in products:
                db.session.delete(product)
            db.session.delete(category)
            db.session.commit()
            flash(f"The Category {category.name} and its associated products is deleted successfully", "success")
        return redirect(url_for('admin'))
    
    
    return render_template('delete_category.html', category=category)



@app.route('/updateproduct/<int:id>', methods=["GET", "POST"])
def updateproduct(id):
    product = Addproduct.query.get_or_404(id)
    categories = Category.query.all()
    form = UpdateProduct(request.form)

    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.category_id = int(request.form['category'])  # Get the selected category from the form

        product.desc = form.discription.data
        db.session.commit()
        flash(f'The Product {product.name} has been updated', 'success')
        return redirect(url_for('admin'))

    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.category.data = product.category_id  

    form.discription.data = product.desc

    return render_template(
    "updateproduct.html", title="Update Product", form=form, categories=categories, product=product
)





@app.route('/deleteproduct/<int:id>', methods=["GET", "POST"])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)

    if request.method == "POST":
        confirm_delete = request.form.get('confirm_delete')
        if confirm_delete == 'yes':
            db.session.delete(product)
            db.session.commit()
            flash(f'The product "{product.name}" is deleted successfully', 'success')
        return redirect(url_for('admin'))

    return render_template('delete_product.html', product=product)



