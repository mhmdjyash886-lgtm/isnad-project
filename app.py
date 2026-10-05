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
# تنسيق التطبيق
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
        color: #20232a;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #666;
        margin-bottom: 35px;
    }

    .answer-box {
        background: #f7f7f7;
        border-radius: 15px;
        padding: 25px;
        margin-top: 25px;
        border-right: 5px solid #444;
        line-height: 2;
    }

    .warning {
        background: #fff8e1;
        border-radius: 12px;
        padding: 15px;
        margin-top: 20px;
        font-size: 15px;
    }

    .stButton button {
        width: 100%;
        border-radius: 10px;
        height: 50px;
        font-size: 18px;
        font-weight: bold;
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
    'منصة ذكية للمساعدة في الوصول إلى الإجابات الشرعية الموثقة '
    'مع العناية بالدليل والمصدر'
    '</div>',
    unsafe_allow_html=True
)

# =========================
# سؤال المستخدم
# =========================
question = st.text_area(
    "اكتب سؤالك الشرعي أو الاستفسار المعرفي هنا:",
    placeholder="مثال: هل المني طاهر؟\nأو: ما حكم الصلاة بدون وضوء؟",
    height=130
)

# =========================
# زر الإرسال
# =========================
if st.button("🔎 البحث عن الحكم الشرعي"):

    if not question.strip():
        st.warning("من فضلك اكتب السؤال أولاً.")
        st.stop()

    # قراءة مفتاح OpenAI من Streamlit Secrets
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        st.error(
            "لم يتم إعداد مفتاح الذكاء الاصطناعي. "
            "أضف OPENAI_API_KEY في Secrets الخاصة بالتطبيق."
        )
        st.stop()

    client = OpenAI(api_key=api_key)

    # =========================
    # التعليمات الشرعية للنموذج
    # =========================
    instructions = """
أنت مساعد بحث شرعي باللغة العربية اسمه "إسناد".

مهمتك مساعدة المستخدم في فهم الأحكام والمسائل الشرعية،
ولست مفتياً مستقلاً، ولا يجوز لك اختلاق نصوص أو أحاديث أو نسب أقوال
إلى العلماء دون علم.

التزم بالقواعد التالية:

1. أجب باللغة العربية الواضحة.
2. افهم السؤال أولاً ثم أجب عنه مباشرة.
3. اذكر الحكم باختصار في البداية.
4. إذا كان هناك دليل من القرآن، اذكر اسم السورة ورقم الآية إن كنت متأكداً.
5. إذا استدللت بحديث، لا تنسب حديثاً إلى النبي ﷺ إلا إذا كنت واثقاً من صحته.
6. إذا كان الحديث ضعيفاً أو مختلفاً في تصحيحه، وضح ذلك.
7. إذا كانت المسألة محل خلاف معتبر بين العلماء، اذكر وجود الخلاف
   وأهم الأقوال باختصار، ولا تعرض قولاً واحداً على أنه إجماع.
8. لا تخترع أسماء علماء أو كتب أو أرقام صفحات.
9. لا تصدر فتوى قطعية في المسائل الشخصية المعقدة أو الخطيرة.
10. في مسائل الطلاق، المواريث، النذور، الكفارات، والقضايا الزوجية الحساسة:
    نبه المستخدم إلى ضرورة سؤال عالم موثوق أو جهة إفتاء مؤهلة.
11. إذا لم تكن متأكداً من الحكم، قل بوضوح:
    "لا أستطيع الجزم بهذه المسألة، والأفضل سؤال عالم موثوق."
12. لا تستخدم الثقة الزائدة.
13. فرّق بوضوح بين:
    - القرآن
    - السنة
    - أقوال العلماء
    - الاستنتاج أو الشرح.
14. لا تجعل الإجابة طويلة بلا حاجة.

استخدم هذا الشكل:

الحكم:
[الجواب المختصر]

الدليل:
[الدليل إن وجد]

أقوال العلماء:
[عند وجود خلاف معتبر]

التوضيح:
[شرح مختصر]

المصدر:
[اذكر المصدر إن كنت متأكداً منه]

تنبيه:
[إذا كانت المسألة تحتاج إلى سؤال مفتٍ مختص]
"""

    # =========================
    # إرسال السؤال
    # =========================
    try:
        with st.spinner("جاري البحث والتحقق من المسألة..."):

            response = client.responses.create(
                model="gpt-5.5",
                instructions=instructions,
                input=question
            )

            answer = response.output_text

        st.markdown(
            '<div class="answer-box">',
            unsafe_allow_html=True
        )

        st.markdown("### 📖 الإجابة الشرعية")
        st.markdown(answer)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            '<div class="warning">'
            '⚠️ <b>تنبيه:</b> هذه الإجابة للمساعدة في البحث والمعرفة '
            'وليست بديلاً عن سؤال عالم أو مفتٍ مؤهل، خصوصاً في المسائل '
            'الشخصية والقضايا التي يترتب عليها حكم أو حق.'
            '</div>',
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error(
            "حدث خطأ أثناء الحصول على الإجابة. "
            "تأكد من إعداد مفتاح API واتصال التطبيق بالإنترنت."
        )
