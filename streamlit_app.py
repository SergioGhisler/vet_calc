import streamlit as st

st.title("Vet Calc :dog:")

st.selectbox("Select formula", ["CRI", "test2", "test3"])


weight = st.number_input("Enter weight")

fluid_volume = st.number_input("CRI fluid volume")

fluid_rate = st.number_input("CRI fluid rate")

used_drug = st.selectbox(
    "Drug",
    [
        "Butorphanol",
        "Metaclopramide",
    ],
)

drug_doses = {
    "Butorphanol": {"concentrations": [10], "min_dose": 0.1, "max_dose": 0.4},
    "Metaclopramide": {"concentrations": [5], "min_dose": 0.01, "max_dose": 0.09},
}

concentration = drug_doses[used_drug]["concentrations"][0]
st.write(f"Drug concentration {concentration} mg/ml")

dose = st.number_input(
    "Dose",
    min_value=drug_doses[used_drug]["min_dose"],
    max_value=drug_doses[used_drug]["max_dose"],
)
if weight !=0 and fluid_rate != 0 and fluid_volume != 0:
    duration = fluid_volume / (fluid_rate * weight)

    total_dose = dose * weight

    total_dose_duration = total_dose * duration

    total_volume = total_dose_duration / concentration

    st.write(f"Total volume {total_volume} ml")
