import google.generativeai as genai
from PIL import Image
import streamlit as st

# 1. إعداد الصفحة
st.set_page_config(
    page_title="المنصة التعليمية السريعة", page_icon="⚡", layout="centered"
)

# 2. ربط مفتاح API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ يرجى إضافة GEMINI_API_KEY في إعدادات Secrets على Streamlit!")

model = genai.GenerativeModel("gemini-1.5-flash")

st.title("⚡ المنصة التعليمية الذكية")

# 3. إنشاء الأقسام
tab1, tab2 = st.tabs(["📸 تصحيح الواجبات", "📚 تلخيص الدروس"])

# --- القسم الأول: تصحيح الواجبات ---
with tab1:
    st.subheader("تصحيح ورقة الواجب")
    uploaded_file = st.file_uploader(
        "اختر صورة الواجب:", type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        # إشعار خفيف بدلاً من عرض الصورة لسرعة الأداء
        st.success(f"📁 تم إرفاق الصورة بنجاح: {uploaded_file.name}")

        if st.button("🚀 تصحيح الواجب الآن", key="btn_hw"):
            with st.spinner("جاري التحليل والتصحيح..."):
                try:
                    image = Image.open(uploaded_file)
                    prompt = "قم بقراءة الأسئلة والإجابات المكتوبة بخط اليد في الصورة. صحح الأخطاء واذكر الإجابة الصحيحة بأسلوب بسيط ومشجع للطالب."
                    response = model.generate_content([prompt, image])

                    st.markdown("### 📊 نتيجة التصحيح:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"حدث خطأ أثناء المعالجة: {e}")

# --- القسم الثاني: تلخيص الدروس ---
with tab2:
    st.subheader("تلخيص النصوص والدروس")
    lesson_text = st.text_area(
        "اضع النص أو الدرس هنا:", height=200, placeholder="اكتب أو انسخ الدرس هنا..."
    )

    if st.button("✨ تلخيص الدرس", key="btn_summary"):
        if lesson_text.strip():
            with st.spinner("جاري التلخيص..."):
                try:
                    prompt = "لخص هذا الدرس في نقاط رئيسية وبسيطة ومحددة لتسهيل الحفظ والمذاكرة على الطالب."
                    response = model.generate_content([prompt, lesson_text])

                    st.markdown("### 📝 الملخص:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"حدث خطأ: {e}")
        else:
            st.warning("يرجى كتابة نص الدرس أولاً!")
