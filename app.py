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
    page_title="Golf Group Handicaps",
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
    --green-soft: #183f34;
    --cream: #f6f1e8;
    --cream-2: #fbf8f2;
    --gold: #b69a5a;
    --gold-soft: #d4c08c;
    --text: #15251f;
    --muted: #6a756f;
    --line: #ddd6c8;
    --white: #ffffff;
}

/* Main page */

.stApp {
    background:
        linear-gradient(
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


/* Typography */

h1, h2, h3, h4 {
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

p, label {
    color: var(--text);
}

[data-testid="stCaptionContainer"] {
    color: var(--muted) !important;
}


/* Hero */

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

    border-radius: 0 0 28px 28px;

    padding:
        35px 24px 30px 24px;

    margin:
        0.8rem -1rem 1.9rem -1rem;

    box-shadow:
        0 16px 34px rgba(10,43,34,0.19);

    border-bottom:
        1px solid rgba(182,154,90,0.42);
}

.golf-hero-kicker {
    color: var(--gold-soft);

    font-size: 0.78rem;
    font-weight: 700;

    letter-spacing: 0.22em;

    text-transform: uppercase;

    margin-bottom: 11px;
}

.golf-hero-title {
    color: #ffffff;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size: 2.55rem;

    line-height: 1.15;

    font-weight: 700;

    letter-spacing: -0.035em;

    margin-bottom: 13px;
}

.golf-hero-subtitle {
    color:
        rgba(255,255,255,0.78);

    font-size:
        0.97rem;

    line-height:
        1.5;

    max-width:
        610px;
}

.golf-flow {
    margin-top:
        19px;

    display:
        inline-block;

    border:
        1px solid rgba(212,192,140,0.78);

    border-radius:
        999px;

    padding:
        8px 13px;

    color:
        #eadfbf;

    font-size:
        0.69rem;

    font-weight:
        700;

    letter-spacing:
        0.055em;

    background:
        rgba(255,255,255,0.025);
}


/* Buttons */

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

    transition:
        all 0.15s ease;
}

.stButton > button:hover {
    border-color:
        var(--gold);

    color:
        var(--green-dark);

    background:
        #fffefa;

    box-shadow:
        0 7px 18px rgba(25,55,42,0.08);

    transform:
        translateY(-1px);
}

.stButton > button:active {
    transform:
        translateY(0px);
}

.stButton > button[kind="primary"] {
    background:
        var(--green-dark);

    color:
        #ffffff;

    border-color:
        var(--green-dark);

    box-shadow:
        0 7px 16px rgba(10,43,34,0.16);
}

.stButton > button[kind="primary"]:hover {
    background:
        var(--green);

    color:
        #ffffff;

    border-color:
        var(--gold);
}

.stButton > button:disabled {
    opacity:
        0.47;
}


/* Inputs */

[data-baseweb="input"],
[data-baseweb="select"] > div,
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input,
.stTextInput input {
    border-radius:
        12px !important;
}


/* Radio controls */

[data-testid="stRadio"] > div {
    gap:
        10px;
}

[data-testid="stRadio"] label {
    font-weight:
        600;
}


/* Metrics */

[data-testid="stMetric"] {
    background:
        rgba(255,255,255,0.92);

    border:
        1px solid #e1dbcf;

    border-radius:
        16px;

    padding:
        15px 16px;

    box-shadow:
        0 5px 15px rgba(20,50,38,0.05);
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

    letter-spacing:
        -0.035em;
}


/* Expanders */

[data-testid="stExpander"] {
    background:
        rgba(255,255,255,0.92);

    border:
        1px solid #e2dcd0;

    border-radius:
        14px;

    overflow:
        hidden;

    box-shadow:
        0 3px 10px rgba(22,50,39,0.035);
}

[data-testid="stExpander"] summary {
    font-weight:
        620;
}


/* Progress bar */

[data-testid="stProgress"] > div > div {
    border-radius:
        999px;
}

[data-testid="stProgress"] > div > div > div {
    background:
        linear-gradient(
            90deg,
            var(--green-dark),
            var(--gold)
        );
}


/* Tables */

[data-testid="stDataFrame"] {
    border:
        1px solid #e0d9cb;

    border-radius:
        15px;

    overflow:
        hidden;

    box-shadow:
        0 4px 14px rgba(20,45,35,0.04);
}


/* Alerts */

[data-testid="stAlert"] {
    border-radius:
        14px;
}


/* Divider */

hr {
    border-color:
        var(--line) !important;

    margin-top:
        2rem !important;

    margin-bottom:
        1.6rem !important;
}


/* Mobile */

@media (max-width: 640px) {

    .block-container {
        padding-left:
            1rem;

        padding-right:
            1rem;
    }

    .golf-hero {
        padding:
            26px 18px 24px 18px;
    }

    .golf-hero-title {
        font-size:
            2.15rem;
    }

    .golf-hero-subtitle {
        font-size:
            0.93rem;
    }

    .golf-flow {
        font-size:
            0.62rem;

        padding:
            7px 9px;
    }

    .stButton > button {
        min-height:
            52px;

        font-size:
            0.96rem;
    }

    [data-testid="stMetric"] {
        padding:
            13px 12px;
    }

    [data-testid="stMetricValue"] {
        font-size:
            1.55rem;
    }
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# HERO HEADER
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

GOLF_API_BASE = "https://api.golfcourseapi.com/v1"

GOLF_API_KEY = st.secrets["GOLF_API_KEY"]
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
ADMIN_PIN = st.secrets["ADMIN_PIN"]

GOLF_HEADERS = {
    "Authorization": f"Bearer {GOLF_API_KEY}"
}

SUPABASE_HEADERS = {
    "apikey": SUPABASE_KEY,
    "Content-Type": "application/json"
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
# CUSTOM ERROR
# =========================================================

class DuplicateRoundError(Exception):
    pass


# =========================================================
# SESSION STATE
# =========================================================

if "selected_player_entry" not in st.session_state:
    st.session_state.selected_player_entry = None

if "player_menu_open" not in st.session_state:
    st.session_state.player_menu_open = False

if "selected_course_id" not in st.session_state:
    st.session_state.selected_course_id = None

if "selected_course_label" not in st.session_state:
    st.session_state.selected_course_label = None

if "selected_course_short_label" not in st.session_state:
    st.session_state.selected_course_short_label = None

if "selected_course_data" not in st.session_state:
    st.session_state.selected_course_data = None

if "course_menu_open" not in st.session_state:
    st.session_state.course_menu_open = False

if "last_saved_round_fingerprint" not in st.session_state:
    st.session_state.last_saved_round_fingerprint = None

if "saved_round_summary" not in st.session_state:
    st.session_state.saved_round_summary = None

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if "pending_delete_round_id" not in st.session_state:
    st.session_state.pending_delete_round_id = None


# =========================================================
# SUPABASE DATABASE
# =========================================================

@st.cache_data(ttl=3600, show_spinner=False)
def load_players_from_database():

    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/players",
        headers=SUPABASE_HEADERS,
        params={
            "select": "id,name",
            "order": "name.asc"
        },
        timeout=15
    )

    response.raise_for_status()

    return response.json()


@st.cache_data(ttl=10, show_spinner=False)
def load_rounds_from_database():

    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/rounds",
        headers=SUPABASE_HEADERS,
        params={
            "select": "*",
            "order": "date_played.asc,created_at.asc"
        },
        timeout=15
    )

    response.raise_for_status()

    return response.json()


def save_round_to_database(round_data):

    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/rounds",
        headers={
            **SUPABASE_HEADERS,
            "Prefer": "return=minimal"
        },
        json=round_data,
        timeout=15
    )

    if not response.ok:

        response_text = response.text.lower()

        if (
            "already been submitted" in response_text
            or "duplicate" in response_text
        ):

            raise DuplicateRoundError(
                "This round appears to have already been saved."
            )

        response.raise_for_status()


