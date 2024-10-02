import streamlit as st
from time import sleep
import os
from st_audiorec import st_audiorec
import wave
from streamlit.components.v1 import html
import audiotext
import imagetext
import textimage
from PIL import Image
from openai import OpenAI
import google.generativeai as genai

st.set_page_config(page_title="Vision of Voice", page_icon="🎤", layout="wide") #making my page title, icon and layout here
st.image("./media/cover.png", width=1500) #cover image
#creating a folder called img, if it doesnt already exist, then listing all image files from that folder.
img_folder = './img'
if not os.path.exists(img_folder):
    os.makedirs(img_folder)
images = [f for f in os.listdir(img_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]

#creating a sidebar that prompts users to enter their openai and google genai api keys, providing relevant information and helpful links.
with st.sidebar:
    st.info("""Please enter your API keys below, API keys are required to use the OpenAI and Google GenerativeAI APIs. They are not saved or stored anywhere.
    \n * [Get an OpenAI API key](https://platform.openai.com/account/api-keys)
    \n * [Get an GoogleAI API key](https://console.cloud.google.com/apis/credentials)
    \n * [View the source code](https://github.com/HuseyinBaytar/VisionOfVoice)
    """)
    open_ai_key = st.text_input("OpenAI API Key", type="password", help="Get your API key from https://platform.openai.com/account/api-keys")
    gen_ai_key = st.text_input("Google GenerativeAI API Key", type="password", help="Get your API key from https://console.cloud.google.com/apis/credentials")

    if not open_ai_key:
        st.error("Please add your OpenAI API key to continue.")
    else:
        client_openai = OpenAI(api_key=open_ai_key)

    if not gen_ai_key:
        st.error("Please add your GoogleAI API key to continue.")
    else:
        genai.configure(api_key=gen_ai_key)
        client_genai = genai.GenerativeModel(model_name="gemini-1.5-flash")
    #in here we check the openai and gen ai api keys are provided, if not ,it displays and error message. it initializes the respective clients for openai and google genai model.
    if len(images) > 0:
        st.sidebar.title("🖼️ Images that created before")
        sidecol1, sidecol2 = st.columns([1, 1])
        for i, img_file in enumerate(images):
            img_path = os.path.join(img_folder, img_file)
            img = Image.open(img_path)

            if i % 2 == 0:
                sidecol1.image(img, caption=None, width=100)
                sidecol1.markdown(f"[{img_file}]({img_path})")
            else:
                sidecol2.image(img, caption=None, width=100)
                sidecol2.markdown(f"[{img_file}]({img_path})")
    #we check if there any images in the images list, if so it displays the image in the sidebar using two columns, alternating their placement and provides links to their respective
    #file paths.
if "latest_image" not in st.session_state:
    st.session_state["latest_image"] = None
    st.session_state["messages"] = []

if "recording_status" not in st.session_state:
    st.session_state["recording_status"] = "🎙️  Please record an audio."
    st.session_state["control"] = "✔️ Ready to record!"

def update_recording_status(status):
    st.session_state["control"] = status

#initializing seassion state variables to track the last image, message, recording status and control status, ensuring they're set if they dont already exist
def describe_image():
    if st.session_state["latest_image"] is not None:
        with col_image:
            with st.spinner("🔍 Describing image..."):
                image_description = image_to_text.gemini_vision_img_to_text(client_genai, st.session_state["latest_image"])
                st.session_state["messages"].append({"role": "bot", "content": image_description})
    else:
        update_recording_status("🚫 No image to describe!")
#function that checks if there is a lastest_image avaible. if so , it describes the image using the gemini_vision_img_to_text method and appends the description to the session messages,
#otherwise, it updates the recording status to indicate that there is no image to describe

def save_audio():
    if wav_audio_data is not None:
        update_recording_status("✅ Audio is valid!")
        sound_file = wave.open("sound.wav", "wb")  # Open sound file in write binary mode
        sound_file.setnchannels(1)  # Set number of channels
        sound_file.setsampwidth(4)  # Set sample width
        sound_file.setframerate(44100)  # Set frame rate
        sound_file.writeframes(wav_audio_data)  # Write frames to file, because frames is list of bytes
        sound_file.close()
    else:
        update_recording_status("🔇 No audio recorded!")
#here we check if audio data exist, if it does it saves the audio to a WAV file with specified parameters and updates the recording status to indicate that the audio is valid, otherwise, it
#updates the status to indicate no audio was recorded

def script():
    with open("./script.js", "r", encoding="utf-8") as scripts:
        open_script = f"""<script>{scripts.read()}</script> """
        html(open_script, width=0, height=0)
#function reads a JavaScript file, embeds its content into a <script> tag, and then renders it as HTML in the Streamlit app without displaying any visible output.

st.info("This app build for skill test, it allows you to convert your voice to an image. Then you can ask to Gemini Vision model to describe the image in every detail.")

col_audio, col_image = st.columns([1,3])
#making two columns on streamlit, first column is col_audio takip up 1 part of the width and the second column is col_image taking up 3 parts, alowing wider space for displaying.

with col_audio: #definin context for the col_audio
    st.divider()                                    #adds a visual divider in the column
    st.info(st.session_state["recording_status"])   #displays an information message using the current value of recording_status from the sesion state
    st.warning(st.session_state["control"])         #shows a warning message based on the value of control from the session state
    st.divider()                                    #adds a visual divider in the column

    subcol_left, subcol_right = st.columns([1,1])   #this line creates two sub columns within the col_audio column.

    with subcol_left:                               #begins a context for the left sub-columns.
        wav_audio_data = st_audiorec()                                              #calls the st_audiorec function to record audio, storing the resulting audio data in the variable wav_audio_data
        check_audio = st.button(label="Check Audio", on_click=save_audio)           #creates a button labed "check audio." when clicked, it triggers the save_audio function to handle the recorded audio.
        send_to_whisper = st.button(label="Send to AI")                             #adds another button labled "send to ai" which presumably sends the recorded audio for processing, though no specific action is tied to it in this line.
        describe = st.button(label="Describe Latest Image", on_click=describe_image) #creates a button labeled "describe lastest image" when clicked, it will call the describe_image function to provide description of the lastest imagine.
    with subcol_right:                                                               #begins a context for the right sub-column
        recorded_audio = st.empty()                                                  #create an empty placeholder in the right sub-column that can be updated later
        if check_audio & (wav_audio_data is not None):                               #checks if the check audio button was clicked and if there is valid audio data avaible
            recorded_audio.audio("sound.wav", format="audio/wav")                    #if the conditions in the previous line are met, this line plays the recoded audio file in the right sub-column.

with col_image:         #begins a context for the col_image columns, which allows you to place streamlit component and elements specific to this column
    st.divider()        #adds a vidual divider in the col_image column.

    for message in st.session_state["messages"]:                        #the line stars a loop that iterates over each message stored in the seassion_state["messages"] list
        if message["role"] == "assistant":                              #if the role of message is assistant. if true it executes the following block of code
            with st.chat_message(name=message["role"], avatar="🤖"):    #this line crates a chat message container for assistants response, displaying an avatar of robot
                st.image(image=message["content"], width=300)           #inside this block, the content of message is displayed with a width of 300 pixels
        elif message["role"] == "user":                                 # this check if the role of message is user. if true it executes following block.
            with st.chat_message(name=message["role"], avatar="👤"):    #creates a chat message container for the user's message, displaying an avatar of a user
                st.success(message["content"])                          #in this blokc, the user's message content is displayed as a success message
        elif message["role"] == "bot":                                  #this checks if the role of the message is bot, if true it executes the following block of code
            with st.chat_message(name=message["role"], avatar="🤖"):    #creates a message container for the bot's response and displaying an avatar of a robot
                st.info(message["content"])                             #in this block, bot's message content is displayed as an informational message

    if send_to_whisper & (wav_audio_data is not None):                                        #condition checks if the send_to_whisper button has been pressed and if there is recorded audio data. if both conditions are ture, it executes the following
        save_audio()                                                                     #this function call saves the recorded audio data to a file using the logic defined in the save_audio function
        update_recording_status("🤖 Sent to AI")                                         #updates the status in the streamplit app that the audio has been sent to the ai for processing.
        with st.chat_message(name="user", avatar="👤"):                                   #line creates a new chat message container that represents the user's message in the chat using avatar of a user.
            with st.spinner("📑 Converting audio to text..."):                            #creates a spinner that displays a loading message while  the audio is being processed.
                voice_prompt = audiotext.whisper_to_text(client_openai,audio_path="sound.wav") #line calls the whisper_to_text function from the audio text module passing in the openai client and the path to the saved audio file. it processes the audio file and converts it into text, storing the result in the variable voice_prompt
                st.success(voice_prompt)        #line displays the converted text as a success message in the streamlit app, indicating that the conversaion from audio to text.

        st.session_state["messages"].append({"role": "user", "content": voice_prompt})  #line adds a new message to the session state under the key "messages", indicating that the user has provided input. the message has a role of "user" and contains the text stored in the variable voice_prompt.
        with st.spinner("📷 Converting text to image..."):                            #creates a spinner to show a loading message while the text is being processed into a image.
            image = textimage.text_to_img_with_dall(client_openai, voice_prompt)   #it calls the text_to_img_with_dall function from the textimage module, passing in the openai client and text . it processes the text to generate an imagine, storing the result in the variable image.
            st.image(image, width=300)                                              #displays the generated image in the streamlit app with a specified width of 300 pixel
        st.session_state["messages"].append({"role": "assistant", "content": image})   #this one adds another message to session state under the key messages, indicatin that the ai has provided an output. the message has a role of assistant and contains the generated image.
        st.session_state["latest_image"] = image           # updates the session state by storing the most recently generated image in the key lastest_image making it accesible for other parts of the application
sleep(0.5) # this line pauses the execution of the program for 0.5 seconds. this could be used to give a brief moment before executing the next part of code.
script()    #this line calls the script function that has javascript code.