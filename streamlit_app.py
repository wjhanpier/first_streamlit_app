import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title ('My Parentss new - ')
streamlit.header('Menú de desayuno')
streamlit.text('🥣 Omega 3 y avena con arándanos')
streamlit.text('🥗 Batido de col rizada, espinacas y rúcula')
streamlit.text('🐔 Huevo de gallinas camperas hervidas')
streamlit.text('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

# Display the table on the page.
streamlit.dataframe(my_fruit_list)

fruits_selected = streamlit.multiselect("Pick some fruits:", list (my_fruit_list.index), ['Avocado','Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

#
def get_fruityvice_data(this_fruit_choise):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choise)
   fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
   return fruityvice_normalized
#
streamlit.header('Fruityvice Fruit Advice!')
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruit_choice: 
         streamlit.error("Please select a fruit to get information.")
   else:
         back_from_function = get_fruityvice_data(fruit_choice)
         streamlit.dataframe(back_from_function)
 
except URLError as e:
    streamlit.error()
  
streamlit.text(fruityvice_response.json())

# write your own comment -what does the next line do? 
# write your own comment - what does this do?
streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select *from PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
my_data_rows = my_cur.fetchall()
streamlit.header("the fruits load list contains:")
streamlit.dataframe(my_data_rows)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")
