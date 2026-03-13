import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import plotly.express as px


st.set_page_config(page_title="World Clock Dashboard", layout="wide")
st.title("🌏 World Clock Dashboard by Countries")
st.write(
    "Select one or more countries to view their current local time."
)


countries = {
    "Germany": "Europe/Berlin",
    "United States": "America/New_York",
    "India": "Asia/Kolkata",
    "United Kingdom": "Europe/London",
    "Japan": "Asia/Tokyo",
    "Australia": "Australia/Sydney",
    "Brazil": "America/Sao_Paulo",
    "Canada": "America/Toronto",
    "China": "Asia/Shanghai",
    "Russia": "Europe/Moscow",
    "South Africa": "Africa/Johannesburg",
    "Dubai": "Asia/Dubai"
}


selected_countries = st.multiselect(
    "Choose Countries:", options=list(countries.keys()),
    default=["Germany", "United States", "India"]
)


def get_local_time(tz_name):
    try:
        tz = pytz.timezone(tz_name)
        now = datetime.now(tz)
        utc_offset = now.strftime("%z")
        day_of_week = now.strftime("%A")
        return now, utc_offset, day_of_week
    except:
        return None, None, None


if selected_countries:
    table_data = []
    chart_data = []
    for country in selected_countries:
        tz_name = countries[country]
        dt, offset, day = get_local_time(tz_name)
        if dt:
            table_data.append({
                "Country": country,
                "Local Time": dt.strftime("%Y-%m-%d %H:%M:%S"),
                "UTC Offset": offset,
                "Day of Week": day,
                "Day/Night": "Day 🌞" if 6 <= dt.hour < 18 else "Night 🌙"
            })
            chart_data.append({
                "Country": country,
                "Hour": dt.hour,
                "Day/Night": "Day 🌞" if 6 <= dt.hour < 18 else "Night 🌙"
            })


    df_table = pd.DataFrame(table_data)
    st.subheader("🕒 Current Local Time Table")
    st.dataframe(df_table)

    df_chart = pd.DataFrame(chart_data)
    st.subheader("🕒 24-Hour Time Comparison")
    fig = px.bar(
        df_chart,
        x="Country",
        y="Hour",
        color="Day/Night",
        text="Hour",
        color_discrete_map={"Day 🌞": "gold", "Night 🌙": "darkblue"},
        labels={"Hour": "Local Hour (0-23)"}
    )
    st.plotly_chart(fig, use_container_width=True)

else:
    st.write("No countries selected.")
