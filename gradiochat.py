# to get the chat responses
import openai
# to build the UI
import gradio as gr
# to get the token count
import tiktoken

# get your apikey from file called key.txt
openai.api_key = open("key.txt", "r").read().strip("\n")
# latest chatgpt model
turbo3dot5="gpt-3.5-turbo"

# maintain a chat history. this will be passed in every completion call.
message_history = [{"role":"user", "content":"You are an expert in Geography. You're very funny and reply with humor all the time. Repond to all the questions truthfully but with humor. If you do not know the answer then simply say I dont know. Do you understand?"},
                   {"role":"assistant", "content":"OK"}]
# method to collect no of token before making a call to openai
def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

# call the completion api and add response to message history
def predict(input, role="user"):
    message_history.append({"role":role, "content":input})
    num_tokens = num_tokens_from_string(str(message_history), "gpt2")
    print("num_tokens", num_tokens, "\n")
    
    #if token size is greater than 4K then do something smart. pop some messages from history or create a summary of message history and pass it.
    if num_tokens > 4000:
        del message_history[:2]
    
    completion = openai.ChatCompletion.create(
    model=turbo3dot5,
    messages=message_history, temperature=0.2,
    )

    reply_content = completion.choices[0].message.content
    print("reply_content",reply_content, "\n")
    # add the latest response to message history
    message_history.append({"role":"assistant", "content":reply_content})
    print("message_history",message_history, "\n")
    
    response = [(message_history[i]["content"], message_history[i+1]["content"]) for i in range(2, len(message_history)-1, 2)]
    print("response",response, "\n")



    return response



# setup gradio chatbot ui
with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Type your message here").style(container=False)
        txt.submit(predict, txt, chatbot)
        # clear ui when submit
        txt.submit(None, None, txt, _js="() => {''}")

demo.launch(share=False)
