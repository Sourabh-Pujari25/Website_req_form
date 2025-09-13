import streamlit as st
import os
import json
from datetime import date

# Ensure images folder exists
if not os.path.exists("images"):
    os.makedirs("images")

st.title("Client Website Requirements Form")

# Form
with st.form("client_form", clear_on_submit=True):
    name = st.text_input("What is your name?")
    email = st.text_input("Email")
    phone = st.text_input("Phone")

    business_name = st.text_input("Business Name")
    business_desc = st.text_area("What does your business do?")
    num_products = st.number_input("How many products do you have?", min_value=0, step=1)

    ref_websites = st.text_area("Do you have any reference websites? (paste links)")
    domain = st.text_input("Do you already have a domain? If yes, type it below")

    deadline = st.date_input("Do you have a deadline for the website launch?", min_value=date.today())
    budget = st.text_input("What is your estimated budget range?")

    logo = st.file_uploader("Upload your business logo", type=["png", "jpg", "jpeg"])

    submitted = st.form_submit_button("Submit")

if submitted:
    try:
        if not name or not email or not phone:
            st.error("Name, Email, and Phone are required fields.")
        else:
            # Save data to JSON
            client_data = {
                "name": name,
                "email": email,
                "phone": phone,
                "business_name": business_name,
                "business_desc": business_desc,
                "num_products": int(num_products),
                "ref_websites": ref_websites,
                "domain": domain,
                "deadline": str(deadline),
                "budget": budget,
                "logo_file": logo.name if logo else None
            }

            # Save JSON
            json_filename = f"{name.replace(' ', '_')}_data.json"
            with open(json_filename, "w") as f:
                json.dump(client_data, f, indent=4)

            # Save logo image
            image_path = None
            if logo:
                image_path = os.path.join("images", logo.name)
                with open(image_path, "wb") as f:
                    f.write(logo.getbuffer())

            st.success("Form submitted successfully!")

            # Show data in expander
            with st.expander("Submitted Data"):
                st.json(client_data)
                if image_path:
                    st.image(image_path, caption="Uploaded Business Logo", use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
