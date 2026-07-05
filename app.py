from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import joblib
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class OrderData(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    mobile_no = db.Column(db.String(15), nullable= False)
    is_verified = db.Column(db.Boolean, nullable= False)
    payment_type = db.Column(db.String(50), nullable = False)
    return_count = db.Column(db.Integer, nullable= False)
    order_value = db.Column(db.Integer, nullable = False)
    city_tier = db.Column(db.String(50), nullable = False)
    prediction_result = db.Column(db.String(50), nullable = False)

with app.app_context():
    db.create_all()



# Loading Translater and Model

preprocessor = joblib.load('preprocessor.pkl')
model = joblib.load('rto_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

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
    app.run(debug=True)