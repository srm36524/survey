import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel('Survey123.xlsx')
    return df

df = load_data()

# Dropdowns for filtering
col1_options = df.iloc[:, 0].dropna().unique()
col2_options = df.iloc[:, 1].dropna().unique()

selected_col1 = st.selectbox('Select ' + df.columns[0], col1_options)
selected_col2 = st.selectbox('Select ' + df.columns[1], col2_options)

filtered_df = df[(df.iloc[:, 0] == selected_col1) & (df.iloc[:, 1] == selected_col2)]

st.title("Survey Results - Horizontal Bar Charts")

# Generate charts for each question
for idx, col in enumerate(df.columns[2:]):
    st.subheader(col)
    
    question_data = filtered_df[col].dropna()
    if question_data.empty:
        st.info("No responses for this question.")
        continue
    
    count_series = question_data.value_counts().sort_values()
    percent_series = (count_series / count_series.sum() * 100).round(2)

    chart_df = pd.DataFrame({
        'Response': count_series.index,
        'Count': count_series.values,
        'Percentage': percent_series.values
    })

    fig = px.bar(
        chart_df,
        y='Response',
        x='Count',
        orientation='h',
        text=chart_df.apply(lambda row: f"{row['Count']} ({row['Percentage']}%)", axis=1),
        labels={'Count': 'Number of Responses', 'Response': 'Response Options'},
        color='Response'
    )

    fig.update_traces(textposition='outside')
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})

    st.plotly_chart(fig, use_container_width=True, key=f"chart_{idx}")

# Frontend Styling
st.markdown("""
<style>
    .css-18e3th9 {
        background-color: #f0f2f6;
    }
    .stSelectbox label {
        font-weight: bold;
        color: #4b4b4b;
    }
    h1, h2, h3 {
        color: #0e4d92;
    }
</style>
""", unsafe_allow_html=True)

st.success("Select filters to view question-wise bar charts.")
