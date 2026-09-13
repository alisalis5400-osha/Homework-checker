import streamlit as st
from openai import OpenAI
import base64

# إعداد عنوان المنصة
st.title("📚 المنصة التعليمية الذكية")
st.write("تصحيح الواجبات وتلخيص المذكرات والصفحات باستعمال الذكاء الاصطناعي")

# القائمة الجانبية أو خيار تحديد الخدمة
mode = st.radio(
    "اختر الخدمة المطلوبة:",
    ["📝 تصحيح الواجبات", "📄 تلخيص صفحة / مذكرة (بامفلت واسئلة امتحانات)"],
    horizontal=True
)

# اختيار المرحلة الدراسية
grade_level = st.selectbox(
    "اختاري المرحلة الدراسية:",
    ["الثانوية", "المرحلة الإعدادية (المتوسطة)", "المرحلة الابتدائية"]
)

# رفع الصورة
uploaded_file = st.file_uploader("ارفعي صورة الواجب أو الصفحة...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # قراءة المفتاح تلقائياً وبأمان من Secrets
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    bytes_data = uploaded_file.getvalue()
    base64_image = base64.b64encode(bytes_data).decode('utf-8')

    # 1. قسم تصحيح الواجبات
    if mode == "📝 تصحيح الواجبات":
        if st.button("📝 تصحيح الواجب الآن"):
            with st.spinner("جاري قراءة الورقة وتحليل الإجابات..."):
                prompt = f"قم بتصحيح هذا الواجب المدرسي لمستوى {grade_level} بأسلوب مبسط، واختم بكلمات تشجيعية."
                
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": prompt},
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{base64_image}"
                                        }
                                    }
                                ]
                            }
                        ]
                    )
                    st.success("تم التصحيح بنجاح! 🎉")
                    st.write(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"حدث خطأ أثناء التصحيح: {e}")

    # 2. قسم التلخيص بأسلوب البامفلت والامتحانات
    elif mode == "📄 تلخيص صفحة / مذكرة (بامفلت واسئلة امتحانات)":
        if st.button("✨ تلخيص الصفحة الآن"):
            with st.spinner("جاري تلخيص المحتوى وتنسيقه بأسلوب البامفلت والامتحانات..."):
                prompt = f"""
                قم بتحليل وتلخيص الصورة المرفقة لمستوى {grade_level} وفق الشروط التالية:
                1. صمم التلخيص بأسلوب "بامفلت تعليمي" (Pamphlet) جذاب ومقسم إلى نقاط رئيسية وعناوين فرعية واضحة.
                2. استخرج أهم المصطلحات والقوانين/المفاهيم المحورية الموجودة في الصفحة.
                3. أضف قسم خاص بعنوان "أسئلة وتوقعات الامتحانات" يتضمن أسئلة متوقعة على هذا الجزء (مثل: علل، قارن، اختر، أو أسئلة مقالية) مع إجاباتها النموذجية المختصرة.
                """
                
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": prompt},
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{base64_image}"
                                        }
                                    }
                                ]
                            }
                        ]
                    )
                    st.success("تم إعداد التلخيص والأسئلة بنجاح! 📖")
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"حدث خطأ أثناء التلخيص: {e}")
