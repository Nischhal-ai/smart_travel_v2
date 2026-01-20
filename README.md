# Smart Travel Planner

Smart Travel Planner is a travel recommendation system that converts natural language trip requests into personalized travel plans.
Users can describe their trip in plain text (days, people, destination, budget, traveller type), and the system generates optimized travel plans including hotels, transport, and day-wise activities.
The planner works even when the budget is not provided by prioritizing the highest-rated options.

# What This Project Does

- Parses human-like trip requests
- Recommends complete travel plans
- Generates day-wise unique activities
- Adjusts recommendations based on traveller type
- Optimizes plans closest to the given budget
- Falls back to quality and ratings when budget is missing

# Key Features

- Natural language input support
- Budget-aware ranking
- Rating-based ranking without budget
- Day-wise activity planning
- Traveller preference filtering (children, young, senior, mixed)
- CSV-based offline dataset
- FastAPI backend

# Purpose

This project demonstrates how intelligent travel discovery can be built without form-based inputs by combining NLP-style parsing, recommendation logic, and backend APIs.
