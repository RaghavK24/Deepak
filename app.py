# Flask code
from flask import Flask, render_template, request, jsonify
from chat import *

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        data = request.get_json()
        
        pre = data.get('messages')  # Use the correct key from your JSON data
        user_message = pre[0]['content']
        p = query(user_message)
        return jsonify({'response': p})

    except Exception as e:
        # Log the error
        app.logger.error("Error: %s", str(e))
        
        # Handle exceptions and return an error response
        return jsonify({'error': str(e)})
    
if __name__ == '__main__':
    app.run(debug=True)
