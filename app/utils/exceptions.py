class OdooIsDeadError(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"Connection error - Odoo is dead. {self.message}"
