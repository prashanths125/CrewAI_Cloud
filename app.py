import streamlit as st
from crew import run_crew

# ─── CONFIG ──────────────────────────────────────────────
APP_PASSWORD   = "trainer123"   # ← change this to your own password
MAX_SEARCHES   = 5              # ← max searches per user per session
# ─────────────────────────────────────────────────────────

st.set_page_config(page_title="AI Research Assistant", page_icon="🤖")
st.title("🤖 AI Research Assistant")

# ── STEP 1: Password Gate ─────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.subheader("Please enter the password to continue")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if pwd == APP_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ Wrong password. Please try again.")
    st.stop()   # nothing below this runs until logged in

# ── STEP 2: Rate Limit ────────────────────────────────────
if "search_count" not in st.session_state:
    st.session_state.search_count = 0

remaining = MAX_SEARCHES - st.session_state.search_count
st.caption(f"🔢 Searches remaining this session: {remaining} / {MAX_SEARCHES}")

if st.session_state.search_count >= MAX_SEARCHES:
    st.warning(f"⚠️ You have used all {MAX_SEARCHES} searches for this session. Please refresh the page to start a new session.")
    st.stop()

# ── STEP 3: Main App ──────────────────────────────────────
st.write("Enter any topic and two AI agents will research it and write a summary for you.")

topic = st.text_input("Topic", placeholder="e.g. benefits of solar energy")

if st.button("🔍 Research", disabled=not topic.strip()):
    st.session_state.search_count += 1
    with st.spinner("Agents are working... this takes 30-60 seconds ⏳"):
        try:
            result = run_crew(topic.strip())
            st.success("✅ Done!")
            st.markdown(result)
        except Exception as e:
            st.session_state.search_count -= 1   # don't count failed attempts
            st.error(f"Something went wrong: {e}")
