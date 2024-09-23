import streamlit as st
import PyPDF2
import io
import pandas as pd
import base64
from openai import OpenAI
import os
from PIL import Image
from pdf2image import convert_from_path
from pdf2image import convert_from_bytes
from pead_ai.prompts import system_prompt, prompt_to_csv, prompt_to_md
import pandas as pd
import io

import fitz  # PyMuPDF
import base64
import boto3
from textractor import Textractor

from pead_ai.pdf2img import Converter
from pead_ai.tableimg2csv import TableImageToCSV

tableimg2csv = TableImageToCSV(
    region_name='eu-central-1',
    aws_access_key_id=os.get_env('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.get_env('AWS_SECRET_ACCESS_KEY')
)


def analyze_page_with_gpt4(csv_table: str, client, prompt=prompt_to_md):
    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt,
                },
                {
                    "type": "text",
                    "text": csv_table
                }
            ]
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=1000
    )

    # TODO: add image to GPT-4o
    
    return response.choices[0].message.content



st.title("File Content Extractor")

uploaded_file = st.file_uploader("Choose a PDF or Excel file", type=["pdf", "xlsx"])

if uploaded_file is not None:
    file_extension = uploaded_file.name.split(".")[-1].lower()

    converter = Converter(uploaded_file)
    converter.pdf_to_jpg()
    images = converter.image_paths
    st.write(len(images))

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    for i, image in enumerate(images):  # TODO: remove this
        st.write(f"Page {i+1}:")
        csv = tableimg2csv.process_image(image)
        analysis = analyze_page_with_gpt4(csv, client)
        st.markdown(analysis)

        # try:
        #     csv2 = analyze_page_with_gpt4(analysis, client, prompt=prompt_to_csv)
        #     df = pd.read_csv(io.StringIO(csv2), sep=',')
        #     st.dataframe(df)
        # except Exception as e:
        #     st.error(e)

        st.divider()



    # Option to download the extracted text
    # TODO
