# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie.")

name_on_order = st.text_input("Name on the smoothie:")
cnx=st.connection("snowflake")
session = cnx.session()

fruit_dataframe = session.table("smoothies.public.fruit_options").select(
    col("fruit_name")
)
fruit_options = [row[0] for row in fruit_dataframe.collect()]
st.dataframe(data=fruit_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    options=fruit_options,
    max_selections=5,
)

if st.button("Submit order"):
    if not name_on_order.strip():
        st.error("Enter a name for the order.")
    elif not ingredients_list:
        st.error("Choose at least one ingredient.")
    else:
        ingredients_string = ", ".join(ingredients_list)
        session.sql(
            "INSERT INTO smoothies.public.orders (ingredients, name_on_order) "
            "VALUES (?, ?)",
            params=[ingredients_string, name_on_order.strip()],
        ).collect()
        st.success("Your smoothie is ordered!", icon="✅")

import requests  
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
#st.text(smoothiefroot_response.json())
st_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
