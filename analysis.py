
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
                    "content": """
قم بتحليل مراجعات جوجل التالية واستخلص أبرز الأفكار والمواضيع التي تطرق إليها العملاء. قدم النتائج على هيئة قائمة مرقمة للأفكار الرئيسية.
لكل فكرة رئيسية، اذكر ما يلي:
 * عنوان موجز للفكرة (مثال: "جودة الخدمة"، "سرعة التوصيل").
 * شرح وصفي للفكرة لا يتجاوز ثلاثة أسطر، يوضح الموضوع بأسلوب طبيعي مع دمج المصطلحات الأساسية والمشاعر المعبر عنها في المراجعات.

بعد قائمة الأفكار، قم بتقدير نسبة تكرار كل فكرة رئيسية ضمن مجموع المراجعات (مثال: جودة الطعام: 45%، سرعة الخدمة: 30%).

يرجى كتابة جميع النتائج باللغة العربية فقط، بشكل احترافي، مناسب لتقرير رسمي.
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

def find_sentiment_score(message):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        completion = client.chat.completions.create(
            model='llama3-8b-8192',
            messages=[
                {
                    "role": "system", 
                    "content": """
قم بتحليل المشاعر المعبر عنها في نص مراجعة جوجل وتقييم النجوم المصاحب لها (من 1 إلى 5). أرجع درجة رقمية فقط تتراوح بين -1 (الأكثر سلبية) و +1 (الأكثر إيجابية)، حيث يمثل 0 الحياد.
لا تقم بتضمين أي شروحات أو نصوص إضافية.
 * عند التحليل، ادمج بين دلالات النص وتقييم النجوم.
 * أعطِ أولوية للإشارات النصية القوية على تقييم النجوم في حال وجود تعارض.

أمثلة للمدخلات والمخرجات:
المدخل:  {'rating': 1.0, 'text': خدمة سيئة للغاية! انتظرت ساعتين وكان الطعام بارداً.}
المخرج: -1.0

المدخل:  {'rating': 3.0, 'text': الطعام جيد، ولكن النادل كان وقحاً.}
المخرج: -0.3

المدخل:  {'rating': 5.0, 'text': لقد كانت تجربة رائعة في تعلم اليوجا مع السيد راجات. أسلوبه في التدريس مدروس ومحفز.}
المخرج: 1.0

المدخل:  {'rating': 4.0, 'text': المكان جميل والخدمة مقبولة، لكن الأسعار مرتفعة قليلاً.}
المخرج: 0.4
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
                    "content": """
أنت مساعد دعم عملاء متخصص في تحليل تجارب المستخدمين. مهمتك هي قراءة مراجعات جوجل التالية وتحديد أي منها يتضمن شكاوى أو تجارب سلبية.
يجب أن تقدم المخرجات النهائية باللغة العربية الفصحى، وتتضمن الآتي:

أولاً: قائمة بالشكاوى المكتشفة، مع عرض كل شكوى بالتنسيق التالي:
 * نص المراجعة: "نص المراجعة الأصلي الذي يحتوي على الشكوى"
 * المشكلة المحددة: "وصف موجز للمشكلة بكلماتك بناءً على فهمك للمراجعة (مثال: سوء الخدمة، تأخر الطلب، جودة المنتج رديئة، فريق عمل غير متعاون، أسعار مرتفعة، نظافة المكان غير مرضية)."
 * الحل المقترح: "اقترح حلاً عملياً واحداً أو اثنين يمكن للشركة تطبيقه لمعالجة هذه المشكلة تحديداً أو تحسين الوضع بناءً على نوع الشكوى."

ثانياً: تحليل إحصائي للشكاوى المكتشفة:
1. جدول ملخص بأنواع الشكاوى ونسبها المئوية:
    | نوع الشكوى          | عدد مرات التكرار | النسبة المئوية (%) |
    |----------------------|-----------------|--------------------|
    | (مثال: سوء الخدمة)   | (عدد)          | (نسبة)            |
    | ... وهكذا            | ...             | ...                |
    | **الإجمالي**         | **(المجموع)**   | **100%**           |

2. توصيات عامة لتحسين تجربة العملاء بناءً على أكثر الشكاوى تكراراً.
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
