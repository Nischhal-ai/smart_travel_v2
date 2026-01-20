import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import math
import re
import random

# ===============================
# LOAD DATA
# ===============================
df = pd.read_csv("dataset/merged_travel_data.csv")

df["destination"] = df["destination"].str.strip().str.lower()
df["features"] = df["features"].str.lower()

hotels = df[df["product_type"] == "hotels"]
flights = df[df["product_type"] == "flight"]
activities = df[df["product_type"] == "activity"]

# ===============================
# ACTIVITY TAGGING
# ===============================
activity_tags = {
    "scuba": "adventure",
    "paragliding": "adventure",
    "trek": "adventure",
    "water": "adventure",
    "beach": "leisure",
    "garden": "leisure",
    "park": "leisure",
    "cruise": "leisure",
    "market": "leisure",
    "temple": "cultural",
    "heritage": "cultural",
    "fort": "cultural",
    "museum": "cultural",
    "ganga": "cultural",
    "church": "cultural"
}

def get_activity_type(text):
    for key, tag in activity_tags.items():
        if key in text:
            return tag
    return "leisure"

activities = activities.copy()
activities["activity_type"] = activities["features"].apply(get_activity_type)

# ===============================
# TRAVELLER PREFERENCE MAP
# ===============================
preference_map = {
    "children": ["leisure"],
    "young": ["adventure", "leisure"],
    "senior": ["cultural", "leisure"],
    "mixed": ["leisure", "cultural"]
}

# ===============================
# NLP PARSER (BUDGET OPTIONAL)
# ===============================
def parse_user_input(text):
    text = text.lower()

    days = int(re.search(r"(\d+)\s*day", text).group(1))
    persons = int(re.search(r"(\d+)\s*(person|people)", text).group(1))
    city = re.search(r"to\s+([a-z\s]+)", text).group(1).strip().split()[0]

    numbers = re.findall(r"\d+", text)
    budget = int(numbers[-1]) if len(numbers) > 2 else None

    return days, persons, city, budget

# ===============================
# HOTEL RATING EXTRACTOR
# ===============================
def extract_rating(text):
    match = re.search(r"(\d\.\d)/5", text)
    return float(match.group(1)) if match else 0.0

# ===============================
# UNIQUE ACTIVITY SELECTION
# ===============================
def select_unique_activities(activity_df, days):
    unique = activity_df.drop_duplicates("features")

    if len(unique) < days:
        days = len(unique)

    selected = unique.sample(days)
    return list(selected["features"]), selected["price"].sum()

# ===============================
# CORE RECOMMENDER (SMART RANKING)
# ===============================
def recommend_trip(text, traveller_type):
    days, persons, city, budget = parse_user_input(text)
    rooms = math.ceil(persons / 2)

    plans = []

    hotel_options = hotels[hotels["destination"] == city]
    flight_options = flights[flights["destination"] == city]
    activity_options = activities[
        (activities["destination"] == city)
        & (activities["activity_type"].isin(preference_map[traveller_type]))
    ]

    if hotel_options.empty or activity_options.empty:
        return []

    for _, hotel in hotel_options.iterrows():

        hotel_cost = hotel["price"] * days * rooms
        rating = extract_rating(hotel["features"])

        # -------- Transport --------
        if not flight_options.empty:
            flight = flight_options.sample(1).iloc[0]
            transport = flight["features"]
            transport_cost = flight["price"] * persons
        else:
            transport = "Local / Self Travel"
            transport_cost = 0

        # -------- Activities --------
        acts, act_cost = select_unique_activities(activity_options, days)
        activity_cost = act_cost * persons

        total_cost = hotel_cost + transport_cost + activity_cost

        # -------- Scoring Logic --------
        if budget is not None:
            if total_cost > budget:
                continue
            score = 1 - abs(budget - total_cost) / budget
            reason = "Closest match to your budget with preferred activities"
        else:
            score = rating
            reason = "Top-rated hotel with suitable activities"

        plans.append({
            "Hotel": hotel["features"],
            "Transport": transport,
            "Activities": acts,
            "Total Cost": round(total_cost, 2),
            "Score": round(score, 4),
            "Rating": rating,
            "Reason": reason
        })

    # -------- Final Ranking --------
    plans = sorted(plans, key=lambda x: x["Score"], reverse=True)

    return plans[:3]
