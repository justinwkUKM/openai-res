import gradio as gr
import openai, subprocess
import os
from gtts import gTTS

# get your apikey from file called key.txt
openai.api_key = open("key.txt", "r").read().strip("\n")
# latest chatgpt model
turbo3dot5="gpt-3.5-turbo"
lang='ms'
messages = [{"role": "system", "content": 'You are a Malaysian therapist. Your name is Yumna. Respond to all input in 25 words or less. Reply back in Malay language'}]

def transcribe(audio):
    global messages

    audio_filename_with_extension = audio + '.wav'
    os.rename(audio, audio_filename_with_extension)
    
    audio_file = open(audio_filename_with_extension, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    messages.append({"role": "user", "content": transcript["text"]})

    response = openai.ChatCompletion.create(model=turbo3dot5, messages=messages)

    system_message = response["choices"][0]["message"]
    messages.append(system_message)
    print(system_message)

    voice_file_name = 'answer.mp3'
    myobj = gTTS(text=system_message["content"], lang=lang, slow=False)
    myobj.save(voice_file_name)

    os.system("mpg123 " + voice_file_name)
    # subprocess.call(["say", system_message['content']])

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"
    return chat_transcript


ui = gr.Interface(fn=transcribe, 
                  inputs=[gr.Audio(source="microphone", type="filepath")], 
                  outputs="text")
ui.launch()
