import streamlit as st
import pickle
import numpy as np
import re

import base64
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )



with open('clustered_orders.p', 'rb') as file:
    clustered_orders = pickle.load(file)

with open('group_association_rules_dic.p', 'rb') as file:
    group_association_rules_dic = pickle.load(file)

with open('unique_products.p', 'rb') as file:
    unique_products = pickle.load(file)



def recommend(prod_name):
    prods=[]
    list_cluster = clustered_orders.loc[clustered_orders['product_name'] == prod_name, 'cluster'].unique()
    for i in list_cluster:
        if i <= 8:
            x = group_association_rules_dic[i]
            x = x[x["product_name_A"] == prod_name]
            if not x.empty:
                x= x.sort_values('lift', ascending = False)
                for j in range(0,min(3,len(x))):
                    if x.iloc[j]['product_name_B']:
                        prods.append(x.iloc[j]['product_name_B'])
    return prods



def show_predict_page():
    st.title("Grocery Recommendation System")
    st.write("""### We need some information to recommend similar products""")

    st.experimental_set_query_params(search='')
    query_params = st.experimental_get_query_params()
    search_query = query_params.get("search", "")
    search_query = st.text_input("Search", search_query)
    st.experimental_set_query_params(search=search_query)
    if search_query:
        regex = re.compile(f".*{search_query}.*", re.IGNORECASE)
        if regex:
            matches = [item for item in unique_products if regex.match(item)]
            if matches:
                selected_match = st.selectbox("Select an option", matches)
            else:
                selected_match = None
                st.write("No matches found.")	
        else:
            selected_match = None
            st.write("Invalid search query.")
    else:
        selected_match = None
	
    if selected_match in unique_products:
        item = selected_match
        ok = st.button("Add to cart")

        if ok:
            prods=recommend(item) 
            if prods:
                for i in prods:
                    st.subheader(i)
            else:
                st.write("Item added to cart!")
                st.write("Here are top products from our store")
                prods = ['Banana', 'Bag of Organic Bananas', 'Organic Strawberries', 'Organic Baby Spinach', 'Organic Hass Avocado']
                for i in prods:
                    st.subheader(i)

