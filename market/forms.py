from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User
class RegisterForm(FlaskForm):
    
    userName = StringField(label='User Name:', validators=[Length(2,50), DataRequired()])
    emailAddress = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:',validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:',validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


    
class LoginForm(FlaskForm):
    userName = StringField(label='User Name:', validators=[ DataRequired()])
    password = PasswordField(label='Password:',validators=[ DataRequired()])
    submit = SubmitField(label="Sign In")