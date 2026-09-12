import streamlit as st
from openai import OpenAI
import base64

# إعدادات عنوان الصفحة
st.set_page_config(page_title="منصة تصحيح الواجبات", page_icon="📚")

st.title("📚 منصة تصحيح الواجبات الذكية")
st.write("ارفعي صورة الواجب واختاري المرحلة الدراسية للحصول على تصحيح وشرح مفصل خطوة بخطوة.")

# أدوات الإدخال
api_key = st.text_input("أدخلي مفتاح API الخاص بكِ:", type="password")

grade_level = st.selectbox(
    "إختاري المرحلة الدراسية:",
    ["المرحلة الابتدائية", "المرحلة الإعدادية (المتوسطة)", "المرحلة الثانوية"]
)

uploaded_file = st.file_uploader("اختر صورة الواجب...", type=["jpg", "jpeg", "png"])

if uploaded_file and api_key:
    client = OpenAI(api_key=api_key)
    bytes_data = uploaded_file.getvalue()
    base64_image = base64.b64encode(bytes_data).decode('utf-8')

    if st.button("تصحيح الواجب الآن 📝"):
        with st.spinner("جاري قراءة الورقة وتحليل الإجابات..."):
            # صياغة التوجيه بناءً على المرحلة الدراسية
            prompt = f"""
            أنت معلم خبير وصابرة ومحفزة جداً. قم بقراءة وتصحيح صورة الواجب المرفقة مع الالتزام بالتعليمات التالية:
            
            1. **المرحلة الدراسية:** الطالب في ({grade_level}). اضبط أسلوب الشرح وتبسيط المفاهيم ليكون مناسباً لسن الطالب في هذه المرحلة.
            2. **مراجعة الإجابات الصحيحة:** أثنِ على الإجابات الصحيحة وشجع الطالب بأسلوب إيجابي ولطيف.
            3. **تصحيح الأخطاء بالتفصيل:** حدد الأخطاء إن وجدت، واشرح سبب الخطأ بأسلوب مبسط وصادق دون تعقيد.
            4. **الشرح بالخطوات:** قدم الحل النموذجي الصحيح خطوة بخطوة حتى يفهم الطالب كيفية الوصول للإجابة الصحيحة بنفسه.
            5. **خاتمة تحفيزية:** اختم بكلمات تشجيعية ودودة تزيد من ثقة الطالب بنفسه.
            """

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }
                ]
            ]
            st.success("تم التصحيح بنجاح!")
            st.markdown(response.choices[0].message.content)
