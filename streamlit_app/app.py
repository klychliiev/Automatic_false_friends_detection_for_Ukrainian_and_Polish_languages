import streamlit as st 
from openai import APIConnectionError, AuthenticationError
from file_manager import FileManager
from settings_config import * 
import json 

st.set_page_config(
    layout="wide", 
    page_title="Класифікатор хибних друзів перекладача та когнатів",
    page_icon="📢"
)

with st.sidebar:
    st.subheader("Налаштування мовних моделей")
    model = st.selectbox(
        "Оберіть мовну модель для класифікації: ",
        ("GPT", "Claude")
    )
    key = st.text_input(
        f"Введіть ваш ключ для моделі {model}:",
        type="password"
    )

    file_manager = FileManager(api_key=key)
    
    key_submit = st.button("Підтвердити")

    if key_submit and not key:
        st.warning("Будь ласка, введіть ключ.")

    st.subheader("Налаштування виводу програми")

    # checkbox_wiki = st.checkbox("Додати лінгвістичні дані Wiktionary")
    checkbox_cognates = st.checkbox("Включати когнати")
    checkbox_json = st.checkbox("Включити генерацію JSON")

main_tab, info_tab = st.tabs(["Класифікатор", "Додатково"])

def create(uk, pl):
    uk_text = uk.read().decode('utf-8')
    pl_text = pl.read().decode('utf-8')

    uk_lemmas, pl_lemmas = file_manager.process_text(uk_text, pl_text)

    word_pairs, cont = file_manager.create_candidate_pairs(uk_lemmas, pl_lemmas)

    if model=="GPT":
        result = file_manager.find_false_friends(word_pairs, cont)
    else: 
        result = file_manager.find_false_friends_claude(word_pairs, cont)

    return result

with main_tab: 
    st.header("Класифікатор хибних друзів перекладача та когнатів")
    st.subheader("Знайди хибні друзі перекладача у власних текстах")

    with st.expander("Інструкція"):
        ### Інструкція:
        st.markdown("""
        ### Інструкція:
        1. **Оберіть мовну модель** для виявлення хибних друзів перекладача.
        2. **Введіть API ключ** для відповідної мовної моделі та натисніть кнопку "Підтвердити".
        3. Оберіть за необхідності **додаткові параметри** виводу програми.
        4. **Завантажте тексти** - українською та польською мовами, натисніть кнопку "Ок".
        5. Зачекайте 5-15 секунд допоки згенерується відповідь.
            """)
    st.markdown("Завантажте два файли, один з українськомовним текстом, інший - польськомовним.")
    uk = st.file_uploader("ukr", type="txt", accept_multiple_files=True, label_visibility="collapsed")

    submit_button = st.button("Ок")

    if submit_button and len(uk) == 2:
        # try:
            result = create(uk[0], uk[1])
            filtered_result = result
            
            if not checkbox_cognates:
                filtered_result['word_pairs'] = [pair for pair in result['word_pairs'] if pair['false_friends'] == 'True']

            if checkbox_json:
                st.json(filtered_result)
                result_json = json.dumps(filtered_result, ensure_ascii=False, indent=4)
                st.download_button(
                    label="Завантажити",
                    data=result_json,
                    file_name="result.json",
                    mime="application/json"
                )
            else:
                # Parsing result and displaying it in a readable format
                st.markdown("---")  # Add a divider
                for item in filtered_result['word_pairs']:
                    pair = item['pair']
                    for word in pair:
                        st.markdown(f"**{word.capitalize()}**: {pair[word]['sentence'][0]}")
                        
                    if checkbox_cognates:
                        st.markdown(f"**Хибні друзі**: {'так' if item['false_friends'] == 'True' else 'ні'}")
                    # st.markdown(f"**Explanation**: {item['explanation']}")
                    st.markdown("---")  # Add a divider
                    
        # except (AuthenticationError, UnicodeEncodeError, APIConnectionError) as e:
        #     st.error(f"Сталася помилка: {str(e)}")

with info_tab: 
    st.header("Інформація про хибні друзі перекладача")
    st.markdown("**Когнати** – лексеми, що мають схоже написання та значення у двох чи більше мовах і при цьому мають спільне походження.")
