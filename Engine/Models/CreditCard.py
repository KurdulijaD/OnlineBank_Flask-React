from Configuration.config import db
from marshmallow import Schema, fields
from datetime import datetime

class CreditCard(db.Model):
    __tablename__ = 'credit_card'
    cardNumber = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(32))
    expirationDate = db.Column(db.DateTime, default = datetime.utcnow)
    cvc = db.Column(db.Integer)
    userEmail = db.Column(db.String(64))


    def __init__(self, cardNumber, userName, expirationDate, cvc, userEmail):
        self.cardNumber = cardNumber
        self.userName = userName
        self.expirationDate = expirationDate
        self.cvc = cvc
        self.userEmail = userEmail

class CreditCardSchema(Schema):
    cardNumber = fields.Number()
    name = fields.Str()
    expirationDate = fields.Str()
    cvc = fields.Number()
    userEmail = fields.Str()