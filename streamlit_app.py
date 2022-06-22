import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 and Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach and Rocket Smoothie')
streamlit.text('🥑🍞Hard-Boiled Free-Range Egg')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
streamlit.dataframe(my_fruit_list)

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#Display the table on page
streamlit.dataframe(fruits_to_show)

#New Section to display fruityvice api response
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    # just writes the data to the screen
    # streamlit.text(fruityvice_response.json())

    # Take the json version of the response and normalise it
    fruityvice_normalise = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalise

try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)

except URLError as e:
    streamlit.error()

#connecting to snowflake via the credentials entered in streamlit

streamlit.header("The fruit load list contains: ")
#Snowflake-related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()
# Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_data_row = my_cur.fetchone()
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

#New Section to display fruityvice api response

fruit_add = streamlit.text_input('What fruit would you like to add?')
streamlit.write('Thanks for adding', fruit_add)

#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +fruit_choice)