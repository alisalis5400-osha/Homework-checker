import google.generativeai as genai
import streamlit as st

st.set_page_config(
    page_title="المنصة التعليمية السريعة", page_icon="⚡", layout="centered"
)

# 1. التأكد من وجود المفتاح
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ يرجى إضافة GEMINI_API_KEY في إعدادات Secrets!")

st.title("⚡ المنصة التعليمية الذكية")

tab1, tab2 = st.tabs(["📸 تصحيح الواجبات", "📚 تلخيص الدروس"])

with tab1:
    st.subheader("تصحيح ورقة الواجب")
    uploaded_file = st.file_uploader(
        "اختر صورة الواجب:", type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        st.success(f"📁 تم إرفاق الصورة: {uploaded_file.name}")

        if st.button("🚀 تصحيح الواجب الآن", key="btn_hw"):
            with st.spinner("جاري قراءة الورقة وتحليل الإجابات..."):
                try:
                    # تحويل ملف الصورة المحمل إلى صيغة يفهمها الموديل مباشرة
                    image_bytes = uploaded_file.getvalue()
                    image_parts = [
                        {
                            "mime_type": uploaded_file.type,
                            "data": image_bytes,
                        }
                    ]

                    # استدعاء الموديل المعتمد والأسرع للصور
                    model = genai.GenerativeModel("gemini-1.5-flash")

                    prompt = "اقرأ الأسئلة والإجابات المكتوبة بخط اليد في هذه الصورة. صحح الأخطاء واكتب الإجابات الصحيحة والتصحيح بأسلوب بسيط ومباشر."

                    response = model.generate_content([prompt, image_parts[0]])

                    st.markdown("### 📊 نتيجة التصحيح:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"حدث خطأ أثناء التصحيح: {e}")

with tab2:
    st.subheader("تلخيص النصوص والدروس")
    lesson_text = st.text_area(
        "اضع النص هنا:", height=200, placeholder="اكتب النص..."
    )

    if st.button("✨ تلخيص الدرس", key="btn_summary"):
        if lesson_text.strip():
            with st.spinner("جاري التلخيص..."):
                try:
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    prompt = "لخص هذا الدرس في نقاط رئيسية بسيطة للمذاكرة."
                    response = model.generate_content([prompt, lesson_text])

                    st.markdown("### 📝 الملخص:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"حدث خطأ: {e}")
