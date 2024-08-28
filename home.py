import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data import load_data  # Ensure you have a function to load your data
from datetime import datetime
# Load data
df = load_data()

def display_basic_stats(df):
    st.header("Basic Statistics")

    # Check for NaN values
    nan_stu_ids = df[df['school_eng'].isna()]['stu_id']
    if not nan_stu_ids.empty:
        st.subheader("Students with Missing School Information")
        st.write(", ".join(map(str, nan_stu_ids.tolist())))

    st.subheader("Total Number of Students")
    st.write(len(df))

    st.subheader("Preview of DataFrame")
    # Show the first 7 rows and the last 7 rows of the DataFrame
    num_rows = 7
    if len(df) > num_rows * 2:
        preview_df = pd.concat([df.head(num_rows), df.tail(num_rows)])
    else:
        preview_df = df

    st.write(preview_df)

def display_province_summary():
    st.header("Province Summary")
    
    province_counts = df.groupby('names').size().reset_index(name='total_students')
    province_counts_sorted = province_counts.sort_values(by='total_students', ascending=False)
    
    st.subheader("Total Number of Students in Each Province")
    fig = px.bar(province_counts_sorted, x='names', y='total_students', title='Total Number of Students in Each Province')
    st.plotly_chart(fig)

    total_students = province_counts_sorted['total_students'].sum()
    province_counts_sorted['percentage'] = (province_counts_sorted['total_students'] / total_students) * 100
    others = province_counts_sorted[province_counts_sorted['percentage'] < 3]
    main_provinces = province_counts_sorted[province_counts_sorted['percentage'] >= 3]
    
    if not others.empty:
        others_total = others['total_students'].sum()
        others_row = pd.DataFrame([{'names': 'Other', 'total_students': others_total, 'percentage': (others_total / total_students) * 100}])
        province_counts_final = pd.concat([main_provinces, others_row])
    else:
        province_counts_final = main_provinces
    
    province_counts_final = province_counts_final.sort_values(by='total_students', ascending=False)
    st.subheader("Proportion of Students in Each Province")
    fig = px.pie(province_counts_final, values='total_students', names='names', title='Proportion of Students in Each Province')
    st.plotly_chart(fig)

def display_top_provinces_faculties():
    st.header("Top Provinces and Faculties")
    
    top_5_provinces = df.groupby('names').size().reset_index(name='total_students').sort_values(by='total_students', ascending=False).head(5)
    top_5_faculties = df.groupby('fac_eng').size().reset_index(name='total_students').sort_values(by='total_students', ascending=False).head(5)
    
    st.subheader("Top 5 Provinces with the Highest Number of Students")
    fig = px.bar(top_5_provinces, x='names', y='total_students', title='Top 5 Provinces with the Highest Number of Students')
    st.plotly_chart(fig)
    
    st.subheader("Top 5 Faculties with the Highest Number of Students")
    fig = px.bar(top_5_faculties, x='fac_eng', y='total_students', title='Top 5 Faculties with the Highest Number of Students')
    st.plotly_chart(fig)

def display_faculty_summary():
    st.header("Faculty Summary")
    
    faculty_counts = df.groupby('fac_eng').size().reset_index(name='total_students')
    top_5_faculties = faculty_counts.sort_values(by='total_students', ascending=False).head(5)
    
    st.subheader("Total Number of Students in Each Faculty")
    fig = px.bar(faculty_counts, x='fac_eng', y='total_students', title='Total Number of Students in Each Faculty')
    st.plotly_chart(fig)

    st.subheader("Top 5 Faculties with the Highest Number of Students")
    fig = px.bar(top_5_faculties, x='fac_eng', y='total_students', title='Top 5 Faculties with the Highest Number of Students')
    st.plotly_chart(fig)

def display_province_faculty_distribution():
    st.header("Province and Faculty Distribution")
    
    province_faculty_counts = df.groupby(['names', 'fac_eng']).size().reset_index(name='total_students')
    fig = px.bar(province_faculty_counts, x='fac_eng', y='total_students', color='names', title='Total Number of Students from Each Province Enrolled in Each Faculty')
    st.plotly_chart(fig)

def display_province_faculty_school_distribution():
    st.header("Province, Faculty, and School Distribution")
    
    province_faculty_counts = df.groupby(['names', 'fac_eng', 'school_eng']).size().reset_index(name='total_students')
    fig = px.bar(province_faculty_counts, x='fac_eng', y='total_students', color='names', title='Total Number of Students from Each Province Enrolled in Each Faculty by School')
    st.plotly_chart(fig)

def display_student_registration():
    st.header("Student Registration Date")
    
    df['ste_reg'] = pd.to_datetime(df['ste_reg'])
    df['year'] = df['ste_reg'].dt.year
    yearly_counts = df.groupby('year').size().reset_index(name='total_students')
    
    st.subheader("Total Number of Students in Each Year")
    fig_bar = px.bar(yearly_counts, x='year', y='total_students', text='total_students', title='Total Number of Students in Each Year')
    fig_bar.update_traces(textposition='outside')
    st.plotly_chart(fig_bar)
    
    st.subheader("Proportion of Students in Each Year")
    fig_pie = px.pie(yearly_counts, names='year', values='total_students', title='Proportion of Students in Each Year')
    st.plotly_chart(fig_pie)

# Create Streamlit app layout
st.sidebar.title("Student Menu")
selection = st.sidebar.radio("Select a page:", [
    "Basic Statistics",
    "Province Summary",
    "Top Provinces and Faculties",
    "Faculty Summary",
    "Province and Faculty Distribution",
    "Province, Faculty, and School Distribution",
    "Student Registration Date"
])

# Display selected page
if selection == "Basic Statistics":
    display_basic_stats(df)
elif selection == "Province Summary":
    display_province_summary()
elif selection == "Top Provinces and Faculties":
    display_top_provinces_faculties()
elif selection == "Faculty Summary":
    display_faculty_summary()
elif selection == "Province and Faculty Distribution":
    display_province_faculty_distribution()
elif selection == "Province, Faculty, and School Distribution":
    display_province_faculty_school_distribution()
elif selection == "Student Registration Date":
    display_student_registration()