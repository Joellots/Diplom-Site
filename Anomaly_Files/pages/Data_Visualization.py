import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import col_definition as cd
import os


st.set_page_config(page_title="ВИЗУАЛИЗАЦИЯ ДАННЫХ", page_icon=":guardsman:", layout="wide")

current_dir = os.path.dirname(os.path.abspath(__file__))
st.title('Визуализация Данных об Обнаружении Аномалий')

st.markdown("""
    **Визуализация данных является важным этапом в процессе машинного обучения. Она позволяет исследовать и интерпретировать данные, выявлять скрытые закономерности и аномалии, а также представлять результаты моделей машинного обучения в наглядной и понятной форме.**

    **Зачем нужна визуализация данных?**
    - **Исследование данных:** На начальном этапе работы с данными визуализация помогает понять структуру и распределение данных. Это позволяет выявить выбросы, пропущенные значения и определить потенциально важные признаки.

    - **Диагностика моделей:** Визуализация результатов работы моделей машинного обучения позволяет понять, насколько хорошо модель обучается и делает предсказания. Например, графики ошибок обучения и валидации могут показать, происходит ли переобучение или недообучение модели.

    - **Интерпретация моделей:** Графики важности признаков, парные диаграммы и тепловые карты корреляций помогают понять, какие признаки вносят наибольший вклад в предсказания модели.

    - **Представление результатов:** Визуализация делает результаты моделей машинного обучения доступными для широкой аудитории, включая тех, кто не обладает глубокими знаниями в области данных. Это важно для принятия решений на основе данных в бизнесе и других областях.
            
    **Основные виды визуализации данных**
    - **Гистограммы:** Используются для отображения распределения числовых данных. Позволяют увидеть, как часто встречаются значения в определенных диапазонах.

    - **Столбчатые диаграммы:** Применяются для визуализации частоты категориальных данных. Помогают сравнивать количество элементов в различных категориях.

    - **Тепловые карты корреляций:** Используются для отображения взаимосвязей между числовыми признаками. Позволяют быстро определить, какие признаки имеют сильные корреляции.

    - **Диаграммы рассеяния:** Помогают визуализировать отношения между двумя числовыми признаками. Полезны для выявления зависимостей и трендов.""")




CUSTOM_CSS = """
<style>
body {
    background-color: #f0f2f6; /* Set background color */
    font-family: Arial, sans-serif;
    line-height: 1.6;
    padding: 20px;
    color: #333; /* Set text color */
}

h1, h2, h3 {
    color: #333; /* Set heading color */
}

.sidebar .sidebar-content {
    background-color: #ffffff; /* Set sidebar background color */
}

/* Add more custom styles as needed */
</style>
"""

# Apply custom CSS styles
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Define CSS styles
st.markdown(
    """
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            padding: 20px;
            color: #333;
        }
        ul {
            list-style-type: disc;
            padding-left: 20px;
        }
        li {
            margin-bottom: 5px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory
parent_directory = os.path.abspath(os.path.join(current_dir, os.pardir))
st.logo(os.path.join(parent_directory, 'knrtu_logo.png'), link=None)


# Sample DataFrame (Replace this with actual data loading)
st.cache_data
def load_data():
    raw_df_1 = pd.read_csv(os.path.join(parent_directory, 'Train.txt'), header=None, names=cd.columns)
    raw_df_2 = pd.read_csv(os.path.join(parent_directory, 'Test.txt'), header=None, names=cd.columns)
    raw_df = pd.concat([raw_df_2, raw_df_1])
    return raw_df

raw_df = load_data()

numeric_cols = cd.numeric_cols

st.sidebar.title('Выберите График')
plot_type = st.sidebar.selectbox('Выберите тип графика:', ['Гистограмма', 'столбчатый график', 'Корреляционная тепловая карта'])

if plot_type == 'Гистограмма':
    selected_col = st.sidebar.selectbox('Выберите столбец:', numeric_cols)
    if st.sidebar.button('Построить'):
        fig, ax = plt.subplots()
        ax.hist(raw_df[selected_col])
        ax.set_xlabel(selected_col)
        ax.set_ylabel('Frequency')
        ax.set_title(f'Distribution of {selected_col}')
        st.pyplot(fig)
        

elif plot_type == 'столбчатый график':
    cat_cols = cd.categorical_cols
    selected_col = st.sidebar.selectbox('Выберите столбец:', cat_cols)
    plt.rcParams["figure.figsize"] = (28, 10)
    if st.sidebar.button('Построить'):
        fig, ax = plt.subplots()
        ax.bar(raw_df[selected_col].value_counts().index, raw_df[selected_col].value_counts().values)
        ax.set_xlabel(selected_col)
        plt.xticks(rotation=45) 
        ax.set_ylabel('Count')
        ax.set_title(f'Distribution of {selected_col}')
        st.pyplot(fig)

elif plot_type == 'Корреляционная тепловая карта':
    if st.sidebar.button('Построить'):
        fig, ax = plt.subplots(figsize=(25, 20))
        correlation_matrix = raw_df[numeric_cols].corr()
        sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        ax.set_title('Correlation Heatmap')
        st.pyplot(fig)
        
