import time
import openai
import os
from config import OPENAI_API_KEY
from dotenv import load_dotenv
from logger import logger

client = openai.OpenAI(api_key = OPENAI_API_KEY)

def get_openai_response(user_input):
    """Try to get a response, and retry after a delay if rate limit is hit."""
    for _ in range(3):  # Attempt up to 3 retries
        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a Joe from Nigeria."},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=50,
                temperature=0.7
            )
            return completion.choices[0].message.content.strip()
        except openai.RateLimitError as e:
            logger.error(f"Rate limit hit: {e}; -- Retrying in 5 seconds...")
            time.sleep(5)  # Wait before retrying
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
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