from flask import Flask, render_template, jsonify, redirect, request, send_file
from fpdf import FPDF
import os
import base64
import json
import datetime

from pymongo import MongoClient

online = True
password = "password"
username = "username"
localURL = 'localURL'
onlineURL = f'onlineURL'


CLIENT = MongoClient(onlineURL if online else localURL)
DATA_BASE = CLIENT['form']
RECORDS = DATA_BASE['records']


# template_dir = os.path.abspath('../../frontend/src')
# app = Flask(__name__, template_folder=template_dir)
app = Flask(__name__)


json_file = 'student_records.json'  # JSON file to store records


student_records = []  # List to store submitted


def generate_pdf(records):
    # Create PDF object
    pdf = FPDF()
    pdf.add_page()

    # Set font and font size
    pdf.set_font('Arial', 'B', 12)

    # Add table header
    header = ['Full Name', 'Phone', 'Student Card ID', 'Signature']
    for item in header:
        pdf.cell(40, 10, item, border=1)
    pdf.ln()

    i = 0
    signature_paths = []

    # Add table rows from records list
    for record in records:
        for key, value in record.items():
            if key == 'Signature':
                # Save signature image to file
                signature_image = value
                signature_data = signature_image.replace(
                    'data:image/png;base64,', '')
                signature_path = f'signature{i}.png'

                try:

                    with open(signature_path, 'wb') as file:
                        file.write(base64.b64decode(signature_data))

                    # Draw border around signature image
                    pdf.set_draw_color(0, 0, 0)  # Set border color (black)
                    # pdf.rect( w=40, h=10)  # Draw rectangle as border
                    # Draw rectangle as border
                    pdf.rect(x=pdf.x, y=pdf.y, w=40, h=10)
                    pdf.image(signature_path, w=40, h=10)
                    signature_paths.append(signature_path)
                    # pdf.image(item, x=10, y=pdf.y, w=40)
                except:
                    pass

            else:
                pdf.cell(40, 10, str(value), border=1)
        i += 1
        pdf.ln(h=0)

    # Save PDF file
    pdf_file = 'students_info.pdf'
    pdf.output(pdf_file)
    for img in signature_paths:
        # Remove the signature image file
        os.remove(img)

    return pdf_file

@app.route('/')
def index():
    return render_template('form.html', details=details)


@app.route('/submit', methods=['POST'])
def submit():
    global student_records
    # Retrieve form inputs
    first_name = request.form['first_name']
    family_name = request.form['family_name']
    room = request.form['room']
    full_name = first_name + " " + family_name
    phone = "00000000000"
    student_card_id = request.form['student_card_id']
    signature_image = request.form['signature']
    # Create dictionary for new record
    new_record = {
        'Full Name': full_name,
        'Phone': phone,
        "Room": room,
        'Student Card ID': student_card_id,
        'Signature': signature_image
    }

    # Append record to student_records list
    student_records.append(new_record)
    cp = new_record.copy()
    print(cp)
    RECORDS.insert_one(cp)

    # Load existing records from JSON file
    existing_records = []
    try:
        with open(json_file, 'r') as file:
            existing_records = json.load(file)
    except FileNotFoundError:
        pass

    # Append new record to existing records
    existing_records.append(new_record)

    # Write updated records to JSON file
    temp_name = datetime.datetime.now().strftime('%Y_%m_%d_%H-%M-%S.%f')
    temp_file = "new/new_"+ full_name[:8]  + "_"+temp_name + ".json"  # or whatever extension is needed
    with open(temp_file, "w") as f:
        json.dump(existing_records, f, indent=4)
    
    return redirect("/submitted")


@app.route('/submitted')
def submitted():
    return render_template('submitted.html')


@app.route('/pdf')
def pdf():
    json_file=""
    existing_records = []
    try:
        with open(json_file, 'r') as file:
            existing_records = json.load(file)
    except FileNotFoundError:
        pass

    pdf_file = generate_pdf(existing_records)
    return send_file(pdf_file, as_attachment=False)


@app.route('/edit/<code>')
def edit(code):
    code = "9999"
    json_file=""
    existing_records = []
    try:
        with open(json_file, 'r') as file:
            existing_records = json.load(file)
    except FileNotFoundError:
        pass

    pdf_file = generate_pdf(existing_records)
    return send_file(pdf_file, as_attachment=False)



@app.route('/records')
def records():
    all_recs = list(RECORDS.find({}))

    for a in all_recs:
        a.pop('_id')
    admin = False

    existing_records = all_recs
    return render_template('pdf.html', records=existing_records, length=len(existing_records), details=details['this'], admin=admin)

# Custom Jinja2 filter to enumerate records
@app.template_filter('enumerate_records')
def enumerate_records(records):
    return list(enumerate(records))

@app.route('/records/<code>', methods=['GET', 'POST'])
def records_admin(code):
    admin = code == "9999"
    backup = code == "backup9"
    print(admin)

    all_recs = list(RECORDS.find({}))

    for a in all_recs:
        a.pop('_id')

    existing_records = all_recs

    if admin:
        if request.method == 'POST':
            record_index = int(request.form['delete'])
            del existing_records[record_index]
            print("len", len(existing_records))
        return render_template('pdf.html', records=existing_records, length=len(existing_records), details=details['this'], admin=True)
    elif backup:
        try:
            temp_name = datetime.datetime.now().strftime('%Y_%m_%d_%H-%M-%S.%f')
            temp_file = "backup/backup_"+temp_name + ".json"  # or whatever extension is needed
            with open(temp_file, "w") as f:
                json.dump(existing_records, f, indent=4)

            return send_file(temp_file, as_attachment=True)
        except FileNotFoundError:
            return redirect("/records")

            pass
    else:
        # return render_template('pdf.html', records=existing_records, length=len(existing_records), details=details['this'], admin=admin)
        return redirect("/records")


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    existing_records = []
    if request.method == 'POST':
        file = request.files['json_file']
        if file.filename.endswith('.json'):
            existing_records = json.load(file)
            return render_template('pdf.html', records=existing_records, length=len(existing_records), details=details['this'], admin=True)
            return jsonify(existing_records)
        
        
    return render_template('upload.html', records=existing_records, length=len(existing_records), details=details['this'], admin=True)
    
    return render_template('upload.html')


@app.route('/save')
def save():
    
    all_recs = list(RECORDS.find({}))

    for a in all_recs:
        a.pop('_id')

    existing_records = all_recs
    try:
        temp_name = datetime.datetime.now().strftime('%Y_%m_%d_%H-%M-%S.%f')
        temp_file = "backup/backup_"+temp_name + ".json"  # or whatever extension is needed
        with open(temp_file, "w") as f:
            json.dump(existing_records, f, indent=4)

        return send_file(temp_file, as_attachment=True)
    except FileNotFoundError:
        pass



if __name__ == '__main__':
    app.run(debug=True)
