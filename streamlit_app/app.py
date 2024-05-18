import streamlit as st 
from openai import AuthenticationError, APIConnectionError
from file_manager import FileManager
from settings_config import * 

import json 

st.set_page_config(
    layout="centered", 
    page_title="Класифікатор хибних друзів перекладача та когнатів",
    page_icon="ji-\U0001F5E3"
)

with st.sidebar:
    st.header("Налаштування")
    model = st.sidebar.selectbox(
        "Оберіть мовну модель для класифікації: ",
        ("GPT-4", "Claude 3 Opus", "Llama 3", "Mistral")
    )
    key = st.text_input(
        f"Введіть ваш ключ для моделі {model}:",
        type="password"
    )

    file_manager = FileManager(api_key=key)
    
    key_submit = st.button("Підтвердити")

    if key_submit and not key:
        st.warning("Будь ласка, ведіть ключ.")

    print(model)

main_tab, info_tab = st.tabs(["Класифікатор", "Додатково"])

def create(uk, pl):
    uk_text = uk.read().decode('utf-8')
    pl_text = pl.read().decode('utf-8')

    uk_lemmas, pl_lemmas = file_manager.process_text(uk_text, pl_text)

    word_pairs, cont = file_manager.create_candidate_pairs(uk_lemmas, pl_lemmas)

    result = file_manager.find_false_friends(word_pairs, cont)

    return result

with main_tab: 
    st.header("Класифікатор хибних друзів перекладача та когнатів")

    st.markdown("Завантажте два текстові файли, один українською мовою, інший - польською.")
    
    uk = st.file_uploader(
        "ukr",
        type="txt",
        accept_multiple_files=True,
        label_visibility="collapsed"

    )

    st.write()

    print(len(uk))

    if len(uk) > 2: 
        st.warning("Будь ласка, виберіть лише два тексти.")

    # pl = st.file_uploader(
    #     "Pl \U0001F1F5\U0001F1F1",
    #     type="txt"
    # )


    submit_button = st.button("Ок")

    if submit_button:
        try:
            if len(uk) == 2:
                result = create(uk[0], uk[1])
                st.json(result)
                # Convert result to JSON string and create a download button
                result_json = json.dumps(result, ensure_ascii=False, indent=4)
                st.download_button(
                    label="Download JSON",
                    data=result_json,
                    file_name="result.json",
                    mime="application/json"
                )
        except (AuthenticationError, UnicodeEncodeError, APIConnectionError):
            st.warning("Невірний API ключ.")     

    # print(type(uk))
    # print(uk)

    # try:
    #     print(uk.read().decode('utf-8'))
    # except AttributeError:
    #     print()


with info_tab: 
    st.header("Інформація про хибні друзі перекладача")

