# import streamlit as st
# import preprocessor,helper
# import matplotlib.pyplot as plt
# import seaborn as sns

# st.sidebar.title("WhatsApp Chat Analyzer")

# uploaded_file = st.sidebar.file_uploader("Choose a file")
# if uploaded_file is not None:
#     bytes_data = uploaded_file.getvalue()
#     data = bytes_data.decode("utf-8")
#     df = preprocessor.preprocess(data)

#     # fetch unique users
#     user_list = df['user'].unique().tolist()
#     user_list.remove('group_notification')
#     user_list.sort()
#     user_list.insert(0,"Overall")

#     selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

#     if st.sidebar.button("Show Analysis"):

#         # Stats Area
#         num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
#         st.title("Top Statistics")
#         col1, col2, col3, col4 = st.columns(4)

#         with col1:
#             st.header("Total Messages")
#             st.title(num_messages)
#         with col2:
#             st.header("Total Words")
#             st.title(words)
#         with col3:
#             st.header("Media Shared")
#             st.title(num_media_messages)
#         with col4:
#             st.header("Links Shared")
#             st.title(num_links)

#         # monthly timeline
#         st.title("Monthly Timeline")
#         timeline = helper.monthly_timeline(selected_user,df)
#         fig,ax = plt.subplots()
#         ax.plot(timeline['time'], timeline['message'],color='green')
#         plt.xticks(rotation='vertical')
#         st.pyplot(fig)

#         # daily timeline
#         st.title("Daily Timeline")
#         daily_timeline = helper.daily_timeline(selected_user, df)
#         fig, ax = plt.subplots()
#         ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
#         plt.xticks(rotation='vertical')
#         st.pyplot(fig)

#         # activity map
#         st.title('Activity Map')
#         col1,col2 = st.columns(2)

#         with col1:
#             st.header("Most busy day")
#             busy_day = helper.week_activity_map(selected_user,df)
#             fig,ax = plt.subplots()
#             ax.bar(busy_day.index,busy_day.values,color='purple')
#             plt.xticks(rotation='vertical')
#             st.pyplot(fig)

#         with col2:
#             st.header("Most busy month")
#             busy_month = helper.month_activity_map(selected_user, df)
#             fig, ax = plt.subplots()
#             ax.bar(busy_month.index, busy_month.values,color='orange')
#             plt.xticks(rotation='vertical')
#             st.pyplot(fig)

#         st.title("Weekly Activity Map")
#         user_heatmap = helper.activity_heatmap(selected_user,df)
#         fig,ax = plt.subplots()
#         ax = sns.heatmap(user_heatmap)
#         st.pyplot(fig)

#         # finding the busiest users in the group(Group level)
#         if selected_user == 'Overall':
#             st.title('Most Busy Users')
#             x,new_df = helper.most_busy_users(df)
#             fig, ax = plt.subplots()

#             col1, col2 = st.columns(2)

#             with col1:
#                 ax.bar(x.index, x.values,color='red')
#                 plt.xticks(rotation='vertical')
#                 st.pyplot(fig)
#             with col2:
#                 st.dataframe(new_df)

#         # WordCloud
#         st.title("WordCloud")
#         df_wc = helper.create_wordcloud(selected_user,df)
#         fig,ax = plt.subplots()
#         ax.imshow(df_wc)
#         st.pyplot(fig)

#         # most common words
#         most_common_df = helper.most_common_words(selected_user,df)

#         fig,ax = plt.subplots()

#         ax.barh(most_common_df[0],most_common_df[1])
#         plt.xticks(rotation='vertical')

#         st.title('Most common words')
#         st.pyplot(fig)

#         # emoji analysis
#         emoji_df = helper.emoji_helper(selected_user,df)
#         st.title("Emoji Analysis")

#         col1,col2 = st.columns(2)

#         with col1:
#             st.dataframe(emoji_df)
#         with col2:
#             fig,ax = plt.subplots()
#             ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
#             st.pyplot(fig)



