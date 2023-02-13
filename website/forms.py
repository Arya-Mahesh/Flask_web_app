from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField , SubmitField 
from wtforms.validators import Length , EqualTo , Email , DataRequired , ValidationError
from website.models import User

class RegisterForm(FlaskForm):
    
    def validate_username(self,username_to_check):
        user=User.query.filter_by(username=username_to_check.data).first()                  
        if user:
            raise ValidationError('user already exists!')

    def validate_email_address(self,email_address_to_check):
        user=User.query.filter_by(email_address=email_address_to_check.data).first()
        if user:
            raise ValidationError('Email already exists!')

    username = StringField(label='Username: ', validators=[Length(min=2,max=30), DataRequired()])
    email_address = StringField(label='Email Address: ', validators=[Email(),  DataRequired()])
    password1 = PasswordField(label='Password: ', validators=[Length(min=8),  DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'),  DataRequired()])
    submit = SubmitField(label='Create Account')
    
class LoginForm(FlaskForm):
    username = StringField(label='Username: ', validators=[DataRequired()])
    password = PasswordField(label='Password: ', validators=[ DataRequired()])
    submit = SubmitField(label='Sign in')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Buy Book')

class AnotherPurchaseItemForm(FlaskForm):
    another_purchased_item = StringField('another_purchased_item', validators=[DataRequired()])
    submit = SubmitField(label='Free Download')

