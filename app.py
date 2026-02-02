import streamlit as st
from anthropic import Anthropic
import base64

# --- Page Config ---
st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Custom CSS - Dark Theme with Cream/White Accents ---
st.markdown("""
<style>
    /* Import font */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Space Grotesk', sans-serif;
    }
    
    /* Main background with subtle abstract gradient */
    .stApp {
        background: 
            radial-gradient(ellipse at 20% 20%, rgba(59, 130, 246, 0.03) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 30%, rgba(139, 92, 246, 0.025) 0%, transparent 50%),
            radial-gradient(ellipse at 40% 80%, rgba(236, 72, 153, 0.02) 0%, transparent 50%),
            radial-gradient(ellipse at 90% 90%, rgba(34, 211, 238, 0.015) 0%, transparent 40%),
            #0a0a0a;
        background-attachment: fixed;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 3rem 0;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        color: #fafaf9;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
        letter-spacing: -0.03em;
        text-shadow: 0 0 40px rgba(250, 250, 249, 0.15);
    }
    
    .main-header .accent {
        background: linear-gradient(90deg, #ffffff, #a8a29e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .main-header p {
        color: #78716c;
        font-size: 1.1rem;
        font-weight: 400;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #0a0a0a;
        border-right: 1px solid #1c1917;
    }
    
    section[data-testid="stSidebar"] .stMarkdown h2 {
        color: #fafaf9 !important;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #d6d3d1 !important;
        font-weight: 500;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    section[data-testid="stSidebar"] label {
        color: #a8a29e !important;
        font-weight: 500;
        font-size: 0.8rem;
    }
    
    section[data-testid="stSidebar"] p {
        color: #78716c !important;
    }
    
    section[data-testid="stSidebar"] .stTextInput > div > div > input {
        background: #171717 !important;
        border: 1px solid #292524 !important;
        color: #fafaf9 !important;
        border-radius: 8px !important;
    }
    
    section[data-testid="stSidebar"] .stTextInput > div > div > input:focus {
        border-color: #fafaf9 !important;
        box-shadow: 0 0 0 1px rgba(250, 250, 249, 0.1) !important;
    }
    
    /* Hide "Press Enter to apply" tooltip */
    .stTextInput > div > div > span,
    .stTextInput [data-testid="InputInstructions"] {
        display: none !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox > div > div {
        background: #171717 !important;
        border: 1px solid #292524 !important;
        border-radius: 8px !important;
        color: #fafaf9 !important;
    }
    
    /* Buttons - cream/white style */
    .stButton > button {
        background: #fafaf9 !important;
        color: #0a0a0a !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 50px !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 20px rgba(250, 250, 249, 0.1) !important;
    }
    
    .stButton > button:hover {
        background: #ffffff !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 0 30px rgba(250, 250, 249, 0.2) !important;
    }
    
    /* Chat message containers */
    .stChatMessage {
        background: #171717 !important;
        border: 1px solid #292524 !important;
        border-radius: 16px !important;
        padding: 1.25rem !important;
    }
    
    .stChatMessage p {
        color: #e7e5e4 !important;
    }
    
    /* Custom chat avatars */
    .stChatMessage [data-testid="chatAvatarIcon-assistant"] {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
        border-radius: 8px !important;
    }
    
    .stChatMessage [data-testid="chatAvatarIcon-user"] {
        background: linear-gradient(135deg, #fafaf9, #d6d3d1) !important;
        border-radius: 50% !important;
    }
    
    /* Override avatar icons with emojis via pseudo-elements */
    [data-testid="chatAvatarIcon-assistant"] svg {
        display: none !important;
    }
    
    [data-testid="chatAvatarIcon-user"] svg {
        display: none !important;
    }
    
    /* Chat input */
    .stChatInput {
        background: #171717 !important;
        border: 1px solid #292524 !important;
        border-radius: 50px !important;
    }
    
    .stChatInput > div {
        background: #171717 !important;
        border-radius: 50px !important;
    }
    
    .stChatInput textarea {
        background: #171717 !important;
        color: #fafaf9 !important;
        border: none !important;
    }
    
    /* Stats cards - transparent/glass effect */
    .stat-card {
        background: rgba(23, 23, 23, 0.75);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(41, 37, 36, 0.5);
        border-radius: 16px;
        padding: 1.5rem 1rem;
        text-align: center;
        min-height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        border-color: rgba(63, 63, 70, 0.5);
        box-shadow: 0 0 30px rgba(250, 250, 249, 0.03);
    }
    
    .stat-card h3 {
        color: #57534e;
        font-size: 0.65rem;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        font-weight: 600;
    }
    
    .stat-card p {
        color: #fafaf9;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0;
    }
    
    /* Stats container - transparent */
    .stats-container {
        background: rgba(10, 10, 10, 0.75);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-top: 1px solid rgba(41, 37, 36, 0.5);
        padding: 1.5rem 0;
        margin-top: 2rem;
    }
    
    /* Intensity colors */
    .intensity-chill { color: #86efac !important; }
    .intensity-balanced { color: #fcd34d !important; }
    .intensity-brutal { color: #fca5a5 !important; }
    
    /* Dividers */
    hr {
        border-color: #1c1917 !important;
        margin: 2rem 0 !important;
    }
    
    /* Alert boxes */
    .stAlert {
        background: #171717 !important;
        border: 1px solid #292524 !important;
        border-radius: 12px !important;
        color: #e7e5e4 !important;
    }
    
    /* File uploader */
    section[data-testid="stSidebar"] .stFileUploader {
        background: #171717 !important;
        border: 1px dashed #292524 !important;
        border-radius: 12px !important;
    }
    
    section[data-testid="stSidebar"] .stFileUploader:hover {
        border-color: #57534e !important;
    }
    
    /* Resume preview */
    .resume-preview {
        background: #171717;
        border: 1px solid #365314;
        border-radius: 8px;
        padding: 0.75rem;
        margin-top: 0.5rem;
        color: #86efac;
        font-size: 0.8rem;
    }
    
    /* Captions */
    small, .stCaption, caption {
        color: #57534e !important;
    }
    
    /* Slider */
    .stSlider > div > div > div > div {
        background: #fafaf9 !important;
    }
    
    .stSlider > div > div > div {
        background: #292524 !important;
    }
    
    .stSlider p {
        color: #a8a29e !important;
    }
    
    /* Success message */
    .stSuccess {
        background: rgba(134, 239, 172, 0.1) !important;
        border: 1px solid #365314 !important;
        color: #86efac !important;
        border-radius: 12px !important;
    }
    
    /* Warning message */
    .stWarning {
        background: rgba(252, 211, 77, 0.1) !important;
        border: 1px solid #713f12 !important;
        color: #fcd34d !important;
        border-radius: 12px !important;
    }
    
    /* Error message */
    .stError {
        background: rgba(252, 165, 165, 0.1) !important;
        border: 1px solid #7f1d1d !important;
        color: #fca5a5 !important;
        border-radius: 12px !important;
    }
    
    /* Info message */
    .stInfo {
        background: rgba(250, 250, 249, 0.05) !important;
        border: 1px solid #292524 !important;
        color: #d6d3d1 !important;
        border-radius: 12px !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #fafaf9 !important;
    }
    
    /* Selectbox dropdown */
    div[data-baseweb="select"] > div {
        background: #171717 !important;
        border-color: #292524 !important;
    }
    
    div[data-baseweb="popover"] {
        background: #171717 !important;
        border: 1px solid #292524 !important;
    }
    
    div[data-baseweb="popover"] li {
        background: #171717 !important;
        color: #fafaf9 !important;
    }
    
    div[data-baseweb="popover"] li:hover {
        background: #292524 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.markdown("## ⚙️ Settings")

# --- Get API key from secrets (no user input needed) ---
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except KeyError:
    st.error("API key not configured. Please contact the developer.")
    st.stop()

# --- Initialize Anthropic Client ---
client = Anthropic(api_key=api_key)

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "question_count" not in st.session_state:
    st.session_state.question_count = 0
if "resume_data" not in st.session_state:
    st.session_state.resume_data = None

# --- Resume Upload (now supports PDF and images) ---
st.sidebar.markdown("---")
st.sidebar.markdown("### Resume")

uploaded_file = st.sidebar.file_uploader(
    "Upload file",
    type=["png", "jpg", "jpeg", "pdf"],
    help="Resume image or PDF"
)

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    base64_data = base64.standard_b64encode(bytes_data).decode("utf-8")
    file_type = uploaded_file.type
    
    # Handle PDF vs image
    if file_type == "application/pdf":
        st.session_state.resume_data = {
            "type": "document",
            "source": {
                "type": "base64",
                "media_type": "application/pdf",
                "data": base64_data
            }
        }
    else:
        st.session_state.resume_data = {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": file_type,
                "data": base64_data
            }
        }
    st.sidebar.markdown('<div class="resume-preview">✓ Resume uploaded</div>', unsafe_allow_html=True)
else:
    st.session_state.resume_data = None

# --- Interview Settings ---
st.sidebar.markdown("---")
st.sidebar.markdown("### Interview")

interview_type = st.sidebar.selectbox(
    "Type",
    ["Behavioral", "Technical (SWE)", "Product/PM", "General"]
)

difficulty = st.sidebar.selectbox(
    "Level",
    ["Entry Level / Intern", "Mid Level", "Senior"]
)

company_style = st.sidebar.text_input(
    "Company",
    placeholder="Amazon, Google, etc."
)

# --- Feedback Intensity ---
st.sidebar.markdown("---")
st.sidebar.markdown("### Intensity")

feedback_intensity = st.sidebar.select_slider(
    "Feedback style",
    options=["Chill", "Balanced", "Brutal"],
    value="Balanced"
)

if feedback_intensity == "Chill":
    st.sidebar.success("Encouraging")
elif feedback_intensity == "Balanced":
    st.sidebar.warning("Honest")
else:
    st.sidebar.error("No mercy")

# --- New Interview Button ---
st.sidebar.markdown("---")

if st.sidebar.button("↻ New Interview"):
    st.session_state.messages = []
    st.session_state.question_count = 0
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("Claude API + Streamlit")

# --- System Prompt ---
def get_system_prompt():
    company_note = f"Tailor to {company_style}'s style." if company_style else ""
    
    resume_note = ""
    if st.session_state.resume_data:
        resume_note = """
RESUME PROVIDED: Ask about specific projects and experiences on their resume. Reference items by name. Grill on details.
"""
    
    if feedback_intensity == "Chill":
        intensity = "ENCOURAGING: Be supportive, find positives, rate generously."
    elif feedback_intensity == "Balanced":
        intensity = "BALANCED: Honest but fair. Rate fairly out of 10."
    else:
        intensity = "BRUTAL: Call out BS. Weak answers get 'This would get you rejected.' Generic = 3-4 not 6-7. Only praise if earned."
    
    return f"""Expert interview coach for {interview_type} at {difficulty} level. {company_note}

{resume_note}

{intensity}

1. Ask ONE question
2. Wait for response  
3. Rate /10, feedback, better example
4. Next question

Behavioral: Use STAR. Technical: Problem-solving focus.

Start with brief intro + first question."""

# --- Main UI ---
st.markdown("""
<div class="main-header">
    <h1>AI <span class="accent">Interview Coach</span></h1>
    <p>Practice interviews with AI-powered feedback</p>
</div>
""", unsafe_allow_html=True)

# Display chat history with custom avatars
for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.chat_message("assistant", avatar="💼"):
            st.markdown(message["content"])
    else:
        with st.chat_message("user", avatar="👤"):
            st.markdown(message["content"])

# Start interview if no messages
if len(st.session_state.messages) == 0:
    with st.chat_message("assistant", avatar="💼"):
        with st.spinner("Starting..."):
            try:
                if st.session_state.resume_data:
                    initial_content = [
                        st.session_state.resume_data,
                        {"type": "text", "text": "Start the interview. Here is my resume."}
                    ]
                else:
                    initial_content = "Start the interview."
                
                response = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1024,
                    system=get_system_prompt(),
                    messages=[{"role": "user", "content": initial_content}]
                )
                assistant_message = response.content[0].text
                st.markdown(assistant_message)
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                st.session_state.question_count = 1
            except Exception as e:
                st.error(f"Error: {e}")
                st.stop()

# Chat input
if prompt := st.chat_input("Your answer..."):
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant", avatar="💼"):
        with st.spinner(""):
            try:
                api_messages = []
                
                if st.session_state.resume_data:
                    api_messages.append({
                        "role": "user",
                        "content": [
                            st.session_state.resume_data,
                            {"type": "text", "text": "Start the interview. Here is my resume."}
                        ]
                    })
                    for i, msg in enumerate(st.session_state.messages):
                        if i == 0 and msg["role"] == "assistant":
                            api_messages.append({"role": "assistant", "content": msg["content"]})
                        elif i > 0:
                            api_messages.append({"role": msg["role"], "content": msg["content"]})
                else:
                    api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                
                response = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1024,
                    system=get_system_prompt(),
                    messages=api_messages
                )
                assistant_message = response.content[0].text
                st.markdown(assistant_message)
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                st.session_state.question_count += 1
            except Exception as e:
                st.error(f"Error: {e}")

# --- Footer Stats with transparency ---
if st.session_state.question_count > 0:
    st.markdown('<div class="stats-container">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <h3>Questions</h3>
            <p>{st.session_state.question_count}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <h3>Type</h3>
            <p>{interview_type.split("(")[0].strip()}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <h3>Level</h3>
            <p>{difficulty.split("/")[0].strip()}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        intensity_class = f"intensity-{feedback_intensity.lower()}"
        st.markdown(f"""
        <div class="stat-card">
            <h3>Intensity</h3>
            <p class="{intensity_class}">{feedback_intensity}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
