import requests
import pandas as pd
import json
import re
import time

def fetch_candidate(candidate_id: int) -> dict | None:
    url = f"https://www.dr.dk/nyheder/politik/folketingsvalg/din-stemmeseddel/kandidater/{candidate_id}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return None
        
        chunks = re.findall(r'self\.__next_f\.push\(\[1,"(.+?)"\]\)', r.text)
        combined = "".join(chunks).replace('\\"', '"').replace("\\'", "'")
        
        candidate_match = re.search(r'"candidate":(\{.*?"LineUps":\[.*?\]\})', combined, re.DOTALL)
        answers_match = re.search(r'"candidateAnswers":(\[.*?\])', combined, re.DOTALL)
        
        if not candidate_match or not answers_match:
            return None
        
        candidate = json.loads(candidate_match.group(1))
        answers = json.loads(answers_match.group(1))
        return {"candidate": candidate, "answers": answers}
    
    except Exception:
        return None


def build_dataframe(id_range: range) -> pd.DataFrame:
    rows = []
    
    for cid in id_range:
        data = fetch_candidate(cid)
        if data is None:
            time.sleep(0.3)
            continue
        
        c = data["candidate"]
        base = {
            "candidate_id": cid,
            "name": f"{c['Firstname']} {c['LastName']}",
            "party": c["CurrentParty"],
            "city": c["City"],
        }
        
        for answer in data["answers"]:
            row = base.copy()
            row["question_id"] = answer["QuestionID"]
            row["answer"] = answer["Answer"]
            row["info"] = answer.get("Info", "")
            row["is_important"] = answer.get("IsImportant", 0)
            rows.append(row)
        
        print(f"Hentet {cid}: {base['name']} ({base['party']})")
        time.sleep(0.3)
    
    return pd.DataFrame(rows)


#df = build_dataframe(range(1, 1001))
#print(f"\nFærdig: {df['candidate_id'].nunique()} kandidater, {len(df)} rækker")
#df.to_csv("kandidater.csv", index=False)

url = "https://www.dr.dk/nyheder/politik/folketingsvalg/din-stemmeseddel/kandidater/512"
headers = {"User-Agent": "Mozilla/5.0"}

r = requests.get(url, headers=headers)
chunks = re.findall(r'self\.__next_f\.push\(\[1,"(.+?)"\]\)', r.text)
combined = "".join(chunks).replace('\\"', '"').replace("\\'", "'")

questions_match = re.search(r'"questions":(\[.*?\])\}', combined, re.DOTALL)
questions = json.loads(questions_match.group(1))

df_questions = pd.DataFrame([
    {"question_id": q["Id"], "title": q["Title"], "question_text": q["Question"]}
    for q in questions
])

print(df_questions)
df_questions.to_csv("questions.csv", index=False)