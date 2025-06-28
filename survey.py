import streamlit as st
import pandas as pd
import plotly.express as px
import textwrap
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import plotly.io as pio
from tempfile import NamedTemporaryFile
import os
from PIL import Image

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

st.title("Community Service Project - Survey Findings of Socio Economic Survey and Skilling and Employment Survey")

# Fixed space between title and first chart (450px)
st.markdown('<div style="height: 450px;"></div>', unsafe_allow_html=True)

questions = list(df.columns[2:])
chart_images = []

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
                'Response': count_series.index.astype(str),
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
                labels={'Count': 'Number of Responses', 'Wrapped_Response': 'Response Options'},
                color_discrete_sequence=px.colors.qualitative.Bold
            )

            fig.update_traces(textposition='outside', textfont_color='black', width=0.6)
            fig.update_layout(
                showlegend=False,
                yaxis={
                    'categoryorder': 'total ascending',
                    'automargin': True,
                    'title_font': dict(size=14),
                    'tickfont': dict(size=14)
                },
                margin=dict(l=100, r=50, t=50, b=50),
                font=dict(color='black', size=12, family='Arial Black'),
                title_font=dict(color='black', size=16, family='Arial Black'),
                plot_bgcolor='rgba(240, 240, 240, 0.8)',
                height=450,
                bargap=0.7,
                xaxis=dict(range=[0, chart_df['Count'].max() * 1.3])
            )

            st.plotly_chart(fig, use_container_width=True, key=f"chart_{i}_{j}")

            with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                tmpfile.write(pio.to_image(fig, format='png', width=1000, height=500))
                chart_images.append(tmpfile.name)

    st.markdown('<div class="pagebreak" style="height: 60px;"></div>', unsafe_allow_html=True)

# PDF Export
if chart_images:
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=A4)
    width, height = A4
    for idx, img_path in enumerate(chart_images):
        img = Image.open(img_path)
        img_width, img_height = img.size
        aspect = img_height / img_width
        draw_width = width - 100
        draw_height = draw_width * aspect
        c.drawImage(ImageReader(img), 50, height - draw_height - 100, width=draw_width, height=draw_height)
        if idx % 2 == 1 or idx == len(chart_images) - 1:
            c.showPage()
    c.save()
    pdf_buffer.seek(0)

    st.download_button("📄 Download Charts as PDF", data=pdf_buffer, file_name="Survey_Charts.pdf")

    # Cleanup temp images
    for img_path in chart_images:
        os.remove(img_path)

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
        margin-top: 60px;
    }
</style>
""", unsafe_allow_html=True)

st.success("Select filters to view question-wise bar charts.")
