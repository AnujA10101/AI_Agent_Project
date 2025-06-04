import streamlit as st
from summary_agent import summarize
from analysis_agent import analyze

# 1) Page setup: full-width, hide sidebar/header/footer, minimal padding
st.set_page_config(
    page_title="AI Financial Assistant",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Inject some custom CSS to remove default Streamlit header/footer and reduce padding
st.markdown(
    """
    <style>
        /* Remove top padding, collapse header and footer */
        .block-container {
            padding-top: 0.5rem;
            padding-bottom: 1rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        header, footer {
            visibility: hidden;
        }
        /* Style the “Analyze” button more like ChatGPT */
        button[kind="primary"] {
            background-color: #444654;
            border: none;
            color: white;
        }
        button[kind="primary"]:hover {
            background-color: #5a6074;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# 2) Title (centered) and a horizontal line
st.markdown("<h1 style='text-align: center; margin-bottom: 0.25rem;'>📈 AI Financial Assistant</h1>", unsafe_allow_html=True)
st.markdown("---")

# 3) Chat-style input using streamlit’s chat_input
#    (Displays a text box at bottom of page, similar to ChatGPT)
query = st.chat_input("Ask anything about finance or trading...")

if query:
    # 4) Display the user’s message
    st.chat_message("user").write(query)

    # 5) Summarization step
    with st.chat_message("assistant"):
        with st.spinner("Summarizing..."):
            summary_obj = summarize(query)

        # Display summary in a “card”-style box
        st.markdown("### 🧾 Summary")
        # Use st.markdown for any intended Markdown formatting
        st.markdown(summary_obj.summary)

        # Show sources as clickable links
        if getattr(summary_obj, "sources", None):
            st.markdown("**Sources:**")
            for src in summary_obj.sources:
                st.markdown(f"- [{src}]({src})")

    # 6) Analysis step
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            analysis_obj = analyze(summary_obj.summary)

        st.markdown("### 📊 Insights")
        st.markdown(analysis_obj.insights)

        if getattr(analysis_obj, "risk_factors", None):
            st.markdown("**Risk Factors:**")
            for rf in analysis_obj.risk_factors:
                st.markdown(f"- {rf}")