import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Life Expectancy Data (Simplified Example)
avg_life_expectancy = {
    "USA": 77, "UK": 81, "Germany": 80, "Spain": 83, "Poland": 78, "France": 82,
    "Japan": 84, "India": 70, "China": 76, "Brazil": 75
}

def calculate_time_left(age, country):
    life_expectancy = avg_life_expectancy.get(country, 80)  # Default to 80 if country not listed
    years_left = max(life_expectancy - age, 0)
    return years_left

def calculate_metrics(age, country, work_hours, sleep_hours, parent_age, visits_per_year, kid_age):
    years_left = calculate_time_left(age, country)
    
    # Basic Life Events
    summers_left = years_left
    christmas_left = years_left
    
    # Family Time
    parent_years_left = calculate_time_left(parent_age, country)
    visits_with_parents = parent_years_left * visits_per_year
    
    # Work & Sleep
    work_years = min(65 - age, years_left)
    work_hours_left = work_years * work_hours * 50  # Assuming 50 work weeks per year
    sleep_years = (sleep_hours / 24) * years_left
    
    return {
        "Years Left": years_left,
        "Summers Left": summers_left,
        "Christmases Left": christmas_left,
        "Visits with Parents": visits_with_parents,
        "Total Work Hours Left": work_hours_left,
        "Total Sleep Years": sleep_years
    }

def main():
    st.title("Scary Life Numbers Calculator")
    
    # User Inputs
    age = st.slider("Your Age", 18, 100, 30)
    country = st.selectbox("Your Country", list(avg_life_expectancy.keys()))
    work_hours = st.slider("Hours Worked per Week", 0, 80, 40)
    sleep_hours = st.slider("Hours Slept per Night", 4, 12, 8)
    parent_age = st.slider("Parent's Age", 40, 100, 65)
    visits_per_year = st.slider("Visits to Parents per Year", 0, 52, 5)
    kid_age = st.slider("Kid’s Age (if any, else leave at 0)", 0, 30, 0)
    
    # Calculate Metrics
    results = calculate_metrics(age, country, work_hours, sleep_hours, parent_age, visits_per_year, kid_age)
    
    # Display Results
    st.subheader("Your Life Overview")
    for key, value in results.items():
        st.write(f"**{key}:** {value}")
    
    # Pie Chart Visualization
    labels = ["Work", "Sleep", "Other Time"]
    sizes = [results['Total Work Hours Left'] / (years_left * 365 * 24),
             results['Total Sleep Years'] / years_left,
             1 - (results['Total Work Hours Left'] / (years_left * 365 * 24)) - (results['Total Sleep Years'] / years_left)]
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    st.pyplot(fig)

if __name__ == "__main__":
    main()
