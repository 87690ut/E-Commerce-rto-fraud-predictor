from flask import Flask, render_template, request, jsonify
from flask.cli import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import joblib
import os
from datetime import datetime
from user_agents import parse
import smtplib
import random
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()



app = Flask(__name__)

def send_email_otp(user_email):
    otp = str(random.randint(100000, 999999))
    msg = EmailMessage()
    msg['Subject'] = 'E-Commerce Fraud Predictor - Verification OTP'
    msg['From'] = os.environ.get('MY_EMAIL')
    msg['To'] = user_email

    msg.set_content(f"Hello, \n\nYour OTP for verification is: {otp}\n\n Do not share with anyone, Thank you for using our service!")

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(os.environ.get('MY_EMAIL'), os.environ.get('EMAIL_APP_PASSWORD'))

        server.send_message(msg)
        server.quit()

        print("OTP email sent successfully!")
        return otp
    except Exception as e:
        print(f"Failed to send OTP email: {e}")
        return None

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

temp_otp_store = {}

class OrderData(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    mobile_no = db.Column(db.String(15), nullable= False)
    is_verified = db.Column(db.Boolean, nullable= False)
    payment_type = db.Column(db.String(50), nullable = False)
    return_count = db.Column(db.Integer, nullable= False)
    order_value = db.Column(db.Integer, nullable = False)
    city_tier = db.Column(db.String(50), nullable = False)
    prediction_result = db.Column(db.String(50), nullable = False)


class VisitorLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(100))
    device_info = db.Column(db.String(300))
    visit_time = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()




# Loading Translater and Model

preprocessor = joblib.load('preprocessor.pkl')
model = joblib.load('rto_model.pkl')

@app.route('/')
def home():
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    raw_ua = request.headers.get('User-Agent')
    
    ua_parsed = parse(raw_ua)
    clean_device = f"{ua_parsed.os.family} | {ua_parsed.browser.family} | {ua_parsed.device.family}"
    new_visitor = VisitorLog(ip_address=user_ip, device_info=clean_device)
    db.session.add(new_visitor)
    db.session.commit()

    return render_template('index.html')

@app.route('/send_otp', methods=['POST'])
def send_otp_route():
    try:
        data = request.get_json()
        user_email = data.get('email')
        if not user_email:
            return jsonify({'error': 'Email is required'}), 400
        
        generated_otp = send_email_otp(user_email)
        
        if generated_otp:
            temp_otp_store[user_email] = generated_otp
            return jsonify({'Message': "OTP sent successfully to your email. Please check your inbox."}), 200
        else:
            return jsonify({'error': 'Failed to send OTP. Please try again later.'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get('email')
    user_otp = data.get('otp')

    if email in temp_otp_store and temp_otp_store[email] == str(user_otp):

        del temp_otp_store[email]
        return jsonify({"message": "Email Verified Successfully!"}), 200
    else:
        return jsonify({"error": "Invalid OTP"}), 400

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        order_value = int(request.form['Order_Value'])
        city_tier = request.form['City_Tier']
        payment_type = request.form['Payment_Type']
        return_count = int(request.form['Return_Count'])
        is_verified_str = request.form['Is_Verified_Mobile']
        is_verified  = True if is_verified_str == 'True' else False
        mobile_num = request.form['mobile_no']

        input_data = pd.DataFrame([[order_value, city_tier, payment_type, return_count, is_verified]],
                                    columns=['Order_Value', 'City_Tier', 'Payment_Type', 'Return_Count', 'Is_Verified_Mobile'])
        
        processed_data = preprocessor.transform(input_data)
        prediction = model.predict(processed_data) [0]

        if prediction == 1:
            result_text = "🚨Alert! High Risk RTO/Fraud Detected"
        else:
            result_text = "✅Safe Order. No RTO/Fraud Detected"

        new_order = OrderData(
            mobile_no = mobile_num,
            is_verified = is_verified,
            payment_type=payment_type,
            return_count=return_count,
            order_value=order_value,
            city_tier=city_tier,
            prediction_result=result_text
        ) 
        db.session.add(new_order)
        db.session.commit()

    return jsonify({'prediction_text': result_text})
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host = '0.0.0.0', port = port)