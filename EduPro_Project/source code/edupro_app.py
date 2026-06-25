
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="EduPro Dashboard", layout="wide")

file = "../dataset/EduPro Online Platform.xlsx"

teachers = pd.read_excel(file, sheet_name="Teachers")
courses = pd.read_excel(file, sheet_name="Courses")
transactions = pd.read_excel(file, sheet_name="Transactions")

data = transactions.merge(teachers, on="TeacherID", how="left")
data = data.merge(courses, on="CourseID", how="left")

st.title("Instructor Performance and Course Quality Evaluation")

st.sidebar.header("Filters")
expertise = st.sidebar.multiselect("Expertise", teachers["Expertise"].unique())
if expertise:
    data = data[data["Expertise"].isin(expertise)]

col1, col2, col3 = st.columns(3)
col1.metric("Avg Teacher Rating", round(teachers["TeacherRating"].mean(),2))
col2.metric("Avg Course Rating", round(courses["CourseRating"].mean(),2))
col3.metric("Enrollments", len(transactions))

st.subheader("Top Instructors")
leader = teachers.sort_values("TeacherRating", ascending=False).head(10)
st.dataframe(leader)

st.subheader("Experience vs Teacher Rating")
fig1 = px.scatter(teachers, x="YearsOfExperience", y="TeacherRating",
                  hover_name="TeacherName")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Course Category Ratings")
cat = courses.groupby("CourseCategory")["CourseRating"].mean().reset_index()
fig2 = px.bar(cat, x="CourseCategory", y="CourseRating")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Expertise Performance")
exp = teachers.groupby("Expertise")["TeacherRating"].mean().reset_index()
fig3 = px.bar(exp, x="Expertise", y="TeacherRating")
st.plotly_chart(fig3, use_container_width=True)
