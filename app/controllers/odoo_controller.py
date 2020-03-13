from app.main import odoo_db, odoo_uid, odoo_password, odoo_models


class OdooController:

    @staticmethod
    def get_odoo_contacts_by_filter_list(filter_list, offset, limit):
        contacts = odoo_models.execute_kw(odoo_db, odoo_uid, odoo_password, 'res.partner', 'search_read',
                [filter_list],
                {'fields': ['name', 'email', 'function', 'parent_id', 'facebook_link', 'linkedin_link', 'is_alumni',
                'bachelor_degree', 'bachelor_faculty', 'bachelor_speciality', 'bachelor_year_in', 'bachelor_year_out',
                'master_degree', 'master_faculty', 'master_speciality', 'master_year_in', 'master_year_out',
                'image_1920'],
                'offset': int(offset),
                'limit': int(limit)})
        return contacts

    @staticmethod
    def get_odoo_contacts_ids_by_filter_list(filter_list):
        odoo_contacts_ids = odoo_models.execute_kw(odoo_db, odoo_uid, odoo_password, 'res.partner',
                        'search',[filter_list])
        return odoo_contacts_ids

    @staticmethod
    def get_odoo_contact_with_groupmates_fields(filter_list):
        contacts = odoo_models.execute_kw(odoo_db, odoo_uid, odoo_password, 'res.partner', 'search_read',
                [filter_list],
                {'fields': ['bachelor_speciality', 'bachelor_year_in', 'master_speciality', 'master_year_in',],})
        return contacts

    @staticmethod
    def count_number_of_odoo_contacts_by_filter_list(filter_list):
        contacts_number = odoo_models.execute_kw(odoo_db, odoo_uid, odoo_password, 'res.partner', 'search_count',
                [filter_list])
        return contacts_number
