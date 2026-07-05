# 🚀 E-Commerce RTO & Fraud Detection Pipeline

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-Backend-green)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Random_Forest-yellow)
![Database](https://img.shields.io/badge/Database-Aiven_MySQL-orange)
![Status](https://img.shields.io/badge/Status-Live_on_Render-brightgreen)

An end-to-end Machine Learning web application designed to predict whether an incoming e-commerce order is "Safe" or poses a "High Risk" of Return-to-Origin (RTO) fraud.

---

## 🎯 The Business Problem

Return to Origin (RTO) and fraudulent Cash-on-Delivery (COD) orders remain major profit drainers in the e-commerce sector. When an order is rejected at the doorstep, the company pays for two-way logistics without making a sale.

**The Solution:** This project utilizes a Machine Learning pipeline to analyze customer order parameters instantly and predict the risk flag, helping businesses reduce logistical losses and optimize their supply chain.

## 🌟 Live Action

No local setup required! Experience the real-time prediction model directly on the cloud:
**[👉 Click Here to Test the Live Prediction Pipeline](https://e-commerce-rto-fraud-predictor.onrender.com)**

---

## ⚙️ The Architecture (How It Works)

This project spans across the entire data engineering lifecycle:

1. **The Interface (Frontend):** A responsive HTML/CSS UI where order parameters are entered.
2. **The AJAX Bridge (Vanilla JS):** JavaScript intercepts the form submission, prevents page reloads, and securely routes the payload to the Flask backend using the Fetch API.
3. **The Brain (ML Pipeline):** A pre-trained **Random Forest model** (balanced using SMOTE) processes the input through a custom preprocessor and instantly predicts the risk flag.
4. **The Ledger (Backend & DB):** Flask and SQLAlchemy ORM intercept the transaction and automatically commit the live prediction data into a structured **Aiven MySQL Cloud Database** for future analytics.

---

## 🚧 The Debugging Journey: Local to Cloud

Building this wasn't a straight line. Here are the major architectural roadblocks I encountered and engineered my way out of:

### 1. 🛡️ The Secret Locker (Security First)

- **The Trap:** Initially hardcoded my Cloud Database URL into `app.py`. GitHub's Secret Scanning blocked the push to prevent a database breach.
- **The Fix:** Implemented **Environment Variables**. Securely stored the DB link in Render's environment settings and dynamically fetched it using `os.environ.get()`, keeping the codebase 100% secure.

### 2. 🐧 OS Clash: Windows vs. Linux Environment

- **The Trap:** The Render cloud deployment crashed continuously with a `metadata-generation-failed` error.
- **The Fix:** Traced the error in build logs back to `pywinpty`. Using `pip freeze` on my Windows machine captured OS-specific packages that choked Render's Linux server. Manually audited `requirements.txt`, stripped Windows dependencies, and the build succeeded.

### 3. 🔌 The "Port 405 Method Not Allowed" & DOM Errors

- **The Trap:** Attempted to test the `POST` request using VS Code Live Server, which only handles static files. Furthermore, the JS Fetch API failed to update the DOM silently.
- **The Fix:** Migrated testing entirely to Flask's native WSGI server. Debugged the execution order, moved the `<script>` tag to the bottom of the `<body>` to ensure the DOM was fully loaded before execution.

---

## 🤝 The "Human + AI" Pair Programming Philosophy

I believe in complete transparency regarding how this project was built:

- **My Execution (Human):** I conceptualized the core architecture, hand-coded the frontend, engineered the mock datasets using Pandas, executed the ML pipeline, designed the database schema, and managed GitHub version control/cloud deployment.
- **AI Assistance (Mentor Role):** I utilized AI strictly as a senior mentor. It guided me through syntax debugging (like resolving Git UI glitches via CLI), explained the deep logic behind SQLAlchemy ORM, and taught me deployment security (Environment Variables). **The AI didn't do the work for me; it taught me _how_ and _why_ the work is done.**

---

## 🚀 Future Scope

- Creating an interactive PowerBI/Excel Dashboard connected directly to the Aiven Cloud DB to track daily RTO fraud rates.
- Implementing automated model retraining (MLOps) as new prediction data flows into the database.

---

### 👨‍💻 Author

**Mr. Uttam Tiwari**  
_Bachelor of Computer Applications (BCA) Student | Aspiring Data Analyst_  
_Always learning, always debugging._

🔗 [Follow my GitHub](https://github.com/87690ut)