import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import html

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background: #0B141A;
    color: #E9EDEF;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111B21;
    border-right: 1px solid #26353D;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] label {
    color: #E9EDEF !important;
}

/* Hero */
.hero {
    background: linear-gradient(120deg, #075E54, #128C7E, #075E54);
    border-radius: 18px;
    padding: 35px 30px;
    margin-bottom: 30px;
    border: 1px solid #20A895;
}

.hero h1 {
    color: white;
    font-size: 38px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero p {
    color: #D9F5EE;
    font-size: 16px;
    margin-bottom: 0;
}

/* Section heading */
.section-title {
    font-size: 25px;
    font-weight: 750;
    color: #E9EDEF;
    margin-top: 35px;
    margin-bottom: 18px;
}

/* KPI cards */
.metric-card {
    background: #18262D;
    border: 1px solid #2B414A;
    border-radius: 15px;
    padding: 22px 18px;
    min-height: 125px;
    transition: 0.3s ease;
}

.metric-card:hover {
    border-color: #25D366;
    transform: translateY(-3px);
}

.metric-label {
    color: #AEBAC1;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 12px;
}

.metric-value {
    color: #25D366;
    font-size: 30px;
    font-weight: 800;
}

/* Chart containers */
.chart-card {
    background: #18262D;
    border: 1px solid #2B414A;
    border-radius: 15px;
    padding: 18px;
    margin-bottom: 20px;
}

.chart-card h3 {
    color: #E9EDEF;
    font-size: 18px;
    margin-bottom: 15px;
}

/* General text */
.stMarkdown p {
    color: #B9C5CB;
}

/* Buttons */
.stButton > button {
    background: #25D366;
    color: #0B141A;
    border: none;
    border-radius: 10px;
    font-weight: 750;
    padding: 12px;
    transition: 0.3s ease;
}

.stButton > button:hover {
    background: #1DAF57;
    color: white;
    border: none;
}

/* Inputs */
.stSelectbox div[data-baseweb="select"],
.stFileUploader section {
    background: #18262D;
    border-radius: 10px;
}

.stSelectbox label,
.stFileUploader label {
    color: #E9EDEF !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid #2B414A;
    border-radius: 10px;
}

/* Footer */
.footer {
    text-align: center;
    color: #81949D;
    padding: 30px 10px 10px;
    font-size: 13px;
}

.footer span {
    color: #25D366;
    font-weight: 700;
}

/* Responsive */
@media (max-width: 768px) {
    .hero h1 {
        font-size: 27px;
    }

    .hero {
        padding: 25px 18px;
    }

    .metric-value {
        font-size: 23px;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# MATPLOTLIB THEME
# ==========================================================

plt.rcParams.update({
    "figure.facecolor": "#18262D",
    "axes.facecolor": "#18262D",
    "axes.edgecolor": "#52636B",
    "axes.labelcolor": "#E9EDEF",
    "text.color": "#E9EDEF",
    "xtick.color": "#B9C5CB",
    "ytick.color": "#B9C5CB",
    "grid.color": "#34454D",
    "font.size": 10
})

sns.set_theme(
    style="darkgrid",
    rc={
        "figure.facecolor": "#18262D",
        "axes.facecolor": "#18262D",
        "axes.labelcolor": "#E9EDEF",
        "text.color": "#E9EDEF",
        "xtick.color": "#B9C5CB",
        "ytick.color": "#B9C5CB",
        "grid.color": "#34454D"
    }
)


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def section_heading(title, subtitle=None):
    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True
    )

    if subtitle:
        st.caption(subtitle)


def metric_card(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def display_chart(fig):
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def style_axis(ax, rotation=0):
    ax.tick_params(axis="x", rotation=rotation)
    ax.grid(axis="y", alpha=0.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


# ==========================================================
# HERO SECTION
# ==========================================================

st.markdown("""
<div class="hero">
    <h1>💬 WhatsApp Chat Analyzer</h1>
    <p>
        Explore your conversations, discover communication patterns,
        and uncover interesting insights from your WhatsApp chats.
    </p>
</div>
""", unsafe_allow_html=True)


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.markdown(
    """
    <div style="text-align:center; padding:15px 5px;">
        <div style="font-size:45px;">💬</div>
        <h2 style="color:#25D366; margin-bottom:5px;">
            Chat Insights
        </h2>
        <p style="color:#AEBAC1; font-size:13px;">
            Your conversations, visualized.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()

st.sidebar.markdown("### 📂 Upload Chat")

uploaded_file = st.sidebar.file_uploader(
    "Upload WhatsApp exported chat",
    type=["txt"],
    help="Upload a WhatsApp chat exported as a .txt file."
)

st.sidebar.markdown(
    """
    <div style="
        background:#18262D;
        padding:12px;
        border-radius:10px;
        margin-top:10px;
        color:#AEBAC1;
        font-size:12px;">
        💡 Export your WhatsApp chat using
        <b>Export Chat → Without Media</b>
        for the best results.
    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# PROCESS UPLOADED CHAT
# ==========================================================

if uploaded_file is not None:

    try:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = preprocessor.preprocess(data)

    except (UnicodeDecodeError, Exception):
        st.error(
            "Unable to process this chat file. "
            "Please upload a valid WhatsApp exported .txt file."
        )
        st.stop()

    if df.empty:
        st.warning("No messages were found in the uploaded chat.")
        st.stop()

    required_columns = {"user", "message", "date"}

    if not required_columns.issubset(df.columns):
        st.error(
            "The processed chat is missing required columns. "
            "Check your preprocessor.py file."
        )
        st.stop()

    # Unique users
    user_list = df["user"].dropna().unique().tolist()

    user_list = [
        user for user in user_list
        if user != "group_notification"
    ]

    user_list.sort()
    user_list.insert(0, "Overall")

    st.sidebar.divider()

    st.sidebar.markdown("### 👤 Select User")

    selected_user = st.sidebar.selectbox(
        "Analyze conversations of",
        user_list,
        label_visibility="collapsed"
    )

    st.sidebar.markdown("")

    show_analysis = st.sidebar.button(
        "🚀 Generate Analysis",
        use_container_width=True
    )

    if show_analysis:
        st.session_state["show_analysis"] = True
        st.session_state["selected_user"] = selected_user
        st.session_state["chat_df"] = df

    if (
        st.session_state.get("show_analysis", False)
        and "chat_df" in st.session_state
    ):

        df = st.session_state["chat_df"]
        selected_user = st.session_state["selected_user"]

        # ==================================================
        # TOP STATISTICS
        # ==================================================

        section_heading(
            "📊 Conversation Overview",
            f"Showing analytics for: {selected_user}"
        )

        num_messages, words, num_media_messages, num_links = (
            helper.fetch_stats(selected_user, df)
        )

        col1, col2, col3, col4 = st.columns(4, gap="medium")

        with col1:
            metric_card("💬 Total Messages", num_messages)

        with col2:
            metric_card("📝 Total Words", words)

        with col3:
            metric_card("📷 Media Shared", num_media_messages)

        with col4:
            metric_card("🔗 Links Shared", num_links)


        # ==================================================
        # TIMELINE ANALYSIS
        # ==================================================

        section_heading(
            "📈 Message Timeline",
            "Understand how your conversation activity changes over time."
        )

        col1, col2 = st.columns(2, gap="large")

        with col1:

            st.markdown("#### 📅 Monthly Timeline")

            timeline = helper.monthly_timeline(selected_user, df)

            if not timeline.empty:

                fig, ax = plt.subplots(figsize=(8, 4))

                ax.plot(
                    timeline["time"],
                    timeline["message"],
                    color="#25D366",
                    linewidth=2.5,
                    marker="o",
                    markersize=4
                )

                ax.fill_between(
                    range(len(timeline)),
                    timeline["message"].values,
                    alpha=0.12,
                    color="#25D366"
                )

                ax.set_ylabel("Number of Messages")
                ax.set_xlabel("Month")
                style_axis(ax, 45)

                display_chart(fig)

            else:
                st.info("No monthly timeline data available.")

        with col2:

            st.markdown("#### 📆 Daily Timeline")

            daily_timeline = helper.daily_timeline(
                selected_user, df
            )

            if not daily_timeline.empty:

                fig, ax = plt.subplots(figsize=(8, 4))

                ax.plot(
                    daily_timeline["only_date"],
                    daily_timeline["message"],
                    color="#00B4D8",
                    linewidth=2,
                    alpha=0.9
                )

                ax.set_ylabel("Number of Messages")
                ax.set_xlabel("Date")
                style_axis(ax, 45)

                display_chart(fig)

            else:
                st.info("No daily timeline data available.")


        # ==================================================
        # ACTIVITY ANALYSIS
        # ==================================================

        section_heading(
            "🔥 Activity Analysis",
            "Discover when your conversations are most active."
        )

        col1, col2 = st.columns(2, gap="large")

        with col1:

            st.markdown("#### 📅 Busiest Days")

            busy_day = helper.week_activity_map(
                selected_user, df
            )

            if not busy_day.empty:

                fig, ax = plt.subplots(figsize=(7, 4))

                ax.bar(
                    busy_day.index,
                    busy_day.values,
                    color="#25D366",
                    width=0.65
                )

                ax.set_ylabel("Messages")
                ax.set_xlabel("Day")
                style_axis(ax, 30)

                display_chart(fig)

            else:
                st.info("No weekly activity data available.")

        with col2:

            st.markdown("#### 🗓️ Busiest Months")

            busy_month = helper.month_activity_map(
                selected_user, df
            )

            if not busy_month.empty:

                fig, ax = plt.subplots(figsize=(7, 4))

                ax.bar(
                    busy_month.index,
                    busy_month.values,
                    color="#00B4D8",
                    width=0.65
                )

                ax.set_ylabel("Messages")
                ax.set_xlabel("Month")
                style_axis(ax, 30)

                display_chart(fig)

            else:
                st.info("No monthly activity data available.")


        # ==================================================
        # WEEKLY HEATMAP
        # ==================================================

        section_heading(
            "🗓️ Weekly Activity Heatmap",
            "Explore the distribution of your messages across days and hours."
        )

        user_heatmap = helper.activity_heatmap(
            selected_user, df
        )

        if user_heatmap is not None and not user_heatmap.empty:

            fig, ax = plt.subplots(figsize=(14, 5))

            sns.heatmap(
                user_heatmap,
                ax=ax,
                cmap="Greens",
                linewidths=0.3,
                linecolor="#18262D",
                cbar_kws={"label": "Message Frequency"}
            )

            ax.set_xlabel("Hour of Day")
            ax.set_ylabel("Day of Week")

            display_chart(fig)

        else:
            st.info("No heatmap data available.")


        # ==================================================
        # MOST ACTIVE USERS
        # ==================================================

        if selected_user == "Overall":

            section_heading(
                "👥 Most Active Users",
                "See who contributes most to the group conversation."
            )

            x, new_df = helper.most_busy_users(df)

            col1, col2 = st.columns([1.5, 1], gap="large")

            with col1:

                if not x.empty:

                    fig, ax = plt.subplots(figsize=(8, 5))

                    ax.bar(
                        x.index.astype(str),
                        x.values,
                        color="#25D366",
                        width=0.65
                    )

                    ax.set_ylabel("Messages")
                    ax.set_xlabel("Users")
                    style_axis(ax, 45)

                    display_chart(fig)

                else:
                    st.info("No user activity data available.")

            with col2:

                st.markdown("#### 📋 User Statistics")

                st.dataframe(
                    new_df,
                    use_container_width=True,
                    hide_index=True
                )


        # ==================================================
        # WORDCLOUD
        # ==================================================

        section_heading(
            "☁️ WordCloud",
            "A visual representation of the most frequently used words."
        )

        df_wc = helper.create_wordcloud(
            selected_user, df
        )

        if df_wc is not None:

            fig, ax = plt.subplots(figsize=(12, 5))

            ax.imshow(df_wc, interpolation="bilinear")
            ax.axis("off")

            display_chart(fig)

        else:
            st.info("Unable to generate a WordCloud for this conversation.")


        # ==================================================
        # MOST COMMON WORDS
        # ==================================================

        section_heading(
            "📝 Most Common Words",
            "Find out which words appear most frequently in the conversation."
        )

        most_common_df = helper.most_common_words(
            selected_user, df
        )

        if most_common_df is not None and not most_common_df.empty:

            fig, ax = plt.subplots(figsize=(10, 5))

            ax.barh(
                most_common_df[0].astype(str).iloc[::-1],
                most_common_df[1].iloc[::-1],
                color="#00B4D8",
                height=0.65
            )

            ax.set_xlabel("Frequency")
            ax.set_ylabel("Words")

            style_axis(ax)

            display_chart(fig)

        else:
            st.info("No common words available.")


        # ==================================================
        # EMOJI ANALYSIS
        # ==================================================

        section_heading(
            "😀 Emoji Analysis",
            "Explore the emojis used throughout your conversations."
        )

        emoji_df = helper.emoji_helper(
            selected_user, df
        )

        if emoji_df is not None and not emoji_df.empty:

            col1, col2 = st.columns([1, 1.3], gap="large")

            with col1:

                st.markdown("#### 🏆 Emoji Statistics")

                st.dataframe(
                    emoji_df,
                    use_container_width=True,
                    hide_index=True
                )

            with col2:

                st.markdown("#### 📊 Top 5 Emojis")

                top_emojis = emoji_df.head(5)

                fig, ax = plt.subplots(figsize=(7, 5))

                ax.pie(
                    top_emojis[1],
                    labels=top_emojis[0],
                    autopct="%1.1f%%",
                    startangle=90,
                    wedgeprops={
                        "width": 0.45,
                        "edgecolor": "#18262D"
                    },
                    textprops={
                        "color": "#E9EDEF",
                        "fontsize": 11
                    }
                )

                ax.set_title(
                    "Emoji Distribution",
                    color="#E9EDEF"
                )

                display_chart(fig)

        else:
            st.info("No emojis found in this conversation.")


        # ==================================================
        # FOOTER
        # ==================================================

        st.markdown("---")

        st.markdown("""
        <div class="footer">
            Made with ❤️ by <span>arsu</span>
            <br><br>
            WhatsApp Chat Analyzer | Powered by Streamlit
        </div>
        """, unsafe_allow_html=True)



# ======================================================
# EMPTY STATE
# ======================================================

else:

    st.markdown("""
    <div style="
        background:#18262D;
        border:1px solid #2B414A;
        border-radius:18px;
        padding:55px 25px;
        text-align:center;
        margin-top:30px;">

        <div style="font-size:65px;">📊</div>

        <h2 style="color:#E9EDEF;">
            Your Chat, Your Insights
        </h2>

        <p style="
            color:#AEBAC1;
            font-size:16px;
            max-width:600px;
            margin:auto;">
            Upload your WhatsApp exported chat from the sidebar
            and generate detailed insights about messages,
            activity patterns, frequently used words and emojis.
        </p>

        <br>

        <div style="color:#25D366; font-weight:700;">
            Upload → Select User → Generate Analysis
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
        Made with ❤️ by <span>arsu</span>
        <br><br>
        WhatsApp Chat Analyzer | Powered by Streamlit
    </div>
    """, unsafe_allow_html=True)
