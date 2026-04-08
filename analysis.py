import requests
import pandas as pd
import json
import re
import time

df = pd.read_csv("kandidater.csv")

df_wide = df.pivot_table(
    index=["candidate_id", "name", "party", "city"],
    columns="question_id",
    values="answer"
).reset_index()

df_wide.columns.name = None

df_wide.to_csv("kandidater_wide.csv", index=False)

print(df_wide.head())

r = requests.get("https://www.dr.dk/nyheder/politik/folketingsvalg/din-stemmeseddel/kandidater/512", headers={"User-Agent": "Mozilla/5.0"})

chunks = re.findall(r'self\.__next_f\.push\(\[1,"(.+?)"\]\)', r.text)
combined = "".join(chunks).replace('\\"', '"').replace("\\'", "'")

# Gem råteksten så vi kan inspicere den
with open("raw.txt", "w") as f:
    f.write(combined)