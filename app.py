import streamlit as st
import requests
from datetime import date

st.set_page_config(
    page_title="Golf Group Handicaps",
    page_icon="⛳",
    layout="centered"
)

st.title("⛳ Golf Group Handicaps")
st.caption("Unofficial handicap tracker using WHS calculation rules")


# ---------------------------------
# Configuration
# ---------------------------------
API_BASE = "https://api.golfcourseapi.com/v1"
API_KEY = st.secrets["GOLF_API_KEY"]

HEADERS = {
    "Authorization": f"Bearer {API_KEY}"
}


# ---------------------------------
# Session storage
# ---------------------------------
if "rounds" not in st.session_state:
    st.session_state.rounds = []

if "course_results" not in st.session_state:
    st.session_state.course_results = []

if "selected_course_data" not in st.session_state:
    st.session_state.selected_course_data = None


# ---------------------------------
# API functions
# ---------------------------------
def search_courses(search_text):
    response = requests.get(
        f"{API_BASE}/search",
        headers=HEADERS,
        params={"search_query": search_text},
        timeout=15
    )

    response.raise_for_status()
    return response.json().get("courses", [])


def get_course_details(course_id):
    response = requests.get(
        f"{API_BASE}/courses/{course_id}",
        headers=HEADERS,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    # Some responses wrap the course inside {"course": {...}}
    return data.get("course", data)


# ---------------------------------
# Handicap differential
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

player = st.text_input(
    "Player",
    placeholder="e.g. Paul"
)

date_played = st.date_input(
    "Date played",
    value=date.today()
)

holes_played = st.radio(
    "Number of holes played",
    options=[18, 9],
    horizontal=True
)


# ---------------------------------
# Course search
# ---------------------------------
st.markdown("### Golf Course")

course_search = st.text_input(
    "Search golf course",
    placeholder="e.g. Brocton Hall, Mijas, The Belfry"
)

if st.button("🔎 Search courses", use_container_width=True):

    if len(course_search.strip()) < 3:
        st.warning("Please enter at least 3 characters.")

    else:

        try:
            with st.spinner("Searching golf courses..."):

                results = search_courses(
                    course_search.strip()
                )

                st.session_state.course_results = results
                st.session_state.selected_course_data = None

        except requests.exceptions.RequestException as error:

            st.error(
                "Course search failed. Please try again."
            )

            st.caption(str(error))


# ---------------------------------
# Course selection
# ---------------------------------
if st.session_state.course_results:

    result_labels = []

    for course in st.session_state.course_results:

        club = course.get("club_name", "")
        course_name = course.get("course_name", "")

        location = course.get("location", {})

        city = location.get("city", "")
        country = location.get("country", "")

        if course_name and course_name != club:
            name = f"{club} – {course_name}"
        else:
            name = club or course_name

        location_text = ", ".join(
            x for x in [city, country] if x
        )

        if location_text:
            label = f"{name} ({location_text})"
        else:
            label = name

        result_labels.append(label)

    selected_label = st.selectbox(
        "Select golf course",
        result_labels
    )

    selected_index = result_labels.index(
        selected_label
    )

    selected_summary = (
        st.session_state.course_results[
            selected_index
        ]
    )

    course_id = selected_summary.get("id")

    if course_id:

        try:

            with st.spinner(
                "Loading course and tee information..."
            ):

                course_data = get_course_details(
                    course_id
                )

                st.session_state.selected_course_data = (
                    course_data
                )

        except requests.exceptions.RequestException:

            st.error(
                "Unable to load the course details."
            )


# ---------------------------------
# Course details
# ---------------------------------
course_data = st.session_state.selected_course_data

if course_data:

    club_name = course_data.get(
        "club_name",
        ""
    )

    course_name = course_data.get(
        "course_name",
        ""
    )

    # ---------------------------------
    # Course / Layout
    # ---------------------------------
    # GolfCourseAPI treats an individual course/layout as
    # a course record. Therefore, once selected, there is
    # only one layout in this record.

    if course_name:

        course_layout = st.selectbox(
            "Course / Layout",
            [course_name],
            disabled=True
        )

    else:

        course_layout = st.selectbox(
            "Course / Layout",
            ["Main Course"],
            disabled=True
        )


    # ---------------------------------
    # Male tees only
    # ---------------------------------
    tees = course_data.get(
        "tees",
        {}
    )

    male_tees = tees.get(
        "male",
        []
    )

    # Filter tees by requested hole count where possible
    suitable_tees = []

    for tee in male_tees:

        tee_holes = tee.get("number_of_holes")

        if tee_holes is None:
            suitable_tees.append(tee)

        elif int(tee_holes) == holes_played:
            suitable_tees.append(tee)


    if not suitable_tees:

        suitable_tees = male_tees


    if suitable_tees:

        tee_names = [
            tee.get(
                "tee_name",
                "Unnamed tee"
            )
            for tee in suitable_tees
        ]

        selected_tee_name = st.selectbox(
            "Tees used",
            tee_names
        )

        selected_tee_index = tee_names.index(
            selected_tee_name
        )

        selected_tee = suitable_tees[
            selected_tee_index
        ]


        # ---------------------------------
        # Automatic ratings
        # ---------------------------------
        course_rating = selected_tee.get(
            "course_rating"
        )

        slope_rating = selected_tee.get(
            "slope_rating"
        )

        par = selected_tee.get(
            "par_total"
        )


        st.markdown(
            "#### Course rating information"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Course Rating",
                course_rating
                if course_rating is not None
                else "N/A"
            )

        with col2:
            st.metric(
                "Slope",
                slope_rating
                if slope_rating is not None
                else "N/A"
            )

        with col3:
            st.metric(
                "Par",
                par
                if par is not None
                else "N/A"
            )


        # ---------------------------------
        # Score entry
        # ---------------------------------
        if (
            course_rating is not None
            and slope_rating is not None
        ):

            adjusted_gross_score = st.number_input(
                "Adjusted Gross Score",
                min_value=20,
                max_value=200,
                value=90 if holes_played == 18 else 45,
                step=1
            )

            differential = calculate_differential(
                adjusted_gross_score,
                float(course_rating),
                int(slope_rating)
            )

            st.info(
                f"Calculated Score Differential: "
                f"**{differential:.1f}**"
            )

            if st.button(
                "Save Round",
                use_container_width=True
            ):

                if not player.strip():

                    st.error(
                        "Please enter the player's name."
                    )

                else:

                    round_record = {
                        "Player": player.strip(),
                        "Date": date_played,
                        "Holes": holes_played,
                        "Golf Course": club_name,
                        "Course / Layout": course_layout,
                        "Tees": selected_tee_name,
                        "Course Rating": course_rating,
                        "Slope Rating": slope_rating,
                        "Par": par,
                        "Adjusted Gross Score":
                            adjusted_gross_score,
                        "Score Differential":
                            round(differential, 1)
                    }

                    st.session_state.rounds.append(
                        round_record
                    )

                    st.success(
                        f"Round saved for "
                        f"{player.strip()} — "
                        f"Differential "
                        f"{differential:.1f}"
                    )

        else:

            st.warning(
                "This tee does not contain Course Rating "
                "and Slope Rating data."
            )

    else:

        st.warning(
            "No men's tee information was found "
            "for this course."
        )


# ---------------------------------
# Recent rounds
# ---------------------------------
st.divider()
st.subheader("Recent Rounds")

if not st.session_state.rounds:

    st.info(
        "No rounds have been entered yet."
    )

else:

    for round_record in reversed(
        st.session_state.rounds
    ):

        st.markdown(
            f"""
            **{round_record['Player']}**  
            {round_record['Golf Course']}  
            {round_record['Course / Layout']} •
            {round_record['Tees']} tees •
            {round_record['Holes']} holes  
            Score: **{round_record['Adjusted Gross Score']}**  
            Differential: **{round_record['Score Differential']:.1f}**
            """
        )

        st.divider()


st.caption(
    "Scores are currently stored temporarily while "
    "the app is being developed."
)