import streamlit as st
from openai import OpenAI
import base64

st.title("📚 منصة تصحيح الواجبات الذكية")
st.write("ارفعي صورة الواجب واختاري المرحلة الدراسية للحصول على تصحيح وشرح مفصل.")

api_key = st.text_input("أدخلي مفتاح API الخاص بكِ:", type="password")

grade_level = st.selectbox(
    "اختاري المرحلة الدراسية:",
    ["المرحلة الابتدائية", "المرحلة الإعدادية (المتوسطة)", "المرحلة الثانوية"]
)

uploaded_file = st.file_uploader("اختر صورة الواجب...", type=["jpg", "jpeg", "png"])

if uploaded_file and api_key:
    client = OpenAI(api_key=api_key)
    bytes_data = uploaded_file.getvalue()
    base64_image = base64.b64encode(bytes_data).decode('utf-8')

    if st.button("تصحيح الواجب الآن 📝"):
        with st.spinner("جاري قراءة الورقة وتحليل الإجابات..."):
            prompt = f"أنت معلم خبير وصابرة ومحفزة. قم بقراءة وتصحيح صورة الواجب المرفقة لطالب في ({grade_level}). أثنِ على الإجابات الصحيحة، واشرح الأخطاء بالتفصيل والخطوات بأسلوب مبسط، واختم بكلمات تشجيعية."

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
            )
            st.success("تم التصحيح بنجاح!")
            st.markdown(response.choices[0].message.content)
