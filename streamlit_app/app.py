import json
from openai import APIConnectionError, AuthenticationError
import streamlit as st
import pandas as pd 
from file_manager import FileManager
from prompt import template
from settings_config import *

st.set_page_config(
    layout="wide",
    page_title="Класифікатор хибних друзів перекладача та когнатів",
    page_icon="📢",
)

# Sidebar configuration
with st.sidebar:
    st.subheader("Налаштування мовних моделей")
    model = st.selectbox("Оберіть мовну модель для класифікації: ", ("GPT-4", ""))
    key = st.text_input(f"Введіть ваш ключ для моделі {model}:", type="password")

    file_manager = FileManager(api_key=key)
    key_submit = st.button("Підтвердити")

    if key_submit and not key:
        st.warning("Будь ласка, введіть ключ.")

    st.subheader("Налаштування виводу програми")
    checkbox_cognates = st.checkbox("Включати когнати")
    checkbox_json = st.checkbox("Включити генерацію JSON")

# Main tabs
main_tab, info_tab = st.tabs(["Класифікатор", "Додатково"])

# Function to create and process the texts
def create(uk, pl):
    uk_text = uk.read().decode("utf-8")
    pl_text = pl.read().decode("utf-8")

    uk_lemmas, pl_lemmas = file_manager.process_text(uk_text, pl_text)
    word_pairs, cont = file_manager.create_candidate_pairs(uk_lemmas, pl_lemmas)
    result = file_manager.find_false_friends(template, word_pairs, cont)

    return result

# Main tab content
with main_tab:
    st.header("Класифікатор хибних друзів перекладача та когнатів")
    st.subheader("Знайди хибні друзі перекладача у власних текстах")

    with st.expander("Інструкція"):
        st.markdown(
            """
            1. Мовна модель для виявлення хибних друзів за замовчуванням — **GPT-4**.
            2. **Введіть API ключ** для роботи з GPT-4 та натисніть кнопку "Підтвердити".
            3. Оберіть за необхідності **додаткові параметри** виводу програми.
            4. **Завантажте тексти** — українською та польською мовами, натисніть кнопку "Ок".
            5. Зачекайте деякий час допоки згенерується відповідь. Час очікування залежить від розміру вхідних файлів.
            """
        )

    st.markdown("Завантажте два файли, один з українськомовним текстом, інший — польськомовним.")
    uk = st.file_uploader("ukr", type="txt", accept_multiple_files=True, label_visibility="collapsed")

    submit_button = st.button("Ок")

    if submit_button and len(uk) == 2:
        try:
            result = create(uk[0], uk[1])
            st.session_state['result'] = result  # Store the result in session state

        except (AuthenticationError, UnicodeEncodeError, APIConnectionError) as e:
            st.error(f"Сталася помилка: {str(e)}")

# Main tab result display logic
with main_tab:
    # Check if the result is in the session state
    if 'result' in st.session_state:
        result = st.session_state['result']

        filtered_result = result.copy()
        if not checkbox_cognates:
            filtered_result["word_pairs"] = [
                pair for pair in result["word_pairs"] if pair["false_friends"] == "True"
            ]

        if checkbox_json:
            st.json(filtered_result)
            result_json = json.dumps(filtered_result, ensure_ascii=False, indent=4)
            st.download_button(
                label="Завантажити",
                data=result_json,
                file_name="result.json",
                mime="application/json",
            )
        else:
            # Parsing result and displaying it in a readable format
            st.markdown("---")  # Add a divider
            for item in filtered_result["word_pairs"]:
                pair = item["pair"]
                for word in pair:
                    st.markdown(f"**{word.capitalize()}**: {pair[word]['sentence'][0]}")

                if checkbox_cognates:
                    st.markdown(f"**Хибні друзі**: {'так' if item['false_friends'] == 'True' else 'ні'}")
                st.markdown("---")  # Add a divider

# Info tab content
with info_tab:
    st.header("Лінгвістична база розробки")
    st.markdown(
        "**Когнати** – лексеми, що мають схоже написання та значення у двох чи більше мовах і при цьому мають спільне походження."
    )
    st.markdown("Приклади українсько-польських когнатів:")
    st.dataframe(pd.DataFrame({
        'Українське слово': ['сніданок', 'напій', 'сіль', 'мʼясо', 'час'],
        'Польське слово': ['śniadanie', 'napój', 'sól', 'mięso', 'czas']
    }))
    
    st.markdown(
        "**Хибні друзі перекладача** – слова, які мають схоже написання у двох чи більше мовах, але мають різне значення."
    )
    st.markdown("Приклади українсько-польських хибних друзів перекладача:")
    st.dataframe(pd.DataFrame({
        'Українське слово': ['ангельський', 'гарбуз', 'байка', 'диня', 'чашка'],
        'Польське слово': ['angielski', 'arbuz', 'bajka', 'dynia', 'czaszka']
    }))

    st.header("Програмна база розробки")
    st.markdown(
        """
        **Класифікатор хибних друзів перекладача та когнатів** – програма, яка виявляє хибні друзі перекладача та когнати у вхідних текстах користувача, написаних українською та польською мовами.
        """
    )
    st.markdown("**Алгоритм роботи програми:**")
    st.markdown("1. Обробка вхідних файлів, наданих користувачем. Після виввантаження користувачем файлів відбувається їхня обробка за допомогою біблотеки spacy та її попередньо натренованих моделей для української та польської мов. Обробка включає токенізацію, лематизацію текстів, а також фільтрування стоп-слів. ")
    st.markdown("2. Генерація лексичних пар-кандидатів. На цьому етапі серед усіх пар слів виокремлюються ті, що мають високий показник орфографічної подібності. Саме ці слова є потенційними когнатами або хибними друзями перекладача, які будуть прокласифіковані в наступному етапі. ")
    st.markdown("3. Класифікація хибних друзів перекладача та когнатів за допомогою мовної моделі GPT-4 та техніки Few-shot learning.")
