import xmlrpc.client

from app.utils.exceptions import OdooIsDeadError


class OdooController:
    """
    Each method has catch for ConnectionRefusedError and ProtocolError in case Odoo is down.
    Import `odoo_db, odoo_uid, odoo_password, odoo_models` should be inside `try-except` block in 
    order to catch the error.
    If error is catch OdooIsDeadError raises.
    """

    @staticmethod
    def get_odoo_contacts_by_filter_list(filter_list, offset, limit):
        try:
            from app.main import odoo_db, odoo_uid, odoo_password, odoo_models
            contacts = odoo_models.execute_kw(odoo_db, odoo_uid, odoo_password, 'res.partner', 'search_read',
                    [filter_list],
                    {'fields': ['name', 'email', 'function', 'parent_id', 'facebook_link', 'linkedin_link', 'is_alumni',
                    'bachelor_degree', 'bachelor_faculty', 'bachelor_speciality', 'bachelor_year_in', 'bachelor_year_out',
                    'master_degree', 'master_faculty', 'master_speciality', 'master_year_in', 'master_year_out',
                    'image_1920'],
                    'offset': int(offset),
                    'limit': int(limit)})
        except ConnectionRefusedError as err:
            raise OdooIsDeadError(err)
        except xmlrpc.cl1ient.ProtocolError as err:
            raise OdooIsDeadError(err)
        return contacts

    @staticmethod
    def get_odoo_contacts_ids_by_filter_list(filter_list):
        try:
            from app.main import odoo_db, odoo_uid, odoo_password, odoo_models
            odoo_contacts_ids = odoo_models.execute_kw(odoo_db, odoo_uid, odoo_password, 'res.partner',
                            'search',[filter_list])
        except ConnectionRefusedError as err:
            raise OdooIsDeadError(err)
        except xmlrpc.cl1ient.ProtocolError as err:
            raise OdooIsDeadError(err)
        return odoo_contacts_ids

    @staticmethod
    def get_odoo_contact_with_groupmates_fields(filter_list):
        try:
            from app.main import odoo_db, odoo_uid, odoo_password, odoo_models
            contacts = odoo_models.execute_kw(odoo_db, odoo_uid, odoo_password, 'res.partner', 'search_read',
                        [filter_list],
                        {'fields': ['bachelor_speciality', 'bachelor_year_in', 'master_speciality', 'master_year_in',],})
        except ConnectionRefusedError as err:
            raise OdooIsDeadError(err)
        except xmlrpc.cl1ient.ProtocolError as err:
            raise OdooIsDeadError(err)
        return contacts

    @staticmethod
    def count_number_of_odoo_contacts_by_filter_list(filter_list):
        try:
            from app.main import odoo_db, odoo_uid, odoo_password, odoo_models
            contacts_number = odoo_models.execute_kw(odoo_db, odoo_uid, odoo_password, 'res.partner', 'search_count',
                    [filter_list])
        except ConnectionRefusedError as err:
            raise OdooIsDeadError(err)
        except xmlrpc.cl1ient.ProtocolError as err:
            raise OdooIsDeadError(err)
        return contacts_number

    @staticmethod
    def get_odoo_companies():
        try:
            from app.main import odoo_db, odoo_uid, odoo_password, odoo_models
            companies = odoo_models.execute_kw(odoo_db, odoo_uid, odoo_password, 'res.partner', 'search_read',
                    [[['is_company', '=', True]]],
                    {'fields': ['name'],})
        except ConnectionRefusedError as err:
            raise OdooIsDeadError(err)
        except xmlrpc.cl1ient.ProtocolError as err:
            raise OdooIsDeadError(err)
        return companies
