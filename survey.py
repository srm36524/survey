# Pre-calculate max heading space
max_question_length = max(len(str(q)) for q in questions)
estimated_lines = (max_question_length // 80) + 1
heading_space_px = estimated_lines * 20 + 10  # Rough estimation

for i in range(0, len(questions), 2):

    for j in range(2):
        if i + j < len(questions):
            col = questions[i + j]

            # Consistent heading space
            st.markdown(f'<div style="height: {heading_space_px}px; display:flex; align-items:center;"><h3>{col}</h3></div>', unsafe_allow_html=True)

            # [Rest of your chart generation code]
