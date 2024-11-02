import streamlit as st
import pandas as pd
import random
import os

# Function to list CSV files
def list_csv_files(directory):
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    return csv_files

# Function to load data
@st.cache_data
def load_data(file):
    try:
        df = pd.read_csv(file)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Word/Phrase", "Definition", "Example Sentence"])
    return df

# Function to save data
def save_data(df, file):
    df.to_csv(file, index=False)
    st.cache_data.clear()

# Initialize the application
st.title("Flashcard App")

# List CSV files
directory = '.'
csv_files = list_csv_files(directory)

# Create a selectbox for file selection
if 'selected_file' not in st.session_state:
    st.session_state.selected_file = csv_files[0] if csv_files else None

selected_file = st.selectbox('Choose a CSV file', csv_files, key='file_selector')

# Update the selected file in session state
if selected_file != st.session_state.selected_file:
    st.session_state.selected_file = selected_file


# Load data based on the selected file
df = load_data(st.session_state.selected_file)

# Create tabs
tab1, tab2, tab3 = st.tabs(["Quiz", "Add Flashcard", "Show All"])

with tab1:
    if not df.empty:
        # Use session_state to store the current state
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
            save_data(df, st.session_state.selected_file)
            st.success("Flashcard added successfully!")
        else:
            st.error("Please enter both question and answer.")

with tab3:
    st.header("Show All Flashcards")
    st.dataframe(df)
