from pipeline import TinyLLM

llm = TinyLLM()

print("Pip is ready. Type something!")

while True:
    try:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break
        response = llm.process(user_input)
        print("Pip:", response)
    except KeyboardInterrupt:
        break
