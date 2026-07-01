from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

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

        input_data = pd.DataFrame([[order_value, city_tier, payment_type, return_count, is_verified]],
                                    columns=['Order_Value', 'City_Tier', 'Payment_Type', 'Return_Count', 'Is_Verified_Mobile'])
        
        processed_data = preprocessor.transform(input_data)
        prediction = model.predict(processed_data) [0]

        if prediction == 1:
            result_text = "🚨Alert! High Risk RTO/Fraud Detected"
        else:
            result_text = "✅Safe Order. No RTO/Fraud Detected"

    return jsonify({'prediction_text': result_text})
if __name__ == '__main__':
    app.run(debug=True)