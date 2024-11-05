import time
import openai
import os
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

# Accessing the variables
OPENAI_API_KEY = os.getenv("OPENAI_KEY")
debug = os.getenv("DEBUG") == "True"

client = openai.OpenAI(api_key = OPENAI_API_KEY)

def get_openai_response(user_input):
    """Try to get a response, and retry after a delay if rate limit is hit."""
    for _ in range(3):  # Attempt up to 3 retries
        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=50,
                temperature=0.7
            )
            return completion.choices[0].message.content.strip()
        except openai.RateLimitError as e:
            print("Rate limit hit. Retrying in 5 seconds...")
            time.sleep(5)  # Wait before retrying
        except Exception as e:
            return f"Error communicating with OpenAI API: {e}"
    return "Failed to get response after multiple attempts."

# Example usage
def main():
    print("Chat with OpenAI! Type 'exit' to end the conversation.")
    
    while True:
        # Get user input
        user_input = input("You: ")
        
        if user_input.lower() == "exit":
            print("Ending the conversation.")
            break
        
        # Get OpenAI's response
        response = get_openai_response(user_input)
        
        # Display the response
        print("OpenAI:", response)

if __name__ == "__main__":
    main()