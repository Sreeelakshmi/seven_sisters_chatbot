import streamlit as st
import pandas as pd
import openai

# Load CSV file
@st.cache_data
def load_data():
    file_path = "/mnt/data/Seven_Sisters_Travel_Packages_Enhanced.csv"
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        return None

data = load_data()

# Get API Key from Streamlit Secrets
api_key = st.secrets["OPENAI_API_KEY"]

# Initialize OpenAI Client
client = openai.OpenAI(api_key=api_key)


def query_openai(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are an expert travel guide on the Seven Sisters of India."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

st.title("Seven Sisters Travel Chatbot")
st.write("Ask me anything about Northeast India or details from your uploaded dataset!")

user_input = st.text_input("Enter your question:")

if user_input:
    if data is not None and any(keyword in user_input.lower() for keyword in data.columns.str.lower()):
        try:
            filtered_data = data.query(user_input)
            st.write(filtered_data if not filtered_data.empty else "No matching data found.")
        except Exception:
            st.write("I couldn't process your query on the dataset. Try rephrasing it!")
    else:
        response = query_openai(user_input)
        st.write(response)

