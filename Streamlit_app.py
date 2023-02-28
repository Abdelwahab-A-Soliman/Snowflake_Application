import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError
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

def get_fruityvice_data (this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_table = pd.json_normalize(fruityvice_response.json())
    return fruityvice_table


# Adding Text input 
try: 
  fruit_choice = streamlit.text_input('What fruit would you like information about')
  if not fruit_choice:
    streamlit.error('Please Select a fruit to get information')
  else: 
    fruity_vice_output = get_fruityvice_data (fruit_choice)
    streamlit.dataframe(fruity_vice_output)

except URLError as e :
  streamlit.error()
  


#streamlit.stop()

# Adding fruit to the list in Snowflake
streamlit.header("The Fruit List Contains : ")
#Opening Snowflake connection function
def get_fruit_list_load() :
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * From FRUIT_LOAD_LIST")
        return  my_cur.fetchall()

# Adding a button to show the fruit list
if streamlit.button('Get Fruit Load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_list_load()
    streamlit.dataframe(my_data_rows)


# Adding Fruit to Snowflake list as an input 
add_my_fruit = streamlit.text_input('What fruit would you like to add')
my_cur.execute("insert into FRUIT_LOAD_LIST values ('from stream_lit')")
streamlit.write("Thank you for adding the Fruit: ",add_my_fruit)
