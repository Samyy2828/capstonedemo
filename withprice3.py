import streamlit as st
from fuzzywuzzy import process
from playsound import playsound

import speech_recognition as sr

from gtts import gTTS

import os

import csv

from datetime import datetime

from googletrans import Translator

import base64

from PIL import Image

from io import BytesIO

import time

 
# ---------------------------------------- css------------------------------------------#

 

st.markdown(

    """

    <style>

    .reportview-container {

        background: #FFFFFF;

    }

    .main .block-container {

        padding-top: 2rem;

    }

    .top-right {

        position: fixed;

        top: 35px;

        right: 0;

        width: 225px;

    }

    </style>

    """,

    unsafe_allow_html=True

)

 


 

# ----------------------------------------- Title and Subtitle -----------------------------------------#

 

st.markdown("<h1 style='text-align: center; color: #4682B4; font-weight: bold;'>Ticketing for Blind People</h1>",

            unsafe_allow_html=True)

st.divider()

speak_message = st.markdown(

    "<h6 style='text-align: left; color: #4682B4;'>Please click the button below and speak anything so that I can understand your language</h6>",

    unsafe_allow_html=True)

 

# -------------------------------------------- Main Page -----------------------------------------------#

 

# CSV file setup

csv_file = 'conversation_log.csv'

if not os.path.exists(csv_file):

    with open(csv_file, mode='w', encoding='utf-8', newline='') as file:

        writer = csv.writer(file)

        writer.writerow(['Timestamp', 'User Responses'])

 

 

# Function to log conversation

def log_conversation(responses):

    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:

        writer = csv.writer(file)

        writer.writerow([datetime.now(), responses])

 

 

# Function to identify language spoken by user

def identifylang():

    warning_placeholder = st.empty()

    with st.spinner("Identifying Your Language Please Wait..."):

        r = sr.Recognizer()

        with sr.Microphone() as source:
            r.pause_threshold = 1

            audio = r.listen(source)

        try:

            query = r.recognize_google(audio)

        except Exception as e:

            warning_placeholder.warning("Please repeat your command.")

            time.sleep(2)

            warning_placeholder.empty()

            return "None"

        return query

 

 

# Function to speak text using gTTS and playsound

def speak(text, language):

    speaktext = gTTS(text=text, lang=language, slow=False)

    speaktext.save("captured_voice.mp3")

    playsound('captured_voice.mp3')

    os.remove('captured_voice.mp3')

 

 

# Function to capture user response

def takeresponse(language, question):

    warning_placeholder = st.empty()

    with st.spinner("Listening..."):

        r = sr.Recognizer()

        with sr.Microphone() as source:

            r.pause_threshold = 1

            audio = r.listen(source)

        try:

            query = r.recognize_google(audio, language=language)

        except Exception as e:

            warning_placeholder.warning("Please repeat your command.")

            time.sleep(2)

            warning_placeholder.empty()

            return "None"

        return query

 

 

# Function to translate questions

def questions(response, src='en', dest='en'):

    text_translate = translator.translate(response, dest=dest, src=src)

    text = text_translate.text

    return text

 

 

# Function to update responses

def update_responses(responses):

    st.write("Review your responses:")

    updated_responses = []

    for i, response in enumerate(responses):

        st.write(f"Current response to '{question_list[i]}': {response}")

        if st.button(f"Update response to '{question_list[i]}'", key=f"update_{i}"):

            st.session_state.updating_response = i

    if 'updating_response' in st.session_state:

        st.write("Please provide your new response...")

        new_response = takeresponse(st.session_state.language, question_list[st.session_state.updating_response])

        while new_response == 'None':

            new_response = takeresponse(st.session_state.language, question_list[st.session_state.updating_response])

        translated_response_en = translator.translate(new_response, dest='en').text

        responses[st.session_state.updating_response] = translated_response_en

        st.session_state.pop('updating_response')

        st.rerun()

    return responses

 

 

# ---------------------------- Translator & question list ---------------------------#

translator = Translator()

question_list = [

    'Select number of adults',

    'Select number of children',

    'Chose between first and second class',
    'What is the starting station',

    'What is your destination',

    'Chose single or return',

    #'Which state are you currently residing in?'

]

 

# Define a mapping dictionary

MapNum = {'zero': '0', 'Zero': '0', 'One': '1', 'one': '1', 'Two': '2', 'two': '2',

          'Three': '3', 'three': '3', 'Four': '4', 'four': '4', 'Five': '5', 'five': '5',

          'Six': '6', 'six': '6', 'Seven': '7', 'seven': '7', 'Eight': '8', 'eight': '8',

          'Nine': '9', 'nine': '9'}
