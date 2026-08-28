import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Golf Group Handicaps",
    page_icon="⛳",
    layout="centered"
)

st.title("⛳ Golf Group Handicaps")
st.caption("Unofficial handicap tracker using WHS calculation rules")


# -----------------------------
# Session storage
# -----------------------------
if "rounds" not in st.session_state:
    st.session_state.rounds = []


# -----------------------------
# WHS functions
# -----------------------------
def calculate_differential(score, course_rating, slope_rating):
    return (113 / slope_rating) * (score - course_rating)


def calculate_whs_handicap(differentials):
    """
    WHS Rule 5.2a style calculation for fewer than 20 scores.
    Returns:
        handicap,
        explanation
    """

    count = len(differentials)

    if count < 3:
        return None, "At least 3 scores are required to establish a WHS-style handicap."

    # Only use most recent 20 scores
    recent = differentials[-20:]
    sorted_diffs = sorted(recent)

    if count == 3:
        handicap = sorted_diffs[0] - 2.0
        explanation = "Lowest 1 differential minus 2.0"

    elif count == 4:
        handicap = sorted_diffs[0] - 1.0
        explanation = "Lowest 1 differential minus 1.0"

    elif count == 5:
        handicap = sorted_diffs[0]
        explanation = "Lowest 1 differential"

    elif count == 6:
        handicap = sum(sorted_diffs[:2]) / 2 - 1.0
        explanation = "Average of lowest 2 differentials minus 1.0"

    elif count in [7, 8]:
        handicap = sum(sorted_diffs[:2]) / 2
        explanation = "Average of lowest 2 differentials"

    elif 9 <= count <= 11:
        handicap = sum(sorted_diffs[:3]) / 3
        explanation = "Average of lowest 3 differentials"

    elif 12 <= count <= 14:
        handicap = sum(sorted_diffs[:4]) / 4
        explanation = "Average of lowest 4 differentials"

    elif 15 <= count <= 16:
        handicap = sum(sorted_diffs[:5]) / 5
        explanation = "Average of lowest 5 differentials"

    elif 17 <= count <= 18:
        handicap = sum(sorted_diffs[:6]) / 6
        explanation = "Average of lowest 6 differentials"

    elif count == 19:
        handicap = sum(sorted_diffs[:7]) / 7
        explanation = "Average of lowest 7 differentials"

    else:
        handicap = sum(sorted_diffs[:8]) / 8
        explanation = "Average of lowest 8 differentials from most recent 20"

    # WHS maximum Handicap Index
    handicap = min(handicap, 54.0)

    return round(handicap, 1), explanation


# -----------------------------
# Add round
# -----------------------------
st.subheader("Add a round")

with st.form("round_form"):

    player = st.text_input("Player name")

    date = st.date_input("Date played")

    course = st.text_input("Course")

    score = st.number_input(
        "Adjusted Gross Score",
        min_value=40,
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

    submitted = st.form_submit_button("Add round")

    if submitted:

        if not player:
            st.error("Please enter the player's name.")

        elif not course:
            st.error("Please enter the course.")

        else:

            differential = calculate_differential(
                score,
                course_rating,
                slope_rating
            )

            st.session_state.rounds.append(
                {
                    "Player": player.strip(),
                    "Date": date,
                    "Course": course.strip(),
                    "Score": score,
                    "Course Rating": course_rating,
                    "Slope": slope_rating,
                    "Differential": round(differential, 1)
                }
            )

            st.success(
                f"Round added. Score Differential: {differential:.1f}"
            )


# -----------------------------
# Handicap section
# -----------------------------
st.divider()
st.subheader("Player handicaps")

if not st.session_state.rounds:

    st.info("No rounds have been entered yet.")

else:

    df = pd.DataFrame(st.session_state.rounds)

    players = sorted(df["Player"].unique())

    selected_player = st.selectbox(
        "Select player",
        players
    )

    player_df = df[
        df["Player"] == selected_player
    ].sort_values("Date")

    differentials = player_df["Differential"].tolist()

    handicap, explanation = calculate_whs_handicap(
        differentials
    )

    number_of_scores = len(player_df)

    if handicap is None:

        st.metric(
            "WHS-calculated handicap",
            "Not yet established"
        )

        st.info(
            f"{selected_player} has submitted "
            f"{number_of_scores} score(s). "
            "A minimum of 3 is required."
        )

    else:

        st.metric(
            "WHS-calculated handicap",
            f"{handicap:.1f}"
        )

        st.caption(
            "Unofficial — calculated using WHS rules."
        )

        st.write(
            f"**Scores recorded:** {number_of_scores}"
        )

        st.write(
            f"**Calculation:** {explanation}"
        )

        if number_of_scores < 20:
            st.progress(number_of_scores / 20)

            st.write(
                f"{number_of_scores} of 20 scores recorded"
            )

        else:
            st.write(
                "Full 20-score scoring record established."
            )


# -----------------------------
# Score history
# -----------------------------
st.divider()
st.subheader("Score history")

if st.session_state.rounds:

    display_df = pd.DataFrame(
        st.session_state.rounds
    )

    display_df = display_df.sort_values(
        "Date",
        ascending=False
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


# -----------------------------
# Reset for testing
# -----------------------------
st.divider()

if st.button("Clear all test scores"):

    st.session_state.rounds = []

    st.rerun()