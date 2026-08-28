import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Golf Group Handicaps",
    page_icon="⛳",
    layout="centered"
)

st.title("⛳ Golf Group Handicaps")
st.caption("Unofficial handicap tracker using WHS calculation rules")


# ---------------------------------
# Session storage for testing
# ---------------------------------
if "rounds" not in st.session_state:
    st.session_state.rounds = []


# ---------------------------------
# Score Differential
# ---------------------------------
def calculate_differential(
    adjusted_gross_score,
    course_rating,
    slope_rating
):
    return (
        (113 / slope_rating)
        * (adjusted_gross_score - course_rating)
    )


# ---------------------------------
# Add Round
# ---------------------------------
st.subheader("➕ Add Round")

with st.form("add_round_form"):

    player = st.text_input(
        "Player",
        placeholder="e.g. Paul"
    )

    date_played = st.date_input(
        "Date played",
        value=date.today()
    )

    golf_course = st.text_input(
        "Golf course",
        placeholder="e.g. Brocton Hall Golf Club"
    )

    course_layout = st.text_input(
        "Course / Layout",
        placeholder="e.g. Main Course"
    )

    tees_used = st.selectbox(
        "Tees used",
        [
            "White",
            "Yellow",
            "Blue",
            "Red",
            "Black",
            "Green",
            "Other"
        ]
    )

    st.markdown("#### Course rating information")

    course_rating = st.number_input(
        "Course Rating",
        min_value=50.0,
        max_value=90.0,
        value=70.0,
        step=0.1,
        format="%.1f"
    )

    slope_rating = st.number_input(
        "Slope Rating",
        min_value=55,
        max_value=155,
        value=113,
        step=1
    )

    par = st.number_input(
        "Par",
        min_value=54,
        max_value=80,
        value=72,
        step=1
    )

    adjusted_gross_score = st.number_input(
        "Adjusted Gross Score",
        min_value=40,
        max_value=200,
        value=90,
        step=1
    )

    differential = calculate_differential(
        adjusted_gross_score,
        course_rating,
        slope_rating
    )

    st.info(
        f"Calculated Score Differential: "
        f"**{differential:.1f}**"
    )

    save_round = st.form_submit_button(
        "Save Round",
        use_container_width=True
    )


# ---------------------------------
# Save round
# ---------------------------------
if save_round:

    if not player.strip():
        st.error("Please enter the player's name.")

    elif not golf_course.strip():
        st.error("Please enter the golf course.")

    else:

        round_record = {
            "Player": player.strip(),
            "Date": date_played,
            "Golf Course": golf_course.strip(),
            "Course / Layout": course_layout.strip(),
            "Tees": tees_used,
            "Course Rating": course_rating,
            "Slope Rating": slope_rating,
            "Par": par,
            "Adjusted Gross Score": adjusted_gross_score,
            "Score Differential": round(differential, 1)
        }

        st.session_state.rounds.append(round_record)

        st.success(
            f"Round saved for {player.strip()} — "
            f"Score Differential {differential:.1f}"
        )


# ---------------------------------
# Recent rounds
# ---------------------------------
st.divider()

st.subheader("Recent Rounds")

if not st.session_state.rounds:

    st.info("No rounds have been entered yet.")

else:

    for round_record in reversed(
        st.session_state.rounds
    ):

        st.markdown(
            f"""
            **{round_record['Player']}**  
            {round_record['Golf Course']}  
            {round_record['Tees']} tees  
            Score: **{round_record['Adjusted Gross Score']}**  
            Differential: **{round_record['Score Differential']:.1f}**
            """
        )

        st.divider()


st.caption(
    "Scores are currently stored temporarily while "
    "the app is being developed."
)