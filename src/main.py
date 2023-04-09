import os
import subprocess
import streamlit as st
from manim import *
import openai
from openai.error import AuthenticationError
from PIL import Image

from utils import *

icon = Image.open(os.path.dirname(__file__) + '/icon.png')

st.set_page_config(
    page_title="رندر",
    page_icon=icon,
)

styl = f"""
<style>
  textarea[aria-label="Code generated: "] {{
    font-family: 'Consolas', monospace !important;
  }}
  }}
</style>
"""
st.markdown(styl, unsafe_allow_html=True)

st.title(":art: رندر")
st.write(":robot_face: با GPT-4 و GPT-3.5 انیمیشن های زیبا و سریع بسازید :sparkles:")

prompt = st.text_area("ایده انیمیشن خود را اینجا بنویسید. از کلمات ساده استفاده کنید.",
                      "Draw a blue circle and convert it to a red square", max_chars=240,
                      key="prompt_input")

openai_api_key = ""

openai_model = st.selectbox(
    "مدل GPT را انتخاب کنید. اگر به GPT-4 دسترسی ندارید، GPT-3.5-Turbo را انتخاب کنید", ["GPT-3.5-Turbo", "GPT-4"])

if st.checkbox("از کلید Open API خود استفاده کنید (توصیه می شود)"):
  openai_api_key = st.text_input(
      "خودتان را بچسبانید [کلید توسعه دهنده OpenAI](https://platform.openai.com/account/api-keys)", value="", type="password")

st.write(":warning: در حال حاضر OpenAI هر 3 ساعت 25 درخواست برای GPT-4 می پذیرد. این بدان معنی است که OpenAI شروع به رد برخی از درخواست ها می کند. دو راه حل وجود دارد: از GPT-3.5-Turbo استفاده کنید یا از کلید OpenAI API خود استفاده کنید.")

generate_video = st.button(":computer: متحرک کردن :sparkles:", type="primary")
show_code = st.checkbox("نمایش کد تولید شده (که انیمیشن را تولید می کند)")

code_response = ""

