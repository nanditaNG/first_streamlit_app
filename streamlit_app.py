import streamlit
import pandas
import requests

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

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +fruit_choice)
#just writes the data to the screen
#streamlit.text(fruityvice_response.json())

#Take the json version of the response and normalise it

fruityvice_normalise = pandas.json_normalize(fruityvice_response.json())
#Output it to the screen as a table

streamlit.title('Fruityvice Fruit advice!')
streamlit.dataframe(fruityvice_normalise)