class_fs=['First','One',1,'1','Second','Two',2,'2']
stations = [
    "Airoli", "Aman Lodge", "Ambarnath", "Ambivli", "Andheri", "Apta", "Asangaon", "Atgaon", "Badlapur",
    "Bamandongri", "Bandra", "Bhandup", "Bhayandar", "Bhivpuri Road", "Bhiwandi Road", "Boisar", "Borivali", "Byculla", 
    "CBD Belapur", "Charni Road", "Chembur", "Chhatrapati Shivaji Maharaj Terminus", "Chikhale", "Chinchpokli", 
    "Chouk", "Chunabhatti", "Churchgate", "Cotton Green", "Currey Road", "Dadar", "Dahanu Road", "Dahisar", 
    "Dativali", "Digha Gaon", "Diva Junction", "Dockyard Road", "Dolavli", "Dombivli", "Dronagiri", "Ghansoli", 
    "Ghatkopar", "Goregaon", "Govandi", "Grant Road", "Guru Tegh Bahadur Nagar", "Hamrapur", "Jite", "Jogeshwari", 
    "Juchandra", "Juinagar", "Jummapatti", "Kalamboli", "Kalwa", "Kalyan Junction", "Kaman Road", "Kandivli", 
    "Kanjur Marg", "Karjat", "Kasara", "Kasu", "Kelavli", "Kelve Road", "Khadavli", "Khandeshwar", "Khar Road", 
    "Kharbav", "Khardi", "Kharghar", "Kharkopar", "Khopoli", "King's Circle", "Kopar", "Koparkhairane", "Kurla", 
    "Lower Parel", "Lowjee", "Mahalaxmi", "Mahim Junction", "Malad", "Mankhurd", "Mansarovar", "Marine Lines", 
    "Masjid", "Matheran", "Matunga", "Matunga Road", "Mira Road", "Mohope", "Mulund", "Mumbai Central", "Mumbra", 
    "Nagothane", "Nahur", "Naigaon", "Nallasopara", "Navde Road", "Neral Junction", "Nerul", "Nhava Sheva", "Nidi", 
    "Nilaje", "Palasdari", "Palghar", "Panvel", "Parel", "Pen", "Prabhadevi", "Rabale", "Ram Mandir", "Ranjanpada", 
    "Rasayani", "Reay Road", "Roha", "Sandhurst Road", "Sanpada", "Santacruz", "Saphale", "Seawoods–Darave", "Sewri", 
    "Shahad", "Shelu", "Sion", "Somatne", "Taloje Panchnand", "Thakurli", "Thane", "Thansit", "Tilak Nagar", "Titwala", 
    "Turbhe", "Ulhasnagar", "Umbermali", "Umroli", "Uran", "Vaitarna", "Vangani", "Vangaon", "Vasai Road", "Vashi", 
    "Vasind", "Vidyavihar", "Vikhroli", "Vile Parle", "Virar", "Vithalwadi", "Wadala Road", "Water Pipe", "Gavan", 
    "Sagar Sangam", "Targhar"
]
 

#valid_cities = [city for cities in state_to_cities.values() for city in cities]

#valid_states = list(state_to_cities.keys())

 

if 'responses' not in st.session_state:

    st.session_state.responses = []

if 'language' not in st.session_state:

    st.session_state.language = ''

 

 

# ------------------------------- main function -------------------------#
station_one=''
def qna():

    response_list = []

    for question in question_list:

        question_translated = questions(question, src='en', dest=st.session_state.language)

        st.markdown(f"<div style='text-align: left; margin-bottom: 10px;'><b> 🤖 </b>{question_translated}</div>",

                    unsafe_allow_html=True)

        speak(question_translated, st.session_state.language)

        inp = takeresponse(st.session_state.language, question)

        while inp == 'None':

            inp = takeresponse(st.session_state.language, question)
            if inp in stations:
                station_one=inp
 

        # Translate the response back to English for validation

        inp_translated_en = translator.translate(inp, dest='en').text

        if question == 'What is the starting station':

            while inp_translated_en not in stations:

                st.warning("Please provide a valid station name.")

                inp = takeresponse(st.session_state.language, question)

                inp_translated_en = translator.translate(inp, dest='en').text
                station_one=inp_translated_en
                st.write(station_one)

 

        # Validate responses

        if question == 'What is your destination':

            while inp_translated_en not in stations:

                st.warning("Please provide a valid station name.")

                inp = takeresponse(st.session_state.language, question)

                inp_translated_en = translator.translate(inp, dest='en').text
                station_one=inp_translated_en
                st.write(station_one)
        #elif question == 'Chose between first and second class':

            #while inp_translated_en not in class_fs:

               # st.warning("Please provide a valid class.")

                #inp = takeresponse(st.session_state.language, question)

                #inp_translated_en = translator.translate(inp, dest='en').text

 

        translated_response_en = translator.translate(inp, dest='en').text

        response_list.append(translated_response_en)

        st.markdown(f"<div style='text-align: right; margin-bottom: 10px;'><b> 👤 </b> {inp}</div>",

                    unsafe_allow_html=True)

    # Save responses in session state

    st.session_state.responses = response_list
    return response_list

 

 

