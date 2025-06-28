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

# Generate all charts, 2 per A4-like page layout (one below other, with page breaks for PDF view)
questions = list(df.columns[2:])

for i in range(0, len(questions), 2):
    for j in range(2):
        if i + j < len(questions):
            col = questions[i + j]
            st.subheader(f"{col}", divider="rainbow")

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
                color_discrete_sequence=px.colors.qualitative.Bold
            )

            fig.update_traces(textposition='outside', textfont_color='black')
            fig.update_layout(
                showlegend=False,
                yaxis={'categoryorder': 'total ascending', 'automargin': True},
                margin=dict(l=400, r=50, t=50, b=50),
                font=dict(color='black', size=16, family='Arial Black'),
                title_font=dict(color='black', size=18, family='Arial Black'),
                plot_bgcolor='rgba(240, 240, 240, 0.8)'
            )

            st.plotly_chart(fig, use_container_width=True, key=f"chart_{i}_{j}")

    st.markdown('<div class="pagebreak"></div>', unsafe_allow_html=True)

# Frontend Styling
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
        margin-top: 50px;
    }
</style>
""", unsafe_allow_html=True)

st.success("Select filters to view question-wise bar charts.")
