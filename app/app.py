import asyncio
import json
from .agent import ConnectionAgent


async def main():
    # Initialize the agent with your Google Cloud details
    project_id = "eloquent-grail-459810-b5"
    location = "asia-east2"
    name = "ruchir_connection_agent"

    agent = ConnectionAgent(project_id=project_id, location=location, name=name)

    print("\n=== Connection Agent Chat Interface ===")
    print("Hello! I'm your electricity connection assistant. How can I help you today?")
    print("(Type 'exit' to end our conversation)")

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if user_input.lower() == 'exit':
                print("\nAssistant: Goodbye! Have a great day!")
                break

            # Send user input to agent and get response
            response = await agent.chat(user_input)

            if 'error' in response:
                print("\nAssistant: I apologize, but I encountered an error:", response['error'])
                print("Could you please rephrase that or try a different request?")
            else:
                # Print the agent's response
                print("\nAssistant:", response['agent_response'])

                # If there was an API action performed, show the results
                if 'api_response' in response:
                    print("\nAction Results:")
                    print(json.dumps(response['api_response'], indent=2))

        except KeyboardInterrupt:
            print("\nAssistant: Goodbye! Have a great day!")
            break
        except Exception as e:
            print(f"\nAssistant: I apologize, but something went wrong: {str(e)}")
            print("Let's try that again, shall we?")


if __name__ == "__main__":
    asyncio.run(main())