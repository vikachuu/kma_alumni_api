from datetime import datetime
from app.main import db


class UpdateForm(db.Model):
    """Namings as in Odoo.
    """
    __tablename__ = "update_form"

    form_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    form_status = db.Column(db.String(100))

    name = db.Column(db.String(100))  # full name in ukrainian
    birth_date = db.Column(db.Date())
    image_1920 = db.Column(db.String(500000))  # Odoo saves image as base64 encoded string, f*cking large str
    # email = db.Column(db.String(100))  # Do not allow to update email here, because we use email for login

    contact_country = db.Column(db.String(100))  # selection field
    contact_city = db.Column(db.String(100))

    mobile = db.Column(db.String(15))
    skype = db.Column(db.String(100))
    telegram = db.Column(db.String(100))
    viber = db.Column(db.String(100))

    facebook_link = db.Column(db.String(100))
    linkedin_link = db.Column(db.String(100))

    diploma_naukma = db.Column(db.Boolean)

    bachelor_degree = db.Column(db.Boolean())
    bachelor_faculty = db.Column(db.String(100))  # selection field
    bachelor_speciality = db.Column(db.String(100))  # selection field
    bachelor_year_in = db.Column(db.String(100))  # selection field
    bachelor_year_out = db.Column(db.String(100))  # selection field

    master_degree = db.Column(db.Boolean())
    master_faculty = db.Column(db.String(100))  # selection field
    master_speciality = db.Column(db.String(100))  # selection field
    master_year_in = db.Column(db.String(100))  # selection field
    master_year_out = db.Column(db.String(100))  # selection field

    parent_id = db.Column(db.Integer)  # company id in Odoo, many2one field in Odoo
    company_name = db.Column(db.String(100))
    function = db.Column(db.String(100))  # job position

    # foreign keys
    alumni_id = db.Column(db.Integer, db.ForeignKey('alumni.alumni_id', onupdate="CASCADE",
                                                    ondelete="NO ACTION"), nullable=False)
    alumni = db.relationship("Alumni", back_populates="update_form")

    operator_id = db.Column(db.Integer, db.ForeignKey('operator.operator_id', onupdate="CASCADE",
                                                      ondelete="NO ACTION"), nullable=True)
    operator = db.relationship("Operator", back_populates="update_form")

    def __init__(self, name, birth_date, image_1920, contact_country, contact_city, mobile, skype,
                telegram, viber, facebook_link, linkedin_link, diploma_naukma, bachelor_degree, bachelor_faculty, bachelor_speciality,
                bachelor_year_in, bachelor_year_out, master_degree, master_faculty, master_speciality,
                master_year_in, master_year_out, parent_id, company_name, function, alumni_id, operator_id):

        self.form_status = 'new'  # TODO: create enum for the form statuses
        self.name = name
        self.birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
        self.image_1920 = image_1920
        
        self.contact_country = contact_country
        self.contact_city = contact_city
        
        self.mobile = mobile
        self.skype = skype
        self.telegram = telegram
        self.viber = viber
        self.facebook_link = facebook_link
        self.linkedin_link = linkedin_link

        self.diploma_naukma = diploma_naukma

        self.bachelor_degree = bachelor_degree
        self.bachelor_faculty = bachelor_faculty
        self.bachelor_speciality = bachelor_speciality
        self.bachelor_year_in = bachelor_year_in
        self.bachelor_year_out = bachelor_year_out

        self.master_degree = master_degree
        self.master_faculty = master_faculty
        self.master_speciality = master_speciality
        self.master_year_in = master_year_in
        self.master_year_out = master_year_out

        self.parent_id = parent_id
        self.company_name = company_name
        self.function = function

        self.alumni_id = alumni_id
        self.operator_id = operator_id


    def update(self, data):
        for key, item in data.items():
            if hasattr(self, key):
                setattr(self, key, item)
            db.session.commit()
