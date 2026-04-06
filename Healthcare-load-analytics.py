import pandas as pd

df = pd.read_csv(r"D:\internship\HHS_Unaccompanied_Alien_Children_Program.csv")

df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')

print(df.head())

print(df.isnull().sum())  #check for missing values
df=df.drop_duplicates()  #remove duplicates
df=df.ffill()  #fill missing values using forward fill method


# Convert columns to numeric (remove commas)

cols = [
    'Children in HHS Care',
    'Children discharged from HHS Care'
]

for col in cols:
    df[col] = df[col].astype(str).str.replace(',', '')  # remove commas
    df[col] = pd.to_numeric(df[col])  # convert to number

df['Children in CBP custody'] = pd.to_numeric(df['Children in CBP custody'])
df['Children transferred out of CBP custody'] = pd.to_numeric(df['Children transferred out of CBP custody'])

df['Total_Load'] = df['Children in CBP custody'] + df['Children in HHS Care']

print(df.dtypes)

df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

# Total System Load
df['Total_Load'] = df['Children in CBP custody'] + df['Children in HHS Care']

# Net Intake
df['Net_Intake'] = df['Children transferred out of CBP custody'] - df['Children discharged from HHS Care']

# Growth Rate
df['Growth_Rate'] = df['Total_Load'].pct_change() * 100

# Rolling Average
df['7_day_avg'] = df['Total_Load'].rolling(7).mean()
#Total load Trend
import matplotlib.pyplot as plt

plt.plot(df['Date'], df['Total_Load'])
plt.title("Total System Load Over Time")
plt.show()
#CBP VS HHS
plt.plot(df['Date'], df['Children in CBP custody'], label="CBP")
plt.plot(df['Date'], df['Children in HHS Care'], label="HHS")
plt.legend()
plt.show()

# Net intake
plt.plot(df['Date'], df['Net_Intake'])
plt.title("Net Intake Trend")
plt.show()

# KPI Calculations
total_children = df['Total_Load'].sum()
avg_net_intake = df['Net_Intake'].mean()
volatility = df['Total_Load'].std()

print(total_children, avg_net_intake, volatility)

#Streamlit Dashboard
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Healthcare Load Dashboard", layout="wide")

st.title("📊 Healthcare Load Analytics Dashboard")

# File Upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Data Cleaning
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    # Convert numeric columns
    cols = [
        'Children in HHS Care',
        'Children discharged from HHS Care',
        'Children in CBP custody',
        'Children transferred out of CBP custody'
    ]

    for col in cols:
        df[col] = df[col].astype(str).str.replace(',', '')
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.ffill()

    # Metrics
    df['Total_Load'] = df['Children in CBP custody'] + df['Children in HHS Care']
    df['Net_Intake'] = df['Children transferred out of CBP custody'] - df['Children discharged from HHS Care']

    # Sidebar Filter
    st.sidebar.header("Filters")
    start_date = st.sidebar.date_input("Start Date", df['Date'].min())
    end_date = st.sidebar.date_input("End Date", df['Date'].max())

    df_filtered = df[(df['Date'] >= pd.to_datetime(start_date)) & 
                     (df['Date'] <= pd.to_datetime(end_date))]

    # KPIs
    total_load = int(df_filtered['Total_Load'].sum())
    avg_net = round(df_filtered['Net_Intake'].mean(), 2)
    volatility = round(df_filtered['Total_Load'].std(), 2)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Load", total_load)
    col2.metric("Avg Net Intake", avg_net)
    col3.metric("Volatility", volatility)

    # Charts
    st.subheader("📈 Total Load Over Time")
    st.line_chart(df_filtered.set_index('Date')['Total_Load'])

    st.subheader("📉 Net Intake Trend")
    st.line_chart(df_filtered.set_index('Date')['Net_Intake'])

    # CBP vs HHS Plot
    st.subheader("📊 CBP vs HHS Comparison")

    fig, ax = plt.subplots()
    ax.plot(df_filtered['Date'], df_filtered['Children in CBP custody'], label='CBP')
    ax.plot(df_filtered['Date'], df_filtered['Children in HHS Care'], label='HHS')
    ax.legend()

    st.pyplot(fig)

else:
    st.info("Please upload a CSV file to see the analytics dashboard.")
   
csv = df_filtered.to_csv(index=False).encode('utf-8')

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name='filtered_data.csv',
    mime='text/csv'
)

col1.metric("Total Load", total_load, delta=None)
col2.metric("Avg Net Intake", avg_net, delta=None)
col3.metric("Volatility", volatility, delta=None)

df_filtered['7_day_avg'] = df_filtered['Total_Load'].rolling(7).mean()

st.subheader("📉 Trend with Rolling Average")
st.line_chart(df_filtered.set_index('Date')[['Total_Load', '7_day_avg']])

st.subheader("📋 Data Preview")
st.dataframe(df_filtered) 
    