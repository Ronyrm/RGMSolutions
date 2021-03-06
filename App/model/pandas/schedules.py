from App import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import  Integer,String,Column


class Schedules(db.Model):
    __tablename__ = 'schedules'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    first_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    title = db.Column(db.String(50))
    suffix = db.Column(db.String(50))
    initials = db.Column(db.String(50))
    webpage = db.Column(db.String(50))
    gender = db.Column(db.String(1))
    birthyday = db.Column(db.Date)
    anniversay = db.Column(db.DateTime)
    location = db.Column(db.String(50))
    language = db.Column(db.String(20))
    internet_free_busy = db.Column(db.String(200))
    notes = db.Column(db.String(50))
    email_address_one = db.Column(db.String(50))
    email_address_two = db.Column(db.String(50))
    email_address_tree = db.Column(db.String(50))
    primary_phone = db.Column(db.String(20))
    home_phone_one = db.Column(db.String(20))
    home_phone_two = db.Column(db.String(20))
    mobile_phone = db.Column(db.String(20))
    company_main_phone = db.Column(db.String(20))
    company_business_phone_one = db.Column(db.String(20))
    company_business_phone_two = db.Column(db.String(20))
    assistents_phone = db.Column(db.String(50))
    company = db.Column(db.String(50))
    job_title = db.Column(db.String(50))
    departament = db.Column(db.String(50))
    ofice_location = db.Column(db.String(50))
    profission = db.Column(db.String(50))
    account = db.Column(db.String(200))
    business_address = db.Column(db.String(50))
    business_street_one = db.Column(db.String(50))
    business_street_two = db.Column(db.String(50))
    business_street_tree = db.Column(db.String(50))
    business_address_po_box = db.Column(db.String(50))
    business_city = db.Column(db.String(50))
    business_states = db.Column(db.String(50))
    business_code_postal = db.Column(db.String(50))
    business_country = db.Column(db.String(50))
    outher_phone = db.Column(db.String(50))
    idcidade = db.Column(db.Integer,db.ForeignKey('cidades.id'))
    cidade = db.relationship("Cidades")