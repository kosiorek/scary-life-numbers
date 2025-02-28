import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Life Expectancy Data (Expanded and Gender-Specific)
avg_life_expectancy = {
    "USA": {"Male": 74, "Female": 80}, "UK": {"Male": 79, "Female": 83}, "Germany": {"Male": 78, "Female": 83}, 
    "Spain": {"Male": 80, "Female": 86}, "Poland": {"Male": 74, "Female": 81}, "France": {"Male": 79, "Female": 85},
    "Japan": {"Male": 81, "Female": 87}, "India": {"Male": 69, "Female": 72}, "China": {"Male": 75, "Female": 78}, 
    "Brazil": {"Male": 72, "Female": 79}, "Canada": {"Male": 80, "Female": 84}, "Australia": {"Male": 81, "Female": 85}, 
    "Italy": {"Male": 79, "Female": 84}, "Netherlands": {"Male": 80, "Female": 84}, "Sweden": {"Male": 81, "Female": 85},
    "Norway": {"Male": 81, "Female": 85}, "Denmark": {"Male": 79, "Female": 83}, "Mexico": {"Male": 71, "Female": 77}
}

def calculate_time_left(age, country, gender):
    life_expectancy = avg_life_expectancy.get(country, {"Male": 80, "Female": 85})[gender]  # Default values if country not listed
    years_left = max(life_expectancy - age, 0)
    years_passed = age
    percent_lived = (years_passed / life_expectancy) * 100
    percent_left = 100 - percent_lived
    return years_left, years_passed, percent_lived, percent_left

def calculate_metrics(age, country, gender, work_hours, sleep_hours, parent_age, visits_per_year, kid_age, social_media_hours, tv_hours, exercise_hours, commute_hours):
    years_left, years_passed, percent_lived, percent_left = calculate_time_left(age, country, gender)
    
    # Basic Life Events
    summers_left = years_left
    christmas_left = years_left
    
    # Family Time
    parent_years_left, _, _, _ = calculate_time_left(parent_age, country, gender)
    visits_with_parents = parent_years_left * visits_per_year
    
    # Work & Sleep
    work_years = min(65 - age, years_left)
    work_hours_left = work_years * work_hours * 50  # Assuming 50 work weeks per year
    sleep_years = (sleep_hours / 24) * years_left
    
    # Leisure and Screen Time
    social_media_years = (social_media_hours / 24) * years_left
    tv_years = (tv_hours / 24) * years_left
    exercise_years = (exercise_hours / 24) * years_left
    commute_years = (commute_hours / 24) * years_left
    
    return {
        "Years Passed": years_passed,
        "Years Left": years_left,
        "Percent Life Lived": percent_lived,
        "Percent Life Left": percent_left,
        "Summers Left": summers_left,
        "Christmases Left": christmas_left,
        "Visits with Parents": visits_with_parents,
        "Total Work Hours Left": work_hours_left,
        "Total Sleep Years": sleep_years,
        "Total Social Media Years": social_media_years,
        "Total TV Years": tv_years,
        "Total Exercise Years": exercise_years,
        "Total Commute Years": commute_years
    }

def main():
    st.set_page_config(page_title="Scary Life Numbers", page_icon="⏳", layout="wide")
    st.title("Scary Life Numbers Calculator")
    
    menu = ["Input Data", "Results & Visuals"]
    choice = st.sidebar.selectbox("Navigation", menu)
    
    if choice == "Input Data":
        st.subheader("Enter Your Information")
        age = st.slider("Your Age", 18, 100, 30)
        country = st.selectbox("Your Country", list(avg_life_expectancy.keys()))
        gender = st.radio("Your Gender", ["Male", "Female"])
        work_hours = st.slider("Hours Worked per Week", 0, 80, 40)
        sleep_hours = st.slider("Hours Slept per Night", 4, 12, 8)
        parent_age = st.slider("Parent's Age", 40, 100, 65)
        visits_per_year = st.slider("Visits to Parents per Year", 0, 52, 5)
        kid_age = st.slider("Kid’s Age (if any, else leave at 0)", 0, 30, 0)
        social_media_hours = st.slider("Hours on Social Media per Day", 0, 12, 2)
        tv_hours = st.slider("Hours Watching TV/Netflix per Day", 0, 12, 2)
        exercise_hours = st.slider("Hours Exercising per Week", 0, 20, 3)
        commute_hours = st.slider("Hours Commuting per Day", 0, 4, 1)
        
        if st.button("Calculate My Life Stats"):
            st.session_state['user_data'] = (age, country, gender, work_hours, sleep_hours, parent_age, visits_per_year, kid_age, social_media_hours, tv_hours, exercise_hours, commute_hours)
            st.experimental_rerun()
    
    elif choice == "Results & Visuals":
        if 'user_data' in st.session_state:
            age, country, gender, work_hours, sleep_hours, parent_age, visits_per_year, kid_age, social_media_hours, tv_hours, exercise_hours, commute_hours = st.session_state['user_data']
            results = calculate_metrics(age, country, gender, work_hours, sleep_hours, parent_age, visits_per_year, kid_age, social_media_hours, tv_hours, exercise_hours, commute_hours)
            
            st.subheader("Your Life Overview")
            fig, ax = plt.subplots()
            ax.pie([results['Percent Life Lived'], results['Percent Life Left']], labels=["Life Lived", "Life Left"], autopct='%1.1f%%')
            st.pyplot(fig)
            
            st.bar_chart({"Category": list(results.keys()), "Years": list(results.values())})
            
            st.write("Want to edit your data? Go back to the Input Data page!")
        else:
            st.warning("Please enter your data first on the Input Data page!")

if __name__ == "__main__":
    main()
