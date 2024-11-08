import streamlit as st
st.title("This is a Tutorial for StreamLit App Building")
container = st.container()
container.write("This is in a container.")


name = st.text_input("Enter your name:")


if st.button("Click me"):
    st.write("Button clicked!")

model_choice = st.selectbox("Choose a model:", ["Model A", "Model B", "Model C"])
st.write(f"You selected: {model_choice}")


age = st.slider("Select your age:", 0, 100)
st.write(f"Age selected: {age}")


agree = st.checkbox("I agree")
if agree:
    st.write("You agreed!")


st.text("This is plain text")
st.markdown("### This is Markdown")
st.code("print('Hello, World!')", language="python")

import pandas as pd
import numpy as np

# Sample data
df = pd.DataFrame(np.random.randn(10, 5), columns=["A", "B", "C", "D", "E"])
st.dataframe(df)
st.table(df.head())


from PIL import Image
img = Image.open("DALL·E 2024-10-30 14.54.58 - Create an image of the YouTube logo, centered and large, with vibrant red and white colors on a clean background, giving it a high-resolution and bold.webp")
st.image(img, caption="Sample Image")

st.line_chart(df)
st.bar_chart(df["A"])


import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.hist(df["A"], bins=15)
st.pyplot(fig)


st.header("Simple Calculator")

num1 = st.number_input("Enter first number", value=0)
num2 = st.number_input("Enter second number", value=0)
operation = st.selectbox("Operation", ["Add", "Subtract", "Multiply", "Divide"])

if st.button("Calculate"):
    if operation == "Add":
        result = num1 + num2
    elif operation == "Subtract":
        result = num1 - num2
    elif operation == "Multiply":
        result = num1 * num2
    elif operation == "Divide":
        result = num1 / num2 if num2 != 0 else "Undefined"
    
    st.write(f"Result: {result}")
