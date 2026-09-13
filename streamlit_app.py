
import streamlit as st
from openai import OpenAI
import base64

# إعداد عنوان المنصة
st.title("📚 المنصة التعليمية الذكية")
st.write("تصحيح الواجبات وتلخيص المذكرات بلغة الورقة المرفوعة تلقائياً مع ترجمة المصطلحات الصعبة")

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
            with st.spinner("جاري قراءة الورقة وتحديد اللغات والحلول..."):
                prompt = f"""
                قم بتحليل وتصحيح هذا الواجب المدرسي لمستوى {grade_level} باتباع القواعد التالية بدقة:
                1. **لغة الإجابة والتصحيح:** اكتب التصحيح والشرح والملاحظات بنفس اللغة الأساسية المكتوب بها الواجب في الصورة (إذا كانت إنجليزية فاكتب بالإنجليزية، فرنسية بالفرنسية، عربية بالعربية... إلخ).
                2. إذا كانت المادة مادة علمية أو رياضية (مثل Math أو Science)، استخدم نفس المصطلحات والرموز الواردة بالورقة.
                3. **قسم الترجمة (Vocabulary/Key Terms):** في نهاية التصحيح، قم بإضافة قسم مخصص بعنوان "💡 ترجمة الكلمات والمصطلحات الهامة" واذكر فيه الكلمات أو المفاهيم الصعبة الواردة بالورقة مع ترجمتها وشرحها المباشر باللغة العربية.
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
                    st.success("تم التصحيح بنجاح! 🎉")
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"حدث خطأ أثناء التصحيح: {e}")

    # 2. قسم التلخيص بأسلوب البامفلت والامتحانات
    elif mode == "📄 تلخيص صفحة / مذكرة (بامفلت واسئلة امتحانات)":
        if st.button("✨ تلخيص الصفحة الآن"):
            with st.spinner("جاري التلخيص وإعداد أسئلة الامتحانات..."):
                prompt = f"""
                قم بتحليل وتلخيص الصورة المرفقة لمستوى {grade_level} وفق الشروط التالية:
                1. **لغة التلخيص:** اكتب التلخيص والأسئلة بنفس اللغة الأساسية للورقة المرفوعة في الصورة (مثل الفرنساوي، الإنجليزي، أو العربي).
                2. صمم التلخيص بأسلوب "بامفلت تعليمي" (Pamphlet) جذاب ومقسم لنقاط رئيسية وعناوين فرعية.
                3. أضف قسم "أسئلة وتوقعات الامتحانات" يتضمن أسئلة متوقعة بنفس لغة النص وإجاباتها النموذجية.
                4. **قسم الترجمة والمصطلحات:** أضف في نهاية التلخيص قسماً خاصاً يستخرج الكلمات والمصطلحات الصعبة/الرئيسية في الصفحة ويرجمها إلى اللغة العربية.
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
