import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Mental Health in Tech Survey",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# COLOUR PALETTE
# =========================================================

NAVY = "#17213D"
TEXT = "#18234A"
PURPLE = "#8B6EDB"
TEAL = "#39AFA8"
PEACH = "#F4A47C"

LIGHT_PURPLE = "#F1EDFF"
LIGHT_TEAL = "#EAF8F6"
LIGHT_PEACH = "#FFF0E8"

BACKGROUND = "#FAFAFC"
MUTED = "#657394"

# =========================================================
# PLOTLY THEME
# =========================================================

px.defaults.template = "plotly_white"

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #FAFAFC;
    color: #18234A;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1450px;
}

/* HEADINGS */

h1, h2, h3 {
    font-family: 'Poppins', sans-serif !important;
    color: #18234A !important;
}

h1 {
    font-size: 2.2rem !important;
    font-weight: 700 !important;
}

h2 {
    font-size: 1.55rem !important;
}

h3 {
    font-size: 1.15rem !important;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #17213D;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.sidebar-title {
    font-family: 'Poppins', sans-serif;
    font-size: 1.45rem;
    font-weight: 700;
    margin-bottom: 5px;
}

.sidebar-subtitle {
    font-size: 0.82rem;
    opacity: 0.75;
    margin-bottom: 25px;
}

/* HEADER */

.dashboard-header {
    background: linear-gradient(
        135deg,
        #F1EDFF 0%,
        #FAFAFC 55%,
        #EAF8F6 100%
    );
    border-radius: 22px;
    padding: 30px 35px;
    margin-bottom: 25px;
    border: 1px solid #E7E4F2;
}

.header-title {
    font-family: 'Poppins', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #18234A;
    margin-bottom: 8px;
}

.header-text {
    color: #536486;
    font-size: 1rem;
    line-height: 1.6;
    max-width: 850px;
}

/* KPI CARDS */

.kpi-card {
    border-radius: 18px;
    padding: 20px 22px;
    min-height: 125px;
    border: 1px solid rgba(0,0,0,0.05);
    box-shadow: 0 5px 18px rgba(23,33,61,0.06);
}

.kpi-purple {
    background: #F1EDFF;
}

.kpi-teal {
    background: #EAF8F6;
}

.kpi-peach {
    background: #FFF0E8;
}

.kpi-title {
    font-size: 0.82rem;
    color: #536486;
    margin-bottom: 7px;
    font-weight: 600;
}

.kpi-value {
    font-family: 'Poppins', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #18234A;
}

.kpi-description {
    font-size: 0.78rem;
    color: #657394;
    margin-top: 4px;
}

/* SECTION */

.section-label {
    font-family: 'Poppins', sans-serif;
    color: #18234A;
    font-size: 1.3rem;
    font-weight: 600;
    margin-top: 25px;
    margin-bottom: 12px;
}

/* INSIGHT */

.insight-box {
    background: #EAF8F6;
    border: 1px solid #CBEDEA;
    border-radius: 14px;
    padding: 16px 18px;
    color: #245F61;
    font-size: 0.9rem;
    line-height: 1.6;
    margin: 10px 0;
}

.insight-purple {
    background: #F1EDFF;
    border: 1px solid #DDD3FA;
    color: #51427D;
}

/* FOOTER */

.footer {
    text-align: center;
    color: #7A86A2;
    font-size: 0.78rem;
    padding: 25px 0 5px 0;
}

/* SELECT BOX */

div[data-baseweb="select"] > div {
    border-radius: 10px;
}

/* DATAFRAME */

div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

