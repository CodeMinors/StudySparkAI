import streamlit as st
from google import genai

# Page setup
st.set_page_config(page_title="StudySpark AI", page_icon="📚", layout="wide")

st.title("📚 StudySpark AI")
st.write("Your personal AI companion for summarizing notes, creating quizzes, and designing study plans[cite: 1].")

# Sidebar - API Key and Model Selection
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Gemini API Key", type="password", help="Enter your Google Gemini API key")
    model_name = st.selectbox("Select Model", ["gemini-3.6-flash", "gemini-2.5-pro"], index=0)

# Helper function to query Gemini API
def generate_ai_response(client, prompt):
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

# Check for API key before rendering app features
if not api_key:
    st.info("👈 Please enter your Gemini API Key in the sidebar to get started.")
else:
    # Initialize Google GenAI client
    client = genai.Client(api_key=api_key)

    # Navigation Tabs
    tab_summary, tab_quiz, tab_planner = st.tabs(["📝 Summarize Notes", "❓ Generate Quiz", "📅 Study Planner"])

    # ---------------------------------------------------------
    # TAB 1: NOTE SUMMARIZER
    # ---------------------------------------------------------
    with tab_summary:
        st.subheader("Summarize Notes")
        notes_input = st.text_area("Paste your study notes or chapter text:", height=200)
        summary_style = st.selectbox("Summary Format", ["Key Bullet Points", "Detailed Outline", "Simple Executive Summary"])

        if st.button("Generate Summary", type="primary", key="sum_btn"):
            if notes_input.strip():
                prompt = f"""You are an expert tutor. Summarize the following study notes in a {summary_style} format. 
Highlight key terms and main concepts clearly.

Study Notes:
{notes_input}"""
                with st.spinner("Processing notes..."):
                    result = generate_ai_response(client, prompt)
                    if result:
                        st.success("Summary Ready!")
                        st.markdown(result)
            else:
                st.warning("Please paste some notes first.")

    # ---------------------------------------------------------
    # TAB 2: QUIZ GENERATOR
    # ---------------------------------------------------------
    with tab_quiz:
        st.subheader("Practice Quiz Generator")
        quiz_source = st.text_area("Enter study material or topic for the quiz:", height=150)
        col1, col2 = st.columns(2)
        with col1:
            num_questions = st.slider("Number of Questions", 1, 10, 5)
        with col2:
            difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])

        if st.button("Generate Quiz", type="primary", key="quiz_btn"):
            if quiz_source.strip():
                prompt = f"""You are an exam master. Generate a {num_questions}-question multiple-choice quiz ({difficulty} level) based on this content.
For each question, provide:
- 4 multiple choice options (A, B, C, D)
- The correct answer and a 1-sentence explanation hidden under an 'Answer Key' section at the end.

Content:
{quiz_source}"""
                with st.spinner("Generating questions..."):
                    result = generate_ai_response(client, prompt)
                    if result:
                        st.success("Quiz Generated!")
                        st.markdown(result)
            else:
                st.warning("Please enter study topics or text to generate a quiz.")

    # ---------------------------------------------------------
    # TAB 3: STUDY PLANNER
    # ---------------------------------------------------------
    with tab_planner:
        st.subheader("Custom Study Schedule")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            subject = st.text_input("Subject/Exam Name", placeholder="e.g., Chemistry Final")
        with col_b:
            days_left = st.number_input("Days Until Exam", min_value=1, max_value=60, value=7)
        with col_c:
            daily_hours = st.slider("Study Hours Per Day", 1, 10, 2)

        topics_list = st.text_area("List specific topics or chapters to cover:")

        if st.button("Create Study Schedule", type="primary", key="plan_btn"):
            if subject and topics_list.strip():
                prompt = f"""You are an academic productivity coach. Create a day-by-day study schedule for an upcoming exam.
- Subject: {subject}
- Timeframe: {days_left} days
- Available Time: {daily_hours} hours per day
- Topics to Cover: {topics_list}

Format the schedule cleanly with specific daily goals, break times, and review milestones."""
                with st.spinner("Building schedule..."):
                    result = generate_ai_response(client, prompt)
                    if result:
                        st.success("Study Schedule Created!")
                        st.markdown(result)
            else:
                st.warning("Please specify a subject and topics to cover.")