def delete_round_from_database(round_id):

    response = requests.delete(
        f"{SUPABASE_URL}/rest/v1/rounds",
        headers={
            **SUPABASE_HEADERS,
            "Prefer": "return=minimal"
        },
        params={
            "id": f"eq.{round_id}"
        },
        timeout=15
    )

    response.raise_for_status()


# =========================================================
# LOAD DATABASE DATA
# =========================================================

try:

    database_players = load_players_from_database()

except requests.exceptions.RequestException as error:

    st.error(
        "Unable to connect to the player database."
    )

    st.caption(
        str(error)
    )

    st.stop()


PLAYER_ID_BY_NAME = {
    row["name"]: row["id"]
    for row in database_players
}

PLAYER_NAME_BY_ID = {
    row["id"]: row["name"]
    for row in database_players
}


try:

    database_rounds = load_rounds_from_database()

except requests.exceptions.RequestException as error:

    st.error(
        "Unable to load scores from the database."
    )

    st.caption(
        str(error)
    )

    st.stop()


# =========================================================
# CONVERT DATABASE ROUNDS TO APP FORMAT
# =========================================================

all_rounds = []

for row in database_rounds:

    player_name = PLAYER_NAME_BY_ID.get(
        row.get("player_id")
    )

    if player_name is None:
        continue

    date_value = row.get(
        "date_played"
    )

    try:

        date_value = pd.to_datetime(
            date_value
        ).date()

    except Exception:
        pass

    all_rounds.append(
        {
            "ID": row.get("id"),
            "Player": player_name,
            "Date": date_value,
            "Holes": row.get("holes"),
            "Nine": row.get("nine"),
            "Golf Course": row.get("golf_course"),
            "Course / Layout": row.get("course_layout"),
            "Course API ID": row.get("course_api_id"),
            "Tees": row.get("tees"),
            "Course Rating": row.get("course_rating"),
            "Slope Rating": row.get("slope_rating"),
            "Par": row.get("par"),
            "Gross Score": row.get("gross_score"),
            "Adjusted Score": row.get("adjusted_score"),
            "Differential": row.get("round_rating"),
            "Entry Method": row.get("entry_method"),
            "Hole Scores": row.get("hole_scores"),
            "Expected Nine": row.get("expected_nine"),
            "Created At": row.get("created_at")
        }
    )


# =========================================================
# COURSE API
# =========================================================

