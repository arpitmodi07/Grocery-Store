from wtforms import IntegerField, StringField, TextAreaField, validators, Form, DecimalField,SelectField,DateField
from wtforms.validators import InputRequired
class Addproducts(Form):
    name = StringField('Name',[validators.DataRequired()])
    price = DecimalField('Price',[validators.DataRequired()])
    unit = SelectField('Unit', choices=[('kg', 'Rs/kg'), ('litre', 'Rs/litre'), ('gram', 'Rs/gram'),('packet','Rs/packet'),('piece','Rs/piece')], validators=[InputRequired()])
    manufacturing_date = DateField('Manufacturing Date', format='%Y-%m-%d', validators=[InputRequired()])

    discount = IntegerField('Discount',default=0)
    stock = IntegerField('Stock',[validators.DataRequired()])
    discription = TextAreaField('Discription',[validators.DataRequired()])
    
class UpdateProduct(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = DecimalField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', [validators.DataRequired()])
    discription = TextAreaField('Discription', [validators.DataRequired()])
    category = SelectField('Category', coerce=int) 