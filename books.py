import urllib.request
import ssl
import certifi

import gender_guesser.detector as gender
import numpy as np
import pandas as pd
import plotly.express as px
import requests
import streamlit as st
import xmltodict
from pandas import json_normalize
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_lottie import st_lottie


ssl.create_default_context(cafile=certifi.where())
st.set_page_config(page_title="Goodreads Analysis App", layout="wide")

import requests
import streamlit as st
from streamlit_lottie import st_lottie
import json
import pandas as pd

import requests
import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd

# Function to fetch Lottie animation
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        r.raise_for_status()  # Raises an error for unsuccessful responses
        return r.json()
    except requests.exceptions.RequestException:
        return None
    
# Lottie animation for location theme
lottie_weather = load_lottieurl("https://assets4.lottiefiles.com/temp/lf20_aKAfIn.json")
if lottie_weather:
    st_lottie(lottie_weather, speed=1, height=200, key="initial")
else:
    st.warning("Failed to load animation. Please check the Lottie URL.")

# Page layout
row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((0.1, 2, 0.2, 1, 0.1))
row0_1.title("IP Geolocation Analysis")

with row0_2:
    st.subheader("A Streamlit web app for analyzing IP-based geolocation data.")

row1_spacer1, row1_1, row1_spacer2 = st.columns((0.1, 3.2, 0.1))

with row1_1:
    st.markdown(
        "Welcome to the IP Geolocation Analysis App! This app fetches real-time geolocation data based on an IP address and provides insights into the country, region, city, and more."
    )

row2_spacer1, row2_1, row2_spacer2 = st.columns((0.1, 3.2, 0.1))

with row2_1:
    ip_address = st.text_input("Enter IP Address (e.g., 134.201.250.155):", "134.201.250.155")

    api_key = st.secrets["ipkey"]  # Store API key securely in Streamlit secrets
    base_url = "http://api.ipstack.com/"

    @st.cache_data
    def get_ip_data(_api_key, ip_address):
        base_url = "http://api.ipstack.com/"
        url = f"{base_url}{ip_address}?access_key={_api_key}"
        
        response = requests.get(url)
        if response.status_code != 200:
            return None
        return response.json()

    ip_data = get_ip_data(api_key, ip_address)

    if not ip_data:
        st.error("Failed to fetch geolocation data. Please check the IP address and try again.")
    else:
        st.header(f"Geolocation Details for: **{ip_address}**")

        country = ip_data.get("country_name", "N/A")
        region = ip_data.get("region_name", "N/A")
        city = ip_data.get("city", "N/A")
        latitude = ip_data.get("latitude", "N/A")
        longitude = ip_data.get("longitude", "N/A")
        isp = ip_data.get("isp", "N/A")

        st.write(f"**Country:** {country}")
        st.write(f"**Region:** {region}")
        st.write(f"**City:** {city}")
        st.write(f"**Latitude:** {latitude}")
        st.write(f"**Longitude:** {longitude}")
        st.write(f"**ISP:** {isp}")

        # Convert data to DataFrame for visualization
        df = pd.DataFrame({
            "Metric": ["Country", "Region", "City", "Latitude", "Longitude", "ISP"],
            "Value": [country, region, city, latitude, longitude, isp]
        })
        st.table(df)

st.warning("Geolocation data is retrieved from IPStack API in real-time.")

st.write("")
row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)


# Load the Iris dataset
df = pd.read_csv("Iris.csv")

# Ensure the column names are as expected
expected_columns = ["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm", "Species"]
if not all(column in df.columns for column in expected_columns):
    st.error("The Iris dataset does not contain the expected columns.")
