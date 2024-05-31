import streamlit as st
from streamlit import config
from text_summarize_code import summarize_with_options, get_pdf_text, translate_text, stream_data
from io import StringIO

st.set_page_config(layout="wide")

page = st.session_state.get("page", "Summarize")

with st.sidebar:
    selected_page = st.selectbox(
        "Select Page",
        options=["Summarize", "Translate"]
    )

    # Update state variable based on selection
    if selected_page != page:
        page = selected_page
        st.session_state["page"] = page

if page == "Summarize":
    with st.sidebar:
        choice = st.selectbox(
            "Select Your Option for Summarize",
            ["Summarize Text", "Summarize Document"]
        )

        format = st.radio(label="Select the Format",
                          options=["***Paragraph***", "***Bullet Points***"])

        values = st.select_slider(
            'Select the summary length',
            options=[100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000])

    if choice == "Summarize Text":
        st.subheader("Summarize Text")
        input_text = st.text_area(label="Enter your text here ", placeholder="Enter Your Text",
                                  label_visibility="collapsed")
        if st.button("Summarize"):
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown("**Your Input Text**")
                st.info(input_text)
            with col2:
                st.markdown("**Summarized Text**")
                st.info(summarize_with_options(input_text=input_text, num_words=values, format=format))


    elif choice == "Summarize Document":
        st.subheader("Summarize Document")
        uploaded_file = st.file_uploader(label="Upload Your File")
        config.set_option("server.maxUploadSize", 2)

        if uploaded_file is not None:
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(uploaded_file)
                st.info(summarize_with_options(input_text=raw_text, num_words=values, format=format))

elif page == "Translate":
    with st.sidebar:
        translate_to = st.selectbox(
            "Select the language:",
            options=["English", "Telugu", "Hindi", "French", "Spanish", "German"],
            key="translate_to"  # Unique key for state management
        )

    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Enter Text to Translate")
        input_text = st.text_area(label=" ", height=500, label_visibility="collapsed")
        if st.button("Translate"):
            with col2:
                st.subheader("Translated Text")
                with st.spinner("Translating text ..."):
                    translated_text = translate_text(input_text, translate_to)


                    # st.text_area(label = "Translated Text:", value= st.write_stream(stream_data(translated_text)), height = 500)
                    st.write_stream(stream_data(translated_text['text']))