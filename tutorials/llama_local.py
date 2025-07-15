from langchain.agents import initialize_agent, Tool, AgentType
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.llms import LlamaCpp
from langchain.chains import LLMChain
import os
#C:\Users\SOURAV\llama.cpp\models\llama-2-13b-chat.ggmlv3.q4_0.bin
os.environ["LLAMA_MODEL_PATH"] = r"C:\Users\SOURAV\llama.cpp\models"
# Set the environment variables or set the path for the LLaMA model
llama_model_path = os.environ['LLAMA_MODEL_PATH']  # Change this to the path of your local LLaMA model

# Initialize the LLaMA model using LangChain
llama = LlamaCpp(model_path=llama_model_path)

# Define a simple tool (for this case, an action to answer questions)
def search_tool(query):
    # Example function that mimics searching or interacting with a database.
    # In a more complex setup, this could be a real database or API call.
    if query.lower() == "who is the president of the usa?":
        return "The President of the USA is Joe Biden."
    elif query.lower() == "what is the capital of France?":
        return "The capital of France is Paris."
    else:
        return "Sorry, I don't know the answer to that question."

# Define tools that the agent can use
tools = [
    Tool(
        name="SearchTool",
        func=search_tool,
        description="Use this tool to get answers to questions like 'Who is the President of the USA?'"
    ),
]

# Initialize the ReAct agent
agent = initialize_agent(
    tools,
    llama,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

def chat_with_react_agent():
    """
    Function for the user to interact with the LLaMA ReAct agent.
    """
    print("Hello! You can ask me anything. Type 'exit' to end the conversation.")
    
    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Pass the user input to the agent to process and respond
        response = agent.run(user_input)
        print(f"Agent: {response}")


if __name__ == "__main__":
    chat_with_react_agent()