else:
    st.write("")
    row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.columns((0.1, 1, 0.1, 1, 0.1))
    df.to_csv("iris_data.csv", index=False)

    with row3_1:
        st.subheader("Iris Species Distribution")
        species_df = df["Species"].value_counts().reset_index()
        species_df.columns = ["Species", "Count"]
        fig = px.bar(
            species_df,
            x="Species",
            y="Count",
            title="Number of Samples per Species",
            color_discrete_sequence=["#9EE6CF"],
        )
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        st.markdown(
            "The dataset consists of **{} samples** from **{} unique species**.".format(
                len(df), df["Species"].nunique()
            )
        )

    with row3_2:
        st.subheader("Sepal Length vs Sepal Width")
        fig = px.scatter(
            df, x="SepalLengthCm", y="SepalWidthCm", color="Species",
            title="Sepal Length vs Sepal Width", labels={"SepalLengthCm": "Sepal Length (cm)", "SepalWidthCm": "Sepal Width (cm)"}
        )
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        st.markdown(
            "Here's a scatter plot showcasing the sepal dimensions for different Iris species."
        )

    add_vertical_space()
    row4_space1, row4_1, row4_space2, row4_2, row4_space3 = st.columns(
        (0.1, 1, 0.1, 1, 0.1)
    )

    with row4_1:
        st.subheader("Petal Length vs Petal Width")
        fig = px.scatter(
            df, x="PetalLengthCm", y="PetalWidthCm", color="Species",
            title="Petal Length vs Petal Width", labels={"PetalLengthCm": "Petal Length (cm)", "PetalWidthCm": "Petal Width (cm)"}
        )
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        st.markdown(
            "Here's a scatter plot showcasing the petal dimensions for different Iris species."
        )

    with row4_2:
        st.subheader("Sepal Length Distribution")
        fig = px.histogram(
            df,
            x="SepalLengthCm",
            title="Sepal Length Distribution",
            color="Species",
            color_discrete_sequence=["#9EE6CF"],
        )
        fig.update_xaxes(title_text="Sepal Length (cm)")
        fig.update_yaxes(title_text="Count")
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        st.markdown(
            "Here is the distribution of sepal length for different Iris species."
        )

    add_vertical_space()
    row5_space1, row5_1, row5_space2, row5_2, row5_space3 = st.columns(
        (0.1, 1, 0.1, 1, 0.1)
    )

    with row5_1:
        st.subheader("Sepal Width Distribution")
        fig = px.histogram(
            df,
            x="SepalWidthCm",
            title="Sepal Width Distribution",
            color="Species",
            color_discrete_sequence=["#9EE6CF"],
        )
        fig.update_xaxes(title_text="Sepal Width (cm)")
        fig.update_yaxes(title_text="Count")
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        st.markdown(
            "Here is the distribution of sepal width for different Iris species."
        )

    with row5_2:
        st.subheader("Petal Length Distribution")
        fig = px.histogram(
            df,
            x="PetalLengthCm",
            title="Petal Length Distribution",
            color="Species",
            color_discrete_sequence=["#9EE6CF"],
        )
        fig.update_xaxes(title_text="Petal Length (cm)")
        fig.update_yaxes(title_text="Count")
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        st.markdown(
            "Here is the distribution of petal length for different Iris species."
        )

    add_vertical_space()
    row6_space1, row6_1, row6_space2, row6_2, row6_space3 = st.columns(
        (0.1, 1, 0.1, 1, 0.1)
    )

    with row6_1:
        st.subheader("Petal Width Distribution")
        fig = px.histogram(
            df,
            x="PetalWidthCm",
            title="Petal Width Distribution",
            color="Species",
            color_discrete_sequence=["#9EE6CF"],
        )
        fig.update_xaxes(title_text="Petal Width (cm)")
        fig.update_yaxes(title_text="Count")
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        st.markdown(
            "Here is the distribution of petal width for different Iris species."
        )

    with row6_2:
        st.subheader("Pair Plot")
        fig = px.scatter_matrix(
            df,
            dimensions=["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"],
            color="Species",
            title="Pair Plot of Iris Dataset",
        )
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        st.markdown(
            "Here is a pair plot showing the relationships between different features of the Iris dataset."
        )

def get_link(recommended):
    if "-" not in recommended:
        link = "https://bookschatter.com/books/" + recommended
    elif "-" in recommended:
        link = "https://www.mostrecommendedbooks.com/" + recommended + "-books"
    return link

# These variables need to be defined before using them
# For example:
most_in_common = "Naval Ravikant"  # Replace with your actual variable
avg_in_common = "Truth Decay"  # Replace with your actual variable
most_recommended = "naval-ravikant"  # Replace with your actual variable
avg_recommended = "barack-obama"  # Replace with your actual variable

st.markdown(
    "For one last bit of analysis, we scraped a few hundred book lists from famous thinkers in technology, media, and government (everyone from Barack and Michelle Obama to Keith Rabois and Naval Ravikant). We took your list of books read and tried to recommend one of their lists to book through based on information we gleaned from your list"
)
st.markdown(
    "You read the most books in common with **{}**, and your book list is the most similar on average to **{}**. Find their book lists [here]({}) and [here]({}) respectively.".format(
        most_in_common,
        avg_in_common,
        get_link(most_recommended),
        get_link(avg_recommended),
    )
)

st.markdown("***")
st.markdown(
    "Thanks for going through this mini-analysis with me! I'd love feedback on this, so if you want to reach out you can find me on [twitter](https://twitter.com/tylerjrichards) or my [website](http://www.tylerjrichards.com/)."
)