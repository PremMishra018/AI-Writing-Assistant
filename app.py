import streamlit as st
from translator import translate_text, get_languages
#from utils import copy_text
from gtts import gTTS
import edge_tts
import asyncio

async def generate_voice(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("translation.mp3")
#from streamlit_mic_recorder import mic_recorder

import edge_tts
import asyncio

async def generate_voice(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("translation.mp3")

voices = {
    "English": {
        "Male": "en-IN-PrabhatNeural",
        "Female": "en-IN-NeerjaNeural"
    },
    "Hindi": {
        "Male": "hi-IN-MadhurNeural",
        "Female": "hi-IN-SwaraNeural"
    },
    "Korean": {
        "Male": "ko-KR-InJoonNeural",
        "Female": "ko-KR-SunHiNeural"
    },
    "Japanese": {
        "Male": "ja-JP-KeitaNeural",
        "Female": "ja-JP-NanamiNeural"
    },
    "French": {
        "Male": "fr-FR-HenriNeural",
        "Female": "fr-FR-DeniseNeural"
    },
    "German": {
        "Male": "de-DE-ConradNeural",
        "Female": "de-DE-KatjaNeural"
    },
    "Spanish": {
        "Male": "es-ES-AlvaroNeural",
        "Female": "es-ES-ElviraNeural"
    },
    "Chinese": {
        "Male": "zh-CN-YunxiNeural",
        "Female": "zh-CN-XiaoxiaoNeural"
    },
    "Arabic": {
        "Male": "ar-SA-HamedNeural",
        "Female": "ar-SA-ZariyahNeural"
    }
}

# Page Configuration

st.set_page_config(
    page_title="AI Translator App",
    page_icon="🌐",
    layout="wide"
)
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
st.markdown("""

""", unsafe_allow_html=True)

# Center Logo
st.image("logo.png", width=120)

# Center Title
st.markdown(
    """
    <h1 style='text-align:center;
                font-size:60px;
                font-weight:bold;
                color:#4F8BF9;'>
        AI Translator
    </h1>
    """,
    unsafe_allow_html=True
)

# Subtitle
st.markdown(
    """
    <p style='text-align:center;
                color:#9CA3AF;
                font-size:24px;'>
        Translate text into 100+ languages instantly
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<center><h4 style='color:gray;'></h4></center>",
    unsafe_allow_html=True
)



# Initialize session state

if "source_lang" not in st.session_state:
    st.session_state.source_lang = "Auto Detect"

if "target_lang" not in st.session_state:
    st.session_state.target_lang = "Hindi"


# Languages

languages = get_languages()
languages = {name.title(): code for name, code in languages.items()}

languages = {"Auto Detect": "auto", **languages}

# Auto Detect add kardiya
languages = {"Auto Detect": "auto", **languages}
tts_languages = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Japanese": "ja",
    "Chinese": "zh-CN",
    "Arabic": "ar"
}


# Select Languages
left, center, right = st.columns([2,1,2])

with center:
    if st.button("🔄 Swap Languages"):
        temp = st.session_state.source_lang
        st.session_state.source_lang = st.session_state.target_lang
        st.session_state.target_lang = temp
        st.rerun()
col1, col2 = st.columns(2)

with col1:
    source_language = st.selectbox(
    "Source Language",
    list(languages.keys())[1:],
    index=list(languages.keys())[1:].index("English"),
    key="source_lang"
)

with col2:
    target_language = st.selectbox(
    "Target Language",
    list(languages.keys())[1:],
    key="target_lang"
)
    voice_gender = st.selectbox(
    "🎤 Voice Type",
    ["Male", "Female"],
    index=0
)
    


# Text Input

left, right = st.columns(2)
with left:
    st.subheader("📝 Enter Text")

    text = st.text_area(
        
        "",
        height=250,
        placeholder="Type or paste text here..."
    )
    st.caption(f"Characters: {len(text.strip())} / 5000")

# Translate Button

col1, col2 = st.columns(2)
with col1:
    translate = st.button("🌍 Translate", use_container_width=True)

with col2:
    clear = st.button("🗑 Clear", use_container_width=True)

if clear:
    st.session_state.pop("translated", None)
    st.rerun()


if translate:
    if text.strip() == "":
        st.warning("Please enter some text.")
    else:
        with st.spinner("🌍 Translating... Please wait"):
            translated = translate_text(
                text,
                languages[source_language],
                languages[target_language]
            )

        st.session_state["translated"] = translated
        st.success("✅ Translation Completed")


# Show Translation

if "translated" in st.session_state:

    with right:
        st.subheader("🌍 Translated Text")

        st.text_area(
            "",
            st.session_state["translated"],
            height=250
        )

        col1, col2 = st.columns(2)

        
    

        with col2:
            st.download_button(
                label="⬇ Download",
                data=st.session_state["translated"],
                file_name="translation.txt",
                mime="text/plain",
                use_container_width=True
            )
if st.button("🔊 Listen"):

    # Edge TTS supported languages
    if target_language in voices:

        voice = voices[target_language][voice_gender]

        asyncio.run(
            generate_voice(
                st.session_state["translated"],
                voice
            )
        )

    # Other languages -> gTTS
    else:

        tts = gTTS(
            text=st.session_state["translated"],
            lang=tts_languages.get(target_language, "en")
        )

        tts.save("translation.mp3")

    with open("translation.mp3", "rb") as audio_file:
        st.audio(audio_file.read(), format="audio/mp3")         # Default Male Voice

    
    
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; color:gray; font-size:16px;">
        
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("---")

st.markdown(
"""
<div style="text-align:center;color:gray">
Made with ❤️ using Python & Streamlit <br>
👨‍💻 Developed by <b>Prem Prakash Mishra</b>
</div>
""",
unsafe_allow_html=True
)