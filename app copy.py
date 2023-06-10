from flask import Flask, render_template, request
from fpdf import FPDF
import os
import base64


# template_dir = os.path.abspath('../../frontend/src')
# app = Flask(__name__, template_folder=template_dir)
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit():
    full_name = request.form['full_name']
    phone = request.form['phone']
    student_card_id = request.form['student_card_id']
    signature = request.form['signature']
    # Save signature image to file
    signature_image = request.form['signature']
    signature_data = signature_image.replace('data:image/png;base64,', '')
    signature_path = 'signature.png'

    with open(signature_path, 'wb') as file:
        file.write(base64.b64decode(signature_data))

    # Create PDF object
    pdf = FPDF()
    pdf.add_page()

    # Set font and font size
    pdf.set_font('Arial', 'B', 12)

    # Add student information to PDF
    pdf.cell(40, 10, 'Full Name:')
    pdf.cell(0, 10, full_name, ln=True)
    pdf.cell(40, 10, 'Phone:')
    pdf.cell(0, 10, phone, ln=True)
    pdf.cell(40, 10, 'Student Card ID:')
    pdf.cell(0, 10, student_card_id, ln=True)

    # Add signature field to PDF
    pdf.cell(40, 10, 'Signature:')
    pdf.ln(20)  # Move cursor to the next line
    pdf.cell(0, 10, '___________________________',
             ln=True)  # Placeholder for signature
    # pdf.image(signature, x=10, y=pdf.y, w=60)
    pdf.image(signature_path, x=10, y=pdf.y, w=60)

    # Add table header
    pdf.ln(20)  # Add space between signature and table
    header = ['Full Name', 'Phone', 'Student Card ID', 'Signature']
    for item in header:
        pdf.cell(40, 10, item, border=1)
    pdf.ln()

    # Add table rows
    data = [
        [full_name, phone, student_card_id, signature_path],
        # Add more rows if needed
    ]
    for row in data:
        for item in row:
            if item == signature_path:
                # Draw border around signature image
                pdf.set_draw_color(0, 0, 0)  # Set border color (black)
                # pdf.rect( w=40, h=10)  # Draw rectangle as border
                pdf.rect(x=pdf.x, y=pdf.y, w=40, h=10)  # Draw rectangle as border
                pdf.image(item, w=40, h=10)
                # pdf.image(item, x=10, y=pdf.y, w=40)

            else:
                pdf.cell(40, 10, str(item), border=1)


        pdf.ln()


    # Save PDF file
    pdf_file = 'student_info.pdf'
    pdf.output(pdf_file)

    # Remove the signature image file
    os.remove(signature_path)

    return f'Form submitted successfully! <a href="{pdf_file}">Download PDF</a>'

if __name__ == '__main__':
    app.run(debug=True)