if generate_video:

  if not openai_model:
    openai_model = "gpt-4"

  if not prompt:
    st.error("Error: لطفاً برای تولید ویدیو یک درخواست بنویسید.")
    st.stop()

  # If prompt is less than 10 characters, it will be rejected
  if len(prompt) < 10:
    st.error("Error: درخواست شما خیلی کوتاه است. لطفا یک درخواست طولانی تر بنویسید")
    st.stop()

  # If prompt exceeds 240 characters, it will be truncated
  if len(prompt) > 240 and not openai_api_key:
    st.error("Error: درخواست شما بیش از 240 کاراکتر است. لطفا کوتاهش کنید")
    st.stop()

  # Prompt must be trimmed of spaces at the beginning and end
  prompt = prompt.strip()

  # Remove ", ', \ characters
  prompt = prompt.replace('"', '')
  prompt = prompt.replace("'", "")
  prompt = prompt.replace("\\", "")

  # If user has their own API key, increase max tokens by 3x
  if not openai_api_key:
    max_tokens = 400
  else:
    max_tokens = 1200

  # If user has their own API key, use it
  if not openai_api_key:
    try:
      # If there is OPENAI_API_KEY in the environment variables, use it
      # Otherwise, use Streamlit secrets variable
      if os.environ["OPENAI_API_KEY"]:
        openai_api_key = os.environ["OPENAI_API_KEY"]
      else:
        openai_api_key = st.secrets["OPENAI_API_KEY"]
    except:
      st.error("Error: متأسفم، کلید OpenAI API خود را غیرفعال کردم (بودجه به پایان رسیده است). لطفاً از کلید API خود استفاده کنید و کاملاً کار خواهد کرد. در غیر این صورت، لطفاً برای من در توییتر پیام ارسال کنید (@360macky)")
      st.stop()
  else:
    try:
      openai.api_key = openai_api_key
    except AuthenticationError:
      st.error(
          "Error: کلید OpenAI API نامعتبر است. لطفا بررسی کنید که آیا درست است.")
      st.stop()
    except:
      st.error(
          "Error: ما نتوانستیم کلید OpenAI API شما را احراز هویت کنیم. لطفا بررسی کنید که آیا درست است.")
      st.stop()

  try:
    response = openai.ChatCompletion.create(
        model=openai_model.lower(),
        messages=[
            {"role": "system", "content": GPT_SYSTEM_INSTRUCTIONS},
            {"role": "user", "content": wrap_prompt(prompt)}
        ],
        max_tokens=max_tokens
    )
  except:
    if openai_model.lower() == "gpt-4":
      st.error(
          "Error: این احتمالاً یک خطای محدودیت نرخ برای GPT-4 است. در حال حاضر OpenAI هر 3 ساعت 25 درخواست برای GPT-4 می پذیرد. این بدان معناست که OpenAI شروع به رد کردن برخی از درخواست ها به صورت تصادفی می کند. دو راه حل وجود دارد: از GPT-3.5-Turbo استفاده کنید یا از کلید OpenAI API خود استفاده کنید.")
      st.stop()
    else:
      st.error(
          "Error: ما نتوانستیم کد تولید شده را ایجاد کنیم. لطفاً صفحه را دوباره بارگیری کنید یا بعداً دوباره امتحان کنید")
      st.stop()

  code_response = extract_construct_code(
      extract_code(response.choices[0].message.content))

  if show_code:
    st.text_area(label="Code generated: ",
                 value=code_response,
                 key="code_input")

  if os.path.exists(os.path.dirname(__file__) + '/../../GenScene.py'):
    os.remove(os.path.dirname(__file__) + '/../../GenScene.py')

  if os.path.exists(os.path.dirname(__file__) + '/../../GenScene.mp4'):
    os.remove(os.path.dirname(__file__) + '/../../GenScene.mp4')

  try:
    with open("GenScene.py", "w") as f:
      f.write(create_file_content(code_response))
  except:
    st.error("Error: ما نتوانستیم کد تولید شده را در فایل پایتون ایجاد کنیم. لطفاً صفحه را دوباره بارگیری کنید یا بعداً دوباره امتحان کنید")
    st.stop()

  COMMAND_TO_RENDER = "manim GenScene.py GenScene --format=mp4 --media_dir . --custom_folders video_dir"

  problem_to_render = False
  try:
    working_dir = os.path.dirname(__file__) + "/../"
    subprocess.run(COMMAND_TO_RENDER, check=True, cwd=working_dir, shell=True)
  except Exception as e:
    problem_to_render = True
    st.error(
        f"Error: ظاهراً GPT کدی را تولید کرده است که Manim (موتور رندر) نمی‌تواند آن را پردازش کند.\n\nاین طبیعی است، زیرا گاهی اوقات GPT می‌تواند کد باگ تولید کند و برای رفع آن نیاز به مداخله انسانی دارد.\n\n**بسیار خوب. اما اکنون چه کاری می‌توانید انجام دهید؟**\n\nاگر می‌خواهید بدانید چه چیزی در داخل شکست خورده است، همچنان می‌توانید فایل Python تولید شده توسط هوش مصنوعی را با دکمه زیر دانلود کنید (یکی که رندر نشد). و دوباره سعی کن. به یاد داشته باشید، درخواست‌های ساده‌تر و واضح‌تر بهتر هستند.\n\nمی‌توانید یک مشکل را در [مخزن GitHub] (https://github.com/360macky/generative-manim) باز کنید، و درخواست خود را پیوست کنید.")
  if not problem_to_render:
    try:
      video_file = open(os.path.dirname(__file__) + '/../GenScene.mp4', 'rb')
      video_bytes = video_file.read()
      st.video(video_bytes)
    except FileNotFoundError:
      st.error("Error: من نتوانستم فایل ویدئویی تولید شده را پیدا کنم. می دانم که این یک باگ است و دارم روی آن کار می کنم. لطفا صفحه را دوباره بارگذاری کنید.")
    except:
      st.error(
          "Error: هنگام نمایش ویدیوی شما مشکلی پیش آمد. لطفا صفحه را دوباره بارگذاری کنید.")
  try:
    python_file = open(os.path.dirname(__file__) + '/../GenScene.py', 'rb')
    st.download_button("Download scene in Python",
                       python_file, "GenScene.py", "text/plain")
  except:
    st.error(
        "Error: هنگام یافتن فایل پایتون مشکلی پیش آمد. لطفا صفحه را دوباره بارگذاری کنید.")


st.write('ساخته شده با :heart: توسط [مارسلو](https://github.com/360macky).')
st.write('[سورس کد پروژه](https://github.com/360macky/generative-manim) - [گزارش ایراد](https://github.com/360macky/generative-manim/issues/new) - [توییتر](https://twitter.com/360macky) - [پروفایل اوپن ای آی](https://community.openai.com/u/360macky/summary)')