</style>
""",
    unsafe_allow_html=True
)

# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv("survey.csv")

df.columns = df.columns.str.strip()

# =========================================================
# CLEAN TREATMENT
# =========================================================

if "treatment" in df.columns:
    df["treatment"] = (
        df["treatment"]
        .astype(str)
        .str.strip()
        .str.title()
    )

# =========================================================
# CLEAN GENDER
# =========================================================

def clean_gender(gender):

    if pd.isna(gender):
        return "Unknown"

    gender = str(gender).strip().lower()

    if gender in [
        "male",
        "m",
        "man",
        "cis male",
        "cis man"
    ]:
        return "Male"

    if gender in [
        "female",
        "f",
        "woman",
        "cis female",
        "cis woman"
    ]:
        return "Female"

    return "Other"


if "Gender" in df.columns:
    df["Gender"] = df["Gender"].apply(clean_gender)

# =========================================================
# CLEAN AGE
# =========================================================

if "Age" in df.columns:

    df["Age"] = pd.to_numeric(
        df["Age"],
        errors="coerce"
    )

    df.loc[
        (df["Age"] < 18) | (df["Age"] > 100),
        "Age"
    ] = None

# =========================================================
# CHART STYLING FUNCTION
# =========================================================

def style_chart(fig, show_values=False):

    if show_values:

        fig.update_traces(
            texttemplate="%{text:.0%}",
            textposition="outside",
            textfont=dict(
                color=TEXT,
                size=13
            )
        )

    fig.update_layout(
        font=dict(
            family="Inter",
            color=TEXT
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="white",
        margin=dict(
            l=35,
            r=35,
            t=55,
            b=45
        ),
        hoverlabel=dict(
            font=dict(
                family="Inter",
                color=TEXT
            )
        )
    )

    fig.update_xaxes(
        tickfont=dict(
            color=TEXT,
            size=12
        ),
        title_font=dict(
            color=TEXT
        )
    )

    fig.update_yaxes(
        tickfont=dict(
            color=TEXT,
            size=12
        ),
        title_font=dict(
            color=TEXT
        ),
        gridcolor="#E6E8EF"
    )

    return fig

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">🧠 Mental Health</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">Technology Workplace Survey</div>',
        unsafe_allow_html=True
    )

    st.markdown("### Explore")

    section = st.radio(
        "",
        [
            "Overview",
            "Treatment Analysis",
            "Workplace Factors",
            "Demographic Analysis",
            "Geographic Analysis",
            "Data Explorer"
        ]
    )

    st.markdown("---")

    st.markdown(
        '<div style="text-align:center;padding:25px 5px;">'
        '<div style="font-size:3rem;">🧠♡</div>'
        '<div style="font-size:0.85rem;margin-top:10px;line-height:1.6;">'
        'Better mental health.<br>'
        'Stronger tech teams.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

# =========================================================
# MAIN HEADER
# =========================================================

st.markdown(
    '<div class="dashboard-header">'
    '<div class="header-title">🧠 Mental Health in Tech Survey</div>'
    '<div class="header-text">'
    'Exploratory analysis of mental health, treatment patterns, '
    'and workplace attitudes in the technology sector.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

# =========================================================
# OVERVIEW
# =========================================================

if section == "Overview":

    st.markdown(
        '<div class="section-label">Project Overview</div>',
        unsafe_allow_html=True
    )

    st.write(
        "This dashboard analyzes survey responses to understand "
        "mental health treatment patterns and workplace attitudes "
        "toward mental health."
    )

    # KPI calculations

    total_responses = len(df)
    total_variables = len(df.columns)

    treatment_yes = (
        (df["treatment"] == "Yes").sum()
    )

    treatment_rate = (
        treatment_yes / total_responses
        if total_responses > 0
        else 0
    )

    # KPI cards

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f'<div class="kpi-card kpi-purple">'
            f'<div class="kpi-title">TOTAL RESPONSES</div>'
            f'<div class="kpi-value">{total_responses:,}</div>'
            f'<div class="kpi-description">Survey participants</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f'<div class="kpi-card kpi-teal">'
            f'<div class="kpi-title">TOTAL VARIABLES</div>'
            f'<div class="kpi-value">{total_variables}</div>'
            f'<div class="kpi-description">Survey questions and fields</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f'<div class="kpi-card kpi-peach">'
            f'<div class="kpi-title">TREATMENT RATE</div>'
            f'<div class="kpi-value">{treatment_rate:.1%}</div>'
            f'<div class="kpi-description">Respondents reporting treatment</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Treatment distribution

    left, right = st.columns([1, 1])

    with left:

        st.markdown(
            '<div class="section-label">Treatment Distribution</div>',
            unsafe_allow_html=True
        )

        treatment_counts = (
            df["treatment"]
            .value_counts()
            .reset_index()
        )

        treatment_counts.columns = [
            "Treatment",
            "Count"
        ]

        fig = px.pie(
            treatment_counts,
            names="Treatment",
            values="Count",
            hole=0.55
        )

        fig.update_traces(
            textinfo="percent",
            textfont=dict(
                color=TEXT,
                size=14
            )
        )

        fig.update_layout(
            font=dict(
                family="Inter",
                color=TEXT
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="white",
            margin=dict(
                l=10,
                r=10,
                t=20,
                b=10
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.markdown(
            '<div class="section-label">Key Insight</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="insight-box">'
            '<b>About the survey</b><br><br>'
            'The survey explores how employees in the technology '
            'sector experience mental health issues and how workplace '
            'policies, support systems, and attitudes relate to treatment.'
            '<br><br>'
            'The analysis identifies important associations between '
            'treatment and factors such as family history, work '
            'interference, benefits, and access to care.'
            '</div>',
            unsafe_allow_html=True
        )

    # Family history

    st.markdown(
        '<div class="section-label">Treatment by Family History</div>',
        unsafe_allow_html=True
    )

    family_treatment = (
        pd.crosstab(
            df["family_history"],
            df["treatment"],
            normalize="index"
        )
        .reset_index()
    )

    if "Yes" in family_treatment.columns:

        fig = px.bar(
            family_treatment,
            x="family_history",
            y="Yes",
            text="Yes",
            labels={
                "family_history": "Family History",
                "Yes": "Treatment Rate"
            }
        )

        fig = style_chart(
            fig,
            show_values=True
        )

        fig.update_yaxes(
            tickformat=".0%",
            range=[0, 1]
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown(
        '<div class="insight-box insight-purple">'
        'Respondents with a family history of mental health '
        'conditions showed a higher treatment rate than respondents '
        'without a family history.<br><br>'
        '<b>Note:</b> This represents an association, not causation.'
        '</div>',
        unsafe_allow_html=True
    )

# =========================================================
# TREATMENT ANALYSIS
# =========================================================

elif section == "Treatment Analysis":

    st.header("Treatment Analysis")

    st.write(
        "Explore the relationship between mental health treatment "
        "and major factors identified during the exploratory analysis."
    )

    # Family history

    st.subheader("Family History")

    family_treatment = (
        pd.crosstab(
            df["family_history"],
            df["treatment"],
            normalize="index"
        )
        .reset_index()
    )

    if "Yes" in family_treatment.columns:

        fig = px.bar(
            family_treatment,
            x="family_history",
            y="Yes",
            text="Yes",
            labels={
                "family_history": "Family History",
                "Yes": "Treatment Rate"
            }
        )

        fig = style_chart(
            fig,
            show_values=True
        )

        fig.update_yaxes(
            tickformat=".0%",
            range=[0, 1]
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Work interference

    st.subheader("Work Interference")

    work_treatment = (
        pd.crosstab(
            df["work_interfere"],
            df["treatment"],
            normalize="index"
        )
        .reset_index()
    )

    if "Yes" in work_treatment.columns:

        fig = px.bar(
            work_treatment,
            x="work_interfere",
            y="Yes",
            text="Yes",
            labels={
                "work_interfere": "Work Interference",
                "Yes": "Treatment Rate"
            }
        )

        fig = style_chart(
            fig,
            show_values=True
        )

        fig.update_yaxes(
            tickformat=".0%",
            range=[0, 1]
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown(
        '<div class="insight-box">'
        'Treatment rates were substantially higher among respondents '
        'who reported that mental health interfered more frequently '
        'with their work.<br><br>'
        'This is an observational association and should not be '
        'interpreted as proof of causation.'
        '</div>',
        unsafe_allow_html=True
    )

# =========================================================
# WORKPLACE FACTORS
# =========================================================

elif section == "Workplace Factors":

    st.header("Workplace Factors")

    st.write(
        "Workplace policies and support systems can be examined "
        "alongside reported mental health treatment."
    )

    workplace_variables = [
        ("benefits", "Mental Health Benefits"),
        ("care_options", "Access to Care Options"),
        ("wellness_program", "Wellness Programs"),
        ("seek_help", "Help-Seeking Support"),
        ("obs_consequence", "Observed Workplace Consequences")
    ]

    for column, title in workplace_variables:

        if column not in df.columns:
            continue

        st.subheader(title)

        analysis = (
            pd.crosstab(
                df[column],
                df["treatment"],
                normalize="index"
            )
            .reset_index()
        )

        if "Yes" not in analysis.columns:
            continue

        fig = px.bar(
            analysis,
            x=column,
            y="Yes",
            text="Yes",
            labels={
                column: title,
                "Yes": "Treatment Rate"
            }
        )

        fig = style_chart(
            fig,
            show_values=True
        )

        fig.update_yaxes(
            tickformat=".0%",
            range=[0, 1]
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# =========================================================
# DEMOGRAPHIC ANALYSIS
# =========================================================

elif section == "Demographic Analysis":

    st.header("Demographic Analysis")

    # Gender

    if "Gender" in df.columns:

        st.subheader("Treatment Rate by Gender")

        gender_treatment = (
            pd.crosstab(
                df["Gender"],
                df["treatment"],
                normalize="index"
            )
            .reset_index()
        )

        if "Yes" in gender_treatment.columns:

            fig = px.bar(
                gender_treatment,
                x="Gender",
                y="Yes",
                text="Yes",
                labels={
                    "Gender": "Gender",
                    "Yes": "Treatment Rate"
                }
            )

            fig = style_chart(
                fig,
                show_values=True
            )

            fig.update_yaxes(
                tickformat=".0%",
                range=[0, 1]
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.markdown(
            '<div class="insight-box insight-purple">'
            '<b>Gender categories standardized:</b> Female, Male, '
            'Other, and Unknown.<br><br>'
            'Smaller groups should be interpreted cautiously because '
            'they contain fewer responses.'
            '</div>',
            unsafe_allow_html=True
        )

    # Age

    if "Age" in df.columns:

        st.subheader("Age Distribution")

        fig = px.histogram(
            df,
            x="Age",
            color="treatment",
            nbins=20,
            labels={
                "Age": "Age",
                "treatment": "Treatment"
            }
        )

        fig = style_chart(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Remote work

    if "remote_work" in df.columns:

        st.subheader("Treatment Rate by Remote Work")

        remote_treatment = (
            pd.crosstab(
                df["remote_work"],
                df["treatment"],
                normalize="index"
            )
            .reset_index()
        )

        if "Yes" in remote_treatment.columns:

            fig = px.bar(
                remote_treatment,
                x="remote_work",
                y="Yes",
                text="Yes",
                labels={
                    "remote_work": "Remote Work",
                    "Yes": "Treatment Rate"
                }
            )

            fig = style_chart(
                fig,
                show_values=True
            )

            fig.update_yaxes(
                tickformat=".0%",
                range=[0, 1]
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

# =========================================================
# GEOGRAPHIC ANALYSIS
# =========================================================

elif section == "Geographic Analysis":

    st.header("Geographic Analysis")

    st.write(
        "Country-level differences should be interpreted carefully "
        "because the survey contains many more responses from some "
        "countries than others."
    )

    if "Country" in df.columns:

        st.subheader("Survey Responses by Country")

        country_counts = (
            df["Country"]
            .value_counts()
            .head(15)
            .reset_index()
        )

        country_counts.columns = [
            "Country",
            "Responses"
        ]

        fig = px.bar(
            country_counts,
            x="Responses",
            y="Country",
            orientation="h",
            labels={
                "Responses": "Number of Responses"
            }
        )

        fig = style_chart(fig)

        fig.update_layout(
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # Country treatment rate

        country_treatment = (
            pd.crosstab(
                df["Country"],
                df["treatment"],
                normalize="index"
            )
            .reset_index()
        )

        country_counts_all = (
            df["Country"]
            .value_counts()
        )

        country_treatment["Responses"] = (
            country_treatment["Country"]
            .map(country_counts_all)
        )

        country_treatment = country_treatment[
            country_treatment["Responses"] >= 10
        ]

        if "Yes" in country_treatment.columns:

            country_treatment = (
                country_treatment
                .sort_values(
                    "Yes",
                    ascending=False
                )
            )

            st.subheader(
                "Treatment Rate by Country "
                "(Minimum 10 Responses)"
            )

            fig = px.bar(
                country_treatment,
                x="Country",
                y="Yes",
                text="Yes",
                labels={
                    "Yes": "Treatment Rate"
                }
            )

            fig = style_chart(
                fig,
                show_values=True
            )

            fig.update_yaxes(
                tickformat=".0%",
                range=[0, 1]
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

# =========================================================
# DATA EXPLORER
# =========================================================

elif section == "Data Explorer":

    st.header("Data Explorer")

    st.write(
        "Use the filter below to explore the survey responses."
    )

    if "Country" in df.columns:

        countries = sorted(
            df["Country"]
            .dropna()
            .astype(str)
            .unique()
        )

        selected_country = st.selectbox(
            "Select Country",
            ["All Countries"] + countries
        )

        filtered_df = df.copy()

        if selected_country != "All Countries":

            filtered_df = filtered_df[
                filtered_df["Country"]
                .astype(str)
                == selected_country
            ]

    else:

        filtered_df = df.copy()

    st.write(
        f"Showing **{len(filtered_df):,}** responses"
    )

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=500
    )

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer">'
    'Mental Health in Tech Survey &nbsp;•&nbsp; '
    'Labmentix Internship Project'
    '<br>'
    'Data-driven insights for healthier technology workplaces.'
    '</div>',
    unsafe_allow_html=True
)
