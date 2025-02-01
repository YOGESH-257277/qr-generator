from flask import Flask, jsonify
from flask_cors import CORS
from serverless_wsgi import handle_request
import qrcode
from io import BytesIO
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)
CORS(app)

# Environment variables (set these in Netlify)
SHOP_EMAIL = os.environ.get('SHOP_EMAIL', 'dharuvijain@gmail.com')
GOOGLE_REVIEW_URL = os.environ.get('GOOGLE_REVIEW_URL', 'https://search.google.com/local/writereview?placeid=ChIJcVeLi8PHxokRcGC_upcoRXM')
DOMAIN = os.environ.get('DOMAIN', 'your-netlify-domain.netlify.app')
EMAIL_APP_PASSWORD = os.environ.get('EMAIL_APP_PASSWORD', 'zkloeedzcrtyhfmf')

def send_feedback_email(rating):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "businessindia2527@gmail.com"
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = SHOP_EMAIL
    msg['Subject'] = f"New {rating}-Star Rating Received"
    
    body = f"A customer has provided a {rating}-star rating for your shop."
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, EMAIL_APP_PASSWORD)
        text = msg.as_string()
        server.sendmail(sender_email, SHOP_EMAIL, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route('/api/qr')
def generate_qr():
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f"{DOMAIN}/rate")
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered)
    qr_img = base64.b64encode(buffered.getvalue()).decode()
    
    return jsonify({'qr_image': qr_img})

@app.route('/api/submit_rating/<int:rating>')
def submit_rating(rating):
    if rating == 5:
        return jsonify({'redirect': GOOGLE_REVIEW_URL})
    else:
        success = send_feedback_email(rating)
        return jsonify({
            'success': success,
            'redirect': '/thank_you.html'
        })

def handler(event, context):
    return handle_request(app, event, context)
