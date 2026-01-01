
from flask import Flask, render_template, request
import psycopg2
from datetime import datetime
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)

def save_db(category, name, total_employees, employees_with_npl, nationality,
            email, phone, sector, facility_to_submit, facility_to_make,
            facility_to_monitor, electronic_calibration, facility_to_check,machine_readable_data, challenges, comments):
    print("Saving to DB:", category, name, total_employees, employees_with_npl, nationality,
        email, phone, sector, facility_to_submit, facility_to_make,
        facility_to_monitor, electronic_calibration, facility_to_check, machine_readable_data, challenges, comments)

    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            dbname="cfct_db",
            user="postgres",
            password="aarti",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO customer_form (
                category, name, total_employees, employees_with_npl, nationality,
                email, phone, sector, facility_to_submit, facility_to_make,
                facility_to_monitor, electronic_calibration, facility_to_check, machine_readable_data, challenges, comments, submit_date&Time
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
           
        """

        values = (
            category, name, total_employees, employees_with_npl, nationality,
            email, phone, sector, facility_to_submit, facility_to_make,
            facility_to_monitor, electronic_calibration, facility_to_check, machine_readable_data,
            # challenges, comments, datetime.now().strftime("%Y-%m-%d")
             challenges, comments, datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        )
        cursor.execute(insert_query, values)
        conn.commit()
        cursor.close()
        conn.close()
        print("Record saved in npl_new_db")

    except Exception as error:
        print("Error while saving to DB:", error)


# @app.route("/submit", methods=['POST'])
@app.route("/submit", methods=['GET', 'POST'])

def submit():
    print(" SUBMIT route reached")
    print("Form data received:", request.form)
    try:
        category = request.form.get("category")
        if category == "ANY":
            other_category = request.form.get("other_category")
            if other_category:
                category = other_category

        name = request.form.get("name")
        total_employees = int(request.form.get("total_employees"))
        employees_with_npl = int(request.form.get("employees_with_npl"))
        nationality = request.form.get("nationality")
        email = request.form.get("email")
        phone = request.form.get("phone")
        sector = request.form.get("sector")
        if sector == "Other":
            other_sector = request.form.get("other_sector")
            if other_sector:
                sector = other_sector

        facility_to_submit = request.form.get("facility_to_submit")
        facility_to_make = request.form.get("facility_to_make")
        facility_to_monitor = request.form.get("facility_to_monitor")
        electronic_calibration = request.form.get("electronic_calibration")
        facility_to_check = request.form.get("facility_to_check")
        machine_readable_data = request.form.get("machine_readable_data")
        challenges = request.form.get("challanges")   # note spelling in form
        comments = request.form.get("any")

        # Save into DB
        save_db(category, name, total_employees, employees_with_npl, nationality,
                email, phone, sector, facility_to_submit, facility_to_make,
                facility_to_monitor, electronic_calibration, facility_to_check, machine_readable_data, 
                challenges, comments)

        return render_template('response.html')

    except Exception as e:
        print("Error:", e)
        return f"Error while submitting: {e}"


@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


# # Mount app under /cfcsir so routes become /cfcsir/, /cfcsir/submit etc.
# application = DispatcherMiddleware(Flask('dummy_root'), {
#     '/cfcsir': app
# })


if __name__ == '__main__':
    app.run(debug=True)