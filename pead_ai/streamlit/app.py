import streamlit as st
import PyPDF2
import io
import pandas as pd

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def excel_to_markdown(df):
    return df.to_markdown(index=False)

st.title("File Content Extractor")

uploaded_file = st.file_uploader("Choose a PDF or Excel file", type=["pdf", "xlsx"])

if uploaded_file is not None:
    file_extension = uploaded_file.name.split(".")[-1].lower()

    if file_extension == "pdf":
        # Handle PDF
        bytes_data = uploaded_file.getvalue()
        pdf_file = io.BytesIO(bytes_data)
        text = extract_text_from_pdf(pdf_file)

        st.subheader("Extracted Text:")
        st.text_area("Content", text, height=300)

        # Option to download the extracted text
        st.download_button(
            label="Download extracted text",
            data=text,
            file_name="extracted_text.txt",
            mime="text/plain"
        )

    elif file_extension == "xlsx":
        # Handle Excel
        df = pd.read_excel(uploaded_file)
        markdown_table = excel_to_markdown(df)

        st.subheader("Excel Content (Markdown Table):")
        st.markdown(markdown_table)

        # Option to download the markdown table
        st.download_button(
            label="Download markdown table",
            data=markdown_table,
            file_name="excel_content.md",
            mime="text/markdown"
        )

        # Display DataFrame
        st.subheader("Excel Content (DataFrame):")
        st.dataframe(df)

        # Option to download CSV
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="excel_content.csv",
            mime="text/csv"
        )