import streamlit as st
import pandas as pd
from fpdf import FPDF

from services.scraper_service import fetch_posts
from services.ai_service import generate_summary
from services.translation_service import translate_text
from services.sentiment_service import analyze_sentiment
from services.category_service import classify_category
from services.gibberish_filter import is_gibberish
from services.clustering_service import cluster_posts

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="PassportPulse AI Dashboard",
    page_icon="🌍",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(to right, #0f172a, #111827);
    color: white;
}

.metric-card {
    background: #1e293b;
    padding: 20px;
    border-radius: 16px;
    text-align: center;
}

.post-card {
    background: #1e293b;
    padding: 20px;
    border-radius: 16px;
    margin-bottom: 20px;
    border-left: 5px solid #8b5cf6;
}

.summary-box {
    background: #312e81;
    padding: 12px;
    border-radius: 10px;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------

st.title("🌍 PassportPulse AI Dashboard")

# ---------------- SIDEBAR ----------------

st.sidebar.header("Filters")

platform_filter = st.sidebar.selectbox(
    "Platform",
    [
        "All",
        "Reddit",
        "Twitter",
        "LinkedIn",
        "Instagram",
        "Facebook",
        "YouTube",
        "TikTok"
    ]
)

category_filter = st.sidebar.selectbox(
    "Category",
    [
        "All",
        "Application",
        "Renewal",
        "Appointments",
        "Tatkal",
        "Visa",
        "Travel Issues",
        "Government Announcements",
        "Scams/Fraud",
        "News",
        "Personal Experiences"
    ]
)

sentiment_filter = st.sidebar.selectbox(
    "Sentiment",
    [
        "All",
        "Positive",
        "Negative",
        "Neutral"
    ]
)

search = st.sidebar.text_input("🔍 Search Posts")

# ---------------- FETCH POSTS ----------------

posts = fetch_posts()

# ---------------- PROCESS POSTS ----------------

clean_posts = []

process_btn = st.button("🚀 AI Process Posts")

if process_btn:

    with st.spinner("Processing posts using AI..."):

        for post in posts:

            # REMOVE GIBBERISH
            if not is_gibberish(post["text"]):

                # AI SUMMARY
                post["summary"] = generate_summary(
                    post["text"]
                )

                # SENTIMENT
                post["sentiment"] = analyze_sentiment(
                    post["text"]
                )

                # CATEGORY
                post["category"] = classify_category(
                    post["text"]
                )

                clean_posts.append(post)

        # CLUSTER POSTS
        clean_posts = cluster_posts(clean_posts)

        st.success("✅ AI Processing Completed!")

else:

    st.warning(
        "Click 'AI Process Posts' to analyze social media posts."
    )


# ---------------- CLUSTER POSTS ----------------

clean_posts = cluster_posts(clean_posts)

# ---------------- CREATE DATAFRAME ----------------

df = pd.DataFrame(clean_posts)

# ---------------- FILTERS ----------------

if not df.empty:

    if "platform" in df.columns:

        if platform_filter != "All":

            df = df[
                df["platform"] == platform_filter
            ]

    if "category" in df.columns:

        if category_filter != "All":

            df = df[
                df["category"] == category_filter
            ]

    if "sentiment" in df.columns:

        if sentiment_filter != "All":

            df = df[
                df["sentiment"] == sentiment_filter
            ]

    if "text" in df.columns:

        if search:

            df = df[
                df["text"].str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]


# ---------------- METRICS ----------------
col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(f"""
    <div class="metric-card">
        <h2>{len(df)}</h2>
        <p>Total Posts</p>
    </div>
    """, unsafe_allow_html=True)

with col2:

    platform_count = (
        df['platform'].nunique()
        if 'platform' in df.columns
        else 0
    )

    st.markdown(f"""
    <div class="metric-card">
        <h2>{platform_count}</h2>
        <p>Platforms</p>
    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown("""
    <div class="metric-card">
        <h2>10</h2>
        <p>Languages</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- EXPORT CSV ----------------

csv = df.to_csv(index=False)

st.download_button(
    label="⬇ Download CSV",
    data=csv,
    file_name="passport_posts.csv",
    mime="text/csv"
)

# ---------------- EXPORT PDF ----------------

def create_pdf(dataframe):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", size=12)

    pdf.cell(
        200,
        10,
        txt="PassportPulse Report",
        ln=True
    )

    for _, row in dataframe.iterrows():

        pdf.multi_cell(
            0,
            10,
            txt=f"{row['platform']} - {row['text']}"
        )

    pdf.output("passport_report.pdf")

create_pdf(df)

with open("passport_report.pdf", "rb") as file:

    st.download_button(
        label="⬇ Download PDF",
        data=file,
        file_name="passport_report.pdf",
        mime="application/pdf"
    )

# ---------------- TABS ----------------

tab1, tab2, tab3 = st.tabs([
    "📄 Posts",
    "📊 Analytics",
    "🧠 Clustered View"
])
# ---------------- POSTS TAB ----------------

with tab1:

    for _, row in df.iterrows():

        st.markdown(f"""
        <div class="post-card">

        <h4>{row['platform']} • {row['author']}</h4>

        <p>{row['text']}</p>

        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="summary-box">
        🤖 {row['summary']}
        </div>
        """, unsafe_allow_html=True)

        st.success(f"Category: {row['category']}")

        st.info(f"Sentiment: {row['sentiment']}")

        # ---------------- TRANSLATION ----------------

        language = st.selectbox(
            "🌐 Translate To",
            [
                "English",
                "Hindi",
                "Punjabi",
                "Spanish",
                "French",
                "German",
                "Arabic",
                "Chinese",
                "Russian",
                "Japanese"
            ],
            key=row["id"]
        )

        if language == "English":

            translated = row["text"]

        else:

            translated = translate_text(
                row["text"],
                language
            )

        st.write(translated)

        st.divider()


# ---------------- ANALYTICS TAB ----------------

with tab2:

    # PLATFORM ANALYTICS
    if "platform" in df.columns and not df.empty:

        st.subheader("Posts by Platform")

        st.bar_chart(
            df["platform"].value_counts()
        )

    else:

        st.warning("No platform data available.")

    # SENTIMENT ANALYTICS
    if "sentiment" in df.columns and not df.empty:

        st.subheader("Sentiment Analysis")

        st.bar_chart(
            df["sentiment"].value_counts()
        )

    else:

        st.warning("No sentiment data available.")

# ---------------- CLUSTERED VIEW ----------------
with tab3:

    if "cluster" in df.columns and not df.empty:

        grouped = df.groupby("cluster")

        for cluster, group in grouped:

            st.subheader(f"Cluster {cluster}")

            for _, row in group.iterrows():

                st.write(f"• {row['text']}")

    else:

        st.warning("No clustered posts available.")

