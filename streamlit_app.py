import io
import google.generativeai as genai
from PIL import Image
import streamlit as st

# ضبط إعدادات الصفحة
st.set_page_config(
    page_title="المنصة التعليمية الشاملة", page_icon="🎓", layout="centered"
)

# الربط بمفتاح الذكاء الاصطناعي من Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.sidebar.warning(
        "⚠️ يرجى إضافة GEMINI_API_KEY في Secrets للتشغيل الآلي لتصحيح الصور والملخصات."
    )

st.title("🎓 المنصة التعليمية الشاملة")
st.write(
    "أهلاً بك! اختاري الخدمة التي تحتاجينها من القائمة الجانبية أو الأبواب أعلاه:"
)

# القائمة الرئيسية للمنصة
tab1, tab2, tab3 = st.tabs(
    ["📝 الاختبار الإلكتروني", "📸 تصحيح الواجبات", "📚 تلخيص المذكرات"]
)

# ==========================================
# 1. قسم الاختبار الإلكتروني
# ==========================================
with tab1:
    st.header("📝 اختبار الدراسات الاجتماعية التفاعلي")

    student_name = st.text_input("اسم الطالب رباعياً:", key="quiz_name")
    student_class = st.selectbox(
        "المرحلة الدراسية:",
        [
            "الصف الأول الإعدادي",
            "الصف الثاني الإعدادي",
            "الصف الثالث الإعدادي",
        ],
        key="quiz_class",
    )

    st.divider()

    # بنك الأسئلة المقالية والنموذجية
    questions = [
        {
            "id": 1,
            "question": "بم تفسر: يُطلق على قارتي آسيا وأوروبا معاً مصطلح 'أوراسيا'؟",
            "model_answer": "لأن قارة أوروبا تبدو وكأنها امتداد طبيعي لقارة آسيا من جهة الغرب.",
        },
        {
            "id": 2,
            "question": "ما المقصود بـ 'الأرخبيل'؟",
            "model_answer": "مجموعة من الجزُر المتجاورة في مسطح مائي (مثل: أرخبيل اليابان وإندونيسيا).",
        },
        {
            "id": 3,
            "question": "بم تفسر: استخدام التيتانيوم في صناعة هياكل الطائرات والصواريخ؟",
            "model_answer": "لأنه يتميز بخفة وزنه وصلابته العالية ومقاومته الكبيرة للتآكل.",
        },
        {
            "id": 4,
            "question": "ما النتائج المترتبة على: تعرج سواحل قارة أوروبا وكثرة جزرها؟",
            "model_answer": "أدى ذلك إلى سهولة إنشاء الموانئ الطبيعية وتسهيل الاتصال بالعالم الخارجي.",
        },
        {
            "id": 5,
            "question": "بم تفسر: شهرة الملك حمورابي في تاريخ العراق القديم؟",
            "model_answer": "لأنه وضع مجموعة من القوانين تضمنت مختلف جوانب الحياة وكفلت حقوق المرأة.",
        },
    ]

    user_answers = {}

    for q in questions:
        st.subheader(f"س{q['id']}: {q['question']}")
        user_answers[q["id"]] = st.text_area(
            "اكتب إجابتك هنا:", key=f"ans_{q['id']}"
        )

    st.divider()

    if st.button("إرسال التقييم وعرض النتيجة 🚀"):
        if not student_name:
            st.warning("⚠️ يرجى كتابة اسمك أولاً قبل تسليم الاختبار!")
        else:
            st.success(f"تم تسليم الإجابات بنجاح يا {student_name}!")
            st.subheader("📊 تقرير الإجابات والتقييم:")

            summary_text = f"تقرير الطالب: {student_name}\nالمرحلة: {student_class}\n\n=========================\n\n"

            for q in questions:
                ans = user_answers[q["id"]]
                st.markdown(f"**س{q['id']}: {q['question']}**")
                st.write(f"✍️ **إجابتك:** {ans if ans else 'لم يتم الإجابة'}")
                st.info(f"💡 **الإجابة النموذجية:** {q['model_answer']}")
                st.divider()

                summary_text += f"س{q['id']}: {q['question']}\nإجابة الطالب: {ans if ans else 'لم يتم الإجابة'}\nالإجابة النموذجية: {q['model_answer']}\n-------------------\n"

            st.download_button(
                label="📥 تحميل تقرير إجاباتك",
                data=summary_text,
                file_name=f"اختبار_{student_name}.txt",
                mime="text/plain",
            )

# ==========================================
# 2. قسم تصحيح الواجبات الذكي
# ==========================================
with tab2:
    st.header("📸 تصحيح أوراق الواجب")
    st.write(
        "ارفعي صورة ورقة الواجب الخاصة بالطالب، وسيقوم الذكاء الاصطناعي بتصحيحها وتوضيح الأخطاء."
    )

    uploaded_hw = st.file_uploader(
        "اختر صورة الواجب:", type=["jpg", "jpeg", "png"], key="hw_file"
    )

    if uploaded_hw is not None:
        image = Image.open(uploaded_hw)
        st.image(
            image, caption="صورة الواجب المرفوعة", use_container_width=True
        )

        if st.button("تصحيح الواجب الآن ✨"):
            with st.spinner("جاري تحليل ورقة الواجب وتصحيحها..."):
                try:
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    prompt = "أنت معلم محترف. قم بفحص صورة الواجب هذه، واستخرج الإجابات الخاطئة وحدد الإجابة الصحيحة مع شرح بسيط لسبب الخطأ بأسلوب تشجيعي للطفل."
                    response = model.generate_content([prompt, image])
                    st.success("تم تصحيح الواجب بنجاح!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(
                        "حدث خطأ أثناء الاتصال بالذكاء الاصطناعي. تأكدي من ضبط API Key."
                    )

# ==========================================
# 3. قسم تلخيص المذكرات والدروس
# ==========================================
with tab3:
    st.header("📚 تلخيص المذكرات والدروس")
    st.write(
        "ارفعي صورة صفحة المذكرة أو كتاب الدرس للتحصلين على ملخص سريع لأهم المفاط النقاط والعناوين."
    )

    uploaded_doc = st.file_uploader(
        "اختر صورة المذكرة/الدرس:",
        type=["jpg", "jpeg", "png"],
        key="doc_file",
    )

    if uploaded_doc is not None:
        doc_image = Image.open(uploaded_doc)
        st.image(
            doc_image,
            caption="صورة المذكرة المرفوعة",
            use_container_width=True,
        )

        if st.button("تلخيص الدرس الآن 📝"):
            with st.spinner("جاري قراءة المذكرة وتلخيصها..."):
                try:
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    prompt = "قم بقراءة المحتوى التعليمي في هذه الصورة وتلخيصه في نقاط رئيسية مركزة وسهلة للحفظ والمراجعة للطلاب."
                    response = model.generate_content([prompt, doc_image])
                    st.success("تم تلخيص الدرس بنجاح!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(
                        "حدث خطأ أثناء الاتصال بالذكاء الاصطناعي. تأكدي من ضبط API Key."
                    )
