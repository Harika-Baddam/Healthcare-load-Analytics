# Healthcare-load-Analytics
System Capacity &amp; Care Load Analytics for Unaccompanied Children
# 🏥 Healthcare Load Analytics Dashboard

## 📌 Project Overview
This project focuses on analyzing healthcare system load data to understand trends, capacity, and resource utilization. The goal is to derive meaningful insights and visualize them using Python and Streamlit.

---

## 🚀 Technologies Used
- Python
- Pandas
- Matplotlib
- Streamlit
- VS Code

---

## 📊 Key Features
- Data cleaning and preprocessing
- Handling missing values and duplicates
- KPI calculations:
  - Total System Load
  - Net Intake
  - Growth Rate
  - 7-Day Rolling Average
- Data visualization using line charts
- Interactive dashboard using Streamlit

---

## 📂 Dataset
- Healthcare dataset containing:
  - Date
  - Children in CBP custody
  - Children in HHS Care
  - Transfers and discharges

---

## 🔍 Data Processing Steps
1. Loaded dataset using Pandas
2. Converted date column to datetime format
3. Removed duplicates
4. Handled missing values using forward fill
5. Converted numeric columns (removed commas)
6. Created new calculated columns:
   - Total_Load
   - Net_Intake
   - Growth_Rate
   - 7_day_avg

---

## 📈 Visualizations
- Total System Load over time
- CBP vs HHS comparison
- Net Intake trends

---

## 📊 KPIs
- Total Children in System
- Average Net Intake
- Load Volatility (Standard Deviation)

---

## 🖥️ Streamlit Dashboard
- Interactive charts
- User-friendly interface
- Real-time data visualization

---

## ▶️ How to Run the Project

### Step 1: Install dependencies
```bash
pip install pandas matplotlib streamlit
