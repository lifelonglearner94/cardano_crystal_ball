import streamlit as st
import requests
import numpy as np
import pandas as pd

def set_background(image_url):
    """
    Function to set background image using custom CSS
    """
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("{image_url}");
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

@st.cache
def creating_df(start, values=None):
    date_range = pd.date_range(start=start, periods=24, freq='H')
    if values == None:
        random_values = np.random.rand(24)  # Generating random values between 0 and 100
        df = pd.DataFrame({'date': date_range, 'rate': random_values})
    else:
        df = pd.DataFrame({'date': date_range, 'rate': values})

    df.set_index('date', inplace=True)

    return df

@st.cache
def api_request():

    url = 'http://127.0.0.1:8000/' # gcloud run deploy --image $GCP_REGION-docker.pkg.dev/$GCP_PROJECT/taxifare/$GAR_IMAGE:prod --memory $GAR_MEMORY --region $GCP_REGION --env-vars-file .env.yaml

    #params = {"current_date_and_time": 1}

    try:
        response = requests.get(url).json()#, params=params).json()
    except:
        return 0, 0, 0, 0, False

    return response["prediction"], response["start_time"], response["yesterdays_rate"], response["yesterdays_start_time"], response["upwards_trend"]

prediction, start_time, yesterdays_rate, yesterdays_start_time, upwards_trend = api_request()

set_background("https://images.freeimages.com/images/large-previews/1ca/green-glass-sphere-1196476.jpg")


st.title('Cardano Crystal Ball 🔮')

st.markdown(f"\n")

button1 = st.button("Predict prices of tomorrow")

st.markdown(f"\n")

df1 = creating_df(yesterdays_start_time, yesterdays_rate)
df2 = creating_df(start_time, prediction)




if button1:

    col1, col2 = st.columns(2, gap="small")

    with col1:
        st.markdown(f"Rate of the last 24h:")
        st.line_chart(data=df1, use_container_width=True)
    with col2:
        st.markdown(f"Forecasted rate of the next 24h:")
        st.line_chart(data=df2, use_container_width=True)

    if upwards_trend:
        st.markdown(f"### The price trend is upwards 📈")
    else:
        st.markdown(f"### The price trend is downwards 📉")
