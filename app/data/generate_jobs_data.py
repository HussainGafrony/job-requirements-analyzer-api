import json
import random

# Data pools to create variety
titles = ["Backend Developer", "Frontend Developer", "Fullstack Developer", "Data Scientist", "DevOps Engineer", "QA Engineer", "Mobile Developer", "Cloud Architect", "Security Analyst"]
cities = ["Berlin", "Munich", "London", "Paris", "New York", "San Francisco", "Tokyo", "Singapore", "Amsterdam", "Sydney"]
countries = ["Germany", "UK", "France", "USA", "Japan", "Singapore", "Netherlands", "Australia"]
levels = ["Entry", "Mid", "Senior"]
skill_pool = ["Java", "Python", "React", "SQL", "Docker", "Git", "Kubernetes", "AWS", "TypeScript", "Node.js", "C++", "Go", "Swift"]

data = []

# Generate exactly 112 records
for i in range(112):
    data.append({
        "job_title": random.choice(titles),
        "city": random.choice(cities),
        "country": random.choice(countries),
        "skills": random.sample(skill_pool, 4),
        "experience_level": random.choice(levels)
    })

# This part saves the file to your computer automatically
with open('jobs_data.json', 'w') as f:
    json.dump(data, f, indent=2)
