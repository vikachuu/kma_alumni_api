from datetime import datetime

from app.main import db
from app.models.alumni_invite_status_model import AlumniInviteStatus


class AlumniInviteStatusController:

    @staticmethod
    def get_all_records():
        records = AlumniInviteStatus.query.all()
        records_list = []
        for record in records:
            records_list.append({"odoo_contact_id": record.odoo_contact_id,
                                "invite_status": record.invite_status,
                                "status_set_date": record.status_set_date.strftime('%Y-%m-%d')})
        return {"data": {
                        "records": records_list,
                        },
                "status": 200,
                "error": None
                } 

    @staticmethod
    def create_invite_status_record(post_data):
        # check if record already exists
        record = AlumniInviteStatus.query.filter_by(odoo_contact_id=post_data.get('odoo_contact_id')).first()
        if not record:
            record = AlumniInviteStatus(
                odoo_contact_id=post_data.get('odoo_contact_id'),
                invite_status=post_data.get('invite_status'),
            )

            # insert the user
            db.session.add(record)
            db.session.commit()

            return {"data": {
                        "record": {
                            "odoo_contact_id": record.odoo_contact_id,
                            "invite_status": record.invite_status,
                            "status_set_date": record.status_set_date.strftime('%Y-%m-%d'),
                        }},
                    "status": 201,
                    "error": None
                    }
        else:
            return {"data": {
                        "record": {
                            "odoo_contact_id": record.odoo_contact_id,
                            "invite_status": record.invite_status,
                            "status_set_date": record.status_set_date.strftime('%Y-%m-%d'),
                        }},
                    "status": 200,
                    "error": f"Record already exists."
                    }

    @staticmethod
    def update_invite_status_record(put_data):
        record = AlumniInviteStatus.query.filter_by(odoo_contact_id=put_data.get('odoo_contact_id')).first()
        # if not exists - create new
        if record is not None:
            record.invite_status = put_data.get('invite_status')
            record.status_set_date = datetime.now().date()
            db.session.commit()

            return {"data": None,
                    "status": 200,
                    "error": None
                }
        else:
            record = AlumniInviteStatus(
                odoo_contact_id=put_data.get('odoo_contact_id'),
                invite_status=put_data.get('invite_status'),
            )

            # insert the user
            db.session.add(record)
            db.session.commit()

            return {"data": None,
                    "status": 201,
                    "error": None
                }