# ------------------------------------ rest of your code ------------------------------------ #

 

if st.button("🗣️"):

    with st.form("my_form"):

        speak_message.empty()

        query = identifylang()

        while query == 'None':

            query = identifylang()

        text_to_translate = translator.translate(query)

        language_code = text_to_translate.src

        st.info(f"Your detected language code is: {language_code}")

        st.session_state.language = text_to_translate.src

        response_list = qna()

        submit = st.form_submit_button("Submit")

 

if st.session_state.responses:

    st.session_state.responses = update_responses(st.session_state.responses)

 

    if st.button("Confirm and Log Responses"):

        all_responses = ' | '.join(st.session_state.responses)

        mapped_responses = []

        for response in st.session_state.responses:

            words = response.split()

            mapped_numbers = []

            for word in words:

                if word in MapNum:

                    mapped_numbers.append(MapNum[word])

                else:

                    mapped_numbers.append(word)

            mapped_response = ' '.join(mapped_numbers)

            mapped_responses.append(mapped_response)

        mapped_responses_str = ' | '.join(mapped_responses)

        log_conversation(mapped_responses_str)

        st.session_state.responses = []

        st.write("Responses have been logged.")


import streamlit as st
import pandas as pd
import qrcode
from io import BytesIO
from PIL import Image
import base64

# --- Read latest ticket data ---
def read_last_ticket_data():
    df = pd.read_csv('conversation_log.csv')
    if df.empty:
        st.error("CSV is empty.")
        return [None] * 7
    last_row = df.iloc[-1]
    timestamp = last_row['Timestamp']
    parts = last_row['User Responses'].split(" | ")
    if len(parts) < 6:
        st.error("Incorrect user response format.")
        return [None] * 7
    return timestamp, *parts

# --- Generate QR code with raw XML content and return base64 string ---
def generate_xml_qr_base64(timestamp, num_adults, num_children, ticket_class, start, dest, t_type):
    date, time = timestamp.split()
    xml = f"""
<Destination>{dest}</Destination>
<From>{start}</From>
<Adults>{num_adults}</Adults>
<Children>{num_children}</Children>
<Class>{ticket_class}</Class>
<Type>{t_type}</Type>
<Date>{date}</Date>
<Time>{time}</Time>
""".strip()
    qr = qrcode.make(xml)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode()
    return img_base64

# --- Get fare from CSV ---
def get_fare(start, dest):
    fares_df = pd.read_csv('mumbai_railway_fares.csv')
    match = fares_df[(fares_df['start'].str.lower() == start.lower()) & 
                     (fares_df['destination'].str.lower() == dest.lower())]
    if not match.empty:
        return float(match.iloc[0]['price'])
    return None

# --- Streamlit App ---
st.title("🎫 Railway Ticket")

