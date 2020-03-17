from datetime import datetime

from app.main import db
from app.models.alumni_invite_status_model import AlumniInviteStatus


class AlumniInviteStatusController:

    @staticmethod
    def get_id_status_records_dict():
        records = AlumniInviteStatus.query.all()
        records_dict = {}
        for record in records:
            records_dict[record.odoo_contact_id] = record.invite_status
        return records_dict

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

            return {
                "odoo_contact_id": record.odoo_contact_id,
                "invite_status": record.invite_status,
                "status_set_date": record.status_set_date.strftime('%Y-%m-%d'),
                }, 201
        else:
            return {
                "error_id": "invite_status_record_exists_error",
                "message": "Conflict: Record already exists."
                }, 409

    @staticmethod
    def update_invite_status_record(put_data):
        record = AlumniInviteStatus.query.filter_by(odoo_contact_id=put_data.get('odoo_contact_id')).first()
        # if not exists - create new
        if record is not None:
            record.invite_status = put_data.get('invite_status')
            record.status_set_date = datetime.now().date()
            db.session.add(record)
            db.session.commit()

            return {
                "message": "Record status successfully updated.",
                }, 200
        else:
            record = AlumniInviteStatus(
                odoo_contact_id=put_data.get('odoo_contact_id'),
                invite_status=put_data.get('invite_status'),
            )

            # insert the user
            db.session.add(record)
            db.session.commit()

            return {
                "message": "New record created.",
                }, 201

    @staticmethod
    def delete_invite_status_record(odoo_contact_id):
        record = AlumniInviteStatus.query.filter_by(odoo_contact_id=odoo_contact_id).first()
        if record is not None:
            db.session.delete(record)
            db.session.commit()

            return {
                "message": "Record successfully deleted.",
                }, 200
        else:
            return {
                "error_id": "invite_status_record_not_found_error",
                "message": "Cannot delete: Record not found.",
                }, 404
