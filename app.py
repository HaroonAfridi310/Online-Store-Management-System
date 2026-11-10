import streamlit as st
from database import get_all_products

st.title("Online store Software")
st.subheader("Available Products")

products = get_all_products()
for product in products:
    st.write(f"**ID:** {product[0]}")
    st.write(f"**Name:** {product[1]}")
    st.write(f"**Category:** {product[2]}")
    st.write(f"**Price:** ${product[3]}")
    st.write(f"**Stock:** {product[4]}")
    st.markdown("---")
