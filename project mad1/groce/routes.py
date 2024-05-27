from flask import render_template,request,redirect
import os
from matplotlib import pyplot as plt
from groce import app
from groce.model import *
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/register', methods = ['GET', 'POST'])

def registrtion():

    if request.method == 'POST':
        first_name = request.form.get('f_name')
        last_name = request.form.get('l_name')
        Mob_number = request.form.get('mobile_number')
        email_id = request.form.get('Email')
        user_name = request.form.get('u_name')
        Password = request.form.get('password')
        add_user = User(first_name = first_name, last_name = last_name, mobile_number = Mob_number, Email_id = email_id, user_name = user_name, password = Password)
        db.session.add(add_user)
        db.session.commit()
        return render_template('firsttimereg.html')
    else:
        return render_template('register.html')

@app.route('/',methods = ["GET","POST"])

def userlogin():
    if request.method == 'POST':
        user_name = request.form.get('u_name')
        pass_word = request.form.get('p_word')
        
        user = User.query.filter_by(user_name = user_name).first()
        if user and user.password == pass_word:
            login_user(user, remember=True)
            return redirect('/user_dashboard')
        else:
            return render_template('userlogin.html', message = 'INVALID USERNAME OR PASSWORD')
    return render_template('userlogin.html')

#-------------------------------------------------------------------------------------------------------------------

@app.route('/user_dashboard')
@login_required
def userdashboard():
    category = Category.query.all()
    #user = User.query.all()
    return render_template('userhome.html', category = category, username =current_user.first_name)
#-------------------------------------------------------------------------------------------------------------------

@app.route('/buy/<int:p_id>/b', methods = ['GET','POST'])
@login_required
def user_buying(p_id):
    product = Product.query.get(p_id)
    carts = Addcart.query.filter_by(user_id = current_user.u_id, product_id = p_id).first()
    if request.method == 'POST':
        if carts:
            carts.cart_quntity = request.form['q_n']
            carts.cart_total = int(carts.cart_quntity) * (carts.cart_price)
        else:
            qn = request.form.get('q_n')
            pr = request.form.get('price')
            k = int(qn)*int(pr)
            pid = product.p_id
            pn = product.p_name
            cn = product.category.c_name
            add = Addcart(cart_quntity = qn, cart_price = pr, cart_total = k, product_id = pid, productn = pn, categoryn = cn, user_id= current_user.u_id)
            db.session.add(add)
        db.session.commit()
        return redirect('/cart')
    return render_template('user_buy.html', product=product, user_name = current_user.first_name)
    
#--------------------------------------------------------------------------------------------------------------------
@app.route('/cart')
@login_required
def cart_item():
    cart = Addcart.query.filter_by(user_id = current_user.u_id).all()
    sum = 0
    for s in cart:
        sum = sum +s.cart_total
    return render_template('cart_item.html', carts = cart, username = current_user.first_name, total = sum)

@app.route('/cart/<int:p_id>/c', methods = ['GET','POST'])
@login_required
def product_cart(p_id):
    product = Product.query.get(p_id)
    carts = Addcart.query.filter_by(user_id = current_user.u_id, product_id = p_id).first()
    if request.method == 'GET':
        if carts:
            return redirect('/cart')
        else:
            q = 1
            price = product.rate
            total = q*int(price)
            pid =product.p_id
            pn = product.p_name
            cn = product.category.c_name
            add = Addcart(cart_quntity = q, cart_price = price, cart_total = total, product_id = pid, productn = pn, categoryn = cn, user_id = current_user.u_id)
            db.session.add(add)
            db.session.commit()
            return redirect('/cart')
@app.route('/buy')
def thanks():
    cart = Addcart.query.filter_by(user_id = current_user.u_id).all()
    for item in cart:
        product = Product.query.get(item.product_id)
        if product and product.quantity >= item.cart_quntity:
            product.quantity -= item.cart_quntity
        db.session.delete(item)
    db.session.commit()
    return render_template('thanks.html')

@app.route('/cart/<int:cart_id>/delete')

def cart_delete(cart_id):
    c = Addcart.query.get(cart_id)
    if c:
        db.session.delete(c)
        db.session.commit()
    return redirect('/cart')

@app.route('/profile' ,methods = ["GET","POST"])
def user_profile():
    user = User.query.filter_by(u_id = current_user.u_id).first()
    if request.method == 'POST':
        user.first_name = request.form['f_name']
        user.last_name = request.form['l_name']
        user.Mob_number = request.form['mobile_number']
        user.email_id = request.form['Email']
        user.user_name = request.form['u_name']
        user.Password = request.form['password']
        db.session.commit()
        return redirect('/user_dashboard')

    return render_template('profile.html', user= user, username = current_user.first_name)

@app.route('/userlogout')

