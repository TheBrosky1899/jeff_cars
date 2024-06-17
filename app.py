import streamlit as st
import hmac
import os
import json
from car_type import Car

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

def render_car(car: Car):
    st.write(car.name)

def main():
    if not check_password():
        st.stop() 
    st.title("Brosky's Garage")
    
    car_list = [pos_json for pos_json in os.listdir("cars") if pos_json.endswith('.json')]
    cars : list[Car] = []
    
    for item in car_list:
        f = open(f"cars/{item}", 'r')
        data = json.load(f)
        
        cars.append(Car(**data))
    
    picked_car_name = st.selectbox("Pick your ride", options=sorted([c.name for c in cars]))
    
    picked_car = [c for c in cars if c.name == picked_car_name][0]
    
    render_car(car=picked_car)

if __name__ == "__main__":
    main()