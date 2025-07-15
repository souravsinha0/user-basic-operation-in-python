import ollama
import subprocess
from llama_index.llms.ollama import Ollama
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool

import os
os.environ["OPENAI_API_KEY"] = "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"

#client = OpenAI(api_key = os.environ['OPENAI_API_KEY'])
#llm = Ollama(model="llama3.2", request_timeout=120.0)
llm = Ollama(model="hf.co/prithivMLmods/Llama-3.2-3B-Instruct-GGUF:F16", request_timeout=120.0)

def multiply(a: float, b: float) -> float:
    """Multiply two numbers and returns the product"""
    return a * b


multiply_tool = FunctionTool.from_defaults(fn=multiply)
def add(a: float, b: float) -> float:
    """Add two numbers and returns the sum"""
    return a + b


add_tool = FunctionTool.from_defaults(fn=add)

agent = ReActAgent.from_tools([multiply_tool, add_tool], llm=llm, verbose=True)
response = agent.chat("What is 20+(2*4)? Use a tool to calculate every step.")


