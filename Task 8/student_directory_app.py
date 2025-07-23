
import streamlit as st
import pandas as pd


# Initialize session state for storing student records
if "students" not in st.session_state:
    st.session_state.students = pd.DataFrame(columns = ["Name","Email","Course","Score"])

st.title("🎓 Student Directory App")

# ------------------ 📝 Input Form ------------------

with st.form("student form"):
    st.subheader("Add New Students")
    name = st.text_input("Name")
    email = st.text_input("Email")
    course = st.selectbox("course",["Math","Science","History","Computer Science"])
    score = st.number_input("Score", min_value=0, max_value=100) 

    submitted = st.form_submit_button("Submit")

    if submitted:
        new_data =  {"Name" : name, "Email" : email,  "Course": course, "Score": score}
        st.session_state.students = pd.concat([st.session_state.students, pd.DataFrame([new_data])],ignore_index = True)
        st.success("✅ Student added successfully!")
    else:
        st.warning("⚠️ Please enter both Name and Email.")

# ------------------ 📄 Display Section ------------------

st.subheader("📋 All Student Records")
st.dataframe(st.session_state.students)

# Filter by Course
st.subheader("🔍 Filtered View")


filter_option = st.selectbox("Filter by course", ["All"] + list(st.session_state.students["Course"].unique()))
if filter_option != "All":
    filtered_data = st.session_state.students[st.session_state.students["Course"] == filter_option]
else:
    filtered_data = st.session_state.students

st.write("Filtered Results:")
st.dataframe(filtered_data)

