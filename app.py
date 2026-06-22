import streamlit as st

from modules.pdf_reader import extract_text
from modules.ai_engine import ask_gemini
from streamlit_mic_recorder import mic_recorder
from modules.pdf_export import create_pdf

st.set_page_config(
    page_title="Smart Exam Prep Generator",
    layout="wide"
)

st.title("📚 Smart Exam Prep Generator")

uploaded_file = st.file_uploader(
    "Upload Notes PDF",
    type=["pdf"]
)
if uploaded_file:

    text = extract_text(uploaded_file)

    st.success("PDF Uploaded Successfully")

    option = st.selectbox(
        "Choose Task",
        [
            "Summary",
            "Important Questions",
            "MCQs",
            "Flashcards",
            "Revision Plan",
            "Viva Questions",
            "Predicted Exam Questions"
        ]
    )

    # Chat with Notes
    user_question = st.text_input(
        "Ask Anything From Notes"
    )

    if st.button("Ask", key="ask_btn"):

        prompt = f"""
        Notes:

        {text[:15000]}

        Question:

        {user_question}
        """

        answer = ask_gemini(prompt)

        st.write(answer)

    # Generate Study Material
    if st.button("Generate", key="generate_btn"):

        if option == "Summary":
            prompt = f"""
            Generate:
            1. Chapter Summary
            2. Key Concepts
            3. Important Formulas

            Notes:
            {text[:15000]}
            """

        elif option == "Important Questions":
            prompt = f"""
            Generate:
            - 10 Short Questions
            - 10 Long Questions

            Notes:
            {text[:15000]}
            """

        elif option == "MCQs":
            prompt = f"""
            Generate 20 MCQs.

            Each MCQ should contain:
            Question
            A
            B
            C
            D
            Correct Answer

            Notes:
            {text[:15000]}
            """

        elif option == "Flashcards":
            prompt = f"""
            Create flashcards.

            Format:

            Question:
            Answer:

            Notes:
            {text[:15000]}
            """

        elif option == "Revision Plan":
            prompt = f"""
            Create a 1-day exam revision plan.

            Notes:
            {text[:15000]}
            """

        elif option == "Viva Questions":
            prompt = f"""
            Generate 25 viva questions with answers.

            Notes:
            {text[:15000]}
            """

        elif option == "Predicted Exam Questions":
            prompt = f"""
            Act as an experienced university professor.

            Predict likely exam questions.

            Give reasons.

            Notes:
            {text[:15000]}
            """

        result = ask_gemini(prompt)

        st.subheader(option)
        st.write(result)

        filename = create_pdf(result, "output.pdf")

        with open(filename, "rb") as file:
            st.download_button(
                "📥 Download PDF",
                file,
                "ExamPrep.pdf"
            )



