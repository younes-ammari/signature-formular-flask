from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import os
import base64
import json


# template_dir = os.path.abspath('../../frontend/src')
# app = Flask(__name__, template_folder=template_dir)
app = Flask(__name__)
demo = [{'Full Name': 'ezfzef', 'Phone': 'zefezf', 'Student Card ID': 'zefzefzfz', 'Signature': 'data:image/png;base64,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'}, {'Full Name': 'ezfzef', 'Phone': 'zefezf', 'Student Card ID': 'zefzefzfz', 'Signature': 'data:image/png;base64,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'}, {'Full Name': 'ezfzef', 'Phone': 'zefezf', 'Student Card ID': 'zefzefzfz', 'Signature': 'data:image/png;base64,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'}]

json_file = 'student_records.json'  # JSON file to store records


student_records = []  # List to store submitted records
@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    global student_records
    # Retrieve form inputs
    full_name = request.form['full_name']
    phone = request.form['phone']
    student_card_id = request.form['student_card_id']
    signature_image = request.form['signature']
    # Create dictionary for new record
    new_record = {
        'Full Name': full_name,
        'Phone': phone,
        'Student Card ID': student_card_id,
        'Signature': signature_image
    }

    # Append record to student_records list
    student_records.append(new_record)

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
    with open(json_file, 'w') as file:
        json.dump(existing_records, file, indent=4)
    # print(student_records)
    
    # Render form.html template with the updated records
    return render_template('form.html', records=student_records)
    return render_template('form.html')

    return f'Form submitted successfully! <a href="/">Back</a>'


# @app.route('/generate_pdf')
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
    signature_paths= []

    # Add table rows from records list
    for record in records:
        for key, value in record.items():
            if key == 'Signature':
                # Save signature image to file
                signature_image = value
                signature_data = signature_image.replace('data:image/png;base64,', '')
                signature_path = f'signature{i}.png'
                
                with open(signature_path, 'wb') as file:
                    file.write(base64.b64decode(signature_data))
                    
                # Draw border around signature image
                pdf.set_draw_color(0, 0, 0)  # Set border color (black)
                # pdf.rect( w=40, h=10)  # Draw rectangle as border
                pdf.rect(x=pdf.x, y=pdf.y, w=40, h=10)  # Draw rectangle as border
                pdf.image(signature_path, w=40, h=10)
                signature_paths.append(signature_path)
                # pdf.image(item, x=10, y=pdf.y, w=40)
                
            else:
                pdf.cell(40, 10, str(value), border=1)
        i+=1
        pdf.ln(h=0)


    # Save PDF file
    pdf_file = 'students_info.pdf'
    pdf.output(pdf_file)
    for img in signature_paths:
        # Remove the signature image file
        os.remove(img)

    # # Remove the signature image file
    # os.remove(signature_path)
    return pdf_file

    # return f'Pdf generated successfully! <a href="/{pdf_file}">See PDF</a>'
    # return f'Pdf generated successfully! <a href="file:///C:/Users/retch/OneDrive/Desktop/py/Create%20Student%20Info%20PDF/student_info.pdf">See PDF</a>'

@app.route('/pdf')
def pdf():
    global student_records
    pdf_file = generate_pdf(demo)
    return send_file(pdf_file, as_attachment=False)


@app.route('/records')
def records():
    cp = [*demo, *demo, *demo, *demo, *demo, *demo, *demo, *demo]
    global student_records
    return render_template('pdf.html', records=cp)



# @app.route('/submit', methods=['POST'])
# def submit():
#     full_name = request.form['full_name']
#     phone = request.form['phone']
#     student_card_id = request.form['student_card_id']
#     signature = request.form['signature']
#     # Save signature image to file
#     signature_image = request.form['signature']
#     signature_data = signature_image.replace('data:image/png;base64,', '')
#     signature_path = 'signature.png'

#     with open(signature_path, 'wb') as file:
#         file.write(base64.b64decode(signature_data))

#     # Create PDF object
#     pdf = FPDF()
#     pdf.add_page()

#     # Set font and font size
#     pdf.set_font('Arial', 'B', 12)

#     # Add student information to PDF
#     pdf.cell(40, 10, 'Full Name:')
#     pdf.cell(0, 10, full_name, ln=True)
#     pdf.cell(40, 10, 'Phone:')
#     pdf.cell(0, 10, phone, ln=True)
#     pdf.cell(40, 10, 'Student Card ID:')
#     pdf.cell(0, 10, student_card_id, ln=True)

#     # Add signature field to PDF
#     pdf.cell(40, 10, 'Signature:')
#     pdf.ln(20)  # Move cursor to the next line
#     pdf.cell(0, 10, '___________________________',
#              ln=True)  # Placeholder for signature
#     # pdf.image(signature, x=10, y=pdf.y, w=60)
#     pdf.image(signature_path, x=10, y=pdf.y, w=60)

#     # Add table header
#     pdf.ln(20)  # Add space between signature and table
#     header = ['Full Name', 'Phone', 'Student Card ID', 'Signature']
#     for item in header:
#         pdf.cell(40, 10, item, border=1)
#     pdf.ln()

#     # Add table rows
#     data = [
#         [full_name, phone, student_card_id, signature_path],
#         # Add more rows if needed
#     ]
#     for row in data:
#         for item in row:
#             if item == signature_path:
#                 # Draw border around signature image
#                 pdf.set_draw_color(0, 0, 0)  # Set border color (black)
#                 # pdf.rect( w=40, h=10)  # Draw rectangle as border
#                 pdf.rect(x=pdf.x, y=pdf.y, w=40, h=10)  # Draw rectangle as border
#                 pdf.image(item, w=40, h=10)
#                 # pdf.image(item, x=10, y=pdf.y, w=40)

#             else:
#                 pdf.cell(40, 10, str(item), border=1)


#         pdf.ln()


#     # Save PDF file
#     pdf_file = 'student_info.pdf'
#     pdf.output(pdf_file)

#     # Remove the signature image file
#     os.remove(signature_path)

#     return f'Form submitted successfully! <a href="{pdf_file}">Download PDF</a>'

if __name__ == '__main__':
    app.run(debug=True)