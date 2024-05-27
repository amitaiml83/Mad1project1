from groce import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(u_id):
    return User.query.get(int(u_id))


class User(db.Model, UserMixin):
    u_id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String)
    mobile_number = db.Column(db.String(10), unique = True)
    Email_id = db.Column(db.String)
    user_name = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, unique = True, nullable = False)
    carts = db.relationship('Addcart',backref = 'user')
    def get_id(self):
        return self.u_id

class Category(db.Model):
    c_id = db.Column(db.Integer, primary_key = True)
    c_name = db.Column(db.String, nullable = False, unique = True)
    products = db.relationship('Product', backref = "category")

class Product(db.Model):
    p_id = db.Column(db.Integer, primary_key = True)
    p_name = db.Column(db.String)
    unit = db.Column(db.String, nullable = False)
    rate = db.Column(db.Integer, nullable = False)
    quantity = db.Column(db.Integer)
    under_c_id = db.Column(db.Integer, db.ForeignKey("category.c_id"))
    carts = db.relationship('Addcart', backref ='cartproduct') 


class Manager(db.Model):
    m_id = db.Column(db.Integer, primary_key = True)
    m_name = db.Column(db.String)
    m_username = db.Column(db.String(15), nullable = False, unique = True)
    m_password = db.Column(db.String, nullable = False)

class Addcart(db.Model):
    cart_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.u_id"))
    product_id = db.Column(db.Integer, db.ForeignKey('product.p_id'))
    cart_quntity = db.Column(db.Integer, nullable = False)
    cart_price = db.Column(db.Integer, nullable = False)
    cart_total = db.Column(db.Integer, nullable = False)
    productn = db.Column(db.Integer, nullable = False)
    categoryn  = db.Column(db.Integer, nullable = False)




