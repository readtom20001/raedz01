
import os
from groq import Groq
from review_fetcher import *
import streamlit as st

def find_theme(reviews):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        completion = client.chat.completions.create(
            model='llama3-70b-8192',
            messages=[
                {
                    "role": "system",
                    "content": """أنت استشاري أعمال وتجربة عملاء رقمي. قم بتحليل المراجعات التالية واستخرج أبرز المواضيع التي يذكرها العملاء. ثم قدم النتائج بشكل منظم واحترافي كما لو كانت موجهة لتقرير Power BI.

أولاً: قائمة منسقة لأهم المواضيع المذكورة، مرتبة حسب التكرار، بالشكل التالي:
| رقم | عنوان الموضوع | الوصف الموجز للفكرة | نسبة التكرار التقديرية (%) |
|-----|----------------|------------------------|-----------------------------|

ثانياً: بناءً على المواضيع المكتشفة، اقترح ما يلي:
* مجالات التحسين الرئيسية.
* مبادرات استراتيجية أو حملات تحسين تجربة العميل.
* توصيات تنفيذية واضحة بلغة استشارية.

كل النتائج يجب أن تكون باللغة العربية الفصحى، وبتنسيق جداول احترافية كما في لوحات المعلومات (Dashboards)."""
                },
                {
                    "role": "user",
                    "content": reviews
                }
            ],
            temperature=0.5,
            top_p=1
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error"

def find_sentiment_score(message):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        completion = client.chat.completions.create(
            model='llama3-8b-8192',
            messages=[
                {
                    "role": "system",
                    "content": """قم بتحليل المشاعر المعبر عنها في مراجعة جوجل التالية وتقييم النجوم المصاحب لها (من 1 إلى 5). أرجع درجة رقمية فقط بين -1 (سلبية تماماً) و +1 (إيجابية تماماً)، حيث يمثل 0 الحياد. لا تكتب أي نص إضافي.

راعي عند التحليل:
* التركيز على الكلمات الدالة على المشاعر في النص.
* الجمع بين تقييم النجوم والتعبير النصي.
"""
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=0.1,
            top_p=1
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error"

def categorize_sentiment(score):
    try:
        score = float(score)
        if score > 0.33:
            return "إيجابي"
        elif score < -0.33:
            return "سلبي"
        else:
            return "محايد"
    except:
        return "غير محدد"

def detect_complaints(reviews):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        completion = client.chat.completions.create(
            model='llama3-70b-8192',
            messages=[
                {
                    "role": "system",
                    "content": """أنت مستشار رقمي متخصص في تجربة العملاء وتحسين الأداء. قم بتحليل المراجعات التالية وحدد الشكاوى مع تقديم تحليل شامل على النحو التالي:

1. جدول تفصيلي لكل شكوى:
| نص المراجعة | نوع المشكلة | الحل المقترح | فرصة التحسين | إجراء مقترح | حملة/مبادرة مقترحة |
|-------------|--------------|----------------|----------------|----------------|------------------------|

2. جدول إحصائي لأنواع الشكاوى:
| نوع المشكلة | عدد مرات التكرار | النسبة المئوية (%) |

3. توصيات عامة للتطوير:
* بناء خطة تحسين خدمات العملاء.
* اقتراح حملات علاقات عامة أو تدريب داخلي بناءً على المشاكل المتكررة.
* أفكار لحملات ترويجية أو تحسين ولاء العملاء مرتبطة بالشكاوى المتكررة.

يرجى تنظيم كل الجداول بشكل احترافي باللغة العربية، وكأن التقرير موجه لإدارة تنفيذية تبحث عن قرارات قابلة للتنفيذ استناداً إلى البيانات.
"""
                },
                {
                    "role": "user",
                    "content": reviews
                }
            ],
            temperature=0.5,
            top_p=1
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error"
