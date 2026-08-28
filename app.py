import streamlit as st
import requests
import pandas as pd
from datetime import date


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="Golf Group Handicaps",
    page_icon="⛳",
    layout="centered"
)

st.title("⛳ Golf Group Handicaps")
st.caption("Unofficial handicap tracker using WHS calculation rules")


# =========================================================
# CONFIG
# =========================================================

API_BASE = "https://api.golfcourseapi.com/v1"
API_KEY = st.secrets["GOLF_API_KEY"]

HEADERS = {
    "Authorization": f"Bearer {API_KEY}"
}

PLAYERS = [
    "Ben",
    "Brinders",
    "Chubb",
    "Colley",
    "Glenn",
    "Jase",
    "Lee",
    "Moseley",
    "Neil",
    "Nige",
    "Ricky",
    "Sexy Tim",
    "Steve",
    "Stonesy",
    "Tim the Younger"
]


# =========================================================
# SESSION STATE
# =========================================================

if "rounds" not in st.session_state:
    st.session_state.rounds = []

if "course_results" not in st.session_state:
    st.session_state.course_results = []

if "selected_course_data" not in st.session_state:
    st.session_state.selected_course_data = None


# =========================================================
# COURSE API
# =========================================================

@st.cache_data(
    ttl=86400,
    show_spinner=False
)
def search_courses(search_text):

    response = requests.get(
        f"{API_BASE}/search",
        headers=HEADERS,
        params={
            "search_query": search_text
        },
        timeout=15
    )

    response.raise_for_status()

    return response.json().get(
        "courses",
        []
    )


