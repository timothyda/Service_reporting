from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app.models import customers


class Reporting:
    def __init__(self,db_data):
        self.id = db_data['id']
        self.customer_name = db_data['customer_name']
        self.machine_type = db_data['machine_type']
        self.case_number = db_data['case_number']
        self.fse_name = db_data['fse_name']
        self.l1_name = db_data['l1_name']
        self.l3_name = db_data['l3_name']
        self.serial_number = db_data['serial_number']
        self.date_reported = db_data['date_reported']
        self.description = db_data['description']
        self.updated_at = db_data['updated_at']
        self.created_at = db_data['created_at']
        self.creator = None


    @classmethod
    def save( cls,data ):
        query = """INSERT INTO reportings (customer_name,machine_type,case_number,fse_name,l1_name,l3_name,serial_number,date_reported,description,user_id) 
        VALUES (%(customer_name)s, %(machine_type)s, %(case_number)s, %(fse_name)s, %(l1_name)s, %(l3_name)s, %(serial_number)s, %(date_reported)s, %(description)s, %(user_id)s);"""
        return connectToMySQL('HP_Reporting').query_db(query,data)


    @classmethod
    def get_customer_with_reports(cls, name):
        query ="SELECT * FROM reportings WHERE customer_name = %(customer_name)s;"
        customer_reports_db = connectToMySQL('HP_Reporting').query_db(query , name)
        customer_reports = []
        for report in customer_reports_db:
            customer_reports.append(cls(report))
        return customer_reports


    @classmethod
    def get_one_with_name(cls, id):
        query = "SELECT * FROM reportings LEFT JOIN users ON reportings.user_id = users.id WHERE reportings.id = %(id)s;"
        reporting_from_db = connectToMySQL('HP_Reporting').query_db(query, {"id" : id})

        this_reporting = []
        if not reporting_from_db:
            return []
        
        for row in reporting_from_db:
            one_reporting = cls(row)
            
            creator_data = {
                "id" : row['id'],
                "user.id" : row['user_id'], 
                "first_name" : row['first_name'],
                "last_name": row['last_name'],
                "email" : row['email'],
                "password" : row['password'],
                "created_at" : row['users.created_at'],
                "updated_at" :row['users.updated_at']
            }
            this_creator = user.User(creator_data)
            one_reporting.creator = this_creator
            this_reporting.append(one_reporting)
        return this_reporting


    @classmethod
    def get_all_with_users(cls):
        query = "SELECT * FROM reportings LEFT JOIN users ON reportings.user_id = users.id;"
        results = connectToMySQL('HP_Reporting').query_db(query)
        
        all_reportings = []
        if not results:
            return []
        
        for row in results:
            one_reporting = cls(row)
            
            creator_data = {
                "id" : row['id'],
                "user.id" : row['user_id'], 
                "first_name" : row['first_name'],
                "last_name": row['last_name'],
                "email" : row['email'],
                "password" : row['password'],
                "created_at" : row['users.created_at'],
                "updated_at" :row['users.updated_at']
            }
            
            this_creator = user.User(creator_data)
            one_reporting.creator = this_creator
            all_reportings.append(one_reporting)
        return all_reportings


    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM reportings WHERE id = %(id)s;"
        return connectToMySQL('HP_Reporting').query_db(query,data)



    @classmethod
    def update(cls,data):
        query = "UPDATE reportings SET customer_name=%(customer_name)s, machine_type=%(machine_type)s, case_number=%(case_number)s, fse_name=%(fse_name)s, l1_name=%(l1_name)s, l3_name=%(l3_name)s, serial_number=%(serial_number)s, date_reported=%(date_reported)s, description=%(description)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('HP_Reporting').query_db(query,data)