def userlogout():
    logout_user()
    return render_template('userlogin.html')

#------------------------------------------------This is for Admin --------------------------------------------------------------------------------------------------------------------

@app.route('/managerhome')
def managerhome():
    category = Category.query.all()
    manager = Manager.query.all()
    product = Product.query.all()
    if len(category)==0:
        return render_template('nocategory.html',m_name = manager[0].m_name)
    else:
        return render_template('managerhome.html', m_name = manager[0].m_name, category = category, products = product)

#-----------------------------------------------------------------------------------------------------------------------------------

@app.route('/managerlogin', methods = ['GET', 'POST'])

def managerlogin():
    manager= Manager.query.all()
    if request.method == 'POST':
        username = request.form.get('user_name')
        p_word = request.form.get('password')
        if username != manager[0].m_username:
            return render_template('managerlogin.html', message = 'INVALID USER ID')
        elif(manager[0].m_password != p_word):
            return render_template('managerlogin.html', message = 'INVALID PASSWORD')
        else:
            return redirect('/managerhome')
    return render_template('managerlogin.html')

#-----------------------------------------------------------------------------------------------------------------------------
@app.route('/addcategory', methods = ["GET", "POST"])

def create_category():
    manager = Manager.query.all()
    if request.method == 'POST':
        add_cat = request.form.get('c_n')
        add_cat = Category(c_name = add_cat)
        db.session.add(add_cat)
        db.session.commit()
        return redirect('/managerhome')
    return render_template('add_category.html', m_name =manager[0].m_name)

#------------------------------------------------------------------------------------------------------------------------------
@app.route('/category/<int:c_id>/edit', methods = ['GET','POST'])

def update_category(c_id):
    
    category = Category.query.get(c_id)
    manager = Manager.query.all()
    if request.method == 'POST':
        category.c_name = request.form['update_c']
        db.session.commit()
        return redirect('/managerhome')
    
    if request.method == 'GET':
        return render_template('editcategory.html', category_r = category, m_name = manager[0].m_name)
    
#---------------------------------------------------------------------------------------------------------------------
@app.route('/category/<int:c_id>/delete')

def delete_category(c_id):
    category = Category.query.get(c_id)
    if category:
        for p in category.products:
            db.session.delete(p)
            db.session.commit()
        db.session.delete(category)
        db.session.commit()
    return redirect('/managerhome')
#------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/addproduct', methods = ['GET','POST'])

def add_products():
    manager = Manager.query.all()
    category = Category.query.all()
    if request.method == 'POST':
        add_p_name = request.form.get('product_name')
        add_unit = request.form.get('u_nit')
        add_rate = request.form.get('rate_per_unit')
        add_quntity = request.form.get('q')
        add_cat = request.form.get('cup')
        p = Product(p_name = add_p_name, unit = add_unit, rate = add_rate, quantity = add_quntity, under_c_id = add_cat)
        db.session.add(p)
        db.session.commit()
        return redirect('/managerhome')
    
    elif request.method == 'GET':
        return render_template('add_product.html', m_name = manager[0].m_name, categoryes = category)

#-------------------------------------------------------------------------------------------------------------------

@app.route('/product/<int:p_id>/update', methods = ["GET","POST"])

def product_update(p_id):
    product = Product.query.get(p_id)
    manager = Manager.query.all()
    category = Category.query.all()
    if request.method == 'POST':
        product.p_name = request.form['product_name']
        product.unit = request.form['u_nit']
        product.rate = request.form['rate_per_unit']
        product.quantity = request.form['q']
        product.under_c_id = request.form['cup']
        db.session.commit()
        return redirect('/managerhome')
    elif request.method == 'GET':
        return render_template('editproduct.html', product = product, m_name = manager[0].m_name, categoryes = category)

#---------------------------------------------------------------------------------------------------------------------------------

@app.route('/product/<int:p_id>/delete')

def delete_product(p_id):
    product = Product.query.get(p_id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return redirect('/managerhome')
#----------------------------------------------------------------------------------------------------------------------------------

@app.route('/summary')

def summary():
    product = Product.query.all()
    cat = []
    qun = []
    for p in product:
        cat.append(p.category.c_name)
        qun.append(p.quantity)
    fig = plt.figure(figsize=(10,5))
    plt.pie(cat,float(qun))
    #plt.xlabel("category")
    #plt.ylabel("quantity")
    plt.axis('equal')
    static_folder = os.path.join(app.root_path, 'static')
    #print(static_folder)
    plot_filename = os.path.join(static_folder, 'my_plot.png')
    plt.savefig(plot_filename)

    #fig.savefig('static/my_plot.png')
    return render_template('summary.html', bargraph = 'my_plot')
    
@app.route('/logout')
def logout():
    return render_template('managerlogin.html')

