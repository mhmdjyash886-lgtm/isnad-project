import streamlit as st
from openai import OpenAI

# =========================
# إعداد الصفحة
# =========================
st.set_page_config(
    page_title="إسناد - المساعد الشرعي",
    page_icon="🛡️",
    layout="centered"
)

# =========================
# التصميم
# =========================
st.markdown("""
<style>
html, body, [class*="css"] {
    direction: rtl;
    text-align: right;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    margin-top: 20px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #666;
    margin-bottom: 30px;
}

.answer {
    background: #f7f7f7;
    padding: 25px;
    border-radius: 15px;
    border-right: 5px solid #333;
    line-height: 2;
}

.warning {
    background: #fff8e1;
    padding: 15px;
    border-radius: 12px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# العنوان
# =========================
st.markdown(
    '<div class="title">🛡️ مشروع إسناد (ISNAD)</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'مساعد ذكي للبحث في الأحكام والمسائل الشرعية'
    '</div>',
    unsafe_allow_html=True
)

# =========================
# السؤال
# =========================
question = st.text_area(
    "اكتب سؤالك الشرعي هنا:",
    placeholder="مثال: ما حكم الصلاة بدون وضوء؟",
    height=140
)

# =========================
# زر البحث
# =========================
if st.button("🔎 البحث عن الحكم الشرعي"):

    if not question.strip():
        st.warning("⚠️ يرجى كتابة السؤال أولاً.")
        st.stop()

    # قراءة مفتاح API من Secrets
    try:
        client = OpenAI(
            api_key=st.secrets["OPENAI_API_KEY"]
        )
    except Exception:
        st.error(
            "❌ لم يتم العثور على OPENAI_API_KEY في إعدادات Secrets."
        )
        st.stop()

    # =========================
    # تعليمات المساعد
    # =========================
    instructions = """
أنت مساعد شرعي اسمه "إسناد".

وظيفتك مساعدة المستخدم على فهم المسائل الشرعية
والبحث عن الحكم مع الدليل، وليس إصدار فتوى شخصية
بلا علم.

التزم بما يلي:

1. أجب باللغة العربية.
2. ابدأ بالحكم المختصر.
3. اذكر الدليل من القرآن أو السنة إذا كان مناسباً.
4. لا تخترع آيات أو أحاديث.
5. لا تنسب قولاً إلى عالم إلا إذا كنت متأكداً منه.
6. إذا كانت المسألة فيها خلاف فقهي معتبر، اذكر الخلاف بوضوح.
7. لا تقل "أجمع العلماء" إلا إذا كان الإجماع ثابتاً.
8. ميّز بين النص الشرعي وبين قول الفقيه وبين الشرح.
9. إذا لم تكن متأكداً من معلومة، صرّح بعدم التأكد.
10. في مسائل الطلاق والمواريث والنذور والكفارات
    والقضايا الشخصية الحساسة، انصح المستخدم بالرجوع
    إلى عالم أو جهة إفتاء موثوقة.
11. لا تقدم رأيك الشخصي على أنه حكم شرعي.
12. اجعل الإجابة واضحة ومختصرة.

استخدم هذا الشكل:

### الحكم
...

### الدليل
...

### أقوال العلماء
...

### التوضيح
...

### المصدر
...

### تنبيه
...
"""

    # =========================
    # إرسال السؤال
    # =========================
    try:

        with st.spinner("🔍 جاري البحث عن الإجابة..."):

            response = client.responses.create(
                model="gpt-6-luna",
                instructions=instructions,
                input=question
            )

            answer = response.output_text

        # =========================
        # عرض الإجابة
        # =========================
        st.markdown(
            '<div class="answer">',
            unsafe_allow_html=True
        )

        st.markdown("## 📖 الإجابة")

        st.markdown(answer)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            '<div class="warning">'
            '⚠️ <b>تنبيه:</b> هذه المنصة للمساعدة في البحث والمعرفة '
            'ولا تغني عن سؤال عالم أو مفتٍ مؤهل، خصوصاً في المسائل '
            'الشخصية والقضايا التي يترتب عليها حكم شرعي أو حق.'
            '</div>',
            unsafe_allow_html=True
        )

    except Exception as e:

        st.error(
            "❌ حدث خطأ أثناء الحصول على الإجابة."
        )

        st.caption(str(e))
