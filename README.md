# מערכת BI לניהול מלאי

פרויקט זה מציג מערכת BI מלאה לניהול וניתוח מלאי ומכירות.  
המערכת בנויה על בסיס **PostgreSQL**, **Python**, **Pandas**, **SQLAlchemy**, **Streamlit** ו־**Plotly**, ומדמה סביבת עבודה עסקית אמיתית.  

---

## מטרות הפרויקט
- ניתוח מלאי: זיהוי מוצרים מתחת לרף המינימום והצגת פילוח לפי קטגוריות.  
- ניתוח מכירות: הצגת מגמות מכירות חודשיות וניתוח לפי קטגוריות מוצרים.  
- תחזית: חיזוי מכירות עתידי באמצעות מודל Machine Learning (Linear Regression).  
- SQL חופשי: יכולת להריץ שאילתות מותאמות אישית מתוך הממשק.  

---

## טכנולוגיות בשימוש
- **PostgreSQL** – מסד נתונים רלציוני לניהול המידע.  
- **Docker + Adminer** – הקמה וניהול סביבה מבוססת קונטיינרים.  
- **Python (Pandas, NumPy, SQLAlchemy, Scikit-learn)** – עיבוד נתונים ו־Machine Learning.  
- **Streamlit** – פיתוח דשבורד אינטראקטיבי.  
- **Plotly** – גרפים אינטראקטיביים ברמה גבוהה.  
- **dotenv** – ניהול משתני סביבה מאובטחים.  

---

## מבנה הפרויקט
inventory-bi/
│
├── app/
│ └── streamlit_app.py # קובץ האפליקציה הראשי (הדשבורד)
│
├── etl/
│ └── load_csv_to_db.py # סקריפט טעינת נתוני דמה למסד הנתונים
│
├── sql/
│ └── schema.sql # סכימת בסיס הנתונים
│
├── docker-compose.yml # הפעלת PostgreSQL ו-Adminer בקונטיינרים
├── requirements.txt # ספריות פייתון נדרשות
├── .env # משתני סביבה (DB host, user, password)
└── README.md # תיעוד הפרויקט

---

## התקנה והרצה מקומית

### שלב 1 – שיבוט המאגר
```bash
git clone https://github.com/<username>/inventory-bi.git
cd inventory-bi
שלב 2 – יצירת סביבת פיתוח והתקנת תלויות
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

שלב 3 – הפעלת מסד הנתונים עם Docker
docker compose up -d


בדיקה: Adminer יעלה בכתובת http://localhost:8080
.

שלב 4 – טעינת נתונים למסד
python etl/load_csv_to_db.py

שלב 5 – הפעלת הדשבורד
streamlit run app/streamlit_app.py


המערכת תעלה על http://localhost:8501
.

פיצ'רים מרכזיים

KPI ראשיים – מציגים במבט אחד את מצב המלאי והמוצרים הקריטיים.

גרפים אינטראקטיביים – מכירות חודשיות, פילוח לפי קטגוריות ומלאי.

מודול חיזוי – תחזית מכירות ל־6 חודשים קדימה באמצעות Machine Learning.

SQL חופשי – ממשק להרצת שאילתות מותאמות אישית מתוך הדשבורד.

דוגמאות מסך

(כאן תוכל להוסיף צילומי מסך של הדשבורד לאחר ההרצה)

הערות

פרויקט זה מדגים יכולות BI מלאות: עבודה עם דאטה, עיבוד, חיבור ל־DB, הצגת תובנות, ו־ML בסיסי.

מיועד להצגה כפרויקט פורטפוליו מקצועי לסטודנט לניהול מערכות מידע / דאטה אנליסט.


---

💡 המלצה:  
תוסיף צילומי מסך יפים של הדשבורד שלך לתיקיית `docs/` ותצרף אותם ל־README עם Markdown, למשל:  

```markdown
![Dashboard Overview](docs/dashboard.png)
