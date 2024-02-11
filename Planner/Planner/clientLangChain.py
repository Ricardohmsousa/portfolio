import requests
from langserve import RemoteRunnable
from langchain_core.messages import HumanMessage, AIMessage

def main():
    remote_runnable = RemoteRunnable("http://localhost:8000/agent")
    chat_history = []

    while True:
        human = input("Human (Q/q to quit): ")
        if human in {"q", "Q"}:
            print('AI: Bye bye human')
            break

        ai =  remote_runnable.invoke({"input": human, "chat_history": chat_history})
        print(f"AI: {ai['output']}")
        chat_history.extend([HumanMessage(content=human), AIMessage(content=ai['output'])])

if __name__ == "__main__":
    import asyncio

    # Run the asynchronous event loop
    main()
