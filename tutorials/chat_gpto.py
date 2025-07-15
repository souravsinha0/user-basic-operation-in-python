from openai import OpenAI


import os
os.environ["OPENAI_API_KEY"] = "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"
#OpenAI.api_key = os.environ['OPENAI_API_KEY']

#from openai import OpenAI
client = OpenAI(api_key = os.environ['OPENAI_API_KEY'])


#Initialization of chat headings:
messages = [{"role": "assistant", "content": "How can I help ?"}]

#display the headings
def display_chat_headings(messages):
    for message in messages:
        print(f"{message['role'].capitalize()}: {message['content']}")

#get assistant's response
def get_assistant_response(messages):
    reply = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": m["role"], "content": m["content"]} for m in messages
        ]
    )
    response = reply.choices[0].message.content
    return response

# Main chat loop
while True:
    #display headings
    display_chat_headings(messages)

    #collect user input
    prompt = input("User: ")
    messages.append({"role": "user", "content": prompt})

    #get assistant's response
    response = get_assistant_response(messages)
    messages.append({"role": "assistant", "content": response})

