import streamlit as st
import requests
import pandas as pd
import json
import hashlib
import hmac
from datetime import date


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="Handicap Builder",
    page_icon="⛳",
    layout="centered"
)


# =========================================================
# PREMIUM VISUAL THEME
# =========================================================

st.markdown(
    """
<style>

:root {
    --green: #0f3d2f;
    --green-dark: #0a2b22;
    --cream: #f6f1e8;
    --gold: #b69a5a;
    --text: #15251f;
    --muted: #6a756f;
    --line: #ddd6c8;
}

.stApp {
    background: linear-gradient(
        180deg,
        #fbf8f2 0%,
        #f7f3eb 100%
    );

    color: var(--text);
}

.block-container {
    max-width: 760px;
    padding-top: 0.8rem;
    padding-bottom: 4rem;
}

h1,
h2,
h3,
h4 {
    color: var(--green-dark) !important;
    letter-spacing: -0.025em;
}

h2 {
    font-size: 2rem !important;
    margin-top: 1.3rem !important;
}

h3 {
    font-size: 1.35rem !important;
}

[data-testid="stCaptionContainer"] {
    color: var(--muted) !important;
}

.secondary-section-title {
    color: var(--green-dark);
    font-size: 1.55rem;
    font-weight: 700;
    letter-spacing: -0.025em;
    margin-top: 0.4rem;
    margin-bottom: 1rem;
}


/* =====================================================
   HERO
   ===================================================== */

.golf-hero {

    background:
        radial-gradient(
            circle at 85% 10%,
            rgba(182,154,90,0.13),
            transparent 28%
        ),
        linear-gradient(
            135deg,
            #071f19 0%,
            #0b3126 55%,
            #124333 100%
        );

    border-radius:
        0 0 28px 28px;

    padding:
        34px 24px 30px 24px;

    margin:
        0.8rem -1rem 1.9rem -1rem;

    box-shadow:
        0 16px 34px rgba(10,43,34,0.19);

    border-bottom:
        1px solid rgba(182,154,90,0.42);
}

.golf-hero-title {

    color:
        #ffffff;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size:
        2.55rem;

    line-height:
        1.15;

    font-weight:
        700;

    letter-spacing:
        -0.035em;

    margin-bottom:
        13px;
}

.golf-hero-subtitle {

    color:
        rgba(255,255,255,0.80);

    font-size:
        0.97rem;

    line-height:
        1.55;

    max-width:
        610px;
}


/* =====================================================
   BUTTONS
   ===================================================== */

.stButton > button {

    min-height:
        50px;

    border-radius:
        14px;

    border:
        1px solid #dad4c8;

    background:
        #ffffff;

    color:
        var(--green-dark);

    font-weight:
        650;

    box-shadow:
        0 4px 12px rgba(22,45,35,0.05);
}

.stButton > button:hover {

    border-color:
        var(--gold);

    color:
        var(--green-dark);

    background:
        #fffefa;
}

.stButton > button[kind="primary"],
button[data-testid="stBaseButton-primary"] {

    background:
        var(--green-dark) !important;

    color:
        #ffffff !important;

    border-color:
        var(--green-dark) !important;
}

.stButton > button[kind="primary"] *,
button[data-testid="stBaseButton-primary"] * {

    color:
        #ffffff !important;
}

.stButton > button:disabled {
    opacity: 0.47;
}


/* =====================================================
   INPUTS
   ===================================================== */

[data-baseweb="input"],
[data-baseweb="select"] > div,
[data-testid="stDateInput"] input,
.stTextInput input {

    border-radius:
        12px !important;
}


/* =====================================================
   GROSS SCORE
   ===================================================== */

.gross-score-heading {

    color:
        var(--green-dark);

    font-size:
        0.82rem;

    font-weight:
        750;

    letter-spacing:
        0.06em;

    text-transform:
        uppercase;

    margin-top:
        0.5rem;

    margin-bottom:
        0.35rem;
}

.gross-score-box
[data-testid="stNumberInput"]
input {

    min-height:
        78px !important;

    background:
        #ffffff !important;

    color:
        var(--green-dark) !important;

    font-size:
        2rem !important;

    font-weight:
        800 !important;

    letter-spacing:
        -0.04em !important;
}


/* =====================================================
   METRICS
   ===================================================== */

[data-testid="stMetric"] {

    background:
        rgba(255,255,255,0.94);

    border:
        1px solid #e1dbcf;

    border-radius:
        16px;

    padding:
        15px 16px;
}

[data-testid="stMetricLabel"] {

    color:
        var(--muted);

    font-size:
        0.75rem;

    text-transform:
        uppercase;

    letter-spacing:
        0.055em;
}

[data-testid="stMetricValue"] {

    color:
        var(--green-dark);

    font-weight:
        800;
}


/* =====================================================
   EXPANDERS
   ===================================================== */

[data-testid="stExpander"] {

    background:
        rgba(255,255,255,0.94);

    border:
        1px solid #e2dcd0;

    border-radius:
        14px;

    overflow:
        hidden;
}


/* =====================================================
   ALERTS
   ===================================================== */

[data-testid="stAlert"] {
    border-radius: 14px;
}


/* =====================================================
   DIVIDERS
   ===================================================== */

hr {

    border-color:
        var(--line) !important;

    margin-top:
        2rem !important;

    margin-bottom:
        1.6rem !important;
}


/* =====================================================
   FORM LABEL VISIBILITY
   ===================================================== */

[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
[data-testid="stRadio"] > label,
[data-testid="stRadio"] > label p {

    color:
        #15251f !important;

    font-weight:
        650 !important;
}

[data-testid="stDateInput"] label p,
[data-testid="stSelectbox"] label p,
[data-testid="stTextInput"] label p,
[data-testid="stNumberInput"] label p {

    color:
        #15251f !important;

    font-weight:
        650 !important;
}


/* =====================================================
   RADIO SELECTORS
   ===================================================== */

[data-testid="stRadio"]
div[role="radiogroup"] {

    display:
        flex !important;

    gap:
        12px !important;

    flex-wrap:
        wrap !important;
}

[data-testid="stRadio"]
div[role="radiogroup"] > label {

    background:
        #ffffff !important;

    border:
        1px solid #d8d0c2 !important;

    border-radius:
        14px !important;

    padding:
        10px 22px !important;

    min-width:
        100px !important;

    min-height:
        48px !important;

    box-shadow:
        0 4px 12px rgba(20,45,35,0.05) !important;
}

[data-testid="stRadio"]
div[role="radiogroup"] > label p {

    color:
        #0a2b22 !important;

    font-size:
        1rem !important;

    font-weight:
        750 !important;
}

[data-testid="stRadio"]
div[role="radiogroup"]
> label:has(input:checked) {

    border-color:
        #0f3d2f !important;

    background:
        #f4f7f5 !important;

    box-shadow:
        0 5px 14px rgba(15,61,47,0.09) !important;
}

[data-testid="stRadio"]
div[role="radiogroup"]
> label:has(input:checked) p {

    color:
        #0a2b22 !important;

    font-weight:
        800 !important;
}


/* =====================================================
   MOBILE
   ===================================================== */

@media (max-width: 640px) {

    .block-container {

        padding-left:
            1rem;

        padding-right:
            1rem;
    }

    .golf-hero {

        padding:
            30px 18px 26px 18px;

        margin:
            0.8rem -1rem 1.8rem -1rem;
    }

    .golf-hero-title {

        font-size:
            2.15rem;
    }

    .stButton > button {

        min-height:
            52px;
    }
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# HERO
# =========================================================

st.markdown(
"""<div class="golf-hero">
<div class="golf-hero-title">Handicap Builder</div>
<div class="golf-hero-subtitle">Track rounds, compare performances and build an unofficial WHS-based Handicap Index.</div>
</div>""",
    unsafe_allow_html=True
)


# =========================================================
# CONFIG
# =========================================================

GOLF_API_BASE = (
    "https://api.golfcourseapi.com/v1"
)

GOLF_API_KEY = (
    st.secrets["GOLF_API_KEY"]
)

SUPABASE_URL = (
    st.secrets["SUPABASE_URL"]
)

SUPABASE_KEY = (
    st.secrets["SUPABASE_KEY"]
)

ADMIN_PIN = (
    st.secrets["ADMIN_PIN"]
)


GOLF_HEADERS = {
    "Authorization":
        f"Bearer {GOLF_API_KEY}"
}


SUPABASE_HEADERS = {

    "apikey":
        SUPABASE_KEY,

    "Content-Type":
        "application/json"
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


class DuplicateRoundError(Exception):
    pass


# =========================================================
# SESSION STATE
# =========================================================

DEFAULT_SESSION_VALUES = {

    "selected_player_entry":
        None,

    "player_menu_open":
        False,

    "selected_course_id":
        None,

    "selected_course_label":
        None,

    "selected_course_short_label":
        None,

    "selected_course_data":
        None,

    "course_menu_open":
        False,

    "last_saved_round_fingerprint":
        None,

    "saved_round_summary":
        None,

    "admin_authenticated":
        False,

    "pending_delete_round_id":
        None
}


for key, value in (
    DEFAULT_SESSION_VALUES.items()
):

    if key not in st.session_state:

        st.session_state[key] = (
            value
        )


# =========================================================
# SUPABASE
# =========================================================

@st.cache_data(
    ttl=3600,
    show_spinner=False
)
def load_players_from_database():

    response = requests.get(

        f"{SUPABASE_URL}/rest/v1/players",

        headers=
            SUPABASE_HEADERS,

        params={
            "select":
                "id,name",

            "order":
                "name.asc"
        },

        timeout=15
    )

    response.raise_for_status()

    return response.json()


@st.cache_data(
    ttl=10,
    show_spinner=False
)
def load_rounds_from_database():

    response = requests.get(

        f"{SUPABASE_URL}/rest/v1/rounds",

        headers=
            SUPABASE_HEADERS,

        params={

            "select":
                "*",

            "order":
                "date_played.asc,created_at.asc"
        },

        timeout=15
    )

    response.raise_for_status()

    return response.json()


def save_round_to_database(
    round_data
):

    response = requests.post(

        f"{SUPABASE_URL}/rest/v1/rounds",

        headers={

            **SUPABASE_HEADERS,

            "Prefer":
                "return=minimal"
        },

        json=
            round_data,

        timeout=15
    )

    if not response.ok:

        text = (
            response.text.lower()
        )

        if (
            "already been submitted"
            in text
            or
            "duplicate"
            in text
        ):

            raise DuplicateRoundError()

        response.raise_for_status()


def delete_round_from_database(
    round_id
):

    response = requests.delete(

        f"{SUPABASE_URL}/rest/v1/rounds",

        headers={

            **SUPABASE_HEADERS,

            "Prefer":
                "return=minimal"
        },

        params={
            "id":
                f"eq.{round_id}"
        },

        timeout=15
    )

    response.raise_for_status()


# =========================================================
# LOAD DATA
# =========================================================

try:

    database_players = (
        load_players_from_database()
    )

    database_rounds = (
        load_rounds_from_database()
    )


except requests.exceptions.RequestException as error:

    st.error(
        "Unable to connect to the handicap database."
    )

    st.caption(
        str(error)
    )

    st.stop()


PLAYER_ID_BY_NAME = {

    row["name"]:
        row["id"]

    for row in database_players
}


PLAYER_NAME_BY_ID = {

    row["id"]:
        row["name"]

    for row in database_players
}


all_rounds = []


for row in database_rounds:

    player_name = (
        PLAYER_NAME_BY_ID.get(
            row.get("player_id")
        )
    )

    if player_name is None:
        continue


    date_value = (
        row.get("date_played")
    )


    try:

        date_value = (
            pd.to_datetime(
                date_value
            ).date()
        )

    except Exception:
        pass


    all_rounds.append(
        {

            "ID":
                row.get("id"),

            "Player":
                player_name,

            "Date":
                date_value,

            "Holes":
                row.get("holes"),

            "Nine":
                row.get("nine"),

            "Golf Course":
                row.get("golf_course"),

            "Course / Layout":
                row.get("course_layout"),

            "Course API ID":
                row.get("course_api_id"),

            "Tees":
                row.get("tees"),

            "Course Rating":
                row.get("course_rating"),

            "Slope Rating":
                row.get("slope_rating"),

            "Par":
                row.get("par"),

            "Gross Score":
                row.get("gross_score"),

            "Adjusted Score":
                row.get("adjusted_score"),

            "Differential":
                row.get("round_rating"),

            "Entry Method":
                row.get("entry_method"),

            "Hole Scores":
                row.get("hole_scores"),

            "Expected Nine":
                row.get("expected_nine"),

            "Created At":
                row.get("created_at")
        }
    )


# =========================================================
# COURSE API
# =========================================================

@st.cache_data(
    ttl=86400,
    show_spinner=False
)
def search_courses(
    search_text
):

    response = requests.get(

        f"{GOLF_API_BASE}/search",

        headers=
            GOLF_HEADERS,

        params={
            "search_query":
                search_text
        },

        timeout=15
    )

    response.raise_for_status()

    return (
        response.json().get(
            "courses",
            []
        )
    )


@st.cache_data(
    ttl=86400,
    show_spinner=False
)
def get_course_details(
    course_id
):

    response = requests.get(

        f"{GOLF_API_BASE}/courses/{course_id}",

        headers=
            GOLF_HEADERS,

        timeout=15
    )

    response.raise_for_status()

    data = (
        response.json()
    )

    return data.get(
        "course",
        data
    )


# =========================================================
# HANDICAP MATH
# =========================================================

def calculate_differential(
    adjusted_score,
    course_rating,
    slope_rating
):

    return (

        113
        /
        float(
            slope_rating
        )

    ) * (

        float(
            adjusted_score
        )

        -

        float(
            course_rating
        )
    )


def estimated_expected_nine(
    handicap_index
):

    return (
        float(
            handicap_index
        )
        / 2
    ) + 1.5


def handicap_calculation(
    differentials
):

    clean = [

        float(value)

        for value
        in differentials

        if (
            value is not None
            and
            pd.notna(value)
        )
    ]


    count = len(
        clean
    )


    if count < 3:

        return (
            None,
            [],
            ""
        )


    recent = (
        clean[-20:]
    )


    sorted_diffs = sorted(

        enumerate(
            recent
        ),

        key=lambda x:
            x[1]
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


    average = (

        sum(
            item[1]
            for item
            in counting
        )

        /

        number_used
    )


    handicap_index = min(

        average
        +
        adjustment,

        54.0
    )


    explanation = (

        f"Best {number_used} "
        f"of {min(count, 20)}"
    )


    if adjustment:

        explanation += (

            f", WHS adjustment "
            f"{adjustment:+.1f}"
        )


    return (

        round(
            handicap_index,
            1
        ),

        [
            item[0]
            for item
            in counting
        ],

        explanation
    )


# =========================================================
# 9-HOLE ROUND HANDLING
# =========================================================

def raw_nine_differential(
    round_item
):

    if int(
        round_item.get(
            "Holes"
        )
        or 0
    ) != 9:

        return None


    adjusted = (
        round_item.get(
            "Adjusted Score"
        )
    )

    rating = (
        round_item.get(
            "Course Rating"
        )
    )

    slope = (
        round_item.get(
            "Slope Rating"
        )
    )


    if (
        adjusted is None
        or
        rating is None
        or
        slope in [None, 0]
    ):

        return None


    return calculate_differential(

        adjusted,
        rating,
        slope
    )


def eighteen_differential(
    round_item
):

    if int(
        round_item.get(
            "Holes"
        )
        or 0
    ) != 18:

        return None


    if (
        round_item.get(
            "Differential"
        )
        is not None
    ):

        return float(
            round_item[
                "Differential"
            ]
        )


    adjusted = (
        round_item.get(
            "Adjusted Score"
        )
    )

    rating = (
        round_item.get(
            "Course Rating"
        )
    )

    slope = (
        round_item.get(
            "Slope Rating"
        )
    )


    if (
        adjusted is None
        or
        rating is None
        or
        slope in [None, 0]
    ):

        return None


    return calculate_differential(

        adjusted,
        rating,
        slope
    )


def build_effective_round_ratings(
    player_rounds
):

    total_holes = sum(

        int(
            round_item.get(
                "Holes"
            )
            or 0
        )

        for round_item
        in player_rounds
    )


    effective = []


    for round_item in player_rounds:

        holes = int(
            round_item.get(
                "Holes"
            )
            or 0
        )


        if holes == 18:

            effective.append(
                eighteen_differential(
                    round_item
                )
            )


        elif (
            holes == 9
            and
            round_item.get(
                "Differential"
            )
            is not None
        ):

            effective.append(

                float(
                    round_item[
                        "Differential"
                    ]
                )
            )


        else:

            effective.append(
                None
            )


    if total_holes < 54:

        return effective


    # -----------------------------------------------------
    # Build a starting Handicap Index estimate.
    #
    # Doubling the raw 9-hole differential here is ONLY
    # used as a temporary seed for the calculation.
    # It is not presented as the player's Round Rating.
    # -----------------------------------------------------

    seed_diffs = []


    for round_item in player_rounds:

        holes = int(
            round_item.get(
                "Holes"
            )
            or 0
        )


        if holes == 18:

            diff = (
                eighteen_differential(
                    round_item
                )
            )

            if diff is not None:

                seed_diffs.append(
                    diff
                )


        elif holes == 9:

            raw9 = (
                raw_nine_differential(
                    round_item
                )
            )

            if raw9 is not None:

                seed_diffs.append(
                    raw9 * 2
                )


    seed_hi, _, _ = (
        handicap_calculation(
            seed_diffs
        )
    )


    if seed_hi is None:

        return effective


    working_hi = (
        seed_hi
    )


    # -----------------------------------------------------
    # Iterate the expected-nine calculation.
    # -----------------------------------------------------

    for _ in range(8):

        candidate = []


        for round_item in player_rounds:

            holes = int(
                round_item.get(
                    "Holes"
                )
                or 0
            )


            if holes == 18:

                diff = (
                    eighteen_differential(
                        round_item
                    )
                )


            elif holes == 9:

                stored = (
                    round_item.get(
                        "Differential"
                    )
                )


                if stored is not None:

                    diff = float(
                        stored
                    )


                else:

                    raw9 = (
                        raw_nine_differential(
                            round_item
                        )
                    )


                    if raw9 is not None:

                        diff = (

                            raw9

                            +

                            estimated_expected_nine(
                                working_hi
                            )
                        )

                    else:

                        diff = None


            else:

                diff = None


            if diff is not None:

                candidate.append(
                    diff
                )


        new_hi, _, _ = (
            handicap_calculation(
                candidate
            )
        )


        if new_hi is None:
            break


        if abs(
            new_hi
            -
            working_hi
        ) < 0.05:

            working_hi = (
                new_hi
            )

            break


        working_hi = (
            new_hi
        )


    final_effective = []


    for round_item in player_rounds:

        holes = int(
            round_item.get(
                "Holes"
            )
            or 0
        )


        if holes == 18:

            diff = (
                eighteen_differential(
                    round_item
                )
            )


        elif holes == 9:

            stored = (
                round_item.get(
                    "Differential"
                )
            )


            if stored is not None:

                diff = float(
                    stored
                )


            else:

                raw9 = (
                    raw_nine_differential(
                        round_item
                    )
                )


                if raw9 is not None:

                    diff = (

                        raw9

                        +

                        estimated_expected_nine(
                            working_hi
                        )
                    )

                else:

                    diff = None


        else:

            diff = None


        final_effective.append(

            round(
                diff,
                1
            )

            if diff is not None

            else None
        )


    return final_effective


# =========================================================
# PLAYER HELPERS
# =========================================================

def get_player_rounds(
    player_name
):

    return sorted(

        [

            round_item

            for round_item
            in all_rounds

            if (
                round_item.get(
                    "Player"
                )
                ==
                player_name
            )
        ],

        key=lambda round_item:
            round_item.get(
                "Date"
            )
    )


def get_completed_holes(
    player_name
):

    return sum(

        int(
            round_item.get(
                "Holes"
            )
            or 0
        )

        for round_item
        in get_player_rounds(
            player_name
        )
    )


def get_player_handicap(
    player_name
):

    player_rounds = (
        get_player_rounds(
            player_name
        )
    )


    total_holes = sum(

        int(
            round_item.get(
                "Holes"
            )
            or 0
        )

        for round_item
        in player_rounds
    )


    if total_holes < 54:

        return None


    effective = (
        build_effective_round_ratings(
            player_rounds
        )
    )


    handicap_index, _, _ = (
        handicap_calculation(

            [
                value
                for value
                in effective
                if value is not None
            ]
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

        float(
            handicap_index
        )

        *

        float(
            slope_rating
        )

        /

        113

        +

        (
            float(
                course_rating
            )

            -

            float(
                par
            )
        )
    )


def handicap_strokes_on_hole(

    course_handicap,
    stroke_index
):

    if stroke_index is None:

        return None


    if course_handicap <= 0:

        return 0


    full_cycles = (
        course_handicap
        //
        18
    )


    remainder = (
        course_handicap
        %
        18
    )


    strokes = (
        full_cycles
    )


    if (
        stroke_index
        <=
        remainder
    ):

        strokes += 1


    return strokes


# =========================================================
# COURSE / HOLE HELPERS
# =========================================================

def build_course_labels(
    course
):

    club = (
        course.get(
            "club_name",
            ""
        )
    )


    course_name = (
        course.get(
            "course_name",
            ""
        )
    )


    location = (
        course.get(
            "location",
            {}
        )
        or {}
    )


    if (
        course_name
        and
        course_name != club
    ):

        short = (
            f"{club} – {course_name}"
        )

    else:

        short = (
            club
            or
            course_name
            or
            "Unnamed course"
        )


    location_text = ", ".join(

        item

        for item in [

            location.get(
                "city",
                ""
            ),

            location.get(
                "country",
                ""
            )
        ]

        if item
    )


    if location_text:

        full = (
            f"{short} "
            f"({location_text})"
        )

    else:

        full = (
            short
        )


    return (
        short,
        full
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


    def first_value(
        keys
    ):

        for key in keys:

            if (
                selected_tee.get(
                    key
                )
                is not None
            ):

                return (
                    selected_tee[
                        key
                    ]
                )

        return None


    return (

        first_value(
            rating_keys
        ),

        first_value(
            slope_keys
        ),

        first_value(
            par_keys
        )
    )


def get_hole_number(
    hole,
    fallback
):

    return (

        hole.get(
            "hole"
        )

        or

        hole.get(
            "hole_number"
        )

        or

        hole.get(
            "number"
        )

        or

        fallback
    )


def get_hole_par(
    hole
):

    return (

        hole.get(
            "par"
        )

        or

        hole.get(
            "par_value"
        )
    )


def get_actual_stroke_index(
    hole
):

    possible_keys = [

        "handicap",
        "stroke_index",
        "strokeIndex",
        "hcp",
        "handicap_index",
        "handicapIndex"
    ]


    for key in possible_keys:

        value = (
            hole.get(
                key
            )
        )


        if (
            value is not None
            and
            value != ""
        ):

            try:

                value = int(
                    value
                )


                if (
                    1
                    <=
                    value
                    <=
                    18
                ):

                    return (
                        value
                    )


            except (
                TypeError,
                ValueError
            ):

                pass


    return None


def yellow_default_index(
    tee_names
):

    for i, tee_name in enumerate(
        tee_names
    ):

        if (
            "yellow"
            in
            str(
                tee_name
            ).lower()
        ):

            return i


    return 0


# =========================================================
# INFORMATION
# =========================================================

def show_round_rating_info():

    with st.expander(
        "What is a Round Rating?"
    ):

        st.markdown(
            """
**Round Rating** is our simpler name for the WHS
**Score Differential**.

It adjusts the score for the difficulty of the
course and tees.

**Lower is better.**

For a 9-hole round, the current WHS approach combines
the differential from the nine holes actually played
with an expected nine-hole differential.

This app follows that approach, but its expected-nine
value is an **unofficial approximation**, so the
result may differ slightly from an authorised WHS
service.
"""
        )


def show_54_hole_info():

    with st.expander(
        "Why do I need 54 completed holes?"
    ):

        st.markdown(
            """
A player needs acceptable scores covering
**54 holes** before establishing an initial
Handicap Index.

Those 54 holes can be any combination of valid
9-hole and 18-hole rounds.

Once 54 holes are reached, this app also converts
earlier 9-hole scores into 18-hole-equivalent Round
Ratings so they contribute to the initial Handicap
Index.

The expected-score part of that conversion is an
unofficial approximation.
"""
        )


def show_total_score_info():

    with st.expander(
        "Do I need to adjust my score?"
    ):

        st.markdown(
            """
Before an initial Handicap Index is established,
the maximum score that counts on a hole is
**par + 5**.

After a Handicap Index is established, the maximum
is **net double bogey**:

**Par + 2 + any handicap strokes received on that
hole.**

If you're unsure, use **Hole-by-hole scores**.

The app will use the actual Stroke Index supplied
by the course data, or ask you to enter it if the
course database doesn't provide one.
"""
        )


# =========================================================
# FINGERPRINT
# =========================================================

def make_round_fingerprint(

    player,
    date_played,
    holes_played,
    nine_choice,
    course_id,
    tee,
    gross,
    adjusted,
    method,
    hole_scores=None
):

    payload = {

        "player":
            player,

        "date":
            str(
                date_played
            ),

        "holes":
            holes_played,

        "nine":
            nine_choice,

        "course":
            str(
                course_id
            ),

        "tee":
            tee,

        "gross":
            gross,

        "adjusted":
            adjusted,

        "method":
            method,

        "hole_scores":
            hole_scores
    }


    return hashlib.sha256(

        json.dumps(
            payload,
            sort_keys=True
        ).encode()

    ).hexdigest()


# =========================================================
# SAVED ROUND CARD
# =========================================================

def show_saved_round_card():

    saved = (
        st.session_state.saved_round_summary
    )


    if not saved:

        return


    rr = (

        f"{saved['round_rating']:.1f}"

        if (
            saved.get(
                "round_rating"
            )
            is not None
        )

        else

        "Pending"
    )


    st.success(

        f"Round saved — "
        f"{saved['player']} • "
        f"{saved['course']} • "
        f"Gross {saved['gross_score']} • "
        f"Round Rating {rr}"
    )


    if st.button(

        "Enter another round",

        use_container_width=True,

        key=
            "clear_saved_round_card"
    ):

        st.session_state.saved_round_summary = (
            None
        )

        st.session_state.last_saved_round_fingerprint = (
            None
        )

        st.session_state.selected_course_id = (
            None
        )

        st.session_state.selected_course_label = (
            None
        )

        st.session_state.selected_course_short_label = (
            None
        )

        st.session_state.selected_course_data = (
            None
        )

        st.session_state.course_menu_open = (
            False
        )

        st.rerun()


# =========================================================
# ADD ROUND
# =========================================================

st.subheader(
    "Add Round"
)

show_saved_round_card()


# =========================================================
# PLAYER
# =========================================================

st.markdown(
    "**Player**"
)


player_button_text = (

    st.session_state.selected_player_entry

    if (
        st.session_state.selected_player_entry
    )

    else

    "Select player"
)


player_arrow = (

    "▲"

    if (
        st.session_state.player_menu_open
    )

    else

    "▼"
)


if st.button(

    f"{player_button_text}  "
    f"{player_arrow}",

    use_container_width=True,

    key=
        "open_player_menu"
):

    st.session_state.player_menu_open = (

        not
        st.session_state.player_menu_open
    )

    st.rerun()


if (
    st.session_state.player_menu_open
):

    for player_name in PLAYERS:

        if st.button(

            player_name,

            use_container_width=True,

            key=
                f"choose_player_{player_name}"
        ):

            st.session_state.selected_player_entry = (
                player_name
            )

            st.session_state.player_menu_open = (
                False
            )

            st.session_state.saved_round_summary = (
                None
            )

            st.session_state.last_saved_round_fingerprint = (
                None
            )

            st.rerun()


player = (
    st.session_state.selected_player_entry
)


# =========================================================
# DATE
# =========================================================

date_played = st.date_input(

    "Date played",

    value=
        date.today()
)


# =========================================================
# NUMBER OF HOLES
# =========================================================

holes_played = st.radio(

    "Number of holes played",

    [
        18,
        9
    ],

    horizontal=True
)


# =========================================================
# HANDICAP PROGRESS
# =========================================================

if player:

    player_completed_holes = (
        get_completed_holes(
            player
        )
    )


    if (
        player_completed_holes
        <
        54
    ):

        st.markdown(
            "### Building your Handicap"
        )

        st.write(

            f"**{player_completed_holes} "
            f"of 54 completed holes**"
        )

        st.progress(

            min(
                player_completed_holes
                /
                54,

                1.0
            )
        )

        show_54_hole_info()


# =========================================================
# COURSE
# =========================================================

st.markdown(
    "### Golf Course"
)


course_button_text = (

    st.session_state.selected_course_short_label

    if (
        st.session_state.selected_course_short_label
    )

    else

    "Select golf course"
)


course_arrow = (

    "▲"

    if (
        st.session_state.course_menu_open
    )

    else

    "▼"
)


if st.button(

    f"{course_button_text}  "
    f"{course_arrow}",

    use_container_width=True,

    key=
        "open_course_menu"
):

    st.session_state.course_menu_open = (

        not
        st.session_state.course_menu_open
    )

    st.rerun()


# =========================================================
# COURSE SEARCH
# =========================================================

if (
    st.session_state.course_menu_open
):

    course_search = st.text_input(

        "Search golf course",

        placeholder=
            "Start typing, e.g. Brocton Hall",

        key=
            "course_search_input"
    )


    if (
        len(
            course_search.strip()
        )
        <
        3
    ):

        st.caption(
            "Type at least 3 letters."
        )


    else:

        try:

            search_results = (
                search_courses(
                    course_search.strip()
                )
            )


            if not search_results:

                st.info(
                    "No matching golf courses found."
                )


            else:

                for result in (
                    search_results[:10]
                ):

                    (
                        short_label,
                        full_label
                    ) = (
                        build_course_labels(
                            result
                        )
                    )


                    result_id = (
                        result.get(
                            "id"
                        )
                    )


                    if (
                        result_id
                        and
                        st.button(

                            full_label,

                            use_container_width=True,

                            key=
                                f"course_result_{result_id}"
                        )
                    ):

                        loaded = (
                            get_course_details(
                                result_id
                            )
                        )


                        st.session_state.selected_course_id = (
                            result_id
                        )

                        st.session_state.selected_course_label = (
                            full_label
                        )

                        st.session_state.selected_course_short_label = (
                            short_label
                        )

                        st.session_state.selected_course_data = (
                            loaded
                        )

                        st.session_state.course_menu_open = (
                            False
                        )

                        st.session_state.saved_round_summary = (
                            None
                        )

                        st.session_state.last_saved_round_fingerprint = (
                            None
                        )

                        st.rerun()


        except requests.exceptions.RequestException as error:

            st.error(
                "Unable to search the golf course database."
            )

            st.caption(
                str(error)
            )


# =========================================================
# SELECTED COURSE
# =========================================================

course_data = (
    st.session_state.selected_course_data
)

course_id = (
    st.session_state.selected_course_id
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


    course_layout = (

        course_name

        or

        club_name

        or

        "Main Course"
    )


    male_tees = (

        course_data.get(
            "tees",
            {}
        )

        or {}

    ).get(
        "male",
        []
    )


    if not male_tees:

        st.warning(
            "No male tee information is available for this course."
        )


    else:

        tee_names = [

            tee.get(
                "tee_name",
                "Unnamed tee"
            )

            for tee
            in male_tees
        ]


        # =================================================
        # YELLOW TEE DEFAULT
        # =================================================

        selected_tee_name = (
            st.selectbox(

                "Tees used",

                tee_names,

                index=
                    yellow_default_index(
                        tee_names
                    )
            )
        )


        selected_tee = (

            male_tees[
                tee_names.index(
                    selected_tee_name
                )
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

            or []
        )


        # =================================================
        # 9 / 18 HOLES
        # =================================================

        nine_choice = (
            None
        )


        if holes_played == 9:

            nine_choice = st.radio(

                "Which 9 holes?",

                [
                    "Front 9",
                    "Back 9"
                ],

                horizontal=True
            )


            (
                course_rating,
                slope_rating,
                course_par
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

            course_par = (
                full_par
            )


        # =================================================
        # COURSE INFORMATION
        # =================================================

        st.markdown(
            "#### Course information"
        )


        c1, c2, c3 = (
            st.columns(
                3
            )
        )


        c1.metric(

            "Course Rating",

            course_rating

            if (
                course_rating
                is not None
            )

            else

            "N/A"
        )


        c2.metric(

            "Slope",

            slope_rating

            if (
                slope_rating
                is not None
            )

            else

            "N/A"
        )


        c3.metric(

            "Par",

            course_par

            if (
                course_par
                is not None
            )

            else

            "N/A"
        )


        # =================================================
        # VALIDATE COURSE DATA
        # =================================================

        if (
            course_rating is None
            or
            slope_rating is None
        ):

            st.warning(

                "This course/tee record does not contain "
                "the rating data needed for this round."
            )


        else:

            existing_handicap = (

                get_player_handicap(
                    player
                )

                if player

                else None
            )


            # =================================================
            # SCORE ENTRY
            # =================================================

            st.markdown(
                "### Enter your score"
            )


            entry_method = st.radio(

                "Entry method",

                [
                    "Total gross score",
                    "Hole-by-hole scores"
                ]
            )


            # =================================================
            # TOTAL GROSS SCORE
            # =================================================

            if (
                entry_method
                ==
                "Total gross score"
            ):

                show_total_score_info()


                st.markdown(

                    '<div class="gross-score-heading">'
                    'Gross Score'
                    '</div>',

                    unsafe_allow_html=True
                )


                handicap_score = (
                    st.number_input(

                        "Gross Score",

                        min_value=
                            40
                            if holes_played == 18
                            else 20,

                        max_value=
                            200
                            if holes_played == 18
                            else 100,

                        value=
                            90
                            if holes_played == 18
                            else 45,

                        step=1,

                        label_visibility=
                            "collapsed"
                    )
                )


                round_rating = (
                    None
                )


                expected_nine = (
                    None
                )


                played_diff = (
                    calculate_differential(

                        handicap_score,
                        course_rating,
                        slope_rating
                    )
                )


                if holes_played == 18:

                    round_rating = (
                        played_diff
                    )


                elif (
                    existing_handicap
                    is not None
                ):

                    expected_nine = (
                        estimated_expected_nine(
                            existing_handicap
                        )
                    )


                    round_rating = (

                        played_diff

                        +

                        expected_nine
                    )


                if (
                    round_rating
                    is not None
                ):

                    st.metric(

                        "Round Rating",

                        f"{round_rating:.1f}"
                    )

                    show_round_rating_info()


                else:

                    st.info(

                        "This 9-hole round will count towards "
                        "the 54-hole minimum. Once an initial "
                        "Handicap Index can be established, "
                        "the app will automatically give this "
                        "round an 18-hole-equivalent Round Rating."
                    )


                fingerprint = (
                    make_round_fingerprint(

                        player,
                        date_played,
                        holes_played,
                        nine_choice,
                        course_id,
                        selected_tee_name,
                        int(
                            handicap_score
                        ),
                        int(
                            handicap_score
                        ),
                        "Total"
                    )
                )


                already_saved = (

                    st.session_state.last_saved_round_fingerprint
                    ==
                    fingerprint
                )


                if st.button(

                    "Save round",

                    use_container_width=True,

                    type="primary",

                    disabled=
                        already_saved,

                    key=
                        "save_total_round"
                ):

                    if not player:

                        st.error(
                            "Please select a player."
                        )


                    else:

                        record = {

                            "player_id":
                                PLAYER_ID_BY_NAME[
                                    player
                                ],

                            "date_played":
                                date_played.isoformat(),

                            "holes":
                                int(
                                    holes_played
                                ),

                            "nine":
                                nine_choice,

                            "golf_course":
                                club_name,

                            "course_layout":
                                course_layout,

                            "course_api_id":
                                str(
                                    course_id
                                ),

                            "tees":
                                selected_tee_name,

                            "course_rating":
                                float(
                                    course_rating
                                ),

                            "slope_rating":
                                int(
                                    slope_rating
                                ),

                            "par":
                                int(
                                    course_par
                                )
                                if (
                                    course_par
                                    is not None
                                )
                                else None,

                            "gross_score":
                                int(
                                    handicap_score
                                ),

                            "adjusted_score":
                                int(
                                    handicap_score
                                ),

                            "round_rating":

                                round(
                                    float(
                                        round_rating
                                    ),
                                    1
                                )

                                if (
                                    round_rating
                                    is not None
                                )

                                else None,

                            "entry_method":
                                "Total",

                            "hole_scores":
                                None,

                            "expected_nine":

                                float(
                                    expected_nine
                                )

                                if (
                                    expected_nine
                                    is not None
                                )

                                else None
                        }


                        try:

                            save_round_to_database(
                                record
                            )


                            st.session_state.last_saved_round_fingerprint = (
                                fingerprint
                            )


                            st.session_state.saved_round_summary = {

                                "player":
                                    player,

                                "course":

                                    st.session_state.selected_course_short_label

                                    or

                                    club_name,

                                "gross_score":
                                    int(
                                        handicap_score
                                    ),

                                "round_rating":

                                    round(
                                        float(
                                            round_rating
                                        ),
                                        1
                                    )

                                    if (
                                        round_rating
                                        is not None
                                    )

                                    else None
                            }


                            load_rounds_from_database.clear()

                            st.rerun()


                        except DuplicateRoundError:

                            st.warning(

                                "This round appears to "
                                "have already been saved."
                            )


                        except requests.exceptions.RequestException as error:

                            st.error(
                                "The round could not be saved."
                            )

                            st.caption(
                                str(error)
                            )


            # =================================================
            # HOLE-BY-HOLE
            # =================================================

            else:

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


                required_holes = (

                    18

                    if holes_played == 18

                    else 9
                )


                if (
                    len(
                        holes_for_round
                    )
                    <
                    required_holes
                ):

                    st.warning(

                        "Complete hole-by-hole data isn't "
                        "available for this course/tee "
                        "selection. Please use Total gross score."
                    )


                else:

                    course_handicap = (
                        None
                    )


                    if (

                        existing_handicap
                        is not None

                        and

                        full_course_rating
                        is not None

                        and

                        full_slope_rating
                        is not None

                        and

                        full_par
                        is not None
                    ):

                        course_handicap = (
                            calculate_course_handicap(

                                existing_handicap,
                                full_slope_rating,
                                full_course_rating,
                                full_par
                            )
                        )


                        c1, c2 = (
                            st.columns(
                                2
                            )
                        )


                        c1.metric(

                            "Handicap Index",

                            f"{existing_handicap:.1f}"
                        )


                        c2.metric(

                            "Course Handicap",

                            course_handicap
                        )


                    raw_scores = []

                    adjusted_scores = []

                    entered_stroke_indexes = []

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
                                or
                                nine_choice == "Front 9"
                            )

                            else

                            i + 10
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

                            or

                            4
                        )


                        api_stroke_index = (
                            get_actual_stroke_index(
                                hole
                            )
                        )


                        # =====================================
                        # ACTUAL STROKE INDEX
                        # =====================================

                        if (
                            api_stroke_index
                            is None
                        ):

                            st.caption(

                                f"Hole {hole_number}: "
                                f"Stroke Index is missing from "
                                f"the course database. Enter the "
                                f"SI shown on the scorecard."
                            )


                            stroke_index = (
                                st.number_input(

                                    f"Stroke Index — "
                                    f"Hole {hole_number}",

                                    min_value=1,

                                    max_value=18,

                                    value=1,

                                    step=1,

                                    key=(

                                        f"manual_si_"
                                        f"{course_id}_"
                                        f"{selected_tee_name}_"
                                        f"{holes_played}_"
                                        f"{nine_choice}_"
                                        f"{hole_number}"
                                    )
                                )
                            )


                        else:

                            stroke_index = (
                                api_stroke_index
                            )


                        entered_stroke_indexes.append(
                            int(
                                stroke_index
                            )
                        )


                        st.write(

                            f"**Hole {hole_number}** — "
                            f"Par {hole_par} • "
                            f"SI {stroke_index}"
                        )


                        hole_score = (
                            st.number_input(

                                f"Score — "
                                f"Hole {hole_number}",

                                min_value=1,

                                max_value=20,

                                value=
                                    int(
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
                                )
                            )
                        )


                        raw_scores.append(
                            int(
                                hole_score
                            )
                        )


                        # =====================================
                        # MAXIMUM HOLE SCORE
                        # =====================================

                        if (

                            existing_handicap
                            is None

                            or

                            course_handicap
                            is None
                        ):

                            maximum_hole_score = (

                                int(
                                    hole_par
                                )

                                +

                                5
                            )


                        else:

                            strokes_received = (
                                handicap_strokes_on_hole(

                                    course_handicap,

                                    int(
                                        stroke_index
                                    )
                                )
                            )


                            maximum_hole_score = (

                                int(
                                    hole_par
                                )

                                +

                                2

                                +

                                int(
                                    strokes_received
                                    or 0
                                )
                            )


                        adjusted_hole_score = min(

                            int(
                                hole_score
                            ),

                            maximum_hole_score
                        )


                        adjusted_scores.append(
                            adjusted_hole_score
                        )


                        if (
                            adjusted_hole_score
                            <
                            int(
                                hole_score
                            )
                        ):

                            adjustment_details.append(

                                (
                                    hole_number,
                                    int(
                                        hole_score
                                    ),
                                    adjusted_hole_score
                                )
                            )


                    # =========================================
                    # VALIDATE STROKE INDEX
                    # =========================================

                    if holes_played == 18:

                        expected_si_set = (
                            set(
                                range(
                                    1,
                                    19
                                )
                            )
                        )


                        si_valid = (

                            set(
                                entered_stroke_indexes
                            )

                            ==

                            expected_si_set
                        )


                    else:

                        si_valid = (

                            len(
                                set(
                                    entered_stroke_indexes
                                )
                            )

                            ==

                            len(
                                entered_stroke_indexes
                            )
                        )


                    if not si_valid:

                        st.error(

                            "The Stroke Index values contain "
                            "duplicates or are not a valid "
                            "scorecard allocation. Please check "
                            "them before saving."
                        )


                    # =========================================
                    # ROUND TOTALS
                    # =========================================

                    gross_score = sum(
                        raw_scores
                    )


                    adjusted_score = sum(
                        adjusted_scores
                    )


                    played_diff = (
                        calculate_differential(

                            adjusted_score,
                            course_rating,
                            slope_rating
                        )
                    )


                    round_rating = (
                        None
                    )


                    expected_nine = (
                        None
                    )


                    if holes_played == 18:

                        round_rating = (
                            played_diff
                        )


                    elif (
                        existing_handicap
                        is not None
                    ):

                        expected_nine = (
                            estimated_expected_nine(
                                existing_handicap
                            )
                        )


                        round_rating = (

                            played_diff

                            +

                            expected_nine
                        )


                    # =========================================
                    # ROUND SUMMARY
                    # =========================================

                    st.markdown(
                        "### Round summary"
                    )


                    c1, c2 = (
                        st.columns(
                            2
                        )
                    )


                    c1.metric(

                        "Gross Score",

                        gross_score
                    )


                    c2.metric(

                        "Round Rating",

                        f"{round_rating:.1f}"

                        if (
                            round_rating
                            is not None
                        )

                        else

                        "Pending"
                    )


                    if (
                        adjusted_score
                        !=
                        gross_score
                    ):

                        st.info(

                            f"Score used for handicap "
                            f"purposes: **{adjusted_score}**"
                        )


                        with st.expander(
                            "See automatic score adjustments"
                        ):

                            for (
                                hole_no,
                                original,
                                adjusted
                            ) in adjustment_details:

                                st.write(

                                    f"Hole {hole_no}: "
                                    f"{original} → {adjusted}"
                                )


                    fingerprint = (
                        make_round_fingerprint(

                            player,
                            date_played,
                            holes_played,
                            nine_choice,
                            course_id,
                            selected_tee_name,
                            gross_score,
                            adjusted_score,
                            "Hole-by-hole",
                            raw_scores
                        )
                    )


                    already_saved = (

                        st.session_state.last_saved_round_fingerprint
                        ==
                        fingerprint
                    )


                    if st.button(

                        "Save round",

                        use_container_width=True,

                        type="primary",

                        disabled=(

                            already_saved

                            or

                            not si_valid
                        ),

                        key=
                            "save_hole_round"
                    ):

                        if not player:

                            st.error(
                                "Please select a player."
                            )


                        else:

                            record = {

                                "player_id":
                                    PLAYER_ID_BY_NAME[
                                        player
                                    ],

                                "date_played":
                                    date_played.isoformat(),

                                "holes":
                                    int(
                                        holes_played
                                    ),

                                "nine":
                                    nine_choice,

                                "golf_course":
                                    club_name,

                                "course_layout":
                                    course_layout,

                                "course_api_id":
                                    str(
                                        course_id
                                    ),

                                "tees":
                                    selected_tee_name,

                                "course_rating":
                                    float(
                                        course_rating
                                    ),

                                "slope_rating":
                                    int(
                                        slope_rating
                                    ),

                                "par":

                                    int(
                                        course_par
                                    )

                                    if (
                                        course_par
                                        is not None
                                    )

                                    else None,

                                "gross_score":
                                    int(
                                        gross_score
                                    ),

                                "adjusted_score":
                                    int(
                                        adjusted_score
                                    ),

                                "round_rating":

                                    round(
                                        float(
                                            round_rating
                                        ),
                                        1
                                    )

                                    if (
                                        round_rating
                                        is not None
                                    )

                                    else None,

                                "entry_method":
                                    "Hole-by-hole",

                                "hole_scores":
                                    raw_scores,

                                "expected_nine":

                                    float(
                                        expected_nine
                                    )

                                    if (
                                        expected_nine
                                        is not None
                                    )

                                    else None
                            }


                            try:

                                save_round_to_database(
                                    record
                                )


                                st.session_state.last_saved_round_fingerprint = (
                                    fingerprint
                                )


                                st.session_state.saved_round_summary = {

                                    "player":
                                        player,

                                    "course":

                                        st.session_state.selected_course_short_label

                                        or

                                        club_name,

                                    "gross_score":
                                        gross_score,

                                    "round_rating":

                                        round(
                                            float(
                                                round_rating
                                            ),
                                            1
                                        )

                                        if (
                                            round_rating
                                            is not None
                                        )

                                        else None
                                }


                                load_rounds_from_database.clear()

                                st.rerun()


                            except DuplicateRoundError:

                                st.warning(

                                    "This round appears to "
                                    "have already been saved."
                                )


                            except requests.exceptions.RequestException as error:

                                st.error(
                                    "The round could not be saved."
                                )

                                st.caption(
                                    str(error)
                                )


# =========================================================
# PLAYER HANDICAPS
# =========================================================

st.divider()


st.markdown(

    '<div class="secondary-section-title">'
    'Player Handicaps'
    '</div>',

    unsafe_allow_html=True
)


if not all_rounds:

    st.info(
        "No scores have been recorded yet."
    )


else:

    rounds_df = (
        pd.DataFrame(
            all_rounds
        )
    )


    players_with_scores = [

        name

        for name in PLAYERS

        if (
            name
            in
            rounds_df[
                "Player"
            ].unique()
        )
    ]


    record_player = (
        st.selectbox(

            "View player",

            players_with_scores
        )
    )


    player_record = (
        get_player_rounds(
            record_player
        )
    )


    record_completed_holes = sum(

        int(
            round_item.get(
                "Holes"
            )
            or 0
        )

        for round_item
        in player_record
    )


    effective_ratings = (
        build_effective_round_ratings(
            player_record
        )
    )


    if (
        record_completed_holes
        <
        54
    ):

        st.markdown(
            "### Building your Handicap"
        )


        st.write(

            f"**{record_completed_holes} "
            f"of 54 completed holes**"
        )


        st.progress(

            min(
                record_completed_holes
                /
                54,

                1.0
            )
        )


        show_54_hole_info()


    else:

        (
            record_hi,
            _,
            explanation
        ) = (
            handicap_calculation(

                [
                    value

                    for value
                    in effective_ratings

                    if (
                        value
                        is not None
                    )
                ]
            )
        )


        if (
            record_hi
            is not None
        ):

            st.metric(

                "Handicap Index",

                f"{record_hi:.1f}"
            )


            st.caption(
                "Unofficial WHS-based calculation"
            )


            st.write(
                f"**{explanation}**"
            )


        else:

            st.warning(

                "There is not yet enough valid rating "
                "information to calculate a Handicap Index."
            )


    # =====================================================
    # SCORING RECORD
    # =====================================================

    display_rows = []


    for (
        round_item,
        effective_rating
    ) in zip(

        player_record,
        effective_ratings
    ):

        display_rows.append(
            {

                "Date":
                    round_item.get(
                        "Date"
                    ),

                "Golf Course":
                    round_item.get(
                        "Golf Course"
                    ),

                "Tees":
                    round_item.get(
                        "Tees"
                    ),

                "Holes":
                    round_item.get(
                        "Holes"
                    ),

                "Gross Score":
                    round_item.get(
                        "Gross Score"
                    ),

                "Round Rating":
                    effective_rating
            }
        )


    display_df = (
        pd.DataFrame(
            display_rows
        )
    )


    if not display_df.empty:

        display_df = (
            display_df.sort_values(

                "Date",

                ascending=False
            )
        )


    st.markdown(
        "### Scoring Record"
    )


    st.dataframe(

        display_df,

        hide_index=True,

        use_container_width=True
    )


    show_round_rating_info()


# =========================================================
# ADMIN
# =========================================================

st.divider()


with st.expander(
    "Admin tools"
):

    if not (
        st.session_state.admin_authenticated
    ):

        entered_pin = (
            st.text_input(

                "Admin PIN",

                type="password",

                key=
                    "admin_pin_input"
            )
        )


        if st.button(

            "Unlock Admin",

            use_container_width=True
        ):

            if hmac.compare_digest(

                str(
                    entered_pin
                ),

                str(
                    ADMIN_PIN
                )
            ):

                st.session_state.admin_authenticated = (
                    True
                )

                st.rerun()


            else:

                st.error(
                    "Incorrect Admin PIN."
                )


    else:

        st.success(
            "Admin access unlocked."
        )


        if st.button(

            "Lock Admin",

            use_container_width=True
        ):

            st.session_state.admin_authenticated = (
                False
            )

            st.session_state.pending_delete_round_id = (
                None
            )

            st.rerun()


        if all_rounds:

            admin_rounds = sorted(

                all_rounds,

                key=lambda round_item:

                    str(
                        round_item.get(
                            "Created At",
                            ""
                        )
                    ),

                reverse=True
            )


            options = {}


            for round_item in admin_rounds:

                label = (

                    f"{round_item.get('Date')} • "
                    f"{round_item.get('Player')} • "
                    f"{round_item.get('Golf Course')} • "
                    f"{round_item.get('Tees')} • "
                    f"Gross "
                    f"{round_item.get('Gross Score')}"
                )


                options[
                    label
                ] = (
                    round_item
                )


            selected_label = (
                st.selectbox(

                    "Select a round",

                    list(
                        options.keys()
                    )
                )
            )


            selected_round = (
                options[
                    selected_label
                ]
            )


            st.write(

                f"**{selected_round.get('Player')} — "
                f"{selected_round.get('Date')}**"
            )


            st.write(

                selected_round.get(
                    "Golf Course"
                )
            )


            st.write(

                f"{selected_round.get('Tees')} tees • "
                f"Gross "
                f"{selected_round.get('Gross Score')}"
            )


            selected_id = (
                selected_round.get(
                    "ID"
                )
            )


            if (

                st.session_state.pending_delete_round_id

                !=

                selected_id
            ):

                if st.button(

                    "Delete selected round",

                    use_container_width=True
                ):

                    st.session_state.pending_delete_round_id = (
                        selected_id
                    )

                    st.rerun()


            else:

                st.error(

                    "This will permanently delete "
                    "the selected round."
                )


                c1, c2 = (
                    st.columns(
                        2
                    )
                )


                with c1:

                    if st.button(

                        "Yes, delete it",

                        use_container_width=True
                    ):

                        try:

                            delete_round_from_database(
                                selected_id
                            )


                            st.session_state.pending_delete_round_id = (
                                None
                            )


                            load_rounds_from_database.clear()

                            st.rerun()


                        except requests.exceptions.RequestException as error:

                            st.error(
                                "The round could not be deleted."
                            )

                            st.caption(
                                str(error)
                            )


                with c2:

                    if st.button(

                        "Cancel",

                        use_container_width=True
                    ):

                        st.session_state.pending_delete_round_id = (
                            None
                        )

                        st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.divider()


st.caption(

    "Handicap Builder provides an unofficial WHS-based "
    "handicap estimate and is not an authorised "
    "handicapping service."
)