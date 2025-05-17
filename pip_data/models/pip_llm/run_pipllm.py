from pip_ai import PipAI

ai = PipAI()

while True:
    user_input = input("You: ")
    response = ai.get_ai_response(user_input)
    print("PipAI:", response)
