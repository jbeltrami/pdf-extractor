from flask import Flask, render_template, request, send_file
from io import BytesIO
from extract_keywords import extract_pages_with_keywords
from datetime import datetime
import os
import schedule
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        keywords = request.form.get('keywords', '').split(',')

        if uploaded_file and allowed_file(uploaded_file.filename):
            result_pdf = extract_keywords(uploaded_file, keywords)
            return send_file(result_pdf, download_name='result.pdf', as_attachment=True)

    return render_template('index.html')

def extract_keywords(uploaded_file, keywords):
    pdf_path = save_uploaded_file(uploaded_file)
    output_path = 'result.pdf'

    extract_pages_with_keywords(pdf_path, keywords, output_path)

    result_pdf = BytesIO()
    with open(output_path, 'rb') as result_file:
        result_pdf.write(result_file.read())

    result_pdf.seek(0)  # Reset the buffer position to the beginning

    return result_pdf

def save_uploaded_file(uploaded_file):
    pdf_path = f'uploads/{datetime.now().strftime("%Y%m%d%H%M%S")}_{uploaded_file.filename}'
    uploaded_file.save(pdf_path)
    return pdf_path

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

if __name__ == '__main__':
    app.run(debug=True)

def clear_uploads_directory():
    uploads_dir = 'uploads/'
    for file_name in os.listdir(uploads_dir):
        file_path = os.path.join(uploads_dir, file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

# Schedule the task to run every day at midnight
schedule.every().day.at("00:00").do(clear_uploads_directory)

# Run the scheduled tasks in a separate thread
def run_scheduled_tasks():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    # Start the Flask app and the scheduled tasks in separate threads
    from threading import Thread

    flask_thread = Thread(target=app.run, kwargs={'debug': True})
    scheduled_tasks_thread = Thread(target=run_scheduled_tasks)

    flask_thread.start()
    scheduled_tasks_thread.start()

    flask_thread.join()
    scheduled_tasks_thread.join()
