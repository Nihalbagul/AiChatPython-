from flask import Flask, request, jsonify
import json
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load service data
with open('chatbot_data.json', 'r') as f:
    service_data = json.load(f)

# OpenAI API key
openai.api_key = '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'  # Replace with your actual API key

def get_service_info(category, subcategory):
    for service in service_data['services']:
        if service['category'] == category:
            for sub in service['subcategories']:
                if sub['service'] == subcategory:
                    return sub
    return None
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # Get user message from request
        user_message = request.json.get('message')
        
        print(f"Received user message: {user_message}")
        
        if not user_message:
            return jsonify({"response": "No message provided"}), 400
        
        # Simple intent extraction (for demonstration)
        if "fix leaky faucet" in user_message.lower():
            category = "Plumbing Services"
            subcategory = "Fixing Leaks and Clogs"
            service_info = get_service_info(category, subcategory)
            
            if service_info:
                response = f"Here is the information on {subcategory}:\n"
                response += f"Minor Fixes: {service_info['minor_fixes']}\n"
                response += f"Average Cost: {service_info['average_cost']}\n"
                response += f"Replacement Time: {service_info['replacement_time']}"
            else:
                response = "Sorry, I couldn't find information on that service."
            
            # Use GPT-4 for more conversational responses
            gpt_prompt = f"User asked: {user_message}\n{response}\nNow respond conversationally as a chatbot."
            
            gpt_response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": gpt_prompt}
                ],
                max_tokens=150
            )
            
            print("GPT-4 response:", gpt_response)
            response_text = gpt_response.choices[0].message['content'].strip()
            return jsonify({"response": response_text})
        
        return jsonify({"response": "I didn't understand that. Can you ask about a specific service?"})
    
    except Exception as e:
        app.logger.error(f"Error: {e}", exc_info=True)
        return jsonify({"response": "An error occurred while processing your request."}), 500


if __name__ == '__main__':
    app.run(port=5000)
