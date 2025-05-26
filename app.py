import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from review_fetcher import *
from analysis import *

st.set_page_config(page_title="Google Review Analyzer", page_icon="🔍", layout="centered")
st.title("🔍 Google Review Analyzer")
st.markdown("أدخل الاسم الكامل للنشاط التجاري أدناه لتحليل مراجعاته الأخيرة على Google")

business_name = st.text_input("اسم النشاط التجاري",placeholder="اكتب اسم النشاط التجاري هنا...")

if st.button("Submit"):
    if business_name:
        with st.spinner("Analyzing reviews..."):
            data_id = get_place_data_id(business_name)
            if not data_id:
                st.error("❌ النشاط التجاري غير موجود. يرجى التحقق من الاسم والمحاولة مرة أخرى.")
                st.stop()
            reviews = get_reviews_from_data_id(data_id, 50)
            reviews_str = str(reviews)
            st.subheader("🧠 الموضوعات الرئيسية في ملاحظات العملاء")
            st.write(find_theme(reviews_str))
            sentiment_scores = [float(find_sentiment_score(str(review))) for review in reviews]
            categories = [categorize_sentiment(score) for score in sentiment_scores]
            st.subheader("📈 اتجاه درجة المشاعر (من الأحدث إلى الأقدم)")
            df_scores = pd.DataFrame({
                'Review Index': list(range(len(sentiment_scores))),
                'Sentiment Score': sentiment_scores
            })
            st.line_chart(df_scores.set_index('Review Index'))

            # Pie Chart: Sentiment Category Distribution
            st.subheader("🥧 توزيع المشاعر")
            df_categories = pd.Series(categories).value_counts()
            fig, ax = plt.subplots()
            ax.pie(df_categories, labels=df_categories.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
            ax.axis('equal')
            st.pyplot(fig)
            st.subheader("🚨 شكاوى ومشكلات العملاء المكتشفة")
            st.write(detect_complaints(reviews_str))
