import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Golf Handicap Tracker",
    page_icon="⛳",
    layout="centered"
)

st.title("⛳ Golf Handicap Tracker")
st.caption("Unofficial WHS-style handicap calculator")

st.subheader("Add a round")

score = st.number_input(
    "Adjusted Gross Score",
    min_value=50,
    max_value=200,
    value=90
)

course_rating = st.number_input(
    "Course Rating",
    min_value=50.0,
    max_value=90.0,
    value=70.0,
    step=0.1
)

slope_rating = st.number_input(
    "Slope Rating",
    min_value=55,
    max_value=155,
    value=113
)

if st.button("Calculate Score Differential"):
    differential = (score - course_rating) * 113 / slope_rating

    st.success(
        f"Score Differential: {differential:.1f}"
    )

st.divider()

st.subheader("How the handicap will work")

st.write(
    """
    Once 20 rounds have been entered, the app will:

    • take the most recent 20 rounds  
    • identify the lowest 8 Score Differentials  
    • average those 8 scores  
    • display the player's Handicap Index
    """
)