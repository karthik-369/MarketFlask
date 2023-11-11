from market import db, login_manager
from market import bcrypt 
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    userName = db.Column(db.String(length=30), nullable=False , unique=True)
    emailAddress = db.Column(db.String(length=100), nullable=False, unique=True)
    passwordHash = db.Column(db.String(length=50), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def budgetPret(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f"{self.budget}$"
        

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.passwordHash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.passwordHash, attempted_password) 

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=20), nullable=False, unique=True)
    description=db.Column(db.String(length=1024), nullable=False)  
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'