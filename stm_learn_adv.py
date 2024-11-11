import streamlit as st
import streamlit.components.v1 as components

def custom_date_picker(label):
    components.html(
        f"""
        <input type="date" id="myDate" />
        <script>
        document.getElementById('myDate').addEventListener('change', (e) => {{
            window.parent.postMessage({{type: 'date', date: e.target.value}}, '*');
        }});
        </script>
        """,
        height=100,
    )


@st.cache_data
def load_data():
    # Simulate a time-consuming operation
    import time
    time.sleep(2)
    return {"data": [1, 2, 3, 4, 5]}

tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])
with tab1:
    st.write("Content for Tab 1")
    data = load_data()
    st.write("Data:", data)
with tab2:
    st.write("Content for Tab 2")
    if "user_data" not in st.session_state:
        st.session_state.user_data = {"name": "", "age": ""}

        # Update user data based on input
        st.session_state.user_data["name"] = st.text_input("Name:", st.session_state.user_data["name"])
        st.session_state.user_data["age"] = st.text_input("Age:", value=st.session_state.user_data["age"])
        st.write("User Data:", st.session_state.user_data)

with tab3:
    st.write("Content for Tab 3")

# Create a sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose a page:", ["Home", "Data", "Settings", "Custom"])

# Custom column layout for main page content
if page == "Home":
    st.title("Home Page")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("yt.png", caption="Sample Image", use_container_width=True)
    with col2:
        st.write("This is the home page content.")

elif page == "Data":
    st.title("Data Page")
    data_col, graph_col = st.columns(2)
    with data_col:
        st.write("Data Table or Input goes here.")
        # Example of a button acting like a callback
        if st.button("Fetch Data"):
            st.write("Fetching data from the database...")
            # Simulate data fetching
            data = {"item1": 100, "item2": 200}
            st.write(data)

    with graph_col:
        st.write("Graph or Visualization goes here.")

elif page == "Settings":
    st.title("Settings Page")
    st.sidebar.write("Customize your app settings here.")
elif page=="Custom":
    st.title("Customizatio Page")
    st.write("Custom Date Picker")
    custom_date_picker("Select a date")

    


with st.expander("See More"):
    st.write("Additional content goes here, visible when expanded.")
