from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain.messages import SystemMessage
from langchain.agents import create_agent
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from src.tools.tools import tool_list

load_dotenv()

# llm = HuggingFaceEndpoint(
#     repo_id="Qwen/Qwen3.5-35B-A3B"
#     # temperature=0
# )

# model = ChatHuggingFace(llm=llm)

model = ChatGroq(model="llama-3.1-8b-instant")

messages = []

agent = create_agent(
    model=model,
    tools=tool_list,
    system_prompt=SystemMessage("""
        You are a financial assistant.

        Use the provided tools to answer questions about financial policies, tax regimes, and calculations.

        Rules:
        - Always use rag_search tool for queries related to budgets, savings schemes.
        - Always use the tax_calculator tool when asked to compute taxes.
        - Always use the calculator tool for all simple arithmetic calculations.
        - Do NOT invent numbers or perform calculations yourself. 
        - If you are asked for regime comparison for taxes for a given salary, 
          compute the taxes in both regimes using the tax_calculator tool and then use the calculator tool to compute the difference.
        - Do not use calculator tool unless user asks for calculation.
        - Always use complete content of tool's returned information to provide a complete and detailed answer to user.
        - Call rag_search once per question with a concise query and use the returned information to answer the question.
        - Do NOT use internet or your own information. Your answer must be solely based on the tools.
        
        Use the information returned by tools to answer the question.
        If the tools return no useful information, say you do not know.

        For greetings, respond politely and explain briefly how you can help.
        """)
)


if __name__ == "__main__":

    while True:

        query = input("\nAsk a question: ")

        if query == "exit":
            break
        
        messages.append({
            "role": "user",
            "content": query
        })
        
        response = agent.invoke({
            "messages": messages
        })
        
        assistant_message = response["messages"][-1]

        print("\nAnswer:\n")
        print(response)

        messages.append(assistant_message)