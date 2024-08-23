import streamlit as st
import stripe
import stripe


def make_charge(amount_pounds):
    try:
        # Create a charge
        charge = stripe.Charge.create(
            amount=int(amount_pounds * 100),  # Convert pounds to pence
            currency='gbp',
            source='tok_visa',  # Replace with a valid payment source token from your front-end
            description=f'Charge for {amount_pounds} pounds',
        )
        return f"Charge successful: {charge['id']}"

    except stripe.error.CardError as e:
        body = e.json_body
        err = body.get('error', {})
        return f"Card error: {err.get('message')}"

    except stripe.error.RateLimitError:
        return "Rate limit error"

    except stripe.error.InvalidRequestError:
        return "Invalid request error"

    except stripe.error.AuthenticationError:
        return "Authentication error"

    except stripe.error.APIConnectionError:
        return "Network error"

    except stripe.error.StripeError:
        return "Stripe error"

    except Exception as e:
        return f"An error occurred: {str(e)}"
    
drug_doses = {
    "Quick search": {"concentrations": [None], "min_dose": None, "max_dose": None},
    "Butorphanol": {"concentrations": [10], "min_dose": 0.1, "max_dose": 0.4},
    "Metaclopramide": {"concentrations": [5], "min_dose": 0.01, "max_dose": 0.09},
}

# Remove + - buttons from number input
st.markdown(
    """
<style>
    button.step-up {display: none;}
    button.step-down {display: none;}
    div[data-baseweb] {border-radius: 4px;}
</style>""",
    unsafe_allow_html=True,
)


st.title("Vet Calc :dog:")

st.link_button('Go premium', 'https://buy.stripe.com/test_28og328IL9fm4lG7ss')


st.selectbox("Select formula", ["CRI", "test2", "test3"])

if "weight" not in st.session_state:
    st.session_state.weight = None

if "fluid_volume" not in st.session_state:
    st.session_state.fluid_volume = None

if "fluid_rate" not in st.session_state:
    st.session_state.fluid_rate = None

if "concentration" not in st.session_state:
    st.session_state.concentration = None

if "dose" not in st.session_state:
    st.session_state.dose = None


weight = st.number_input(
    "Enter weight",
    value=st.session_state.weight,
    key="weight",
)

col1, col2 = st.columns(2)
with col1:
    fluid_volume = st.number_input(
        "CRI fluid volume",
        value=st.session_state.fluid_volume,
        key="fluid_volume",
    )

with col2:
    fluid_rate = st.number_input(
        "CRI fluid rate",
        value=st.session_state.fluid_rate,
        key="fluid_rate",
    )




used_drug = st.selectbox(
    "Drug",
    drug_doses.keys(),
    # index=st.session_state.used_drug, #TODO: fix this
    key="used_drug",
)

concentration = st.number_input(
    "Concentration",
    value=drug_doses[used_drug]["concentrations"][0],
    key="concentration",
)

dose_tag = (
    f"Dose ({drug_doses[used_drug]['min_dose']} - {drug_doses[used_drug]['max_dose']} mg/kg/hr)"
    if drug_doses[used_drug]["min_dose"]
    else "Dose"
)
dose = st.number_input(dose_tag, value=None, key="dose")

col1, col2 = st.columns(2)
with col1:
    calculate = st.button("Calculate")
with col2:
    st.button("Refresh")

if calculate:
    if weight and fluid_rate and fluid_volume:
        duration = fluid_volume / (fluid_rate * weight)

        total_dose = dose * weight

        total_dose_duration = total_dose * duration

        total_volume = total_dose_duration / concentration

        st.write(f"Total volume {total_volume} ml")

    else:
        st.write("Not enoguh data")
        st.stop()
