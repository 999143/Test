import requests
import random
import time

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSe_8EKN8Kt15Jl93s8Orh0JdB6bXczlly7GxPVrZsxPFlC3Vg/formResponse"

# CONFIGURATION
SPECIAL_QUESTION_INDEX = 6  # Question 6 gets Disagree answers
TOTAL_SUBMISSIONS = 25

# Demographics (Page 0)
ID_GENDER = "entry.944541891"
ID_LEVEL  = "entry.1983958125"

# Page 1 is just the introduction text - no questions

# Cluster 1 - Questions 1 to 5 (Page 2)
CLUSTER_1 = [
    "entry.866798967",
    "entry.1120846754",
    "entry.972941930",
    "entry.1456128915",
    "entry.248101704",
]

# Cluster 2 - Questions 6 to 10 (Page 3)
CLUSTER_2 = [
    "entry.681149660",
    "entry.1521890492",
    "entry.1560804312",
    "entry.604083069",
    "entry.167999886",
]

# Cluster 3 - Questions 11 to 15 (Page 4)
CLUSTER_3 = [
    "entry.155523541",
    "entry.643327493",
    "entry.1560644530",
    "entry.1200607050",
    "entry.162326002",
]

# Cluster 4 - Questions 16 to 20 (Page 5)
CLUSTER_4 = [
    "entry.2122543053",
    "entry.909546748",
    "entry.611065129",
    "entry.1267463292",
    "entry.1463950316",
]

# All questions combined in order
ALL_QUESTIONS = CLUSTER_1 + CLUSTER_2 + CLUSTER_3 + CLUSTER_4

def get_answer(question_number):
    if question_number == SPECIAL_QUESTION_INDEX:
        return random.choice(["Disagree", "Strongly Disagree"])
    else:
        return random.choice(["Agree", "Strongly Agree"])

def submit(i):
    payload = {
        ID_GENDER: "Male",
        ID_LEVEL: random.choices(
            ["200 Level", "300 Level"],
            weights=[80, 20]
        )[0],
        # KEY FIX: 6 sections = pages 0,1,2,3,4,5
        "pageHistory": "0,1,2,3,4,5",
    }

    # Fill all 20 questions
    for idx, q_id in enumerate(ALL_QUESTIONS):
        q_num = idx + 1
        payload[q_id] = get_answer(q_num)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://docs.google.com/forms/d/e/1FAIpQLSe_8EKN8Kt15Jl93s8Orh0JdB6bXczlly7GxPVrZsxPFlC3Vg/viewform"
    }

    try:
        r = requests.post(FORM_URL, data=payload, headers=headers, timeout=10)
        if r.status_code == 200:
            return True, payload[ID_LEVEL]
        else:
            return False, None
    except Exception as e:
        print(f"Error: {e}")
        return False, None

if __name__ == "__main__":
    print(f"🚀 Starting {TOTAL_SUBMISSIONS} submissions...")
    print(f"📋 6 Sections | Q{SPECIAL_QUESTION_INDEX} = Disagree\n")

    success_count = 0
    level_200 = 0
    level_300 = 0

    for i in range(TOTAL_SUBMISSIONS):
        success, level = submit(i)

        if success:
            success_count += 1
            if level == "200 Level":
                level_200 += 1
            else:
                level_300 += 1
            print(f"✅ {i+1}/{TOTAL_SUBMISSIONS} | Level: {level}")
        else:
            print(f"❌ {i+1}/{TOTAL_SUBMISSIONS} Failed")

        time.sleep(0.5)

    print(f"""
==========================
        SUMMARY
==========================
✅ Successful : {success_count}
❌ Failed     : {TOTAL_SUBMISSIONS - success_count}
--------------------------
🎓 200 Level  : {level_200}
🎓 300 Level  : {level_300}
==========================
    """)
