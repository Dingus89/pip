from pip_ai import PipAi

ai = PipAi()

while True:
    user_input = input("You: ")
    response = ai.get_ai_response(user_input)
    print("PipAi:", response)
