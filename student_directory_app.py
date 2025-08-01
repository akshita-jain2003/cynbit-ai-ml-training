
import streamlit as st
import pandas as pd

# Initialize session state for storing student records
if "students" not in st.session_state:
    st.session_state.students = pd.DataFrame(columns = ["Name","Email","Course","Score"])

st.title("🎓 Student Directory App")

# ------------------ 📝 Input Form ------------------
st.header("➕ Add New Student")

with st.form("student form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    course = st.selectbox("course",["C++","Python","Java","Computer Science"])
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
st.sidebar.subheader("🔍 Filtered View")


course_filter = st.sidebar.selectbox("Filter by course", ["All"] + list(st.session_state.students["Course"].unique()))

name_filter = st.sidebar.selectbox("Filter by Name", ["All"] + list(st.session_state.students["Name"].unique()))

# Start with all data
filtered_data = st.session_state.students

# Apply course filter
if course_filter != "All":
    filtered_data = filtered_data[filtered_data["Course"] == course_filter]

# Apply name filter
if name_filter != "All":
    filtered_data = filtered_data[filtered_data["Name"] == name_filter]

st.write("Filtered Results:")
st.dataframe(filtered_data)
