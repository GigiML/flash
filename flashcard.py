import streamlit as st
import pandas as pd
import random
import os



def list_csv_files(directory):
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    return csv_files
directory = '.'  
csv_files = list_csv_files(directory)

selected_file = st.selectbox('Choose a CSV file', csv_files)
# Fonction pour charger les données
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(selected_file)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Word/Phrase", "Definition", "Example Sentence"])
    return df

# Fonction pour sauvegarder les données
def save_data(df):
    df.to_csv(selected_file, index=False)
    load_data.clear()

# Initialisation de l'application
st.title("Flashcard App")

# Chargement des données
df = load_data()

# Création des onglets
tab1, tab2, tab3 = st.tabs(["Quiz", "Add Flashcard", "Show All"])

with tab1:
    if not df.empty:
        # Utiliser session_state pour stocker l'état actuel
        if 'current_card' not in st.session_state:
            st.session_state.current_card = None
        if 'show_answer' not in st.session_state:
            st.session_state.show_answer = False

        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Choose a random flashcard"):
                st.session_state.current_card = random.randint(0, len(df) - 1)
                st.session_state.show_answer = False

        with col2:
            if st.button("Next flashcard"):
                st.session_state.current_card = random.randint(0, len(df) - 1)
                st.session_state.show_answer = False

        if st.session_state.current_card is not None:
            question = df.iloc[st.session_state.current_card]["Word/Phrase"]
            answer = df.iloc[st.session_state.current_card]["Definition"]
            sentence = df.iloc[st.session_state.current_card]["Example Sentence"]
            
            st.write("Question:")
            st.write(question)
            
            if st.button("Show/Hide the answer"):
                st.session_state.show_answer = not st.session_state.show_answer

            if st.session_state.show_answer:
                st.write("Answer:")
                st.write(answer)
                st.write(sentence)
    else:
        st.write("No flashcards available. Please add some flashcards.")

with tab2:
    st.header("Add Flashcard")
    new_question = st.text_input("Enter the question:")
    new_answer = st.text_input("Enter the answer:")
    new_sentence = st.text_input("Enter the sentence:")
    
    if st.button("Add Flashcard"):
        if new_question and new_answer:
            new_row = pd.DataFrame({"Word/Phrase": [new_question], "Definition": [new_answer], "Example Sentence": [new_sentence]})
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.success("Flashcard added successfully!")
            df = load_data()
        else:
            st.error("Please enter both question and answer.")

with tab3:
    st.header("Show All Flashcards")
    st.dataframe(df)


