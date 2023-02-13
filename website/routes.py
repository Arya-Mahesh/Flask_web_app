from website import app
from flask import render_template , redirect , url_for , flash , request
from website.models import Item , User , Item1
from website.forms import RegisterForm , LoginForm , PurchaseItemForm , AnotherPurchaseItemForm
from website import db
from flask_login import login_user ,logout_user , login_required

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/book', methods=['GET','POST'])
@login_required
def book():
    purchase_form = PurchaseItemForm()
    another_purchase_form = AnotherPurchaseItemForm()
    if purchase_form.validate_on_submit() or another_purchase_form.validate_on_submit():
        if another_purchase_form.validate_on_submit():
            print(request.form.get('another_purchased_item'))
            return redirect('/next')  
        if purchase_form.validate_on_submit():
            print(request.form.get('purchased_item'))
            return redirect('/next_page')
    items = Item.query.all()
    another_items = Item1.query.all()       
    return render_template('book.html', items=items, another_items=another_items,purchase_form=purchase_form, another_purchase_form=another_purchase_form)

@app.route('/next_page')
def next_page():
    return render_template("next_page.html")

@app.route('/next')
def next():
    return render_template("next.html")


@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                            email_address=form.email_address.data,
                            password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('book'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user:{err_msg}', category='danger')

    return render_template('register.html',form = form)


@app.route('/login', methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user=User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('book'))
        else:
            flash('Username and password are not match! Please try again', category='danger')
         
    return render_template('login.html',form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You are successfully logged out" ,category='info')
    return redirect(url_for('home_page'))