@st.cache_data(
    ttl=86400,
    show_spinner=False
)
def search_courses(search_text):

    response = requests.get(
        f"{GOLF_API_BASE}/search",
        headers=GOLF_HEADERS,
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
        f"{GOLF_API_BASE}/courses/{course_id}",
        headers=GOLF_HEADERS,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    return data.get(
        "course",
        data
    )


# =========================================================
# ROUND FINGERPRINT
# =========================================================

def make_round_fingerprint(
    player,
    date_played,
    holes_played,
    nine_choice,
    course_id,
    selected_tee_name,
    gross_score,
    adjusted_score,
    entry_method,
    hole_scores=None
):

    fingerprint_data = {
        "player": player,
        "date": str(date_played),
        "holes": int(holes_played),
        "nine": nine_choice,
        "course_id": str(course_id),
        "tee": selected_tee_name,
        "gross": int(gross_score),
        "adjusted": int(adjusted_score),
        "method": entry_method,
        "hole_scores": hole_scores
    }

    fingerprint_text = json.dumps(
        fingerprint_data,
        sort_keys=True
    )

    return hashlib.sha256(
        fingerprint_text.encode("utf-8")
    ).hexdigest()


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

    return (
        float(handicap_index) / 2
    ) + 1.5


def calculate_9_hole_round_rating(
    played_nine_differential,
    handicap_index
):

    expected = estimated_expected_nine(
        handicap_index
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

    clean_differentials = [
        float(value)
        for value in differentials
        if value is not None
        and pd.notna(value)
    ]

    count = len(
        clean_differentials
    )

    if count < 3:
        return None, [], ""

    recent = clean_differentials[
        -20:
    ]

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

    counting = sorted_diffs[
        :number_used
    ]

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

def valid_player_name(player_name):

    if player_name in PLAYERS:

        return player_name

    return None


def get_player_rounds(player_name):

    player_name = valid_player_name(
        player_name
    )

    if player_name is None:

        return []

    results = [
        round_item
        for round_item in all_rounds
        if round_item.get("Player") == player_name
    ]

    return sorted(
        results,
        key=lambda round_item: round_item["Date"]
    )


def get_completed_holes(player_name):

    player_rounds = get_player_rounds(
        player_name
    )

    return sum(
        int(
            round_item.get(
                "Holes",
                0
            )
            or 0
        )
        for round_item in player_rounds
    )


def get_player_handicap(player_name):

    player_rounds = get_player_rounds(
        player_name
    )

    holes_completed = sum(
        int(
            round_item.get(
                "Holes",
                0
            )
            or 0
        )
        for round_item in player_rounds
    )

    if holes_completed < 54:

        return None

    completed_differentials = [
        round_item.get(
            "Differential"
        )
        for round_item in player_rounds
        if round_item.get(
            "Differential"
        ) is not None
    ]

    if len(
        completed_differentials
    ) < 3:

        return None

    handicap_index, _, _ = handicap_calculation(
        completed_differentials
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
            float(handicap_index)
            * float(slope_rating)
            / 113
        )
        + (
            float(course_rating)
            - float(par)
        )
    )


def handicap_strokes_on_hole(
    course_handicap,
    stroke_index
):

    if course_handicap <= 0:

        return 0

    full_cycles = (
        course_handicap
        // 18
    )

    remainder = (
        course_handicap
        % 18
    )

    strokes = full_cycles

    if stroke_index <= remainder:

        strokes += 1

    return strokes


# =========================================================
# COURSE HELPERS
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

        if selected_tee.get(
            key
        ) is not None:

            rating = selected_tee[
                key
            ]

            break

    for key in slope_keys:

        if selected_tee.get(
            key
        ) is not None:

            slope = selected_tee[
                key
            ]

            break

    for key in par_keys:

        if selected_tee.get(
            key
        ) is not None:

            par = selected_tee[
                key
            ]

            break

    return (
        rating,
        slope,
        par
    )


def build_course_labels(
    course
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
    ) or {}

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

        short_label = (
            f"{club} – {course_name}"
        )

    else:

        short_label = (
            club
            or course_name
            or "Unnamed course"
        )

    location_text = ", ".join(
        item
        for item in [
            city,
            country
        ]
        if item
    )

    if location_text:

        full_label = (
            f"{short_label} "
            f"({location_text})"
        )

    else:

        full_label = short_label

    return (
        short_label,
        full_label
    )


# =========================================================
# INFORMATION BOXES
# =========================================================

def show_round_rating_info():

    with st.expander(
        "What is a Round Rating?"
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
        "Why do I need 54 completed holes?"
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
        "Do I need to adjust my score?"
    ):

        st.markdown(
            """
A very high score on an individual hole may need to
be reduced before you enter your total for handicap
purposes.

**If you are building your first Handicap Index:**

The maximum score that counts on any hole is
**par + 5**.

For example, on a par 4, no more than **9** counts
for handicap purposes.

**If you already have a Handicap Index:**

The maximum is **net double bogey**:

**Par + 2 + any handicap strokes you receive on
that hole.**

If you're unsure, choose **Hole-by-hole scores** and
the app will make the adjustment automatically where
the course scorecard information is available.
            """
        )


# =========================================================
# SAVED ROUND CARD
# =========================================================

def show_saved_round_card():

    saved = st.session_state.saved_round_summary

    if not saved:

        return

    round_rating_text = (
        f"{saved['round_rating']:.1f}"
        if saved.get(
            "round_rating"
        ) is not None
        else "Pending"
    )

    nine_text = (
        f" • {saved['nine']}"
        if saved.get(
            "nine"
        )
        else ""
    )

    st.markdown(
        f"""<div style="
background:#ffffff;
border:1px solid #ded7ca;
border-radius:18px;
padding:20px;
margin:8px 0 20px 0;
box-shadow:0 8px 22px rgba(20,45,35,0.06);
">
<div style="
display:flex;
align-items:center;
gap:12px;
margin-bottom:8px;
">
<div style="
width:38px;
height:38px;
min-width:38px;
border-radius:50%;
background:#0a2b22;
color:#d4c08c;
display:flex;
align-items:center;
justify-content:center;
font-size:20px;
font-weight:700;
">✓</div>
<div>
<div style="
font-family:Georgia,'Times New Roman',serif;
font-size:1.45rem;
font-weight:700;
color:#0a2b22;
">Round Saved</div>
<div style="
font-size:0.84rem;
color:#6a756f;
">Your score has been added to the group record.</div>
</div>
</div>
<div style="
height:1px;
background:#e7e0d4;
margin:17px 0;
"></div>
<div style="
display:grid;
grid-template-columns:repeat(3,1fr);
gap:12px;
">
<div>
<div style="
font-size:0.64rem;
letter-spacing:0.07em;
color:#777e79;
text-transform:uppercase;
font-weight:700;
">Player</div>
<div style="
margin-top:4px;
color:#15251f;
font-weight:650;
">{saved['player']}</div>
</div>
<div>
<div style="
font-size:0.64rem;
letter-spacing:0.07em;
color:#777e79;
text-transform:uppercase;
font-weight:700;
">Date</div>
<div style="
margin-top:4px;
color:#15251f;
font-weight:650;
">{saved['date']}</div>
</div>
<div>
<div style="
font-size:0.64rem;
letter-spacing:0.07em;
color:#777e79;
text-transform:uppercase;
font-weight:700;
">Holes</div>
<div style="
margin-top:4px;
color:#15251f;
font-weight:650;
">{saved['holes']}{nine_text}</div>
</div>
</div>
<div style="
height:1px;
background:#eee8dd;
margin:16px 0;
"></div>
<div style="
font-size:0.64rem;
letter-spacing:0.07em;
color:#777e79;
text-transform:uppercase;
font-weight:700;
">Course</div>
<div style="
margin-top:4px;
color:#15251f;
font-size:1rem;
font-weight:650;
">{saved['course']}</div>
<div style="
margin-top:3px;
color:#6a756f;
font-size:0.84rem;
">{saved['tees']} tees</div>
<div style="
height:1px;
background:#eee8dd;
margin:16px 0;
"></div>
<div style="
display:grid;
grid-template-columns:repeat(2,1fr);
gap:12px;
">
<div style="
background:#f6f2e9;
border:1px solid #ece4d5;
border-radius:13px;
padding:13px;
">
<div style="
color:#747d77;
font-size:0.64rem;
letter-spacing:0.07em;
font-weight:700;
text-transform:uppercase;
">Gross Score</div>
<div style="
color:#0a2b22;
font-size:1.7rem;
font-weight:800;
margin-top:2px;
">{saved['gross_score']}</div>
</div>
<div style="
background:#f6f2e9;
border:1px solid #ece4d5;
border-radius:13px;
padding:13px;
">
<div style="
color:#747d77;
font-size:0.64rem;
letter-spacing:0.07em;
font-weight:700;
text-transform:uppercase;
">Round Rating</div>
<div style="
color:#967632;
font-size:1.7rem;
font-weight:800;
margin-top:2px;
">{round_rating_text}</div>
</div>
</div>
</div>""",
        unsafe_allow_html=True
    )

    if st.button(
        "Enter another round",
        use_container_width=True,
        key="clear_saved_round_card"
    ):

        st.session_state.saved_round_summary = None

        st.session_state.last_saved_round_fingerprint = None

        st.session_state.selected_course_id = None

        st.session_state.selected_course_label = None

        st.session_state.selected_course_short_label = None

        st.session_state.selected_course_data = None

        st.session_state.course_menu_open = False

        st.rerun()


# =========================================================
# ADD ROUND
# =========================================================

st.subheader(
    "Add Round"
)

show_saved_round_card()


# =========================================================
# PLAYER SELECTION
# =========================================================

st.markdown(
    "**Player**"
)

player_button_text = (
    st.session_state.selected_player_entry
    if st.session_state.selected_player_entry
    else "Select player"
)

player_arrow = (
    "▲"
    if st.session_state.player_menu_open
    else "▼"
)

if st.button(
    f"{player_button_text}  {player_arrow}",
    use_container_width=True,
    key="open_player_menu"
):

    st.session_state.player_menu_open = (
        not st.session_state.player_menu_open
    )

    st.rerun()


if st.session_state.player_menu_open:

    for player_name in PLAYERS:

        selected_marker = (
            " ✓"
            if (
                player_name
                == st.session_state.selected_player_entry
            )
            else ""
        )

        if st.button(
            f"{player_name}{selected_marker}",
            use_container_width=True,
            key=f"choose_player_{player_name}"
        ):

            st.session_state.selected_player_entry = (
                player_name
            )

            st.session_state.player_menu_open = False

            st.session_state.saved_round_summary = None

            st.session_state.last_saved_round_fingerprint = None

            st.rerun()


player = (
    st.session_state.selected_player_entry
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
# PLAYER HANDICAP PROGRESS
# =========================================================

if player is not None:

    player_completed_holes = (
        get_completed_holes(
            player
        )
    )

    if player_completed_holes < 54:

        st.markdown(
            "### Building your Handicap"
        )

        st.write(
            f"**{player_completed_holes} "
            f"of 54 completed holes**"
        )

        st.progress(
            min(
                player_completed_holes / 54,
                1.0
            )
        )

        show_54_hole_info()


# =========================================================
# GOLF COURSE SELECTOR
# =========================================================

st.markdown(
    "### Golf Course"
)

course_button_text = (
    st.session_state.selected_course_short_label
    if st.session_state.selected_course_short_label
    else "Select golf course"
)

course_arrow = (
    "▲"
    if st.session_state.course_menu_open
    else "▼"
)

if st.button(
    f"{course_button_text}  {course_arrow}",
    use_container_width=True,
    key="open_course_menu"
):

    st.session_state.course_menu_open = (
        not st.session_state.course_menu_open
    )

    st.rerun()


# =========================================================
# COURSE SEARCH
# =========================================================

if st.session_state.course_menu_open:

    course_search = st.text_input(
        "Search golf course",
        placeholder="Start typing, e.g. Brocton Hall",
        key="course_search_input"
    )

    clean_search = course_search.strip()

    if len(
        clean_search
    ) < 3:

        st.caption(
            "Type at least 3 letters."
        )

    else:

        try:

            with st.spinner(
                "Finding matching courses..."
            ):

                search_results = search_courses(
                    clean_search
                )

            if not search_results:

                st.info(
                    "No matching golf courses found."
                )

            else:

                st.caption(
                    "Tap the correct course:"
                )

                for result in search_results[
                    :10
                ]:

                    (
                        short_label,
                        full_label
                    ) = build_course_labels(
                        result
                    )

                    result_id = result.get(
                        "id"
                    )

                    if result_id:

                        if st.button(
                            full_label,
                            use_container_width=True,
                            key=f"course_result_{result_id}"
                        ):

                            try:

                                with st.spinner(
                                    "Loading course..."
                                ):

                                    loaded_course_data = get_course_details(
                                        result_id
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
                                    loaded_course_data
                                )

                                st.session_state.course_menu_open = False

                                st.session_state.saved_round_summary = None

                                st.session_state.last_saved_round_fingerprint = None

                                st.rerun()

                            except requests.exceptions.RequestException:

                                st.error(
                                    "Unable to load course details."
                                )

                if len(
                    search_results
                ) > 10:

                    st.caption(
                        "Type more letters to narrow the search results."
                    )

        except requests.exceptions.RequestException as error:

            st.error(
                "Unable to search the golf course database."
            )

            st.caption(
                str(error)
            )


# =========================================================
# SELECTED COURSE DATA
# =========================================================

course_data = (
    st.session_state.selected_course_data
)

course_id = (
    st.session_state.selected_course_id
)

if course_data:

    club_name = course_data.get(
        "club_name",
        ""
    )

    course_name = course_data.get(
        "course_name",
        ""
    )

    course_layout = (
        course_name
        or club_name
        or "Main Course"
    )

    tees = course_data.get(
        "tees",
        {}
    )

    male_tees = tees.get(
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
            for tee in male_tees
        ]

        selected_tee_name = st.selectbox(
            "Tees used",
            tee_names
        )

        tee_index = tee_names.index(
            selected_tee_name
        )

        selected_tee = male_tees[
            tee_index
        ]

        full_course_rating = selected_tee.get(
            "course_rating"
        )

        full_slope_rating = selected_tee.get(
            "slope_rating"
        )

        full_par = selected_tee.get(
            "par_total"
        )

        hole_data = selected_tee.get(
            "holes",
            []
        )


        # =================================================
        # 9 / 18 HOLE VALUES
        # =================================================

        nine_choice = None

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
            ) = get_9_hole_values(
                selected_tee,
                nine_choice
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

        rating_col, slope_col, par_col = st.columns(
            3
        )

        rating_col.metric(
            "Course Rating",
            (
                course_rating
                if course_rating is not None
                else "N/A"
            )
        )

        slope_col.metric(
            "Slope",
            (
                slope_rating
                if slope_rating is not None
                else "N/A"
            )
        )

        par_col.metric(
            "Par",
            (
                course_par
                if course_par is not None
                else "N/A"
            )
        )


        # =================================================
        # VALIDATE COURSE DATA
        # =================================================

        if (
            course_rating is None
            or slope_rating is None
        ):

            if holes_played == 9:

                st.warning(
                    "This course record does not contain a valid "
                    "9-hole Course Rating and Slope Rating for this nine."
                )

            else:

                st.warning(
                    "Course Rating or Slope Rating is unavailable "
                    "for these tees."
                )

        else:

            existing_handicap = (
                get_player_handicap(
                    player
                )
                if player is not None
                else None
            )


            # =============================================
            # ENTRY METHOD
            # =============================================

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


            # =============================================
            # TOTAL GROSS SCORE
            # =============================================

            if entry_method == "Total gross score":

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

                maximum_total_score = (
                    200
                    if holes_played == 18
                    else 100
                )

                handicap_score = st.number_input(
                    "Gross score for handicap purposes",
                    min_value=minimum_score,
                    max_value=maximum_total_score,
                    value=default_score,
                    step=1
                )

                round_rating = None

                expected_nine = None

                if holes_played == 18:

                    round_rating = calculate_18_hole_differential(
                        handicap_score,
                        course_rating,
                        slope_rating
                    )

                else:

                    played_nine_differential = calculate_9_hole_differential(
                        handicap_score,
                        course_rating,
                        slope_rating
                    )

                    if existing_handicap is not None:

                        (
                            round_rating,
                            expected_nine
                        ) = calculate_9_hole_round_rating(
                            played_nine_differential,
                            existing_handicap
                        )

                if round_rating is not None:

                    st.metric(
                        "Round Rating",
                        f"{round_rating:.1f}"
                    )

                    show_round_rating_info()

                elif holes_played == 9:

                    st.info(
                        "This 9-hole score will count towards your "
                        "**54 completed holes**. A full Round Rating "
                        "cannot yet be created because you don't have "
                        "an established Handicap Index."
                    )


                # =========================================
                # DUPLICATE PROTECTION
                # =========================================

                current_round_fingerprint = make_round_fingerprint(
                    player,
                    date_played,
                    holes_played,
                    nine_choice,
                    course_id,
                    selected_tee_name,
                    handicap_score,
                    handicap_score,
                    "Total",
                    None
                )

                already_saved = (
                    st.session_state.last_saved_round_fingerprint
                    == current_round_fingerprint
                )


                # =========================================
                # SAVE TOTAL ROUND
                # =========================================

                if st.button(
                    "Save Round",
                    use_container_width=True,
                    key="save_total_round",
                    disabled=already_saved,
                    type="primary"
                ):

                    if player is None:

                        st.error(
                            "Please select a player."
                        )

                    elif player not in PLAYER_ID_BY_NAME:

                        st.error(
                            "This player could not be found in the database."
                        )

                    else:

                        database_record = {
                            "player_id": PLAYER_ID_BY_NAME[
                                player
                            ],
                            "date_played": date_played.isoformat(),
                            "holes": int(
                                holes_played
                            ),
                            "nine": nine_choice,
                            "golf_course": club_name,
                            "course_layout": course_layout,
                            "course_api_id": (
                                str(
                                    course_id
                                )
                                if course_id is not None
                                else None
                            ),
                            "tees": selected_tee_name,
                            "course_rating": float(
                                course_rating
                            ),
                            "slope_rating": int(
                                slope_rating
                            ),
                            "par": (
                                int(
                                    course_par
                                )
                                if course_par is not None
                                else None
                            ),
                            "gross_score": int(
                                handicap_score
                            ),
                            "adjusted_score": int(
                                handicap_score
                            ),
                            "round_rating": (
                                round(
                                    float(
                                        round_rating
                                    ),
                                    1
                                )
                                if round_rating is not None
                                else None
                            ),
                            "entry_method": "Total",
                            "hole_scores": None,
                            "expected_nine": (
                                float(
                                    expected_nine
                                )
                                if expected_nine is not None
                                else None
                            )
                        }

                        try:

                            save_round_to_database(
                                database_record
                            )

                            st.session_state.last_saved_round_fingerprint = (
                                current_round_fingerprint
                            )

                            st.session_state.saved_round_summary = {
                                "player": player,
                                "date": date_played.strftime(
                                    "%d %b %Y"
                                ),
                                "holes": holes_played,
                                "nine": nine_choice,
                                "course": (
                                    st.session_state.selected_course_short_label
                                    or club_name
                                ),
                                "tees": selected_tee_name,
                                "gross_score": int(
                                    handicap_score
                                ),
                                "round_rating": (
                                    round(
                                        float(
                                            round_rating
                                        ),
                                        1
                                    )
                                    if round_rating is not None
                                    else None
                                )
                            }

                            load_rounds_from_database.clear()

                            st.rerun()

                        except DuplicateRoundError:

                            st.session_state.last_saved_round_fingerprint = (
                                current_round_fingerprint
                            )

                            st.warning(
                                "This round was already submitted, "
                                "so another copy was not saved."
                            )

                        except requests.exceptions.RequestException as error:

                            st.error(
                                "The round could not be saved to the database."
                            )

                            st.caption(
                                str(error)
                            )


            # =============================================
            # HOLE-BY-HOLE
            # =============================================

            else:

                required_holes = (
                    18
                    if holes_played == 18
                    else 9
                )

                if holes_played == 18:

                    holes_for_round = (
                        hole_data[
                            :18
                        ]
                    )

                elif nine_choice == "Front 9":

                    holes_for_round = (
                        hole_data[
                            :9
                        ]
                    )

                else:

                    holes_for_round = (
                        hole_data[
                            9:18
                        ]
                    )


                if len(
                    holes_for_round
                ) < required_holes:

                    st.warning(
                        "Complete hole-by-hole scorecard data isn't "
                        "available for this selection."
                    )

                    st.info(
                        "Please choose **Total gross score** instead."
                    )

                else:

                    course_handicap = None

                    if (
                        existing_handicap is not None
                        and full_course_rating is not None
                        and full_slope_rating is not None
                        and full_par is not None
                    ):

                        course_handicap = calculate_course_handicap(
                            existing_handicap,
                            full_slope_rating,
                            full_course_rating,
                            full_par
                        )

                        hi_col, ch_col = st.columns(
                            2
                        )

                        hi_col.metric(
                            "Handicap Index",
                            f"{existing_handicap:.1f}"
                        )

                        ch_col.metric(
                            "Course Handicap",
                            course_handicap
                        )


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

                        hole_number = get_hole_number(
                            hole,
                            fallback_hole
                        )

                        hole_par = get_hole_par(
                            hole
                        )

                        stroke_index = get_stroke_index(
                            hole,
                            fallback_hole
                        )

                        if hole_par is None:

                            hole_par = 4

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

                            strokes_received = handicap_strokes_on_hole(
                                course_handicap,
                                stroke_index
                            )

                            maximum_hole_score = (
                                int(
                                    hole_par
                                )
                                + 2
                                + strokes_received
                            )

                        hole_info_col, score_col = st.columns(
                            [
                                1,
                                1
                            ]
                        )

                        with hole_info_col:

                            st.write(
                                f"**Hole {hole_number}**  \n"
                                f"Par {hole_par} • SI {stroke_index}"
                            )

                        with score_col:

                            hole_score = st.number_input(
                                f"Hole {hole_number}",
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
                                label_visibility="collapsed"
                            )

                        raw_scores.append(
                            int(
                                hole_score
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

                        if adjusted_hole_score < hole_score:

                            adjustment_details.append(
                                (
                                    hole_number,
                                    int(
                                        hole_score
                                    ),
                                    adjusted_hole_score
                                )
                            )


                    gross_score = sum(
                        raw_scores
                    )

                    adjusted_score = sum(
                        adjusted_scores
                    )

                    round_rating = None

                    expected_nine = None

                    if holes_played == 18:

                        round_rating = calculate_18_hole_differential(
                            adjusted_score,
                            course_rating,
                            slope_rating
                        )

                    else:

                        played_nine_differential = calculate_9_hole_differential(
                            adjusted_score,
                            course_rating,
                            slope_rating
                        )

                        if existing_handicap is not None:

                            (
                                round_rating,
                                expected_nine
                            ) = calculate_9_hole_round_rating(
                                played_nine_differential,
                                existing_handicap
                            )


                    # =====================================
                    # SUMMARY
                    # =====================================

                    st.markdown(
                        "### Round summary"
                    )

                    gross_col, rating_col = st.columns(
                        2
                    )

                    gross_col.metric(
                        "Gross score",
                        gross_score
                    )

                    if round_rating is not None:

                        rating_col.metric(
                            "Round Rating",
                            f"{round_rating:.1f}"
                        )

                        show_round_rating_info()

                    else:

                        rating_col.metric(
                            "Round Rating",
                            "Pending"
                        )


                    if adjusted_score != gross_score:

                        st.info(
                            "Score used for handicap purposes: "
                            f"**{adjusted_score}**"
                        )

                        with st.expander(
                            "See automatic score adjustments"
                        ):

                            for (
                                adjusted_hole_number,
                                original_score,
                                new_score
                            ) in adjustment_details:

                                st.write(
                                    f"Hole {adjusted_hole_number}: "
                                    f"{original_score} → {new_score}"
                                )


                    # =====================================
                    # DUPLICATE PROTECTION
                    # =====================================

                    current_round_fingerprint = make_round_fingerprint(
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

                    already_saved = (
                        st.session_state.last_saved_round_fingerprint
                        == current_round_fingerprint
                    )


                    # =====================================
                    # SAVE HOLE-BY-HOLE
                    # =====================================

                    if st.button(
                        "Save Round",
                        use_container_width=True,
                        key="save_hole_round",
                        disabled=already_saved,
                        type="primary"
                    ):

                        if player is None:

                            st.error(
                                "Please select a player."
                            )

                        elif player not in PLAYER_ID_BY_NAME:

                            st.error(
                                "This player could not be found in the database."
                            )

                        else:

                            database_record = {
                                "player_id": PLAYER_ID_BY_NAME[
                                    player
                                ],
                                "date_played": date_played.isoformat(),
                                "holes": int(
                                    holes_played
                                ),
                                "nine": nine_choice,
                                "golf_course": club_name,
                                "course_layout": course_layout,
                                "course_api_id": (
                                    str(
                                        course_id
                                    )
                                    if course_id is not None
                                    else None
                                ),
                                "tees": selected_tee_name,
                                "course_rating": float(
                                    course_rating
                                ),
                                "slope_rating": int(
                                    slope_rating
                                ),
                                "par": (
                                    int(
                                        course_par
                                    )
                                    if course_par is not None
                                    else None
                                ),
                                "gross_score": int(
                                    gross_score
                                ),
                                "adjusted_score": int(
                                    adjusted_score
                                ),
                                "round_rating": (
                                    round(
                                        float(
                                            round_rating
                                        ),
                                        1
                                    )
                                    if round_rating is not None
                                    else None
                                ),
                                "entry_method": "Hole-by-hole",
                                "hole_scores": raw_scores,
                                "expected_nine": (
                                    float(
                                        expected_nine
                                    )
                                    if expected_nine is not None
                                    else None
                                )
                            }

                            try:

                                save_round_to_database(
                                    database_record
                                )

                                st.session_state.last_saved_round_fingerprint = (
                                    current_round_fingerprint
                                )

                                st.session_state.saved_round_summary = {
                                    "player": player,
                                    "date": date_played.strftime(
                                        "%d %b %Y"
                                    ),
                                    "holes": holes_played,
                                    "nine": nine_choice,
                                    "course": (
                                        st.session_state.selected_course_short_label
                                        or club_name
                                    ),
                                    "tees": selected_tee_name,
                                    "gross_score": int(
                                        gross_score
                                    ),
                                    "round_rating": (
                                        round(
                                            float(
                                                round_rating
                                            ),
                                            1
                                        )
                                        if round_rating is not None
                                        else None
                                    )
                                }

                                load_rounds_from_database.clear()

                                st.rerun()

                            except DuplicateRoundError:

                                st.session_state.last_saved_round_fingerprint = (
                                    current_round_fingerprint
                                )

                                st.warning(
                                    "This round was already submitted, "
                                    "so another copy was not saved."
                                )

                            except requests.exceptions.RequestException as error:

                                st.error(
                                    "The round could not be saved to the database."
                                )

                                st.caption(
                                    str(error)
                                )


# =========================================================
# PLAYER HANDICAPS
# =========================================================

st.divider()

st.subheader(
    "Player Handicaps"
)

if not all_rounds:

    st.info(
        "No scores have been recorded yet."
    )

else:

    rounds_df = pd.DataFrame(
        all_rounds
    )

    players_with_scores = [
        player_name
        for player_name in PLAYERS
        if player_name in rounds_df[
            "Player"
        ].unique()
    ]

    record_player = st.selectbox(
        "View player",
        players_with_scores
    )

    player_record_df = (
        rounds_df[
            rounds_df[
                "Player"
            ]
            == record_player
        ]
        .sort_values(
            "Date"
        )
        .reset_index(
            drop=True
        )
    )

    record_completed_holes = int(
        player_record_df[
            "Holes"
        ]
        .fillna(
            0
        )
        .sum()
    )


    # =====================================================
    # HANDICAP STATUS
    # =====================================================

    if record_completed_holes < 54:

        st.markdown(
            "### Building your Handicap"
        )

        st.write(
            f"**{record_completed_holes} "
            f"of 54 completed holes**"
        )

        st.progress(
            min(
                record_completed_holes / 54,
                1.0
            )
        )

        show_54_hole_info()

    else:

        record_differentials = [
            value
            for value in player_record_df[
                "Differential"
            ].tolist()
            if pd.notna(
                value
            )
        ]

        (
            record_handicap_index,
            record_counting_indexes,
            record_explanation
        ) = handicap_calculation(
            record_differentials
        )

        if record_handicap_index is None:

            st.warning(
                "54 completed holes have been recorded, "
                "but there is not yet enough completed "
                "Round Rating information to establish "
                "the Handicap Index automatically."
            )

        else:

            st.metric(
                "Handicap Index",
                f"{record_handicap_index:.1f}"
            )

            st.caption(
                "Unofficial WHS-based calculation"
            )

            st.write(
                f"**{record_explanation}**"
            )


    # =====================================================
    # SCORING RECORD
    # =====================================================

    st.markdown(
        "### Scoring Record"
    )

    display_df = (
        player_record_df.copy()
    )

    display_df[
        "Round Rating"
    ] = display_df[
        "Differential"
    ]

    display_columns = [
        "Date",
        "Golf Course",
        "Tees",
        "Holes",
        "Gross Score",
        "Round Rating"
    ]

    available_columns = [
        column
        for column in display_columns
        if column in display_df.columns
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
# ADMIN TOOLS
# =========================================================

st.divider()

with st.expander(
    "Admin tools"
):

    if not st.session_state.admin_authenticated:

        st.caption(
            "Administrative access is required to "
            "delete an incorrect round."
        )

        entered_admin_pin = st.text_input(
            "Admin PIN",
            type="password",
            key="admin_pin_input"
        )

        if st.button(
            "Unlock Admin",
            use_container_width=True,
            key="admin_login_button"
        ):

            entered_value = str(
                entered_admin_pin
            )

            correct_value = str(
                ADMIN_PIN
            )

            if hmac.compare_digest(
                entered_value,
                correct_value
            ):

                st.session_state.admin_authenticated = True

                st.session_state.pending_delete_round_id = None

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
            use_container_width=True,
            key="admin_logout_button"
        ):

            st.session_state.admin_authenticated = False

            st.session_state.pending_delete_round_id = None

            st.rerun()


        if all_rounds:

            st.markdown(
                "### Recorded rounds"
            )

            admin_rounds = sorted(
                all_rounds,
                key=lambda round_item: str(
                    round_item.get(
                        "Created At",
                        ""
                    )
                ),
                reverse=True
            )

            admin_display_rows = []

            for round_item in admin_rounds:

                admin_display_rows.append(
                    {
                        "Player": round_item.get(
                            "Player"
                        ),
                        "Date": round_item.get(
                            "Date"
                        ),
                        "Course": round_item.get(
                            "Golf Course"
                        ),
                        "Tees": round_item.get(
                            "Tees"
                        ),
                        "Holes": round_item.get(
                            "Holes"
                        ),
                        "Gross": round_item.get(
                            "Gross Score"
                        ),
                        "Round Rating": round_item.get(
                            "Differential"
                        )
                    }
                )

            admin_df = pd.DataFrame(
                admin_display_rows
            )

            st.dataframe(
                admin_df,
                hide_index=True,
                use_container_width=True
            )


            # =============================================
            # SELECT ROUND TO DELETE
            # =============================================

            round_options = {}

            for index, round_item in enumerate(
                admin_rounds
            ):

                round_id = round_item.get(
                    "ID"
                )

                short_id = (
                    str(
                        round_id
                    )[-8:]
                    if round_id is not None
                    else "unknown"
                )

                label = (
                    f"{round_item.get('Date')} • "
                    f"{round_item.get('Player')} • "
                    f"{round_item.get('Golf Course')} • "
                    f"{round_item.get('Tees')} • "
                    f"{round_item.get('Holes')} holes • "
                    f"Gross {round_item.get('Gross Score')} • "
                    f"{short_id}"
                )

                round_options[
                    label
                ] = round_item


            selected_admin_label = st.selectbox(
                "Select a round",
                list(
                    round_options.keys()
                ),
                key="admin_round_selector"
            )

            selected_admin_round = round_options[
                selected_admin_label
            ]

            st.markdown(
                "#### Selected round"
            )

            st.write(
                f"**Player:** "
                f"{selected_admin_round.get('Player')}"
            )

            st.write(
                f"**Date:** "
                f"{selected_admin_round.get('Date')}"
            )

            st.write(
                f"**Course:** "
                f"{selected_admin_round.get('Golf Course')}"
            )

            st.write(
                f"**Tees:** "
                f"{selected_admin_round.get('Tees')}"
            )

            st.write(
                f"**Gross score:** "
                f"{selected_admin_round.get('Gross Score')}"
            )

            st.write(
                f"**Adjusted score:** "
                f"{selected_admin_round.get('Adjusted Score')}"
            )

            if selected_admin_round.get(
                "Differential"
            ) is not None:

                st.write(
                    f"**Round Rating:** "
                    f"{selected_admin_round.get('Differential')}"
                )


            selected_round_id = selected_admin_round.get(
                "ID"
            )


            # =============================================
            # FIRST DELETE BUTTON
            # =============================================

            if (
                st.session_state.pending_delete_round_id
                != selected_round_id
            ):

                if st.button(
                    "Delete selected round",
                    use_container_width=True,
                    key="prepare_delete_round"
                ):

                    st.session_state.pending_delete_round_id = (
                        selected_round_id
                    )

                    st.rerun()


            # =============================================
            # CONFIRM DELETE
            # =============================================

            else:

                st.error(
                    "This will permanently delete the selected round."
                )

                st.write(
                    "Check the details above carefully before continuing."
                )

                confirm_col, cancel_col = st.columns(
                    2
                )

                with confirm_col:

                    if st.button(
                        "Yes, delete it",
                        use_container_width=True,
                        key="confirm_delete_round"
                    ):

                        try:

                            delete_round_from_database(
                                selected_round_id
                            )

                            st.session_state.pending_delete_round_id = None

                            load_rounds_from_database.clear()

                            st.rerun()

                        except requests.exceptions.RequestException as error:

                            st.error(
                                "The round could not be deleted."
                            )

                            st.caption(
                                str(error)
                            )

                with cancel_col:

                    if st.button(
                        "Cancel",
                        use_container_width=True,
                        key="cancel_delete_round"
                    ):

                        st.session_state.pending_delete_round_id = None

                        st.rerun()

        else:

            st.info(
                "There are currently no rounds to manage."
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Golf Group Handicaps provides an "
    "unofficial WHS-based handicap estimate "
    "and is not an authorised handicapping service."
)