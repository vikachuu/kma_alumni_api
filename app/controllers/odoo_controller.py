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

    def get_odoo_countries():
        try:
            from app.main import odoo_db, odoo_uid, odoo_password, odoo_models
            companies = odoo_models.execute_kw(odoo_db, odoo_uid, odoo_password, 'res.country', 'search_read',
                    [],
                    {'fields': ['name'],})
        except ConnectionRefusedError as err:
            raise OdooIsDeadError(err)
        except xmlrpc.cl1ient.ProtocolError as err:
            raise OdooIsDeadError(err)
        return companies

    @staticmethod
    def update_odoo_contact(odoo_contact_id, post_data):
        try:
            update_data = {
                'name': post_data.get('full_name_uk'),
                'birth_date': post_data.get('date_of_birth'),
                'image_1920': post_data.get('image', ''), # binary type
                'email': post_data.get('email'),

                'contact_country': post_data.get('country', ''),
                'contact_city': post_data.get('city', ''),

                'mobile': post_data.get('mobile', ''),
                'skype': post_data.get('skype', ''),
                'telegram': post_data.get('telegram', ''),
                'viber': post_data.get('viber', ''),
                'facebook_link': post_data.get('facebook', ''),
                'linkedin_link': post_data.get('linkedin', ''),

                'bachelor_degree': post_data.get('is_bachelor', False),
                'show_bachelor': post_data.get('is_bachelor', False),
                'bachelor_faculty': post_data.get('bachelor_faculty', ''), 
                'bachelor_speciality': post_data.get('bachelor_speciality', ''),
                'bachelor_year_in': post_data.get('bachelor_entry_year', ''),
                'bachelor_year_out': post_data.get('bachelor_finish_year', ''),

                'master_degree': post_data.get('is_master', False),
                'show_master': post_data.get('is_master', False),
                'master_faculty': post_data.get('master_faculty', ''),
                'master_speciality': post_data.get('master_speciality', ''),
                'master_year_in': post_data.get('master_entry_year', ''),
                'master_year_out': post_data.get('master_finish_year', ''),

                'function': post_data.get('job_position', '')
            }
            company_id = post_data.get('company_id')
            update_data.update({'parent_id': company_id}) if company_id is not None else None

            from app.main import odoo_db, odoo_uid, odoo_password, odoo_models
            odoo_models.execute_kw(odoo_db, odoo_uid, odoo_password, 'res.partner', 'write',
                                    [[odoo_contact_id], update_data])
        except ConnectionRefusedError as err:
            raise OdooIsDeadError(err)
        except xmlrpc.cl1ient.ProtocolError as err:
            raise OdooIsDeadError(err)