if st.button("🎟️ Show My Ticket"):
    timestamp, num_adults, num_children, ticket_class, start, dest, t_type = read_last_ticket_data()

    if timestamp:
        date, time = timestamp.split()
        qr_base64 = generate_xml_qr_base64(timestamp, num_adults, num_children, ticket_class, start, dest, t_type)

        # Get fare
        fare_per_ticket = get_fare(start, dest)
        if fare_per_ticket is None:
            st.error(f"Fare data not found for {start} to {dest}")
        else:
            total_tickets = int(num_adults) + int(num_children)
            total_fare = total_tickets * fare_per_ticket

            st.markdown(
                f"""
                <div style="border:2px solid #1a2a6c; padding:20px; border-radius:15px; width: 500px; margin:auto; background-color: #f5f7fa; font-family:sans-serif; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                    <h2 style="text-align:center; color:#1a2a6c; margin-bottom: 10px;">🚆 TRAIN TICKET</h2>
                    <hr style="border:none; border-top:1px dashed #1a2a6c; margin:10px 0;">
                    <p style="text-align:center;"><strong>DATE:</strong> {date} &nbsp; | &nbsp; <strong>TIME:</strong> {time}</p>
                    <p style="text-align:center;"><strong>ADULTS:</strong> {num_adults} &nbsp; | &nbsp; <strong>CHILDREN:</strong> {num_children}</p>
                    <p style="text-align:center;"><strong>CLASS:</strong> {ticket_class}</p>
                    <p style="text-align:center;"><strong>FROM:</strong> {start} &nbsp; → &nbsp; <strong>TO:</strong> {dest}</p>
                    <p style="text-align:center;"><strong>TYPE:</strong> {t_type}</p>
                    <hr style="border:none; border-top:1px dashed #1a2a6c; margin:10px 0;">
                    <p style="text-align:center;"><strong>Fare per ticket:</strong> ₹{fare_per_ticket}</p>
                    <p style="text-align:center;"><strong>Total Tickets:</strong> {total_tickets}</p>
                    <p style="text-align:center; font-size:18px;"><strong>Total Price:</strong> ₹{total_fare}</p>
                    <div style="text-align:center; margin-top:20px;">
                        <img src="data:image/png;base64,{qr_base64}" width="160" alt="QR Code" style="background:#fff; padding:10px; border-radius:10px;" />
                        <p style="font-size:12px; color:gray;">Scan QR to view ticket in XML format</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )







import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Streamlit setup
# st.set_page_config(layout="wide")

# Function to get the latest start and end station from the conversation_log.csv
def get_last_stations():
    df = pd.read_csv('conversation_log.csv')
    
    # Split the 'User Responses' column and get start and end stations
    last_row = df.iloc[-1]['User Responses'].split(' | ')
    
    # Extract the start and end stations
    start_station = last_row[3].strip()  # 'Andheri' is at index 3
    end_station = last_row[4].strip()    # 'Dadar' is at index 4
    
    return start_station, end_station

# Initialize the Mumbai Railway Network graph
def create_mumbai_network():
    G = nx.Graph()
   
    # Central Line
    central_line = {
        "Chhatrapati Shivaji Maharaj Terminus": [("Masjid", 1.0)],
        "Masjid": [("Chhatrapati Shivaji Maharaj Terminus", 1.0), ("Sandhurst Road", 1.2)],
        "Sandhurst Road": [("Masjid", 1.2), ("Byculla", 1.5)],
        "Byculla": [("Sandhurst Road", 1.5), ("Chinchpokli", 1.5)],
        "Chinchpokli": [("Byculla", 1.5), ("Currey Road", 1.0)],
        "Currey Road": [("Chinchpokli", 1.0), ("Parel", 1.5)],
        "Parel": [("Currey Road", 1.5), ("Dadar", 1.5)],
        "Dadar": [("Parel", 1.5), ("Matunga", 1.5)],
        "Matunga": [("Dadar", 1.5), ("Sion", 1.0)],
        "Sion": [("Matunga", 1.0), ("Kurla", 3.0)],
        "Kurla": [("Sion", 3.0), ("Vidyavihar", 1.8)],
        "Vidyavihar": [("Kurla", 1.8), ("Ghatkopar", 2.0)],
        "Ghatkopar": [("Vidyavihar", 2.0), ("Vikhroli", 3.0)],
        "Vikhroli": [("Ghatkopar", 3.0), ("Kanjur Marg", 2.0)],
        "Kanjur Marg": [("Vikhroli", 2.0), ("Bhandup", 2.5)],
        "Bhandup": [("Kanjur Marg", 2.5), ("Nahur", 2.0)],
        "Nahur": [("Bhandup", 2.0), ("Mulund", 2.0)],
        "Mulund": [("Nahur", 2.0), ("Thane", 5.0)],
        "Thane": [("Mulund", 5.0), ("Kalwa", 6.0)],
        "Kalwa": [("Thane", 6.0), ("Mumbra", 2.0)],
        "Mumbra": [("Kalwa", 2.0), ("Diva Junction", 6.0)],
        "Diva Junction": [("Mumbra", 6.0), ("Kopar", 4.0)],
        "Kopar": [("Diva Junction", 4.0), ("Dombivli", 2.5)],
        "Dombivli": [("Kopar", 2.5), ("Thakurli", 2.5)],
        "Thakurli": [("Dombivli", 2.5), ("Kalyan Junction", 4.0)],
        "Kalyan Junction": [("Thakurli", 4.0)]
    }
 
    # Harbour Line
    harbour_line = {
        "Chhatrapati Shivaji Maharaj Terminus": [("Masjid", 1.0)],
        "Masjid": [("Chhatrapati Shivaji Maharaj Terminus", 1.0), ("Sandhurst Road", 1.2)],
        "Sandhurst Road": [("Masjid", 1.2), ("Dockyard Road", 1.5)],
        "Dockyard Road": [("Sandhurst Road", 1.5), ("Reay Road", 1.5)],
        "Reay Road": [("Dockyard Road", 1.5), ("Cotton Green", 1.2)],
        "Cotton Green": [("Reay Road", 1.2), ("Sewri", 1.1)],
        "Sewri": [("Cotton Green", 1.1), ("Wadala Road", 1.2)],
        "Wadala Road": [("Sewri", 1.2), ("Guru Tegh Bahadur Nagar", 1.5)],
        "Guru Tegh Bahadur Nagar": [("Wadala Road", 1.5), ("Chunabhatti", 1.5)],
        "Chunabhatti": [("Guru Tegh Bahadur Nagar", 1.5), ("Kurla", 2.0)],
        "Kurla": [("Chunabhatti", 2.0), ("Tilak Nagar", 1.0)],
        "Tilak Nagar": [("Kurla", 1.0), ("Chembur", 1.5)],
        "Chembur": [("Tilak Nagar", 1.5), ("Mankhurd", 2.5)],
        "Mankhurd": [("Chembur", 2.5), ("Vashi", 2.0)],
        "Vashi": [("Mankhurd", 2.0), ("Sanpada", 2.0)],
        "Sanpada": [("Vashi", 2.0), ("Panvel", 3.5)]
    }
 
    # Create nodes and edges for Central and Harbour Lines
    for line in [central_line, harbour_line]:
        for station, neighbors in line.items():
            for neighbor, distance in neighbors:
                G.add_edge(station, neighbor, weight=distance)
 
    # Western Line (simple list for demo)
    stations_western = [
        "Churchgate", "Marine Lines", "Charni Road", "Grant Road", "Mumbai Central", "Mahalaxmi",
        "Lower Parel", "Prabhadevi", "Dadar_W", "Matunga Road", "Mahim Junction", "Bandra",
        "Khar Road", "Santacruz", "Vile Parle", "Andheri", "Jogeshwari", "Ram Mandir",
        "Goregaon", "Malad", "Kandivli", "Borivali", "Dahisar", "Mira Road", "Bhayandar",
        "Naigaon", "Vasai Road", "Nallasopara", "Virar"
    ]
   
    western_distances = [1, 1, 1, 2, 1.5, 1.5, 1.5, 2, 1.5, 2, 3, 1.5, 1.5, 2, 3, 2.5, 1.5, 2, 3, 3, 3.5, 4, 4, 2.5, 4]
    for i in range(len(western_distances)):
        G.add_edge(stations_western[i], stations_western[i + 1], weight=western_distances[i])
 
    # Metro Line 1
    G.add_edge("Ghatkopar", "Andheri", weight=12.0)
    return G
 
# Visualize the entire network
def draw_graph(G, pos):
    plt.figure(figsize=(16, 12))
    nx.draw_networkx_nodes(G, pos, node_size=200, node_color="skyblue", alpha=0.8)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=2, alpha=0.5, edge_color="black")
    nx.draw_networkx_labels(G, pos, font_size=8, font_color="black", font_weight="bold")
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6, font_color="red")
    plt.axis('off')
    st.pyplot(plt)
 
# Streamlit main logic
def main():
    st.title("Mumbai Railway Network Visualization")
    G = create_mumbai_network()
 
    # Get the latest start and end stations from the CSV
    start_station, end_station = get_last_stations()
    st.write(f"Start Station: {start_station} | End Station: {end_station}")
   
    # Button for generating and displaying the subgraph
    if st.button("Generate Subgraph"):
        if nx.has_path(G, start_station, end_station):
            path = nx.shortest_path(G, source=start_station, target=end_station)
            subgraph = G.subgraph(path)
            st.write(f"Path from **{start_station}** to **{end_station}**: {' -> '.join(path)}")
 
            plt.figure(figsize=(10, 8))
            nx.draw(subgraph, pos=nx.spring_layout(subgraph), with_labels=True, node_color="skyblue", edge_color="gray")
            st.pyplot(plt)
        else:
            st.error(f"No path exists between {start_station} and {end_station}.")
 
if __name__ == "__main__":
    main()
