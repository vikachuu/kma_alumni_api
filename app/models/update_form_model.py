from datetime import datetime
from app.main import db


class UpdateForm(db.Model):
    __tablename__ = "update_form"

    form_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    form_status = db.Column(db.String(100))

    full_name_uk = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date())
    image = db.Column(db.String(10000))
    email = db.Column(db.String(100))

    country = db.Column(db.String(100))  # selection field
    city = db.Column(db.String(100))

    mobile = db.Column(db.String(15))
    skype = db.Column(db.String(100))
    telegram = db.Column(db.String(100))
    viber = db.Column(db.String(100))

    facebook = db.Column(db.String(100))
    linkedin = db.Column(db.String(100))

    is_bachelor = db.Column(db.Boolean())
    bachelor_faculty = db.Column(db.String(100))  # selection field
    bachelor_speciality = db.Column(db.String(100))  # selection field
    bachelor_entry_year = db.Column(db.String(100))  # selection field
    bachelor_finish_year = db.Column(db.String(100))  # selection field

    is_master = db.Column(db.Boolean())
    master_faculty = db.Column(db.String(100))  # selection field
    master_speciality = db.Column(db.String(100))  # selection field
    master_entry_year = db.Column(db.String(100))  # selection field
    master_finish_year = db.Column(db.String(100))  # selection field

    company = db.Column(db.String(100))  # many2one field, tag when create new
    job_position = db.Column(db.String(100))

    # foreign keys
    alumni_id = db.Column(db.Integer, db.ForeignKey('alumni.alumni_id', onupdate="CASCADE",
                                                    ondelete="NO ACTION"), nullable=False)
    alumni = db.relationship("Alumni", back_populates="update_form")

    operator_id = db.Column(db.Integer, db.ForeignKey('operator.operator_id', onupdate="CASCADE",
                                                      ondelete="NO ACTION"), nullable=True)
    operator = db.relationship("Operator", back_populates="update_form")

    def __init__(self, full_name_uk, date_of_birth, image, email, country, city, mobile, skype,
                telegram, viber, facebook, linkedin, is_bachelor, bachelor_faculty, bachelor_speciality,
                bachelor_entry_year, bachelor_finish_year, is_master, master_faculty, master_speciality,
                master_entry_year, master_finish_year, company, job_position, alumni_id, operator_id):

        self.form_status = 'new'
        self.full_name_uk = full_name_uk
        self.date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        self.image = image
        self.email = email
        
        self.country = country
        self.city = city
        self.mobile = mobile
        self.skype = skype
        self.telegram = telegram
        self.viber = viber
        self.facebook = facebook
        self.linkedin = linkedin

        self.is_bachelor = is_bachelor
        self.bachelor_faculty = bachelor_faculty
        self.bachelor_speciality = bachelor_speciality
        self.bachelor_entry_year = bachelor_entry_year
        self.bachelor_finish_year = bachelor_finish_year

        self.is_master = is_master
        self.master_faculty = master_faculty
        self.master_speciality = master_speciality
        self.master_entry_year = master_entry_year
        self.master_finish_year = master_finish_year

        self.company = company
        self.job_position = job_position

        self.alumni_id = alumni_id
        self.operator_id = operator_id

#     diploma_naukma = 
#     phone = 
#     name_en = 
#     address = 
