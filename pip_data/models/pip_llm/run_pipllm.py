from pipeline import TinyLLM
from pip_ai import get_response

llm = TinyLLM()

print("Pip is online!")

while True:
    try:
        user_input = input("You: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            break

        reply = get_response(user_input)
        print("Pip:", reply)

    except KeyboardInterrupt:
        break
