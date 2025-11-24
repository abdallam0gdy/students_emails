import streamlit as st
import pandas as pd

# 1. إعداد الصفحة
st.set_page_config(page_title="نظام الاستعلام عن بيانات الطلاب", layout="centered")

# 2. تحميل البيانات (يتم مرة واحدة وتبقى في الكاش لتسريع الموقع)
@st.cache_data
def load_data():
    # تأكد أن ملفك محفوظ بصيغة CSV
    # dtype={'NationalID': str, 'StudentCode': str} مهم جداً عشان الصفر اللي على الشمال ما يطيرش
    df = pd.read_csv("data.csv", dtype=str)
    # تنظيف المسافات الزائدة في الأسماء والأكواد
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()
    
    # 3. واجهة المستخدم
    st.title("🎓 بوابة الاستعلام عن بيانات الطالب")
    st.markdown("---")

    # خانات الإدخال
    col1, col2 = st.columns(2)
    with col1:
        student_code = st.text_input("كود الطالب", max_chars=20)
    with col2:
        national_id = st.text_input("الرقم القومي", type="password", max_chars=14) # type=password يخفي الأرقام

    # زر البحث
    if st.button("استعلام"):
        if not student_code or not national_id:
            st.warning("برجاء إدخال الكود والرقم القومي")
        else:
            # 4. منطق البحث الآمن
            # البحث عن صف يطابق الشرطين معاً (الكود والرقم القومي)
            # افترضت هنا أن أسماء الأعمدة في ملفك هي 'الكود' و 'رقم البطاقة' بناء على الملف اللي رفعته
            # لازم تغير أسماء الأعمدة في الكود لو مختلفة في ملف الـ csv النهائي
            result = df[(df['الكود'] == student_code) & (df['رقم البطاقة'] == national_id)]

            if not result.empty:
                st.success(f"مرحباً بك: {result.iloc[0]['الاسم باللغة العربية']}")
                
                # عرض البيانات الحساسة في صندوق أنيق
                st.info("بيانات الدخول الخاصة بك:")
                st.code(f"Username: {result.iloc[0]['Username']}", language="text")
                st.code(f"Password: {result.iloc[0]['Password']}", language="text")
                
            else:
                st.error("البيانات المدخلة غير صحيحة. تأكد من الكود والرقم القومي.")

except FileNotFoundError:
    st.error("عفواً، ملف البيانات غير موجود.")
except Exception as e:
    st.error(f"حدث خطأ ما: {e}")

# إخفاء القائمة الجانبية وحقوق ستريم ليت عشان الشكل العام
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
