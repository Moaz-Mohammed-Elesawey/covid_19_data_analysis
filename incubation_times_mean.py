import re
import os
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm


dirs = ["biorxiv_medrxiv", "comm_use_subset", "custom_license", "noncomm_use_subset"]
# dirs = ["biorxiv_medrxiv"]
docs = []
for d in dirs:
    for file in tqdm(os.listdir(f"{d}/{d}")):
        file_path = f"{d}/{d}/{file}"
        j = json.load(open(file_path, "rb"))

        title = j['metadata']['title']
        try:
            body_text = j['body_text'][0]
            abstract = j['abstract']
        except:
            body_text = ""
            abstract = ""

        tot_txt = ""

        for abs_text in j['abstract']:
            tot_txt += abs_text['text']

        for bod_text in j['body_text']:
            tot_txt += bod_text['text']+"\n\n"

        docs.append([title, abstract, body_text, tot_txt])

df = pd.DataFrame(docs, columns=['title', 'abstract', 'body_text', 'tot_txt'])


incubation = df[df['tot_txt'].str.contains("incubation")]

incubation_times = []

texts = incubation['tot_txt'].values

for t in texts:
    for sentence in t.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("?", "").replace(",", "").split('. '):
        if "incubation" in sentence:
            single_day = re.findall(r" \d{1,3} day", sentence)
            if len(single_day) == 1:
                case = single_day[0].split(" ")
                incubation_times.append(float(case[1]))
            elif len(single_day) == 1:
                case_1 = single_day[0].split(" ")
                case_2 = single_day[1].split(" ")
                incubation_times.append(float(case_1[1]))
                incubation_times.append(float(case_2[1]))
            elif len(single_day) == 1:
                case_1 = single_day[0].split(" ")
                case_2 = single_day[1].split(" ")
                case_3 = single_day[2].split(" ")
                incubation_times.append(float(case_1[1]))
                incubation_times.append(float(case_2[1]))
                incubation_times.append(float(case_3[1]))



with open("incubation_times_body_text.txt", "w") as f:
    f.write(str(incubation_times))

# with open("incubation_times_body_text.txt", "r") as f:
#     incubation_times = np.array(f.read().replace("\n", "").replace("[", "").replace("]", "").split(", "))

incubation_times = np.array(incubation_times).astype('float64')

print(incubation_times)
print(f"The Len of incubation times : {len(incubation_times)}")
print(f"The mean projected incubation time is {np.mean(incubation_times)} days")

plt.style.use("seaborn")
plt.hist(incubation_times, bins=50)
plt.ylabel("bins counts")
plt.xlabel("incubation times")
plt.show()
