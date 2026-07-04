import streamlit as st
import google.generativeai as genai
from pathlib import Path
API_KEY = st.secrets["API_KEY"]


# Gemini Configuration
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(
    page_title="AI Autocorrect Tool",
    page_icon="🤖",
    layout="centered"
)
# this is for theme
st.markdown("""
<style>

/* Buttons */
.stButton > button{
    width:100%;
    height:50px;
    border-radius:12px;
    border:none;
    background:#2563EB;
    color:white !important;
    font-size:16px;
    font-weight:600;
}

.stButton > button:hover{
    background:#1D4ED8;
}

/* Text Area */
textarea{
    border-radius:12px !important;
}

/* Metric Cards */
div[data-testid="metric-container"]{
    border-radius:12px;
    padding:15px;
}

/* Success / Info Boxes */
div[data-testid="stAlert"]{
    border-radius:12px;
}

</style>
""", unsafe_allow_html=True)



#Ye current UI se kaafi clean lagega.


col1, col2 = st.columns([1,4])

with col1:
    st.image("assets/logo.png", width=100)

with col2:
    st.title("🤖 AI Writing Assistant")
    st.caption("Powered by Google Gemini AI")


st.markdown("---")



with st.sidebar:
    
    #st.image("assets/logo.png", width=90)
    logo_path = Path(__file__).parent / "assets" / "logo.png"

if logo_path.exists():
    st.image(str(logo_path), width=90)
else:
    st.warning("Logo file not found.")
    st.title("🤖 AI Assistant")

    st.markdown("""
### Features

✅ Grammar Correction

✅ Professional Rewrite

✅ Friendly Rewrite

✅ Email Generator

✅ WhatsApp Generator

✅ Text Summarizer
""")
    st.markdown("---")
    st.info("Powered by Google Gemini AI")
    st.markdown("---")


    st.write("### 👨 Developer")
    st.write("Prem Prakash Mishra")

    st.write("B.Tech CSE (AI & ML)")


st.write("Enter your text below and click the button to correct it.")

text = st.text_area("Type your text here...")
if text:
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Words", len(text.split()))

    with col2:
        st.metric("Characters", len(text))
mode = st.selectbox(
    "Choose Action",
    [
        "Correct Grammar",
        "Professional",
        "Friendly",
        "Formal Email",
        "WhatsApp Message",
        "Summarize"
    ]
)


col1, col2 = st.columns(2)

with col1:
    generate = st.button("🚀Start ")

with col2:
    clear = st.button("🗑 Clear")
    if text.strip():

        prompt = f"""
You are an AI writing assistant.

Action: {mode}

Text:
{text}

Rules:
- If action is Correct Grammar, only fix grammar and spelling.
- If action is Professional, rewrite the text in a professional tone.
- If action is Friendly, rewrite the text in a friendly tone.
- If action is Formal Email, convert it into a formal email.
- If action is WhatsApp Message, rewrite it as a natural WhatsApp message.
- If action is Summarize, provide a short summary.

Return only the final text.
"""

        try:
            with st.spinner("🤖 AI is thinking..."):
                response = model.generate_content(prompt)

            st.success("🎉 AI Generated Result")
            st.markdown("### 📄 Result")
            st.text_area(
    "📄 Result",
    response.text,
    height=180
)

            st.download_button(
                label="📥 Download Result",
                data=response.text,
                file_name="ai_result.txt",
                mime="text/plain"
            )

        except Exception as e:
            error_message = str(e)

            if "429" in error_message or "quota" in error_message.lower():
                st.warning("⚠️ API limit reached. Please wait 1 minute and try again.")
            else:
                st.error("❌ Something went wrong. Please try again.")

            

    else:
        st.warning("Please enter some text.")

        st.markdown("---")
        st.caption("🚀 Developed by Prem Prakash Mishra | Powered by Google Gemini AI")