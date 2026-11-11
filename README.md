# ערכת התחלה: מערכת RAG לחברת הרכב "אופק רכב"

החברה והנתונים דמיוניים, ונכתבו לצורך התרגיל.

## מה יש בתיקייה

- `data/` — 16 מסמכים של החברה: מפרט טכני לכל דגם, מחירון, קטלוג אביזרים, אחריות, טיפולים, קודי התרעה וקריאות שירות.
- `golden.json` — 15 שאלות בדיקה, ולכל שאלה הטקסט שחייב להופיע בקטע הנכון.
- `rag/` — הצינור: `loader.py`, `chunking.py`, `embed.py`, `search.py`, `answer.py`.
- `eval_retrieval.py` — מדידת האחזור. חינם, בלי קריאה ל־Claude.
- `eval_answers.py` — מדידת התשובות. עולה בערך סנט אחד עם claude-haiku-5-5.
- `bonus_split.py` — בונוס: פירוק של שאלה 12 לשני חיפושים.
- `REPORT.md` — הדוח: אבחון, תוצאות לפי גרסה ותשובות לשאלות.
- `.cache/` — וקטורים שכבר חושבו. התיקייה לא נכנסת ל־git, ונבנית מחדש אוטומטית בהרצה הראשונה (זה לוקח כמה דקות).

## התקנה

נדרש Python 3.10 ומעלה.

```
pip install -r requirements.txt
python eval_retrieval.py
```

אם הכול תקין, השורה האחרונה תהיה `total 6/13 0.37`.

## מה מומש

| קובץ | פונקציה | מה היא עושה |
|---|---|---|
| `rag/chunking.py` | `chunk_by_headings` | קטע אחד לכל כותרת `##`. כל קטע מתחיל בשורת נתיב, למשל `אופק סיטי (OF-210) › מנוע והנעה`, וטבלאות נשארות שלמות |
| `rag/search.py` | `rrf` | איחוד של הדירוג לפי משמעות ושל הדירוג של BM25 לפי המקום: כל קטע מקבל `1 / (60 + מקום)` מכל רשימה |
| `rag/search.py` | `is_current` | מסנן מסמכים שבמטא־דאטה שלהם כתוב `status: superseded` |
| `rag/answer.py` | `verify_citations` | מחזיר את הציטוטים שלא מופיעים מילה במילה בקטע שהם מפנים אליו. הבדיקה מתעלמת מהבדלים ברווחים ובשורות חדשות |

### בונוס

- **הגנה מפני הזרקת הוראות** (`rag/answer.py`): ה־system prompt קובע שהטקסט שבתוך `<chunk>` הוא מידע ולא הוראות, והפונקציה `clean()` מוחקת הערות HTML מהקטעים לפני שהם נשלחים למודל.
- **פירוק שאלה עם כמה מקורות** (`bonus_split.py`): חיפוש נפרד לכל רכב, ואיחוד של התוצאות.

## הרצה

```
python eval_retrieval.py                                                   # הבסיס: 6/13 · 0.37
python eval_retrieval.py --chunker headings                                # חיתוך לפי כותרות: 9/13 · 0.65
python eval_retrieval.py --chunker headings --mode hybrid                  # היברידי: 9/13 · 0.69
python eval_retrieval.py --chunker headings --mode hybrid --current-only   # מטא־דאטה: 11/13 · 0.76
python eval_answers.py --chunker headings --mode hybrid --current-only     # תשובות Claude: 13/15
python bonus_split.py                                                      # בונוס: שאלה 12
```

הניתוח המלא נמצא ב־`REPORT.md`.

## וקטורים

ברירת המחדל היא המודל `intfloat/multilingual-e5-small`, שרץ על המחשב בחינם ותומך בעברית. אפשר במקומו להשתמש ב־Voyage AI:

```
pip install voyageai
```

ואז להגדיר את משתני הסביבה `EMBED_BACKEND=voyage` ו־`VOYAGE_API_KEY`.

## מפתחות

`ANTHROPIC_API_KEY` ו־`VOYAGE_API_KEY` מוגדרים רק כמשתני סביבה בטרמינל. לעולם לא בקוד ולא ב־git.
