import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="Client Website Requirement Form", layout="centered")

# ---- SESSION STATE INITIALIZATION ----
if "services" not in st.session_state:
    st.session_state.services = [{"name": "", "description": ""}]

# ---- FUNCTIONS ----
def add_service():
    st.session_state.services.append({"name": "", "description": ""})

def remove_service(index):
    if len(st.session_state.services) > 1:
        st.session_state.services.pop(index)

# ---- TITLE ----
st.title("🖥️ Client Website Requirement Form")
st.write("Please fill out the details below to help us design your website.")

with st.form("website_form", clear_on_submit=False):
    # --- Basic Info ---
    st.subheader("Basic Information")
    name = st.text_input("Full Name", placeholder="Enter your name")
    company = st.text_input("Company / Brand Name", placeholder="Enter company name")
    email = st.text_input("Email Address")
    contact = st.text_input("Contact Number")

    # --- Pages Required ---
    st.subheader("Website Pages Required")
    pages = st.multiselect(
        "Select the pages you want on your website:",
        [
            "Home / Landing Page", "About Us", "Services", "Contact Us",
            "Products / Shop Page", "Gallery / Portfolio", "Blog / News",
            "Testimonials", "FAQ Page", "Careers / Job Openings"
        ],
    )
    custom_page = st.text_input("Custom Page (if any)")

    # --- Services Section ---
    st.subheader("Services Required")
    for i, service in enumerate(st.session_state.services):
        col1, col2, col3 = st.columns([3, 5, 1])
        with col1:
            st.session_state.services[i]["name"] = st.text_input(
                f"Service Name {i+1}", value=service["name"], key=f"service_name_{i}"
            )
        with col2:
            st.session_state.services[i]["description"] = st.text_area(
                f"Description {i+1}", value=service["description"], key=f"service_desc_{i}"
            )
        with col3:
            if st.form_submit_button(f"🗑️ Delete {i+1}", use_container_width=True):
                remove_service(i)

    # Button to add a service
    if st.form_submit_button("➕ Add Service"):
        add_service()

    # --- Additional Info ---
    st.subheader("Additional Information")
    color_theme = st.text_input("Preferred Color Theme / Branding Guidelines")
    inspiration = st.text_area("Any Websites You Like for Inspiration")
    notes = st.text_area("Additional Notes or Requirements")

    # --- Submit ---
    submitted = st.form_submit_button("✅ Submit Form")

if submitted:
    data = {
        "name": name,
        "company": company,
        "email": email,
        "contact": contact,
        "pages": pages,
        "custom_page": custom_page,
        "services": st.session_state.services,
        "color_theme": color_theme,
        "inspiration": inspiration,
        "notes": notes,
        "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Save to JSON
    filename = f"client_website_requirements_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    st.success(f"Form submitted successfully! Data saved to {filename}")

    # Show in Expander
    with st.expander("📂 View Submitted Data"):
        st.json(data)
