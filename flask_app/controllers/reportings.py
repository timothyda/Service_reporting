from flask import render_template,redirect,request,session, flash
from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)
from flask_app.models.user import User
from flask_app.models.reporting import Reporting
from flask_app.models.customers import Customer



"""starting page"""
@app.route('/')
def index():
    return render_template("index.html")


"""Start of log/reg validation"""

"""route to login"""
@app.route('/login_page')
def load_login():
    return render_template("login_page.html")


"""route to register"""
@app.route('/register_page')
def load_register():
    return render_template("register_page.html")


"""register user"""
@app.route('/register', methods=['POST'])
def create():
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name":request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash,
        "confirm_password" : request.form['confirm_password']
    }
    if not User.validate_user(request.form):
        return redirect('/register_page')
    
    if not request.form['password'] == request.form['confirm_password'] :
        flash("Password doesnt match")
        return redirect('/register_page')

    if not User.validate_registration(request.form):
        return redirect('/register_page')

    else :
        user_id = User.save(data)
        session['user_id'] = user_id
        return redirect('/dashboard')


"""log-in user"""
@app.route('/login', methods=['POST' , 'GET'])
def login():
    data= {
        "email": request.form['email']
    }
    user_in_db = User.login(data)
    if not user_in_db:
        flash("Invalid Email")
        return redirect("/login_page")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Password")
        return redirect("/login_page")
    
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')


"""log user out"""
@app.route('/logout')
def logout():
    session.pop("user_id" , 0)

    return redirect("/")

"""End of log/reg validation"""


"""customer list"""
@app.route('/dashboard')
def get_name():
    if "user_id" not in session:
        return redirect("/")  
    
    else:
        data = {
            'id' : session['user_id']
        }
        return render_template("customer_page.html" , user = User.get_one(data) , all_customers = Customer.get_customers())


"""add reporting"""
@app.route('/add_report')
def add_report():
    if "user_id" not in session:
        return redirect("/")  
    else:
        data = {
            'id' : session['user_id']
        }
        return render_template("add_report.html", user = User.get_one(data), all_customers = Customer.get_customers())


"""send report to DB"""
@app.route('/send_report', methods=['POST'])
def send_report():
    data = {
        "user_id" : session['user_id'],
        "customer_name" : request.form['customer_name'],
        "machine_type" : request.form['machine_type'],
        "case_number" : request.form['case_number'],
        "fse_name" : request.form['fse_name'],
        "l1_name" : request.form['l1_name'],
        "l3_name" : request.form['l3_name'],
        "serial_number" : request.form['serial_number'],
        "date_reported" : request.form['date_reported'],
        "description" : request.form['description']
    }
    Reporting.save(data)
    return redirect('/dashboard')


"""add customer"""
@app.route('/add_customer')
def add_customer():
    if "user_id" not in session:
        return redirect("/")
    else: 
        data = {
            'id' : session['user_id']
        }
        return render_template("add_customer.html", user = User.get_one(data))


"""send customer to DB"""
@app.route('/send_customer', methods=['POST'])
def send_customer():
    data = {
        "customer_name" : request.form['customer_name'],
        "address" : request.form['address'],
        "contact_name" : request.form['contact_name'],
        "contact_email" : request.form['contact_email'],
        "contact_phone" : request.form['contact_phone']
    }
    Customer.save_customer(data)
    return redirect('/dashboard')


"""customer report page"""
@app.route('/cust_page/<customer_name>')
def customer_reports(customer_name):
    if "user_id" not in session:
        return redirect("/")
    else: 
        data = {
            'id' : session['user_id']
        }
        name = {
            "customer_name" : customer_name
        }
        user = User.get_one(data)

        return render_template("reporting_list.html" , user = user , all_customer_reports = Reporting.get_customer_with_reports(name))

"""all reports page"""
@app.route('/all_reports')
def all_reports():
    if "user_id" not in session:
        return redirect("/")
    else: 
        data = {
            'id' : session['user_id']
        }
        user = User.get_one(data)
        return render_template("reporting_list.html" , user = user , all_customer_reports = Reporting.get_all_with_users())

"""report details"""
@app.route('/report_details/<int:report_id>')
def report_details(report_id):
    if "user_id" not in session:
        return redirect("/")
    else: 
        data = {
            'id' : session['user_id']
        }
        
        return render_template("report_detail.html", user=User.get_one(data), reportings = Reporting.get_one_with_name(report_id) )

"""delete report"""
@app.route('/delete/<int:report_id>')
def delete(report_id):
    data = {
        "id" : report_id
    } 
    Reporting.destroy(data)
    return redirect('/dashboard')

"""edit reporting"""
@app.route('/edit_report/<int:report_id>')
def edit_report(report_id):
    if "user_id" not in session:
        return redirect("/")
    else: 
        data = {
            'id' : session['user_id']
        }
        return render_template('edit_reporting.html', user=User.get_one(data), reportings = Reporting.get_one_with_name(report_id), all_customers = Customer.get_customers() )

"""update report"""
@app.route('/update/<int:report_id>', methods=['POST'])
def report_update(report_id ):
    data = {
    "id" : report_id,
    "user_id" : session['user_id'],
    "customer_name" : request.form['customer_name'],
    "machine_type" : request.form['machine_type'],
    "case_number" : request.form['case_number'],
    "fse_name" : request.form['fse_name'],
    "l1_name" : request.form['l1_name'],
    "l3_name" : request.form['l3_name'],
    "serial_number" : request.form['serial_number'],
    "date_reported" : request.form['date_reported'],
    "description" : request.form['description']
    }
    Reporting.update(data)
    return redirect('/dashboard')