@st.cache_data(
    ttl=86400,
    show_spinner=False
)
def get_course_details(course_id):

    response = requests.get(
        f"{API_BASE}/courses/{course_id}",
        headers=HEADERS,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    return data.get(
        "course",
        data
    )


# =========================================================
# ROUND RATING FUNCTIONS
# =========================================================

def calculate_18_hole_differential(
    adjusted_score,
    course_rating,
    slope_rating
):

    return (
        113 / float(slope_rating)
    ) * (
        float(adjusted_score)
        - float(course_rating)
    )


def calculate_9_hole_differential(
    adjusted_score,
    course_rating,
    slope_rating
):

    return (
        113 / float(slope_rating)
    ) * (
        float(adjusted_score)
        - float(course_rating)
    )


def estimated_expected_nine(
    handicap_index
):

    # Unofficial approximation.
    # The authorised WHS system performs the
    # official expected-score calculation.

    return (
        float(handicap_index) / 2
    ) + 1.5


def calculate_9_hole_round_rating(
    played_nine_differential,
    handicap_index
):

    expected = (
        estimated_expected_nine(
            handicap_index
        )
    )

    combined = (
        played_nine_differential
        + expected
    )

    return (
        round(
            combined,
            1
        ),
        round(
            expected,
            2
        )
    )


# =========================================================
# HANDICAP INDEX
# =========================================================

def handicap_calculation(
    differentials
):

    count = len(
        differentials
    )

    if count < 3:
        return None, [], ""

    recent = (
        differentials[-20:]
    )

    indexed = list(
        enumerate(
            recent
        )
    )

    sorted_diffs = sorted(
        indexed,
        key=lambda x: x[1]
    )

    adjustment = 0.0

    if count == 3:

        number_used = 1
        adjustment = -2.0

    elif count == 4:

        number_used = 1
        adjustment = -1.0

    elif count == 5:

        number_used = 1

    elif count == 6:

        number_used = 2
        adjustment = -1.0

    elif count in [7, 8]:

        number_used = 2

    elif 9 <= count <= 11:

        number_used = 3

    elif 12 <= count <= 14:

        number_used = 4

    elif 15 <= count <= 16:

        number_used = 5

    elif 17 <= count <= 18:

        number_used = 6

    elif count == 19:

        number_used = 7

    else:

        number_used = 8

    counting = (
        sorted_diffs[
            :number_used
        ]
    )

    counting_indexes = [
        item[0]
        for item in counting
    ]

    average = (
        sum(
            item[1]
            for item in counting
        )
        / number_used
    )

    handicap_index = (
        average
        + adjustment
    )

    handicap_index = min(
        handicap_index,
        54.0
    )

    return (
        round(
            handicap_index,
            1
        ),
        counting_indexes,
        (
            f"Best {number_used} "
            f"of {min(count, 20)}"
            + (
                f", WHS adjustment "
                f"{adjustment:+.1f}"
                if adjustment != 0
                else ""
            )
        )
    )


# =========================================================
# PLAYER HELPERS
# =========================================================

def valid_player_name(
    player_name
):

    if player_name in PLAYERS:
        return player_name

    return None


def get_player_rounds(
    player_name
):

    player_name = (
        valid_player_name(
            player_name
        )
    )

    if player_name is None:
        return []

    results = [
        r
        for r in st.session_state.rounds
        if r.get("Player") == player_name
    ]

    return sorted(
        results,
        key=lambda r: r["Date"]
    )


def get_completed_holes(
    player_name
):

    player_rounds = (
        get_player_rounds(
            player_name
        )
    )

    return sum(
        int(
            r.get(
                "Holes",
                0
            )
        )
        for r in player_rounds
    )


def get_player_handicap(
    player_name
):

    player_rounds = (
        get_player_rounds(
            player_name
        )
    )

    completed_holes = sum(
        int(
            r.get(
                "Holes",
                0
            )
        )
        for r in player_rounds
    )

    if completed_holes < 54:
        return None

    completed_differentials = [
        r["Differential"]
        for r in player_rounds
        if r.get(
            "Differential"
        ) is not None
    ]

    if len(
        completed_differentials
    ) < 3:

        return None

    handicap_index, _, _ = (
        handicap_calculation(
            completed_differentials
        )
    )

    return handicap_index


def calculate_course_handicap(
    handicap_index,
    slope_rating,
    course_rating,
    par
):

    return round(
        (
            handicap_index
            * float(
                slope_rating
            )
            / 113
        )
        + (
            float(
                course_rating
            )
            - float(
                par
            )
        )
    )


def handicap_strokes_on_hole(
    course_handicap,
    stroke_index
):

    if course_handicap <= 0:
        return 0

    full_cycles = (
        course_handicap // 18
    )

    remainder = (
        course_handicap % 18
    )

    strokes = full_cycles

    if stroke_index <= remainder:
        strokes += 1

    return strokes


# =========================================================
# COURSE DATA HELPERS
# =========================================================

def get_hole_number(
    hole,
    fallback
):

    return (
        hole.get("hole")
        or hole.get("hole_number")
        or hole.get("number")
        or fallback
    )


def get_hole_par(
    hole
):

    return (
        hole.get("par")
        or hole.get("par_value")
    )


def get_stroke_index(
    hole,
    fallback
):

    value = (
        hole.get("handicap")
        or hole.get("stroke_index")
        or hole.get("hcp")
        or hole.get("handicap_index")
    )

    if value is None:
        return fallback

    return int(
        value
    )


def get_9_hole_values(
    selected_tee,
    nine_choice
):

    if nine_choice == "Front 9":

        rating_keys = [
            "front_course_rating",
            "front_nine_course_rating",
            "course_rating_front"
        ]

        slope_keys = [
            "front_slope_rating",
            "front_nine_slope_rating",
            "slope_rating_front"
        ]

        par_keys = [
            "front_par",
            "front_nine_par",
            "par_front"
        ]

    else:

        rating_keys = [
            "back_course_rating",
            "back_nine_course_rating",
            "course_rating_back"
        ]

        slope_keys = [
            "back_slope_rating",
            "back_nine_slope_rating",
            "slope_rating_back"
        ]

        par_keys = [
            "back_par",
            "back_nine_par",
            "par_back"
        ]

    rating = None
    slope = None
    par = None

    for key in rating_keys:

        if selected_tee.get(key) is not None:
            rating = selected_tee[key]
            break

    for key in slope_keys:

        if selected_tee.get(key) is not None:
            slope = selected_tee[key]
            break

    for key in par_keys:

        if selected_tee.get(key) is not None:
            par = selected_tee[key]
            break

    return (
        rating,
        slope,
        par
    )


# =========================================================
# INFORMATION BOXES
# =========================================================

def show_round_rating_info():

    with st.expander(
        "ℹ️ What is a Round Rating?"
    ):

        st.markdown(
            """
**Round Rating** is our simpler name for the WHS
**Score Differential**.

It tells you how good that round was after allowing
for the difficulty of the course and tees.

**Lower is better.**

An 85 on a difficult course can therefore have a
better Round Rating than an 82 on an easier course.

Your best Round Ratings are used to calculate your
Handicap Index.
            """
        )


def show_54_hole_info():

    with st.expander(
        "ℹ️ Why do I need 54 completed holes?"
    ):

        st.markdown(
            """
To establish your first **Handicap Index**, WHS
requires acceptable scores covering at least
**54 completed holes**.

These can be made up of **9-hole and 18-hole rounds
in any combination**.

For example:

- Three 18-hole rounds = 54 holes
- Six 9-hole rounds = 54 holes
- Two 18-hole rounds + two 9-hole rounds = 54 holes

Until you reach 54 completed holes, the app will
show your progress but will not give you an initial
Handicap Index.

Once 54 completed holes have been reached, the app
can establish your initial Handicap Index from your
eligible scores.

This app provides an **unofficial WHS-based**
Handicap Index and is not an authorised handicapping
service.
            """
        )


def show_total_score_info():

    with st.expander(
        "ℹ️ Do I need to adjust my score?"
    ):

        st.markdown(
            """
A very high score on an individual hole may need to
be reduced before you enter your total for handicap
purposes.

**If you are establishing your first Handicap
Index:**

The maximum score that counts on any hole is
**par + 5**.

For example, on a par 4, no more than **9** counts
for handicap purposes.

**If you already have a Handicap Index:**

The maximum is **net double bogey**:

**Par + 2 + any handicap strokes you receive on
that hole.**

For example, if you receive one handicap stroke on a
par 4, the maximum that counts is **7**.

If you are unsure, choose **Hole-by-hole scores** and
the app will make the adjustment automatically where
the course scorecard information is available.
            """
        )


# =========================================================
# ADD ROUND
# =========================================================

st.subheader(
    "➕ Add Round"
)


# =========================================================
# PLAYER SELECTION
# Mobile-friendly list opens DOWNWARDS
# =========================================================

st.markdown(
    "**Player**"
)

with st.expander(
    "Select player",
    expanded=False
):

    player = st.radio(
        "Choose player",
        PLAYERS,
        index=None,
        label_visibility="collapsed"
    )


if player is not None:

    st.caption(
        f"Selected player: **{player}**"
    )


# =========================================================
# DATE / HOLES
# =========================================================

date_played = st.date_input(
    "Date played",
    value=date.today()
)

holes_played = st.radio(
    "Number of holes played",
    [
        18,
        9
    ],
    horizontal=True
)


# =========================================================
# PLAYER ESTABLISHMENT PROGRESS
# =========================================================

if player is not None:

    completed_holes = (
        get_completed_holes(
            player
        )
    )

    if completed_holes < 54:

        st.markdown(
            "### Establishing Handicap Index"
        )

        shown_holes = min(
            completed_holes,
            54
        )

        st.write(
            f"**{shown_holes} of "
            f"54 completed holes**"
        )

        st.progress(
            shown_holes / 54
        )

        show_54_hole_info()


# =========================================================
# AUTOMATIC COURSE SEARCH
# =========================================================

st.markdown(
    "### Golf Course"
)

course_search = st.text_input(
    "Golf course",
    placeholder=(
        "Start typing, e.g. Brocton Hall"
    )
)

clean_search = (
    course_search.strip()
)

if len(clean_search) >= 3:

    try:

        with st.spinner(
            "Finding matching courses..."
        ):

            results = (
                search_courses(
                    clean_search
                )
            )

        st.session_state.course_results = (
            results
        )

        if not results:

            st.session_state.selected_course_data = (
                None
            )

            st.info(
                "No matching golf courses found."
            )

    except requests.exceptions.RequestException as error:

        st.session_state.course_results = []

        st.session_state.selected_course_data = (
            None
        )

        st.error(
            "Unable to search the golf course database."
        )

        st.caption(
            str(error)
        )

else:

    st.session_state.course_results = []

    st.session_state.selected_course_data = (
        None
    )


# =========================================================
# MATCHING COURSE SELECTION
# =========================================================

course_id = None

if st.session_state.course_results:

    labels = []

    for course in (
        st.session_state.course_results
    ):

        club = course.get(
            "club_name",
            ""
        )

        course_name = course.get(
            "course_name",
            ""
        )

        location = course.get(
            "location",
            {}
        )

        city = location.get(
            "city",
            ""
        )

        country = location.get(
            "country",
            ""
        )

        if (
            course_name
            and course_name != club
        ):

            name = (
                f"{club} – "
                f"{course_name}"
            )

        else:

            name = (
                club
                or course_name
            )

        location_text = ", ".join(
            x
            for x in [
                city,
                country
            ]
            if x
        )

        if location_text:

            name = (
                f"{name} "
                f"({location_text})"
            )

        labels.append(
            name
        )


    selected_label = (
        st.selectbox(
            "Matching courses",
            labels,
            index=None,
            placeholder=(
                "Select the correct course"
            )
        )
    )


    if selected_label is not None:

        selected_index = (
            labels.index(
                selected_label
            )
        )

        selected_summary = (
            st.session_state.course_results[
                selected_index
            ]
        )

        course_id = (
            selected_summary.get(
                "id"
            )
        )

        if course_id:

            try:

                with st.spinner(
                    "Loading course details..."
                ):

                    course_data = (
                        get_course_details(
                            course_id
                        )
                    )

                st.session_state.selected_course_data = (
                    course_data
                )

            except requests.exceptions.RequestException:

                st.session_state.selected_course_data = (
                    None
                )

                st.error(
                    "Unable to load course details."
                )


# =========================================================
# COURSE DETAILS
# =========================================================

course_data = (
    st.session_state.selected_course_data
)

if course_data:

    club_name = (
        course_data.get(
            "club_name",
            ""
        )
    )

    course_name = (
        course_data.get(
            "course_name",
            ""
        )
    )


    # =====================================================
    # COURSE / LAYOUT
    # =====================================================

    course_layout = (
        st.selectbox(
            "Course / Layout",
            [
                course_name
                or "Main Course"
            ],
            disabled=True
        )
    )


    # =====================================================
    # TEES
    # =====================================================

    tees = (
        course_data.get(
            "tees",
            {}
        )
    )

    male_tees = (
        tees.get(
            "male",
            []
        )
    )

    if not male_tees:

        st.warning(
            "No male tee information is available "
            "for this course."
        )

    else:

        tee_names = [
            tee.get(
                "tee_name",
                "Unnamed tee"
            )
            for tee in male_tees
        ]

        selected_tee_name = (
            st.selectbox(
                "Tees used",
                tee_names
            )
        )

        tee_index = (
            tee_names.index(
                selected_tee_name
            )
        )

        selected_tee = (
            male_tees[
                tee_index
            ]
        )

        full_course_rating = (
            selected_tee.get(
                "course_rating"
            )
        )

        full_slope_rating = (
            selected_tee.get(
                "slope_rating"
            )
        )

        full_par = (
            selected_tee.get(
                "par_total"
            )
        )

        hole_data = (
            selected_tee.get(
                "holes",
                []
            )
        )


        # =================================================
        # 9 OR 18 HOLE COURSE VALUES
        # =================================================

        nine_choice = None

        if holes_played == 9:

            nine_choice = (
                st.radio(
                    "Which 9 holes?",
                    [
                        "Front 9",
                        "Back 9"
                    ],
                    horizontal=True
                )
            )

            (
                course_rating,
                slope_rating,
                par
            ) = (
                get_9_hole_values(
                    selected_tee,
                    nine_choice
                )
            )

        else:

            course_rating = (
                full_course_rating
            )

            slope_rating = (
                full_slope_rating
            )

            par = (
                full_par
            )


        # =================================================
        # COURSE INFORMATION
        # =================================================

        st.markdown(
            "#### Course information"
        )

        c1, c2, c3 = (
            st.columns(3)
        )

        c1.metric(
            "Course Rating",
            (
                course_rating
                if course_rating is not None
                else "N/A"
            )
        )

        c2.metric(
            "Slope",
            (
                slope_rating
                if slope_rating is not None
                else "N/A"
            )
        )

        c3.metric(
            "Par",
            (
                par
                if par is not None
                else "N/A"
            )
        )


        # =================================================
        # VALIDATE RATING DATA
        # =================================================

        if (
            course_rating is None
            or slope_rating is None
        ):

            if holes_played == 9:

                st.warning(
                    "This course record does not "
                    "contain a valid 9-hole Course "
                    "Rating and Slope Rating for "
                    "this nine."
                )

                st.caption(
                    "WHS requires a valid 9-hole "
                    "Course Rating and Slope Rating "
                    "before a 9-hole score can be "
                    "used."
                )

            else:

                st.warning(
                    "Course Rating or Slope Rating "
                    "is unavailable for these tees."
                )


        else:

            # =============================================
            # CURRENT PLAYER HANDICAP
            # =============================================

            existing_handicap = (
                get_player_handicap(
                    player
                )
                if player is not None
                else None
            )


            # =============================================
            # SCORE ENTRY METHOD
            # =============================================

            st.markdown(
                "### Enter your score"
            )

            entry_method = (
                st.radio(
                    "Entry method",
                    [
                        "Total gross score",
                        "Hole-by-hole scores"
                    ]
                )
            )


            # =============================================
            # TOTAL GROSS SCORE
            # =============================================

            if (
                entry_method
                ==
                "Total gross score"
            ):

                show_total_score_info()

                default_score = (
                    90
                    if holes_played == 18
                    else 45
                )

                minimum_score = (
                    40
                    if holes_played == 18
                    else 20
                )

                maximum_score = (
                    200
                    if holes_played == 18
                    else 100
                )

                handicap_score = (
                    st.number_input(
                        "Gross score for handicap purposes",
                        min_value=minimum_score,
                        max_value=maximum_score,
                        value=default_score,
                        step=1
                    )
                )

                round_rating = None
                expected_nine = None


                # =========================================
                # CALCULATE ROUND RATING
                # =========================================

                if holes_played == 18:

                    round_rating = (
                        calculate_18_hole_differential(
                            handicap_score,
                            course_rating,
                            slope_rating
                        )
                    )

                else:

                    played_nine = (
                        calculate_9_hole_differential(
                            handicap_score,
                            course_rating,
                            slope_rating
                        )
                    )

                    if existing_handicap is not None:

                        (
                            round_rating,
                            expected_nine
                        ) = (
                            calculate_9_hole_round_rating(
                                played_nine,
                                existing_handicap
                            )
                        )


                # =========================================
                # ROUND RATING DISPLAY
                # =========================================

                if round_rating is not None:

                    st.metric(
                        "Round Rating",
                        f"{round_rating:.1f}"
                    )

                    show_round_rating_info()

                    if holes_played == 9:

                        with st.expander(
                            "ℹ️ How was this 9-hole "
                            "Round Rating created?"
                        ):

                            st.markdown(
                                f"""
Your played nine produces a 9-hole performance
differential.

WHS combines that with an **expected score** for the
other nine based on your Handicap Index.

For this unofficial tracker, the expected component
is estimated at **{expected_nine:.2f}**.

The authorised WHS handicapping system uses its own
expected-score calculation, so the official result
may differ slightly.
                                """
                            )

                elif holes_played == 9:

                    st.info(
                        "This 9-hole score will count "
                        "towards your **54 completed "
                        "holes**. A full Round Rating "
                        "cannot yet be created because "
                        "you do not have an established "
                        "Handicap Index."
                    )


                # =========================================
                # SAVE TOTAL ROUND
                # =========================================

                if st.button(
                    "Save Round",
                    use_container_width=True,
                    key="save_total_round"
                ):

                    if player is None:

                        st.error(
                            "Please select a player."
                        )

                    else:

                        st.session_state.rounds.append(
                            {
                                "Player":
                                    player,

                                "Date":
                                    date_played,

                                "Holes":
                                    holes_played,

                                "Nine":
                                    nine_choice,

                                "Golf Course":
                                    club_name,

                                "Course / Layout":
                                    course_layout,

                                "Tees":
                                    selected_tee_name,

                                "Course Rating":
                                    course_rating,

                                "Slope Rating":
                                    slope_rating,

                                "Par":
                                    par,

                                "Gross Score":
                                    handicap_score,

                                "Adjusted Score":
                                    handicap_score,

                                "Differential":
                                    (
                                        round(
                                            round_rating,
                                            1
                                        )
                                        if round_rating is not None
                                        else None
                                    ),

                                "Entry Method":
                                    "Total",

                                "Expected Nine":
                                    expected_nine
                            }
                        )

                        st.success(
                            "Round saved."
                        )

                        st.rerun()


            # =============================================
            # HOLE-BY-HOLE SCORE ENTRY
            # =============================================

            else:

                required_holes = (
                    18
                    if holes_played == 18
                    else 9
                )

                if holes_played == 18:

                    holes_for_round = (
                        hole_data[:18]
                    )

                elif nine_choice == "Front 9":

                    holes_for_round = (
                        hole_data[:9]
                    )

                else:

                    holes_for_round = (
                        hole_data[9:18]
                    )


                # =========================================
                # CHECK SCORECARD DATA
                # =========================================

                if (
                    len(
                        holes_for_round
                    )
                    < required_holes
                ):

                    st.warning(
                        "Complete hole-by-hole "
                        "scorecard data isn't available "
                        "for this selection."
                    )

                    st.info(
                        "Please choose "
                        "**Total gross score** instead."
                    )


                else:

                    course_handicap = None

                    if (
                        existing_handicap is not None
                        and full_course_rating is not None
                        and full_slope_rating is not None
                        and full_par is not None
                    ):

                        course_handicap = (
                            calculate_course_handicap(
                                existing_handicap,
                                full_slope_rating,
                                full_course_rating,
                                full_par
                            )
                        )

                        h1, h2 = (
                            st.columns(2)
                        )

                        h1.metric(
                            "Handicap Index",
                            f"{existing_handicap:.1f}"
                        )

                        h2.metric(
                            "Course Handicap",
                            course_handicap
                        )


                    # =====================================
                    # HOLE SCORES
                    # =====================================

                    raw_scores = []
                    adjusted_scores = []
                    adjustment_details = []

                    st.markdown(
                        "#### Hole scores"
                    )

                    for i, hole in enumerate(
                        holes_for_round
                    ):

                        fallback_hole = (
                            i + 1
                            if (
                                holes_played == 18
                                or nine_choice == "Front 9"
                            )
                            else i + 10
                        )

                        hole_number = (
                            get_hole_number(
                                hole,
                                fallback_hole
                            )
                        )

                        hole_par = (
                            get_hole_par(
                                hole
                            )
                        )

                        stroke_index = (
                            get_stroke_index(
                                hole,
                                fallback_hole
                            )
                        )

                        if hole_par is None:
                            hole_par = 4


                        # =================================
                        # WHS MAXIMUM HOLE SCORE
                        # =================================

                        if (
                            existing_handicap is None
                            or course_handicap is None
                        ):

                            maximum_hole_score = (
                                int(
                                    hole_par
                                )
                                + 5
                            )

                        else:

                            strokes_received = (
                                handicap_strokes_on_hole(
                                    course_handicap,
                                    stroke_index
                                )
                            )

                            maximum_hole_score = (
                                int(
                                    hole_par
                                )
                                + 2
                                + strokes_received
                            )


                        # =================================
                        # SCORE INPUT
                        # =================================

                        col1, col2 = (
                            st.columns(
                                [
                                    1,
                                    1
                                ]
                            )
                        )

                        with col1:

                            st.write(
                                f"**Hole "
                                f"{hole_number}**  \n"
                                f"Par {hole_par} • "
                                f"SI {stroke_index}"
                            )

                        with col2:

                            score = (
                                st.number_input(
                                    f"Hole "
                                    f"{hole_number}",
                                    min_value=1,
                                    max_value=20,
                                    value=int(
                                        hole_par
                                    ),
                                    step=1,
                                    key=(
                                        f"score_"
                                        f"{course_id}_"
                                        f"{selected_tee_name}_"
                                        f"{holes_played}_"
                                        f"{nine_choice}_"
                                        f"{hole_number}"
                                    ),
                                    label_visibility=(
                                        "collapsed"
                                    )
                                )
                            )

                        raw_scores.append(
                            int(
                                score
                            )
                        )

                        adjusted = min(
                            int(
                                score
                            ),
                            maximum_hole_score
                        )

                        adjusted_scores.append(
                            adjusted
                        )

                        if adjusted < score:

                            adjustment_details.append(
                                (
                                    hole_number,
                                    score,
                                    adjusted
                                )
                            )


                    # =====================================
                    # ROUND TOTALS
                    # =====================================

                    gross_score = sum(
                        raw_scores
                    )

                    adjusted_score = sum(
                        adjusted_scores
                    )

                    round_rating = None
                    expected_nine = None


                    if holes_played == 18:

                        round_rating = (
                            calculate_18_hole_differential(
                                adjusted_score,
                                course_rating,
                                slope_rating
                            )
                        )

                    else:

                        played_nine = (
                            calculate_9_hole_differential(
                                adjusted_score,
                                course_rating,
                                slope_rating
                            )
                        )

                        if existing_handicap is not None:

                            (
                                round_rating,
                                expected_nine
                            ) = (
                                calculate_9_hole_round_rating(
                                    played_nine,
                                    existing_handicap
                                )
                            )


                    # =====================================
                    # ROUND SUMMARY
                    # =====================================

                    st.markdown(
                        "### Round summary"
                    )

                    s1, s2 = (
                        st.columns(2)
                    )

                    s1.metric(
                        "Gross score",
                        gross_score
                    )

                    if round_rating is not None:

                        s2.metric(
                            "Round Rating",
                            f"{round_rating:.1f}"
                        )

                        show_round_rating_info()

                    else:

                        s2.metric(
                            "Round Rating",
                            "Pending"
                        )


                    if adjusted_score != gross_score:

                        st.info(
                            "Score used for handicap "
                            f"purposes: "
                            f"**{adjusted_score}**"
                        )

                        with st.expander(
                            "See automatic score adjustments"
                        ):

                            for (
                                hole_number,
                                original,
                                adjusted
                            ) in adjustment_details:

                                st.write(
                                    f"Hole "
                                    f"{hole_number}: "
                                    f"{original} → "
                                    f"{adjusted}"
                                )


                    # =====================================
                    # SAVE HOLE-BY-HOLE ROUND
                    # =====================================

                    if st.button(
                        "Save Round",
                        use_container_width=True,
                        key="save_hole_round"
                    ):

                        if player is None:

                            st.error(
                                "Please select a player."
                            )

                        else:

                            st.session_state.rounds.append(
                                {
                                    "Player":
                                        player,

                                    "Date":
                                        date_played,

                                    "Holes":
                                        holes_played,

                                    "Nine":
                                        nine_choice,

                                    "Golf Course":
                                        club_name,

                                    "Course / Layout":
                                        course_layout,

                                    "Tees":
                                        selected_tee_name,

                                    "Course Rating":
                                        course_rating,

                                    "Slope Rating":
                                        slope_rating,

                                    "Par":
                                        par,

                                    "Gross Score":
                                        gross_score,

                                    "Adjusted Score":
                                        adjusted_score,

                                    "Differential":
                                        (
                                            round(
                                                round_rating,
                                                1
                                            )
                                            if round_rating is not None
                                            else None
                                        ),

                                    "Entry Method":
                                        "Hole-by-hole",

                                    "Hole Scores":
                                        raw_scores,

                                    "Expected Nine":
                                        expected_nine
                                }
                            )

                            st.success(
                                "Round saved."
                            )

                            st.rerun()


# =========================================================
# PLAYER HANDICAPS
# =========================================================

st.divider()

st.subheader(
    "🏌️ Player Handicaps"
)

if not st.session_state.rounds:

    st.info(
        "No scores have been recorded yet."
    )

else:

    df = pd.DataFrame(
        st.session_state.rounds
    )

    players_with_scores = [
        p
        for p in PLAYERS
        if p in df[
            "Player"
        ].unique()
    ]


    # =====================================================
    # PLAYER RECORD SELECTOR
    # =====================================================

    selected_player = (
        st.selectbox(
            "View player",
            players_with_scores
        )
    )

    player_df = (
        df[
            df["Player"]
            == selected_player
        ]
        .sort_values(
            "Date"
        )
        .reset_index(
            drop=True
        )
    )

    completed_holes = int(
        player_df[
            "Holes"
        ].sum()
    )


    # =====================================================
    # INITIAL HANDICAP STATUS
    # =====================================================

    if completed_holes < 54:

        st.markdown(
            "### Establishing Handicap Index"
        )

        st.write(
            f"**{completed_holes} of "
            f"54 completed holes**"
        )

        st.progress(
            min(
                completed_holes / 54,
                1.0
            )
        )

        show_54_hole_info()


    else:

        differentials = [
            value
            for value
            in player_df[
                "Differential"
            ].tolist()
            if pd.notna(
                value
            )
        ]

        (
            handicap_index,
            counting_indexes,
            explanation
        ) = (
            handicap_calculation(
                differentials
            )
        )


        if handicap_index is None:

            st.warning(
                "54 completed holes have been "
                "recorded, but there is not yet "
                "enough completed Round Rating "
                "information to establish the "
                "Handicap Index automatically."
            )

            st.caption(
                "This can occur when the initial "
                "54 holes include 9-hole scores "
                "whose official expected-score "
                "values are not available to this "
                "unofficial tracker."
            )


        else:

            st.metric(
                "Handicap Index",
                f"{handicap_index:.1f}"
            )

            st.caption(
                "Unofficial WHS-based calculation"
            )

            st.write(
                f"**{explanation}**"
            )


    # =====================================================
    # SCORING RECORD
    # =====================================================

    st.markdown(
        "### Scoring Record"
    )

    display_df = (
        player_df.copy()
    )

    if (
        "Differential"
        in display_df.columns
    ):

        display_df[
            "Round Rating"
        ] = (
            display_df[
                "Differential"
            ]
        )

    display_columns = [
        "Date",
        "Golf Course",
        "Tees",
        "Holes",
        "Gross Score",
        "Round Rating"
    ]

    available_columns = [
        col
        for col in display_columns
        if col in display_df.columns
    ]

    display_df = (
        display_df[
            available_columns
        ]
        .sort_values(
            "Date",
            ascending=False
        )
    )

    st.dataframe(
        display_df,
        hide_index=True,
        use_container_width=True
    )

    show_round_rating_info()


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Golf Group Handicaps provides an "
    "unofficial WHS-based handicap estimate "
    "and is not an authorised handicapping service."
)