import streamlit as st
import os
from PIL import Image

icon = Image.open(os.path.dirname(__file__) + '/../icon.png')

st.set_page_config(page_icon=icon)

st.title("⚡️چگونه کار می کند")

st.markdown("""
**نظر شما در مورد رندر تاکنون چیست؟**

لطفا به من بگویید در [Twitter](https://twitter.com/360macky) یا با طرح یک موضوع در [GitHub Repository](https://github.com/360macky/generative-manim).
""")

st.write("## مفهوم")

st.markdown("""

آینده ای را تصور کنید که در آن می توانید یک ویدیوی انیمیشن از مفهومی که در ذهن خود دارید را در چند ثانیه تماشا کنید. این برای معلمان، دانش آموزان و غیره مفید خواهد بود. افرادی که می خواهند یک ویدیو تولید کنند، نیازی به یادگیری نحوه استفاده از ویرایشگر ویدیو، نحوه ترسیم یا کدنویسی ندارند. شما فقط باید یک متن توصیفی بنویسید.

این در واقع یک آینده است. و آنقدرها هم دور نیست. ما می توانیم از قبل شروع به کار روی آن کنیم.

airender یک کتابخانه پایتون برای ایجاد گرافیک و انیمیشن های پیچیده است. مزیت اصلی airender برای GPT این است که از آنجایی که زبانی برای LLM است، تولید کد مناسب از یک درخواست آسان‌تر است.

من احساس می کنم که یک ویرایشگر هوش مصنوعی خالص مانند [Runway] (https://runwayml.com)، یا یک ویرایشگر انیمیشن پیشرفته مانند [Jitter] (https://jitter.video) می تواند از یک گردش کاری مانند این استفاده کند:

""")

blueprint = Image.open(os.path.dirname(__file__) + "/blueprint.png")

st.image(blueprint, caption="طرح رندر هوش مصنوعی", output_format="PNG")

st.markdown("""

ایده پشت * رندر AI* این است که آزمایش کنید با GPT-3.5 و GPT-4 چقدر می توانیم پیش برویم.

## مشکلات رندرینگ

در حالی که GPT-3.5 و GPT-4 قادر به تولید کد خوب هستند. آنها دارای محدودیت های زیر هستند:

- اطلاعات تا سال 2021 محدود است. این بدان معناست که ویژگی‌های رندرایی که پس از سال 2021 اضافه شده‌اند در دسترس نخواهند بود.
- کد تولید شده توسط GPT-3.5 و GPT-4 همیشه صحیح نیست.

:white_check_mark: در این لحظه **render ai** قادر به رندر کردن انیمیشن های ساده متکی بر بسته های مانیم و مث است.

:x: اما نمی‌تواند انیمیشن‌های واقعاً پیچیده‌ای را ارائه کند که می‌توانند به خطوط کد بیشتری نیاز داشته باشند تا حد توکن‌های ارائه‌شده توسط GPT-3.5 یا GPT-4.

## پیامدهای هزینه

در حال حاضر GPT-4 30 برابر گرانتر از GPT-3.5 است.

[GPT-4 برای 1000 توکن 3 (ورودی) تا 6 سنت (تولید شده) هزینه دارد که حدود 1 میلیون توکن برای 30 دلار است.](https://github.com/360macky/generative-manim/issues/2). اون پول زیادیه. اما اگر به احتمالات فکر کنید زیاد نیست.

اگر می خواهید از این برنامه بدون محدودیت کاراکتر استفاده کنید، به شما توصیه می کنم از کلید API خود استفاده کنید.

""")


st.write("## سپاسگزاریها")

st.markdown("""

- [آشیش شوکلا](https://github.com/treuille/streamlit-manim/issues/1#issuecomment-1475134874) - برای ارائه داکر برای اجرای رندر در استریملیت.
- [انجمن مانیم ردیت](https://www.reddit.com/r/manim/) - جامعه توسعه دهندگان مانیم.
- [جامعه OpenAI](https://community.openai.com) - جامعه توسعه دهندگان OpenAI.
- [یادگیری ماشینی استریت تاک](https://twitter.com/MLStreetTalk/status/1636647985621745664) -توییتی که الهام بخش مفهوم برنامه GPT-4 بود.

""")
