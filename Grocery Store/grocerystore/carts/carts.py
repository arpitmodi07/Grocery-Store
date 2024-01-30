from flask import render_template,session, request,redirect,url_for,flash
from grocerystore import app
from grocerystore.products.models import Addproduct


def MergeDicts(dict1,dict2):
    if isinstance(dict1, list) and isinstance(dict2,list):
        return dict1  + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))

@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
       
        product = Addproduct.query.filter_by(id=product_id).first()

        if request.method =="POST":
            DictItems = {product_id:{'name':product.name,'price':float(product.price),'discount':product.discount,'quantity':quantity}}
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                else:
                    session['Shoppingcart'] = MergeDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
              
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)
    





@app.route('/carts')
def getCart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart'])<=0:
        return redirect(url_for('home'))
    grandtotal = 0
    for key, product in session['Shoppingcart'].items():
        discount = (product['discount']/100)*float(product['price'])*(product['quantity'])
        grandtotal+= float(product['price'])*int(product['quantity'])
        grandtotal-=discount
        
    return render_template('carts.html',grandtotal=grandtotal)






@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    
    if request.method =="POST":
        product = Addproduct.query.get_or_404(code)
        quantity = int(request.form.get('quantity'))
        if quantity <= product.stock:
            try:
                session.modified = True
                for key , item in session['Shoppingcart'].items():
                    if int(key) == code:
                        item['quantity'] = quantity
                        
                        flash(f'The item {product.name} is update successfully','success')
                        return redirect(url_for('getCart'))
            except Exception as e:
                print(e)
                flash('Something went wrong while updating the cart.', 'danger')
        else:
            flash(f'The requested quantity should be less than or equal to {product.stock}', 'danger')
        
        return redirect(url_for('getCart'))





@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session and len(session['Shoppingcart'])<=0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key,item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key,None)
                return redirect(url_for('getCart'))
        
    except Exception as e:
        print(e)
        return redirect(url_for('getcart'))
    

@app.route('/clearcart')
def clearcart():
    try:
        session.pop('Shoppingcart',None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)