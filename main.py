from flask import Flask, request
from groq import Groq  # Assuming you have the correct import for the Groq API

app = Flask(__name__)

# Initialize your history to keep track of conversations
history = [{"role": "system", "content": ""}]  # Add your system prompt if necessary


@app.route('/ai-chat', methods=['POST'])
def chat_with_ai():
    try:
        # Get the JSON data from the POST request
        data = request.get_json()
        if not data or 'prompt' not in data:
            return "No prompt provided", 400

        # Extract the prompt from the request
        prompt = data['prompt']

        # Append the user's prompt to the history
        history.append({"role": "user", "content": prompt})

        # Initialize the Groq client with your API key
        client = Groq(api_key="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")

        # Send the chat request to the Groq API
        chat_completion = client.chat.completions.create(
            messages=history,
            model="llama3-8b-8192"
        )

        # Retrieve the AI-generated response from the completion
        response = chat_completion.choices[0].message.content

        # Append the assistant's response to the history
        history.append({"role": "assistant", "content": response})

        # Return the AI response as plain text
        return response

    except Exception as e:
        # In case of an error, return the error message
        return "An error occurred: " + str(e), 500


if __name__ == '__main__':
    app.run(debug=True)
