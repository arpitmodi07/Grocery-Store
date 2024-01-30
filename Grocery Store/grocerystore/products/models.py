from grocerystore import db

class Addproduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    unit = db.Column(db.String, nullable=False)
    manufacturing = db.Column(db.Date,nullable=False)
    
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, default=0)
    desc = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def __repr__(self):
        return f"Addproduct('{self.name}', '{self.price}', '{self.stock}',{self.category_id}')"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    products = db.relationship('Addproduct', backref='products_category', lazy=True)

    def __repr__(self):
        return f"Category('{self.name}')"
