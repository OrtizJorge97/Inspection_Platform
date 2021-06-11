from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    title = db.Column(db.String(20), nullable=False)

class PurchaseOrdersTable(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    PurchaseOrder = db.Column(db.String(20), unique=True, nullable=False)
    Status = db.Column(db.String(20), unique=False, nullable=False)
    StatusTime = db.Column(db.String(20), unique=False, nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
    RequestDate = db.Column(db.String(20), nullable=False)
    StartDate = db.Column(db.String(20), nullable=False)
    EndDate = db.Column(db.String(20), nullable=False)
    ModifiedDate = db.Column(db.DateTime, nullable=False)
    FilePath = db.Column(db.String(100), unique=False, nullable=False)
    FileName = db.Column(db.String(30), unique=False, nullable=False)
    FileType = db.Column(db.String(30), unique=False, nullable=False)

class InspectionsTable(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    PartNumber = db.Column(db.String(50), unique=True, nullable=False)
    PurchaseOrder = db.Column(db.String(20), unique=False, nullable=False)
    Status = db.Column(db.String(20), unique=False, nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
    ModifiedDate = db.Column(db.DateTime, nullable=False)
    FilePath = db.Column(db.String(100), unique=False, nullable=False)
    FileName = db.Column(db.String(30), unique=False, nullable=False)
    Result = db.Column(db.String(30), unique=False, nullable=True)
    Comments = db.Column(db.String(200), unique=False, nullable=True)
    ResponsableName = db.Column(db.String(50), unique=False, nullable=True)

