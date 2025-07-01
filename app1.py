import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

# -----------------------------------
# Emission Factors (Per Unit)
# -----------------------------------
EMISSION_FACTORS = {
    "India": {
        "Transportation": {
            "Car": 0.21,
            "Bus": 0.1,
            "Train": 0.05
        },
        "Electricity": 0.82,  # kgCO2/kWh
        "Diet": 1.25,  # kgCO2/meal
        "Waste": 0.1  # kgCO2/kg
    }
}

# Tips for reduction
TIPS = {
    "Transportation": "Consider using public transport, carpooling, or biking more often.",
    "Electricity": "Switch to energy-efficient appliances, use solar power if possible.",
    "Diet": "Reduce red meat intake and choose more plant-based meals.",
    "Waste": "Compost organic waste and recycle non-organics properly."
}

# -----------------------------------
# UI Layout Setup
# -----------------------------------
st.set_page_config(layout="wide", page_title="Carbon Footprint Tracker")
st.title("🌍 Personal Carbon Footprint Tracker")

# -----------------------------------
# Input Section
# -----------------------------------
st.subheader("Country")
country = st.selectbox("Select your country:", list(EMISSION_FACTORS.keys()))

col1, col2 = st.columns(2)
with col1:
    st.subheader("🚗 Transportation")
    mode = st.selectbox("Mode of Transport:", list(EMISSION_FACTORS[country]["Transportation"].keys()))
    distance_km = st.slider("Daily travel distance (in km)", 0.0, 100.0)

    st.subheader("💡 Electricity")
    electricity_kwh = st.slider("Monthly usage (in kWh)", 0.0, 1000.0)

with col2:
    st.subheader("🗑️ Waste")
    waste_kg = st.slider("Weekly waste generation (in kg)", 0.0, 100.0)

    st.subheader("🍽️ Diet")
    meals_per_day = st.number_input("Number of meals per day", min_value=0, max_value=10, value=3)

# -----------------------------------
# Normalize Inputs to Yearly
# -----------------------------------
distance_km *= 365
meals_per_day *= 365
waste_kg *= 52

# -----------------------------------
# Calculate Emissions (kg/year)
# -----------------------------------
transport_emission = distance_km * EMISSION_FACTORS[country]["Transportation"][mode]
electricity_emission = electricity_kwh * 12 * EMISSION_FACTORS[country]["Electricity"]
diet_emission = meals_per_day * EMISSION_FACTORS[country]["Diet"]
waste_emission = waste_kg * EMISSION_FACTORS[country]["Waste"]

# Convert to tonnes
transport_emission = round(transport_emission / 1000, 2)
electricity_emission = round(electricity_emission / 1000, 2)
diet_emission = round(diet_emission / 1000, 2)
waste_emission = round(waste_emission / 1000, 2)
total_emission = round(transport_emission + electricity_emission + diet_emission + waste_emission, 2)

# -----------------------------------
# Show Results
# -----------------------------------
if st.button("🔍 Calculate My Footprint"):
    st.header("📊 Results")
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("By Category (tonnes CO2/year)")
        st.info(f"🚗 Transportation: {transport_emission}")
        st.info(f"💡 Electricity: {electricity_emission}")
        st.info(f"🍽️ Diet: {diet_emission}")
        st.info(f"🗑️ Waste: {waste_emission}")

    with col4:
        st.subheader("🌍 Total Footprint")
        st.success(f"Your total annual footprint: {total_emission} tonnes CO2")
        st.warning("India's per capita CO2 emissions (2021): 1.9 tonnes")

        # Tip based on highest contributor
        max_cat = max([
            ("Transportation", transport_emission),
            ("Electricity", electricity_emission),
            ("Diet", diet_emission),
            ("Waste", waste_emission)
        ], key=lambda x: x[1])[0]

        st.info(f"💡 Tip to reduce your impact: {TIPS[max_cat]}")

# -----------------------------------
# Visualization
# -----------------------------------
if st.button("📈 Show Emission Breakdown"):
    categories = ['Transportation', 'Electricity', 'Diet', 'Waste']
    values = [transport_emission, electricity_emission, diet_emission, waste_emission]
    df = pd.DataFrame({'Category': categories, 'Emissions': values})

    pie_fig, pie_ax = plt.subplots()
    pie_ax.pie(values, labels=categories, autopct='%1.1f%%', startangle=90)
    pie_ax.axis('equal')
    st.pyplot(pie_fig)

    bar_chart = alt.Chart(df).mark_bar().encode(
        x='Category', y='Emissions', color='Category'
    ).properties(title='Carbon Emission by Category', width=500)
    st.altair_chart(bar_chart)

# -----------------------------------
# Session History
# -----------------------------------
if "history" not in st.session_state:
    st.session_state["history"] = []

if st.button("💾 Save This Result"):
    st.session_state["history"].append({
        "Transportation": transport_emission,
        "Electricity": electricity_emission,
        "Diet": diet_emission,
        "Waste": waste_emission,
        "Total": total_emission
    })
    st.success("Result saved to session history!")

if st.button("📚 Show History"):
    if st.session_state["history"]:
        st.dataframe(pd.DataFrame(st.session_state["history"]))
    else:
        st.info("No history available yet.")
