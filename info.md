## 🔥 Hits

## 🧠 HIGH LEVEL — תיאור הפרויקט (קבוע)

**AI Knowledge Assistant לקבצים אישיים**
Pipeline יחיד:

**Files → Text → Chunks → Knowledge Store → Retrieval → Answer + Source**

CLI הוא העטיפה.
הלוגיקה היא הלב.
אין UI אחר עד סוף ה־Pipeline.

---

## 🧩 הפרקים (מפת־על קבועה)

1. **Entry Point** — CLI ושלד
2. **Ingestion** — קבצים → טקסט
3. **Normalization** — טקסט → chunks
4. **Knowledge Store v0** — JSON
5. **Retrieval v0** — חיפוש נאיבי
6. **Representation** — embeddings
7. **Knowledge Store v1** — Vector DB
8. **Retrieval v1** — semantic search
9. **Reasoning** — RAG
10. **Grounding** — מניעת הזיות
11. **Interface** — CLI יציב
12. **Maintainability** — ניקוי קוד
13. **Productization** — README
14. **Proof** — Demo



## 🔥 Hits

אותה טבלה — שכבה אחת מעל.
עכשיו אתה רואה **איך כל חלק משרת את המוצר**, לא רק מה כותבים.

---

## 🧠 HIGH-LEVEL MAP (לפני הטבלה)

המערכת כולה היא **Pipeline אחד**:

**קבצים → ידע מובנה → חיפוש → תשובה עם מקור**

כל פרק מטפל **בשלב אחד בשרשרת**.
אין פרקים “לידע כללי”.

---

## 📋 תוכנית מלאה עם HIGH LEVEL

| #  | High-Level שלב במוצר | נושא             | מה קורה עקרונית        | מה בונים בפועל            | תוצר מחייב        |
| -- | -------------------- | ---------------- | ---------------------- | ------------------------- | ----------------- |
| 1  | Entry Point          | שלד פרויקט + CLI | נקודת כניסה אחת למערכת | `cli.py` עם `index / ask` | CLI לא נופל       |
| 2  | Ingestion            | קריאת קבצים      | הפיכת קבצים לטקסט      | Reader ל-PDF / TXT / MD   | טקסט בזיכרון      |
| 3  | Normalization        | ניקוי ופיצול     | הפיכת טקסט ליחידות ידע | chunks                    | רשימת chunks      |
| 4  | Knowledge Store (v0) | Indexing נאיבי   | אחסון ידע בלי חוכמה    | JSON                      | `index.json`      |
| 5  | Retrieval (v0)       | Ask נאיבי        | מציאת ידע רלוונטי      | חיפוש מחרוזות             | תשובה + מקור      |
| 6  | Representation       | Embeddings       | ייצוג ידע מספרי        | vectors                   | embeddings נשמרים |
| 7  | Knowledge Store (v1) | Vector DB        | אחסון וחיפוש סמנטי     | FAISS / Chroma            | top-k מדויק       |
| 8  | Retrieval (v1)       | Retriever        | בחירת קונטקסט נכון     | rank + filter             | מקורות טובים      |
| 9  | Reasoning            | RAG בסיסי        | שילוב ידע + LLM        | prompt עם context         | תשובה מבוססת      |
| 10 | Grounding            | Guardrails       | מניעת הזיות            | source check              | סירוב חכם         |
| 11 | Interface            | CLI יציב         | UX מינימלי             | flags / errors            | CLI נוח           |
| 12 | Maintainability      | Refactor         | קוד קריא               | הפרדה לקבצים              | קוד נקי           |
| 13 | Productization       | README           | שימוש ברור             | docs                      | משתמש מבין        |
| 14 | Proof                | Demo             | הוכחה שזה עובד         | דוגמה מלאה                | ריצה מלאה         |

---

## 🧭 איך לקרוא את הטבלה נכון

אם אתה בשורה:

* 2–4 → אתה **בונה ידע**
* 5–8 → אתה **שולף ידע**
* 9–10 → אתה **חושב עם ידע**
* 11–14 → אתה **מוכר מוצר**

אם אתה מנסה “לחשוב” לפני שיש לך ידע —
אתה מקדים את עצמך.

---

## ⛔ נקודת עצירה חשובה

אסור:

* לעבוד על שתי שורות במקביל
* לדלג High-Level
* “להבין הכול מראש”

כל שורה = יום או יומיים. לא יותר.

---

## משפט סיום

AI טוב זה לא מודל חכם.
זה צינור פשוט שלא משקר.

—
{N/A} / {N/A}
