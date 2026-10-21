# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie.")

name_on_order = st.text_input("Name on the smoothie:")
cnx=st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(
    col("fruit_name"),col("Search_on")
)
#fruit_options = [row[0] for row in fruit_dataframe.collect()]
#st.dataframe(data=fruit_dataframe, use_container_width=True)

#convert the snowpark dataframe to pandas dataframe to use LOC funtion
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
     my_dataframe,
     max_selections=5,
)

if ingredients_list:
    ingredients_string=''
    
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen + ''
        
        search_on= pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'Search_on'].iloc[0]
        
        st.subheader(fruit_chosen + 'Nutrition information')
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")  
        st_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
  

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
    

