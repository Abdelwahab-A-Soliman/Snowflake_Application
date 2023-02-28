import streamlit
import pandas as pd
import snowflake.connector

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#change index to fruit
my_fruit_list = my_fruit_list.set_index("Fruit")

streamlit.title("My Mom's New Healthy Dinner")
streamlit.header("Breakfast Favorites")
streamlit.text(" 🥣 Omega 3 & Blueberry Oatmeal")
streamlit.text(" 🥗 Kale, Spinach & Rocket Smoothie")
streamlit.text(" 🐔 Hard-Boiled Free-range Egg")
streamlit.text(" 🥑🍞 Avocado Toast")


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
# Pick up list for fruits (Take indices of the fruits selected)
# ['Avocado" , ...] list is as  default
fruits_selected = streamlit.multiselect("Pick some fruits: ", list(my_fruit_list.index) ,["Avocado","Strawberries"] )
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

#Adding FRUITYVICE API

# FRUITYVICE ADVICE HEADER 
streamlit.header("Fruityvice Fruit Advice!")
import requests
# Adding Text input 
fruit_choice = streamlit.text_input('What fruit would you like information about', 'Kiwi')
streamlit.write('The user entered ', fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
fruityvice_table = pd.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_table)
