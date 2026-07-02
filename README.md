# 🚀 E-Commerce RTO & Fraud Detection Pipeline

## 📌 Project Overview

As e-commerce platforms grow, Return-to-Origin (RTO) and fraudulent cash-on-delivery (COD) orders remain major profit drainers. This project is a complete, end-to-end Machine Learning web application designed to predict whether an incoming order is "Safe" or poses a "High Risk" of RTO/Fraud.

It spans across the entire data engineering lifecycle: from synthetic data generation and model training to full-stack web deployment and database integration.

## 🛠️ Tech Stack & Architecture

- **Data Science & ML:** Python, Pandas, Scikit-Learn (Random Forest Classifier), SMOTE (for handling class imbalance).
- **Backend:** Flask (Python).
- **Frontend:** HTML, CSS, Vanilla JavaScript (AJAX/Fetch API).
- **Database:** MySQL, SQLAlchemy (ORM).
- **Tools:** VS Code, Jupyter Notebook, Git/GitHub.

## ⚙️ How It Works (The Pipeline)

1. **The Interface:** A responsive UI where order parameters (Order Value, City Tier, Payment Type, Return History, Mobile Verification) are entered.
2. **The AJAX Bridge:** JavaScript intercepts the form submission, prevents page reloads, and securely routes the payload to the Flask backend.
3. **The Brain:** A pre-trained Random Forest model processes the input through a custom preprocessor pipeline and instantly predicts the risk flag.
4. **The Ledger:** SQLAlchemy ORM intercepts the transaction and automatically commits the live prediction data into a structured MySQL database for future analytics.

## 🚧 Roadblocks & Debugging Journey

Building this wasn't a straight line. Here are the major architectural issues I encountered and resolved:

- **The "Port 405 Method Not Allowed" Trap:** Initially attempted to test the `POST` request form using VS Code Live Server (Port 5500) before realizing Live Server only handles static files. **Fix:** Migrated testing entirely to Flask's native WSGI server (Port 5000).
- **The "Silent" DOM Execution Error:** The JavaScript Fetch API failed to update the DOM without throwing server errors. **Fix:** Debugged the execution order and realized the `<script>` tag was loading before the HTML form was rendered. Moved the script to the bottom of the `<body>` to ensure the DOM is fully loaded.
- **Persistent Data Architecture:** Real-world apps don't rely on in-memory execution. **Fix:** Upgraded the backend from stateless execution to a persistent database model using `Flask-SQLAlchemy`, allowing automated table creation and data logging upon every successful submission.

## 🤝 The "Human + AI" Pair Programming Approach

I believe in complete transparency regarding how this project was built:

- **My Execution (Human):** I conceptualized the core architecture, hand-coded the frontend structure, engineered the mock datasets using Pandas, executed the machine learning pipeline, identified bugs (like DOM element ID mismatches), and managed the local environment/GitHub version control.
- **AI Assistance (Mentor Role):** I utilized AI strictly as a senior mentor. It guided me through syntax corrections, explained the deep logic behind backend-to-database routing (ORM concepts), and helped me write clean AJAX calls for seamless user experience. The AI didn't do the work for me; it taught me _how_ and _why_ the work is done.

## 👨‍💻 Author

**Mr. Uttam Tiwari**
_Bachelor of Computer Applications (BCA) Student & Aspiring Data Analyst._
Always learning, always debugging.
