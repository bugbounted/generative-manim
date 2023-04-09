import streamlit as st
import os
import openai
from PIL import Image

from utils import *

icon = Image.open(os.path.dirname(__file__) + '/../icon.png')

st.set_page_config(page_icon=icon)

st.markdown('# 🤖 موتور پرامپت')

st.write("مهندسی سریع در مورد ارائه دستورالعمل های صحیح به GPT-4 است. هرچه دستورالعمل دقیق تر باشد، نتایج بهتری خواهد داشت. هدف تولید کد رندر از قسمت خاصی از کد است. سپس می توانید از کد برای ارائه انیمیشن استفاده کنید.")

prompt = st.text_area("ایده انیمیشن خود را اینجا بنویسید. از کلمات ساده استفاده کنید.",
                      "Draw a blue circle and convert it to a red square")

openai_api_key = st.text_input(
    "خودتان را بچسبانید [کلید وب سرویس Open AI](https://platform.openai.com/account/api-keys)", value="", type="password")

openai_model = st.selectbox(
    "مدل GPT را انتخاب کنید. اگر به GPT-4 دسترسی ندارید، GPT-3.5-Turbo را انتخاب کنید", ["GPT-3.5-Turbo", "GPT-4"])

generate_prompt = st.button(
    ":computer: تولید پرامپت :sparkles:", type="primary")

if generate_prompt:
  if not openai_api_key:
    st.error("خطا: برای استفاده از این ویژگی باید کلید Open API خود را ارائه دهید.")
    st.stop()
  if not prompt:
    st.error("خطا: باید یک درخواست ارائه دهید.")
    st.stop()

  response = openai.ChatCompletion.create(
      model=openai_model.lower(),
      messages=[
          {"role": "system", "content": GPT_SYSTEM_INSTRUCTIONS},
          {"role": "user", "content": wrap_prompt(prompt)}
      ]
  )

  code_response = extract_code(response.choices[0].message.content)

  code_response = extract_construct_code(code_response)

  st.text_area(label="Code generated: ",
               value=code_response,
               key="code_input")
