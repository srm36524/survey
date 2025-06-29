import streamlit as st
import pandas as pd
import plotly.express as px
import textwrap

# Load Data
@st.cache_data
def load_data():
    df = pd.read_excel('Survey123.xlsx', engine='openpyxl')
    return df

df = load_data()

# Dropdown filters
col1_options = df.iloc[:, 0].dropna().unique()
col2_options = df.iloc[:, 1].dropna().unique()

selected_col1 = st.selectbox(f"Select {df.columns[0]}", col1_options)
selected_col2 = st.selectbox(f"Select {df.columns[1]}", col2_options)

# Filter data based on dropdown selection
filtered_df = df[(df.iloc[:, 0] == selected_col1) & (df.iloc[:, 1] == selected_col2)]

st.title("Community Service Project - Survey Findings of Socio Economic Survey and Skilling and Employment Survey")

# Add full A4 page space to start first chart from second page
st.markdown('<div style="height: 1122px;"></div>', unsafe_allow_html=True)

# Get valid question columns
questions = [col for col in df.columns[2:] if isinstance(col, str) and col.strip().lower() not in ["", "undefined", "nan"]]

# Heading space adjustment
max_question_length = max(len(str(q)) for q in questions)
estimated_lines = (max_question_length // 60) + 1
heading_space_px = estimated_lines * 25 + 20

# A4 Height: 1122px; Margins Top/Bottom: 1cm ≈ 38px; Left: 2cm ≈ 76px
a4_total_height_px = 1122
top_bottom_margin_px = 38
available_height = a4_total_height_px - (2 * top_bottom_margin_px)
chart_height = available_height / 2  # Two charts per A4

for idx, col in enumerate(questions):

    st.markdown(f'<div style="height: {heading_space_px}px; display:flex; align-items:center;"><h3>{col}</h3></div>', unsafe_allow_html=True)

    question_data = filtered_df[col].dropna().astype(str)
    if question_data.empty:
        st.info("No responses for this question.")
        continue

    count_series = question_data.value_counts()
    count_series = count_series[count_series > 0]

    if count_series.empty:
        st.info("No valid responses to display.")
        continue

    percent_series = (count_series / count_series.sum() * 100).round(2)

    chart_df = pd.DataFrame({
        'Response': count_series.index,
        'Count': count_series.values,
        'Percentage': percent_series.values
    })

    def wrap_label(label, width=25):
        return "<br>".join(textwrap.wrap(label, width=width))

    chart_df['Wrapped_Response'] = chart_df['Response'].apply(lambda x: wrap_label(str(x)))

    fig = px.bar(
        chart_df,
        y='Wrapped_Response',
        x='Count',
        orientation='h',
        text=chart_df.apply(lambda row: f"{int(row['Count'])} ({row['Percentage']}%)", axis=1),
        labels={'Count': 'Number of Responses'},
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    fig.update_traces(textposition='outside', textfont_color='black', width=0.6)
    fig.update_layout(
        title="",
        showlegend=False,
        yaxis_title="",
        yaxis=dict(
            categoryorder='total ascending',
            automargin=True,
            tickfont=dict(size=14),
            type='category'
        ),
        margin=dict(l=76, r=50, t=50, b=50),
        font=dict(color='black', size=12, family='Arial Black'),
        plot_bgcolor='rgba(240, 240, 240, 0.8)',
        height=chart_height,
        bargap=0.7,
        xaxis=dict(range=[0, chart_df['Count'].max() * 1.3])
    )

    st.plotly_chart(fig, use_container_width=True, key=f"chart_{idx}")

    # Page break after every 2 charts
    if (idx + 1) % 2 == 0:
        st.markdown('<div class="pagebreak"></div>', unsafe_allow_html=True)

# Styling
st.markdown("""
<style>
    .css-18e3th9 {
        background-color: #f0f2f6;
    }
    .stSelectbox label {
        font-weight: bold;
        color: #0e0e0e;
    }
    h1, h2, h3 {
        color: #002060;
        font-weight: bold;
    }
    .pagebreak {
        page-break-after: always;
    }
</style>
""", unsafe_allow_html=True)

st.success("Select filters to view question-wise bar charts.")
