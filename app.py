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
# VISUAL THEME
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
}

/* ---------------------------------------------------------
   HEADER
--------------------------------------------------------- */

.golf-hero {
    background: linear-gradient(
        135deg,
        #071f19 0%,
        #0b3126 55%,
        #124333 100%
    );

    border-radius: 0 0 28px 28px;

    padding:
        34px
        24px
        30px
        24px;

    margin:
        0.8rem
        -1rem
        1.9rem
        -1rem;

    box-shadow:
        0 16px 34px
        rgba(10, 43, 34, 0.19);
}

.golf-hero-title {
    color: white !important;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size: 2.55rem;

    font-weight: 700;

    line-height: 1.1;
}

.golf-hero-subtitle {
    color:
        rgba(255, 255, 255, 0.82)
        !important;

    margin-top: 10px;

    font-size: 1rem;

    line-height: 1.5;
}


/* ---------------------------------------------------------
   BUTTONS
--------------------------------------------------------- */

.stButton > button {
    min-height: 50px;

    border-radius: 14px;

    font-weight: 650;
}

.stButton > button[kind="primary"],
button[data-testid="stBaseButton-primary"] {
    background:
        var(--green-dark)
        !important;

    color:
        white
        !important;
}

.stButton > button[kind="primary"] *,
button[data-testid="stBaseButton-primary"] * {
    color:
        white
        !important;
}


/* ---------------------------------------------------------
   METRICS
--------------------------------------------------------- */

[data-testid="stMetric"] {
    background: white;

    border:
        1px solid
        #e1dbcf;

    border-radius: 16px;

    padding:
        15px
        16px;
}


/* ---------------------------------------------------------
   EXPANDERS
--------------------------------------------------------- */

[data-testid="stExpander"] {
    background: white;

    border:
        1px solid
        #e2dcd0;

    border-radius: 14px;
}


/* ---------------------------------------------------------
   HOLE CARDS
--------------------------------------------------------- */

[data-testid="stVerticalBlockBorderWrapper"] {
    background:
        rgba(
            255,
            255,
            255,
            0.96
        );

    border-radius: 16px;

    box-shadow:
        0 3px 12px
        rgba(
            10,
            43,
            34,
            0.05
        );
}


/* ---------------------------------------------------------
   SCORE FIELD
--------------------------------------------------------- */

.gross-score-heading {
    color:
        var(--green-dark);

    font-size:
        0.82rem;

    font-weight:
        750;

    text-transform:
        uppercase;

    margin-top:
        0.5rem;

    margin-bottom:
        0.35rem;
}


/* ---------------------------------------------------------
   SECTION HEADINGS
--------------------------------------------------------- */

.secondary-section-title {
    color:
        var(--green-dark);

    font-size:
        1.55rem;

    font-weight:
        700;

    margin-bottom:
        1rem;
}


/* ---------------------------------------------------------
   MOBILE
--------------------------------------------------------- */

