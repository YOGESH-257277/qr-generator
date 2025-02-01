from flask import Flask, render_template, redirect, url_for
import qrcode
from io import BytesIO
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SHOP_EMAIL, GOOGLE_REVIEW_URL, DOMAIN

app = Flask(__name__)

def send_feedback_email(rating):
    # Email server settings (using Gmail as example)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "businessindia2527@gmail.com"  # Your Gmail address
    app_password = "zkloeedzcrtyhfmf"  # Your Gmail App Password
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = SHOP_EMAIL
    msg['Subject'] = f"New {rating}-Star Rating Received"
    
    body = f"A customer has provided a {rating}-star rating for your shop."
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Create secure SSL/TLS connection
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, app_password)
        
        # Send email
        text = msg.as_string()
        server.sendmail(sender_email, SHOP_EMAIL, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

@app.route('/')
def generate_qr():
    # Generate QR code pointing to the rating page
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f"{DOMAIN}/rate")
    qr.make(fit=True)
    
    # Create QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered)
    qr_img = base64.b64encode(buffered.getvalue()).decode()
    
    return render_template('qr.html', qr_image=qr_img)

@app.route('/rate')
def rating_page():
    return render_template('rate.html')

@app.route('/submit_rating/<int:rating>')
def submit_rating(rating):
    if rating == 5:
        return redirect(GOOGLE_REVIEW_URL)
    else:
        send_feedback_email(rating)
        return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)

