from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app.models import reporting

class Customer:
    def __init__(self,db_data):
        self.id = db_data['id']
        self.customer_name = db_data['customer_name']
        self.address = db_data['address']
        self.contact_name = db_data['contact_name']
        self.contact_email = db_data['contact_email']
        self.contact_phone = db_data['contact_phone']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.reporter = None
        self.reportings = None


    @classmethod
    def save_customer( cls,data ):
        query = """INSERT INTO customers (customer_name , address , contact_name , contact_email , contact_phone , created_at , updated_at)
        VALUES (%(customer_name)s, %(address)s, %(contact_name)s, %(contact_email)s, %(contact_phone)s, NOW(), NOW());"""
        print(data)
        return connectToMySQL('HP_Reporting').query_db(query,data)


    @classmethod
    def get_customers(cls):
        query = "SELECT * FROM customers;"
        customers_from_db = connectToMySQL('HP_Reporting').query_db(query)
        customers = []
        for customer in customers_from_db:
            customers.append(cls(customer))
        return customers