@media (
    max-width: 640px
) {

    .block-container {
        padding-left:
            1rem;

        padding-right:
            1rem;
    }

    .golf-hero {
        padding:
            30px
            18px
            26px
            18px;

        margin:
            0.8rem
            -1rem
            1.8rem
            -1rem;
    }

    .golf-hero-title {
        font-size:
            2.15rem;
    }

    .golf-hero-subtitle {
        font-size:
            0.95rem;
    }
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================
#
# IMPORTANT:
# Keep this HTML on a single constructed string.
# Indented multiline HTML can sometimes be interpreted by
# Streamlit/Markdown as a code block.
# =========================================================

hero_html = (
    '<div class="golf-hero">'
    '<div class="golf-hero-title">'
    'Handicap Builder'
    '</div>'
    '<div class="golf-hero-subtitle">'
    'Track rounds, compare performances and build an '
    'unofficial WHS-based Handicap Index.'
    '</div>'
    '</div>'
)

st.markdown(
    hero_html,
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


# =========================================================
# STORED 9-HOLE RATINGS
# =========================================================
#
# For a 9-hole submission:
#
# - Course Rating is NOT taken from the API.
# - Slope is NOT taken from the API.
# - Par is NOT taken from the API.
#
# These stored values are used where available.
#
# Brocton Hall and Castle are estimates.
# The user can overwrite any stored value.
# =========================================================

NINE_HOLE_RATINGS = [

    {
        "aliases": [
            "brocton hall",
            "brocton hall golf club"
        ],

        "tee":
            "yellow",

        "nine":
            "Front 9",

        "course_rating":
            33.8,

        "slope_rating":
            125,

        "par":
            34,

        "status":
            "Estimated"
    },

    {
        "aliases": [
            "the manor golf club",
            "manor golf club",
            "manor golf club ltd"
        ],

        "tee":
            "yellow",

        "nine":
            "Front 9",

        "course_rating":
            34.2,

        "slope_rating":
            130,

        "par":
            35,

        "status":
            "Published"
    },

    {
        "aliases": [
            "barlaston golf club",
            "barlaston"
        ],

        "tee":
            "yellow",

        "nine":
            "Front 9",

        "course_rating":
            32.3,

        "slope_rating":
            112,

        "par":
            35,

        "status":
            "Published"
    },

    {
        "aliases": [
            "stone golf club",
            "stone golf"
        ],

        "tee":
            "yellow",

        "nine":
            "Front 9",

        "course_rating":
            34.9,

        "slope_rating":
            124,

        "par":
            35,

        "status":
            "Published"
    },

    {
        "aliases": [
            "the castle golf & leisure",
            "castle golf & leisure",
            "the castle golf and leisure",
            "castle golf club"
        ],

        "tee":
            "blue",

        "nine":
            "Front 9",

        "course_rating":
            34.8,

        "slope_rating":
            122,

        "par":
            37,

        "status":
            "Estimated"
    }
]


# =========================================================
# ERRORS
# =========================================================

class DuplicateRoundError(
    Exception
):
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

    if key not in (
        st.session_state
    ):

        st.session_state[
            key
        ] = value


# =========================================================
# SUPABASE
# =========================================================

@st.cache_data(
    ttl=3600,
    show_spinner=False
)
def load_players_from_database():

    response = requests.get(

        f"{SUPABASE_URL}"
        f"/rest/v1/players",

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

        f"{SUPABASE_URL}"
        f"/rest/v1/rounds",

        headers=
            SUPABASE_HEADERS,

        params={
            "select":
                "*",

            "order":
                (
                    "date_played.asc,"
                    "created_at.asc"
                )
        },

        timeout=15
    )

    response.raise_for_status()

    return response.json()


def save_round_to_database(
    round_data
):

    response = requests.post(

        f"{SUPABASE_URL}"
        f"/rest/v1/rounds",

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

            or "duplicate"
            in text
        ):

            raise (
                DuplicateRoundError()
            )

        response.raise_for_status()


def delete_round_from_database(
    round_id
):

    response = requests.delete(

        f"{SUPABASE_URL}"
        f"/rest/v1/rounds",

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
# LOAD DATABASE
# =========================================================

try:

    database_players = (
        load_players_from_database()
    )

    database_rounds = (
        load_rounds_from_database()
    )


except (
    requests.exceptions
    .RequestException
) as error:

    st.error(
        "Unable to connect to "
        "the handicap database."
    )

    st.caption(
        str(error)
    )

    st.stop()


PLAYER_ID_BY_NAME = {

    row["name"]:
        row["id"]

    for row
    in database_players
}


PLAYER_NAME_BY_ID = {

    row["id"]:
        row["name"]

    for row
    in database_players
}


all_rounds = []


for row in database_rounds:

    player_name = (
        PLAYER_NAME_BY_ID.get(
            row.get(
                "player_id"
            )
        )
    )

    if player_name is None:
        continue


    date_value = (
        row.get(
            "date_played"
        )
    )


    try:

        date_value = (
            pd.to_datetime(
                date_value
            ).date()
        )

    except Exception:
        pass


    all_rounds.append({

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
            row.get(
                "golf_course"
            ),

        "Course / Layout":
            row.get(
                "course_layout"
            ),

        "Course API ID":
            row.get(
                "course_api_id"
            ),

        "Tees":
            row.get("tees"),

        "Course Rating":
            row.get(
                "course_rating"
            ),

        "Slope Rating":
            row.get(
                "slope_rating"
            ),

        "Par":
            row.get("par"),

        "Gross Score":
            row.get(
                "gross_score"
            ),

        "Adjusted Score":
            row.get(
                "adjusted_score"
            ),

        "Differential":
            row.get(
                "round_rating"
            ),

        "Entry Method":
            row.get(
                "entry_method"
            ),

        "Hole Scores":
            row.get(
                "hole_scores"
            ),

        "Expected Nine":
            row.get(
                "expected_nine"
            ),

        "Created At":
            row.get(
                "created_at"
            )
    })


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

        f"{GOLF_API_BASE}"
        f"/courses/{course_id}",

        headers=
            GOLF_HEADERS,

        timeout=15
    )

    response.raise_for_status()

    data = (
        response.json()
    )

    return (
        data.get(
            "course",
            data
        )
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
        / float(
            slope_rating
        )
    ) * (
        float(
            adjusted_score
        )
        - float(
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

            and pd.notna(
                value
            )
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


    elif count in [
        7,
        8
    ]:

        number_used = 2


    elif (
        9
        <= count
        <= 11
    ):

        number_used = 3


    elif (
        12
        <= count
        <= 14
    ):

        number_used = 4


    elif (
        15
        <= count
        <= 16
    ):

        number_used = 5


    elif (
        17
        <= count
        <= 18
    ):

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

        / number_used
    )


    handicap_index = min(

        average
        + adjustment,

        54.0
    )


    explanation = (

        f"Best "
        f"{number_used} "
        f"of "
        f"{min(count, 20)}"
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

        or rating is None

        or slope in (
            None,
            0
        )
    ):

        return None


    return (
        calculate_differential(

            adjusted,
            rating,
            slope
        )
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

        or rating is None

        or slope in (
            None,
            0
        )
    ):

        return None


    return (
        calculate_differential(

            adjusted,
            rating,
            slope
        )
    )


def build_effective_round_ratings(
    player_rounds
):

    total_holes = sum(

        int(
            r.get(
                "Holes"
            )
            or 0
        )

        for r
        in player_rounds
    )


    effective = []


    for round_item in (
        player_rounds
    ):

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

            and round_item.get(
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


    seed_diffs = []


    for round_item in (
        player_rounds
    ):

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


    (
        seed_hi,
        _,
        _
    ) = handicap_calculation(
        seed_diffs
    )


    if seed_hi is None:

        return effective


    working_hi = (
        seed_hi
    )


    for _ in range(8):

        candidate = []


        for round_item in (
            player_rounds
        ):

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

                            + estimated_expected_nine(
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


        (
            new_hi,
            _,
            _
        ) = handicap_calculation(
            candidate
        )


        if new_hi is None:
            break


        if abs(
            new_hi
            - working_hi
        ) < 0.05:

            working_hi = (
                new_hi
            )

            break


        working_hi = (
            new_hi
        )


    final_effective = []


    for round_item in (
        player_rounds
    ):

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

                        + estimated_expected_nine(
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


def get_player_rounds(
    player_name
):

    return sorted(

        [
            r

            for r
            in all_rounds

            if (
                r.get(
                    "Player"
                )
                == player_name
            )
        ],

        key=lambda r:
            r.get(
                "Date"
            )
    )


def get_completed_holes(
    player_name
):

    return sum(

        int(
            r.get(
                "Holes"
            )
            or 0
        )

        for r
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


    if sum(

        int(
            r.get(
                "Holes"
            )
            or 0
        )

        for r
        in player_rounds

    ) < 54:

        return None


    effective = (
        build_effective_round_ratings(
            player_rounds
        )
    )


    (
        handicap_index,
        _,
        _
    ) = handicap_calculation(

        [
            x

            for x
            in effective

            if x is not None
        ]
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

        * float(
            slope_rating
        )

        / 113

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

    if stroke_index is None:

        return None


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


    strokes = (
        full_cycles
    )


    if (
        stroke_index
        <= remainder
    ):

        strokes += 1


    return strokes


# =========================================================
# COURSE HELPERS
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
        and course_name != club
    ):

        short = (
            f"{club} – "
            f"{course_name}"
        )

    else:

        short = (
            club
            or course_name
            or "Unnamed course"
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


def yellow_default_index(
    tee_names
):

    for (
        i,
        tee_name
    ) in enumerate(
        tee_names
    ):

        if (
            "yellow"
            in str(
                tee_name
            ).lower()
        ):

            return i


    return 0


def normalise_text(
    value
):

    return (
        str(
            value
            or ""
        )
        .strip()
        .lower()
    )


def find_known_nine_rating(
    club_name,
    course_name,
    tee_name,
    nine_choice
):

    course_text = (

        normalise_text(
            club_name
        )

        + " "

        + normalise_text(
            course_name
        )
    )


    tee_text = (
        normalise_text(
            tee_name
        )
    )


    for item in (
        NINE_HOLE_RATINGS
    ):

        if (
            item["nine"]
            != nine_choice
        ):

            continue


        if (
            item["tee"]
            not in tee_text
        ):

            continue


        if any(

            alias
            in course_text

            for alias
            in item[
                "aliases"
            ]

        ):

            return item


    return None


def get_hole_number(
    hole,
    fallback
):

    return (

        hole.get(
            "hole"
        )

        or hole.get(
            "hole_number"
        )

        or hole.get(
            "number"
        )

        or fallback
    )


def get_hole_par(
    hole
):

    value = (

        hole.get(
            "par"
        )

        or hole.get(
            "par_value"
        )
    )


    try:

        return int(
            value
        )

    except (
        TypeError,
        ValueError
    ):

        return None


# =========================================================
# INFORMATION
# =========================================================

def show_round_rating_info():

    with st.expander(
        "What is a Round Rating?"
    ):

        st.markdown(
            """
**Round Rating** is our simpler name for the WHS **Score Differential**.

It adjusts a score for the difficulty of the course and tees. **Lower is better.**

For a 9-hole round, Handicap Builder combines the differential from the nine holes played with an expected-nine value.

The expected-nine calculation used here is an **unofficial approximation**, so it may differ slightly from an authorised WHS service.
"""
        )


def show_54_hole_info():

    with st.expander(
        "Why do I need 54 completed holes?"
    ):

        st.markdown(
            """
A player needs acceptable scores covering **54 holes** before an initial Handicap Index can be established.

Those 54 holes can be any combination of valid 9-hole and 18-hole rounds.

Once 54 holes have been reached, Handicap Builder can convert earlier 9-hole scores into 18-hole-equivalent Round Ratings.
"""
        )


def show_total_score_info():

    with st.expander(
        "Do I need to adjust my score?"
    ):

        st.markdown(
            """
Before an initial Handicap Index is established, the maximum score that counts on a hole is **par + 5**.

After a Handicap Index has been established, the maximum is **net double bogey**:

**Par + 2 + handicap strokes received**

If you're unsure whether your total needs adjusting, use **Hole-by-hole scores** instead. Handicap Builder will calculate the adjustment for you.
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


    return (
        hashlib.sha256(

            json.dumps(
                payload,
                sort_keys=True
            ).encode()

        ).hexdigest()
    )


# =========================================================
# SAVED ROUND CARD
# =========================================================

def show_saved_round_card():

    saved = (
        st.session_state
        .saved_round_summary
    )


    if not saved:

        return


    if (
        saved.get(
            "round_rating"
        )
        is not None
    ):

        rr = (
            f"{saved['round_rating']:.1f}"
        )

    else:

        rr = (
            "Pending"
        )


    st.success(

        f"Round saved — "
        f"{saved['player']} • "
        f"{saved['course']} • "
        f"Gross "
        f"{saved['gross_score']} • "
        f"Round Rating "
        f"{rr}"
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

    st.session_state
    .selected_player_entry

    if (
        st.session_state
        .selected_player_entry
    )

    else "Select player"
)


if st.button(

    (
        f"{player_button_text}  "
        f"{'▲' if st.session_state.player_menu_open else '▼'}"
    ),

    use_container_width=True,

    key=
        "open_player_menu"
):

    st.session_state.player_menu_open = (

        not (
            st.session_state
            .player_menu_open
        )
    )

    st.rerun()


if (
    st.session_state
    .player_menu_open
):

    for player_name in (
        PLAYERS
    ):

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
    st.session_state
    .selected_player_entry
)


date_played = (
    st.date_input(

        "Date played",

        value=
            date.today()
    )
)


holes_label = (
    st.radio(

        "Number of holes played",

        [
            "18 holes",
            "9 holes"
        ],

        horizontal=True
    )
)


holes_played = (

    18

    if (
        holes_label
        == "18 holes"
    )

    else 9
)


if player:

    player_completed_holes = (
        get_completed_holes(
            player
        )
    )


    if (
        player_completed_holes
        < 54
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
                / 54,

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

    st.session_state
    .selected_course_short_label

    if (
        st.session_state
        .selected_course_short_label
    )

    else (
        "Select golf course"
    )
)


if st.button(

    (
        f"{course_button_text}  "
        f"{'▲' if st.session_state.course_menu_open else '▼'}"
    ),

    use_container_width=True,

    key=
        "open_course_menu"
):

    st.session_state.course_menu_open = (

        not (
            st.session_state
            .course_menu_open
        )
    )

    st.rerun()


if (
    st.session_state
    .course_menu_open
):

    course_search = (
        st.text_input(

            "Search golf course",

            placeholder=
                "Start typing, e.g. Brocton Hall",

            key=
                "course_search_input"
        )
    )


    if (
        len(
            course_search.strip()
        )
        < 3
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
                    ) = build_course_labels(
                        result
                    )


                    result_id = (
                        result.get(
                            "id"
                        )
                    )


                    if (
                        result_id

                        and st.button(

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


        except (
            requests.exceptions
            .RequestException
        ) as error:

            st.error(
                "Unable to search the golf course database."
            )

            st.caption(
                str(error)
            )


course_data = (
    st.session_state
    .selected_course_data
)


course_id = (
    st.session_state
    .selected_course_id
)


# =========================================================
# SELECTED COURSE
# =========================================================

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

        or club_name

        or "Main Course"
    )


    male_tees = (

        (
            course_data.get(
                "tees",
                {}
            )
            or {}
        )

        .get(
            "male",
            []
        )
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


        # -----------------------------------------------------
        # 18-hole API information
        # -----------------------------------------------------

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


        nine_choice = (
            None
        )

        rating_status = (
            None
        )


        # =====================================================
        # 9 HOLES
        # =====================================================

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


            known_rating = (
                find_known_nine_rating(

                    club_name,
                    course_name,
                    selected_tee_name,
                    nine_choice
                )
            )


            if known_rating:

                default_cr = (
                    float(
                        known_rating[
                            "course_rating"
                        ]
                    )
                )

                default_slope = (
                    int(
                        known_rating[
                            "slope_rating"
                        ]
                    )
                )

                default_par = (
                    int(
                        known_rating[
                            "par"
                        ]
                    )
                )

                rating_status = (
                    known_rating[
                        "status"
                    ]
                )


            else:

                default_cr = (
                    None
                )

                default_slope = (
                    None
                )

                default_par = (
                    None
                )

                rating_status = (
                    "Manual"
                )


            st.markdown(
                "#### 9-hole course information"
            )


            if (
                rating_status
                == "Estimated"
            ):

                st.warning(
                    "These 9-hole rating figures are estimates. "
                    "You can overwrite them below."
                )


            elif (
                rating_status
                == "Published"
            ):

                st.success(
                    "Stored 9-hole rating found. "
                    "You can overwrite it if required."
                )


            else:

                st.info(
                    "No stored 9-hole rating was found for this "
                    "course and tee. Enter Course Rating, Slope "
                    "and Par manually."
                )


            c1, c2, c3 = (
                st.columns(3)
            )


            with c1:

                course_rating = (
                    st.number_input(

                        "9-hole Course Rating",

                        min_value=20.0,

                        max_value=50.0,

                        value=
                            default_cr,

                        step=0.1,

                        format="%.1f",

                        placeholder=
                            "e.g. 34.2",

                        key=(
                            f"nine_cr_"
                            f"{course_id}_"
                            f"{selected_tee_name}_"
                            f"{nine_choice}"
                        )
                    )
                )


            with c2:

                slope_rating = (
                    st.number_input(

                        "9-hole Slope",

                        min_value=55,

                        max_value=155,

                        value=
                            default_slope,

                        step=1,

                        placeholder=
                            "e.g. 125",

                        key=(
                            f"nine_slope_"
                            f"{course_id}_"
                            f"{selected_tee_name}_"
                            f"{nine_choice}"
                        )
                    )
                )


            with c3:

                course_par = (
                    st.number_input(

                        "9-hole Par",

                        min_value=25,

                        max_value=45,

                        value=
                            default_par,

                        step=1,

                        placeholder=
                            "e.g. 35",

                        key=(
                            f"nine_par_"
                            f"{course_id}_"
                            f"{selected_tee_name}_"
                            f"{nine_choice}"
                        )
                    )
                )


        # =====================================================
        # 18 HOLES
        # =====================================================

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

                    if (
                        course_rating
                        is not None
                    )

                    else "N/A"
                )
            )


            c2.metric(

                "Slope",

                (
                    slope_rating

                    if (
                        slope_rating
                        is not None
                    )

                    else "N/A"
                )
            )


            c3.metric(

                "Par",

                (
                    course_par

                    if (
                        course_par
                        is not None
                    )

                    else "N/A"
                )
            )


        ratings_complete = (

            course_rating
            is not None

            and slope_rating
            is not None

            and course_par
            is not None
        )


        if not ratings_complete:

            st.warning(
                "Course Rating, Slope and Par must all "
                "be entered before the score can be processed."
            )


        else:

            existing_handicap = (

                get_player_handicap(
                    player
                )

                if player

                else None
            )


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


            # =================================================
            # TOTAL GROSS SCORE
            # =================================================

            if (
                entry_method
                == "Total gross score"
            ):

                show_total_score_info()


                st.markdown(

                    (
                        '<div class="gross-score-heading">'
                        'Gross Score'
                        '</div>'
                    ),

                    unsafe_allow_html=True
                )


                handicap_score = (
                    st.number_input(

                        "Gross Score",

                        min_value=(
                            40

                            if holes_played
                            == 18

                            else 20
                        ),

                        max_value=(
                            200

                            if holes_played
                            == 18

                            else 100
                        ),

                        value=None,

                        step=1,

                        placeholder=
                            "Enter gross score",

                        label_visibility=
                            "collapsed"
                    )
                )


                if (
                    handicap_score
                    is not None
                ):

                    played_diff = (
                        calculate_differential(

                            handicap_score,
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


                    if (
                        holes_played
                        == 18
                    ):

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

                            + expected_nine
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
                            "the app will create its 18-hole-equivalent "
                            "Round Rating."
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

                        st.session_state
                        .last_saved_round_fingerprint

                        == fingerprint
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
                                    ),

                                "gross_score":
                                    int(
                                        handicap_score
                                    ),

                                "adjusted_score":
                                    int(
                                        handicap_score
                                    ),

                                "round_rating":
                                    (
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
                                    ),

                                "entry_method":
                                    "Total",

                                "hole_scores":
                                    None,

                                "expected_nine":
                                    (
                                        float(
                                            expected_nine
                                        )

                                        if (
                                            expected_nine
                                            is not None
                                        )

                                        else None
                                    )
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
                                        (
                                            st.session_state
                                            .selected_course_short_label

                                            or club_name
                                        ),

                                    "gross_score":
                                        int(
                                            handicap_score
                                        ),

                                    "round_rating":
                                        (
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
                                        )
                                }


                                load_rounds_from_database.clear()

                                st.rerun()


                            except DuplicateRoundError:

                                st.warning(
                                    "This round appears to "
                                    "have already been saved."
                                )


                            except (
                                requests.exceptions
                                .RequestException
                            ) as error:

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

                required_holes = (

                    18

                    if (
                        holes_played
                        == 18
                    )

                    else 9
                )


                if (
                    holes_played
                    == 18
                ):

                    holes_for_round = (
                        hole_data[:18]
                    )


                elif (
                    nine_choice
                    == "Front 9"
                ):

                    holes_for_round = (
                        hole_data[:9]
                    )


                else:

                    holes_for_round = (
                        hole_data[9:18]
                    )


                # -------------------------------------------------
                # For 9-hole entry we don't depend on API hole data.
                # Create blank hole records if necessary.
                # -------------------------------------------------

                if (
                    holes_played
                    == 9
                ):

                    holes_for_round = list(
                        holes_for_round
                    )


                    while (
                        len(
                            holes_for_round
                        )
                        < 9
                    ):

                        holes_for_round.append(
                            {}
                        )


                if (
                    holes_played
                    == 18

                    and len(
                        holes_for_round
                    )
                    < 18
                ):

                    st.warning(
                        "Complete 18-hole par information isn't "
                        "available for this course and tee. "
                        "Please use Total gross score."
                    )


                else:

                    course_handicap = (
                        None
                    )


                    if (
                        existing_handicap
                        is not None

                        and course_rating
                        is not None

                        and slope_rating
                        is not None

                        and course_par
                        is not None
                    ):

                        course_handicap = (
                            calculate_course_handicap(

                                existing_handicap,
                                slope_rating,
                                course_rating,
                                course_par
                            )
                        )


                        c1, c2 = (
                            st.columns(2)
                        )


                        c1.metric(

                            "Handicap Index",

                            f"{existing_handicap:.1f}"
                        )


                        c2.metric(

                            "Course Handicap",

                            course_handicap
                        )


                    st.markdown(
                        "#### Hole-by-hole entry"
                    )


                    st.caption(
                        "Enter the Stroke Index exactly as shown "
                        "on the scorecard. Stroke Index and score "
                        "are deliberately left blank."
                    )


                    raw_scores = []

                    adjusted_scores = []

                    entered_stroke_indexes = []

                    entered_pars = []

                    adjustment_details = []

                    complete_holes = 0


                    for i in range(
                        required_holes
                    ):

                        hole = (

                            holes_for_round[i]

                            if (
                                i
                                < len(
                                    holes_for_round
                                )
                            )

                            else {}
                        )


                        fallback_hole = (

                            i + 1

                            if (
                                holes_played
                                == 18

                                or nine_choice
                                == "Front 9"
                            )

                            else i + 10
                        )


                        hole_number = (
                            get_hole_number(

                                hole,
                                fallback_hole
                            )
                        )


                        api_par = (
                            get_hole_par(
                                hole
                            )
                        )


                        with st.container(
                            border=True
                        ):

                            st.markdown(
                                f"### Hole {hole_number}"
                            )


                            top1, top2 = (
                                st.columns(2)
                            )


                            # =====================================
                            # PAR
                            # =====================================

                            with top1:

                                if (
                                    holes_played
                                    == 9
                                ):

                                    par_options = [
                                        None,
                                        3,
                                        4,
                                        5,
                                        6
                                    ]


                                    hole_par = (
                                        st.selectbox(

                                            "Par",

                                            par_options,

                                            index=0,

                                            format_func=
                                                lambda x: (
                                                    "Select par"

                                                    if (
                                                        x
                                                        is None
                                                    )

                                                    else str(x)
                                                ),

                                            key=(
                                                f"par_"
                                                f"{course_id}_"
                                                f"{selected_tee_name}_"
                                                f"{nine_choice}_"
                                                f"{hole_number}"
                                            )
                                        )
                                    )


                                else:

                                    hole_par = (
                                        api_par
                                    )


                                    if (
                                        hole_par
                                        is not None
                                    ):

                                        st.markdown(
                                            "**Par**"
                                        )

                                        st.markdown(
                                            f"### {hole_par}"
                                        )


                                    else:

                                        par_options = [
                                            None,
                                            3,
                                            4,
                                            5,
                                            6
                                        ]


                                        hole_par = (
                                            st.selectbox(

                                                "Par",

                                                par_options,

                                                index=0,

                                                format_func=
                                                    lambda x: (
                                                        "Select par"

                                                        if (
                                                            x
                                                            is None
                                                        )

                                                        else str(x)
                                                    ),

                                                key=(
                                                    f"par_"
                                                    f"{course_id}_"
                                                    f"{selected_tee_name}_"
                                                    f"{hole_number}"
                                                )
                                            )
                                        )


                            # =====================================
                            # STROKE INDEX
                            # =====================================

                            with top2:

                                si_options = (

                                    [None]

                                    + list(
                                        range(
                                            1,
                                            19
                                        )
                                    )
                                )


                                stroke_index = (
                                    st.selectbox(

                                        "Stroke Index",

                                        si_options,

                                        index=0,

                                        format_func=
                                            lambda x: (
                                                "Select SI"

                                                if (
                                                    x
                                                    is None
                                                )

                                                else str(x)
                                            ),

                                        help=(
                                            "Choose the Stroke Index "
                                            "shown on the scorecard."
                                        ),

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


                            # =====================================
                            # SCORE
                            # =====================================

                            st.markdown(
                                "**Shots taken**"
                            )


                            hole_score = (
                                st.number_input(

                                    (
                                        f"Shots taken "
                                        f"on hole "
                                        f"{hole_number}"
                                    ),

                                    min_value=1,

                                    max_value=20,

                                    value=None,

                                    step=1,

                                    placeholder=
                                        "Enter score",

                                    label_visibility=
                                        "collapsed",

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


                            hole_complete = (

                                hole_par
                                is not None

                                and stroke_index
                                is not None

                                and hole_score
                                is not None
                            )


                            if hole_complete:

                                complete_holes += 1


                                entered_pars.append(

                                    int(
                                        hole_par
                                    )
                                )


                                entered_stroke_indexes.append(

                                    int(
                                        stroke_index
                                    )
                                )


                                raw_scores.append(

                                    int(
                                        hole_score
                                    )
                                )


                                # ---------------------------------
                                # Maximum score for handicap use
                                # ---------------------------------

                                if (
                                    existing_handicap
                                    is None

                                    or course_handicap
                                    is None
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

                                            int(
                                                stroke_index
                                            )
                                        )
                                    )


                                    maximum_hole_score = (

                                        int(
                                            hole_par
                                        )

                                        + 2

                                        + int(
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

                                    < int(
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


                    # =================================================
                    # ENTRY PROGRESS
                    # =================================================

                    st.caption(

                        f"{complete_holes} of "
                        f"{required_holes} holes "
                        f"are fully entered."
                    )


                    entry_complete = (

                        complete_holes
                        == required_holes
                    )


                    si_valid = (
                        False
                    )


                    par_valid = (
                        False
                    )


                    if entry_complete:

                        # ---------------------------------------------
                        # STROKE INDEX VALIDATION
                        # ---------------------------------------------

                        if (
                            holes_played
                            == 18
                        ):

                            si_valid = (

                                set(
                                    entered_stroke_indexes
                                )

                                == set(
                                    range(
                                        1,
                                        19
                                    )
                                )
                            )


                        else:

                            # Nine-hole scorecards may retain
                            # the full 1-18 SI allocation.
                            # We therefore only require nine
                            # distinct valid SI values.

                            si_valid = (

                                len(
                                    set(
                                        entered_stroke_indexes
                                    )
                                )

                                == 9
                            )


                        if not si_valid:

                            st.error(
                                "The Stroke Index values contain "
                                "duplicates or do not form a valid "
                                "scorecard allocation. Please check "
                                "the scorecard."
                            )


                        # ---------------------------------------------
                        # PAR VALIDATION
                        # ---------------------------------------------

                        entered_par_total = (
                            sum(
                                entered_pars
                            )
                        )


                        if (
                            holes_played
                            == 9
                        ):

                            par_valid = (

                                entered_par_total

                                == int(
                                    course_par
                                )
                            )


                            if not par_valid:

                                st.error(

                                    f"The individual hole pars total "
                                    f"{entered_par_total}, but the "
                                    f"9-hole course par entered above "
                                    f"is {int(course_par)}."
                                )


                        else:

                            par_valid = (
                                True
                            )


                    if not entry_complete:

                        st.info(
                            "Complete Par, Stroke Index and "
                            "Shots taken for every hole to see "
                            "the round calculation."
                        )


                    # =================================================
                    # ROUND CALCULATION
                    # =================================================

                    if (
                        entry_complete

                        and si_valid

                        and par_valid
                    ):

                        gross_score = (
                            sum(
                                raw_scores
                            )
                        )


                        adjusted_score = (
                            sum(
                                adjusted_scores
                            )
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


                        if (
                            holes_played
                            == 18
                        ):

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

                                + expected_nine
                            )


                        st.markdown(
                            "### Round summary"
                        )


                        c1, c2 = (
                            st.columns(2)
                        )


                        c1.metric(

                            "Gross Score",

                            gross_score
                        )


                        c2.metric(

                            "Round Rating",

                            (
                                f"{round_rating:.1f}"

                                if (
                                    round_rating
                                    is not None
                                )

                                else "Pending"
                            )
                        )


                        if (
                            adjusted_score
                            != gross_score
                        ):

                            st.info(

                                f"Score used for handicap purposes: "
                                f"**{adjusted_score}**"
                            )


                            with st.expander(
                                "See automatic score adjustments"
                            ):

                                for (
                                    hole_no,
                                    original,
                                    adjusted
                                ) in (
                                    adjustment_details
                                ):

                                    st.write(

                                        f"Hole "
                                        f"{hole_no}: "
                                        f"{original} "
                                        f"→ "
                                        f"{adjusted}"
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

                            st.session_state
                            .last_saved_round_fingerprint

                            == fingerprint
                        )


                        if st.button(

                            "Save round",

                            use_container_width=True,

                            type="primary",

                            disabled=
                                already_saved,

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
                                        ),

                                    "gross_score":
                                        int(
                                            gross_score
                                        ),

                                    "adjusted_score":
                                        int(
                                            adjusted_score
                                        ),

                                    "round_rating":
                                        (
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
                                        ),

                                    "entry_method":
                                        "Hole-by-hole",

                                    "hole_scores":
                                        raw_scores,

                                    "expected_nine":
                                        (
                                            float(
                                                expected_nine
                                            )

                                            if (
                                                expected_nine
                                                is not None
                                            )

                                            else None
                                        )
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
                                            (
                                                st.session_state
                                                .selected_course_short_label

                                                or club_name
                                            ),

                                        "gross_score":
                                            gross_score,

                                        "round_rating":
                                            (
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
                                            )
                                    }


                                    load_rounds_from_database.clear()

                                    st.rerun()


                                except DuplicateRoundError:

                                    st.warning(
                                        "This round appears to "
                                        "have already been saved."
                                    )


                                except (
                                    requests.exceptions
                                    .RequestException
                                ) as error:

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

    (
        '<div class="secondary-section-title">'
        'Player Handicaps'
        '</div>'
    ),

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

        for name
        in PLAYERS

        if name in (
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
            r.get(
                "Holes"
            )
            or 0
        )

        for r
        in player_record
    )


    effective_ratings = (
        build_effective_round_ratings(
            player_record
        )
    )


    if (
        record_completed_holes
        < 54
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
                / 54,

                1.0
            )
        )

        show_54_hole_info()


    else:

        (
            record_hi,
            _,
            explanation
        ) = handicap_calculation(

            [
                x

                for x
                in effective_ratings

                if x is not None
            ]
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


    display_rows = []


    for (
        round_item,
        effective_rating
    ) in zip(

        player_record,
        effective_ratings
    ):

        display_rows.append({

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
        })


    display_df = (
        pd.DataFrame(
            display_rows
        )
    )


    if not (
        display_df.empty
    ):

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
        st.session_state
        .admin_authenticated
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

            if (
                hmac.compare_digest(

                    str(
                        entered_pin
                    ),

                    str(
                        ADMIN_PIN
                    )
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

                key=lambda r:
                    str(
                        r.get(
                            "Created At",
                            ""
                        )
                    ),

                reverse=True
            )


            options = {}


            for r in (
                admin_rounds
            ):

                label = (

                    f"{r.get('Date')} • "
                    f"{r.get('Player')} • "
                    f"{r.get('Golf Course')} • "
                    f"{r.get('Tees')} • "
                    f"Gross "
                    f"{r.get('Gross Score')}"
                )


                options[
                    label
                ] = r


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

                f"**"
                f"{selected_round.get('Player')} "
                f"— "
                f"{selected_round.get('Date')}"
                f"**"
            )


            st.write(

                selected_round.get(
                    "Golf Course"
                )
            )


            st.write(

                f"{selected_round.get('Tees')} "
                f"tees • Gross "
                f"{selected_round.get('Gross Score')}"
            )


            selected_id = (
                selected_round.get(
                    "ID"
                )
            )


            if (

                st.session_state
                .pending_delete_round_id

                != selected_id
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
                    st.columns(2)
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


                        except (
                            requests.exceptions
                            .RequestException
                        ) as error:

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