from flask import Flask, request

app = Flask(__name__)

# Simple translation dictionary
translations = {
    'en': {
        'welcome': 'Welcome to the AI-Powered Survey Tool',
        'question_label': 'Enter Survey Question:',
        'submit': 'Add Question',
        'added': 'Survey Question Added',
        'error': 'Error: Question cannot be empty or less than 5 characters.',
        'id_label': 'Enter Identifier (e.g., Aadhaar/Phone):',
        'prepopulate': 'Prepopulate Survey',
        'adaptive': 'Adaptive Follow-up Added',
        'response_label': 'Enter Response:',
        'validation_error': 'Error: Response must be at least 2 characters.',
        'auto_coded': 'Auto-Coded Category:',
        'dashboard': 'Monitoring Dashboard',
        'progress': 'Surveys Completed: ',
        'quality': 'Quality Score: ',
        'chat_welcome': 'Chat with AI Avatar',
        'chat_message': 'Hello! How can I assist with your survey today?',
        'chat_response': 'Thank you for your input!'
    },
    'hi': {
        'welcome': 'एआई-पावर्ड सर्वे टूल में आपका स्वागत है',
        'question_label': 'सर्वे प्रश्न दर्ज करें:',
        'submit': 'प्रश्न जोड़ें',
        'added': 'सर्वे प्रश्न जोड़ा गया',
        'error': 'त्रुटि: प्रश्न खाली नहीं हो सकता या 5 अक्षरों से कम नहीं हो सकता।',
        'id_label': 'पहचानकर्ता दर्ज करें (जैसे, आधार/फोन):',
        'prepopulate': 'सर्वे को पहले से भरें',
        'adaptive': 'अनुकूली फॉलो-अप जोड़ा गया',
        'response_label': 'प्रतिक्रिया दर्ज करें:',
        'validation_error': 'त्रुटि: प्रतिक्रिया कम से कम 2 अक्षरों की होनी चाहिए।',
        'auto_coded': 'स्वचालित कोडित श्रेणी:',
        'dashboard': 'निगरानी डैशबोर्ड',
        'progress': 'पूर्ण सर्वेक्षण: ',
        'quality': 'गुणवत्ता स्कोर: ',
        'chat_welcome': 'एआई अवतार के साथ चैट करें',
        'chat_message': 'नमस्ते! आज मैं आपके सर्वे में कैसे सहायता कर सकता हूँ?',
        'chat_response': 'आपकी प्रतिक्रिया के लिए धन्यवाद!'
    }
}

# Mock database for prepopulation, adaptive logic, and dashboard
mock_data = {
    '123456789012': {'question': 'What is your age?', 'answer': '30', 'adaptive': 'Are you employed?'},
    '9876543210': {'question': 'What is your occupation?', 'answer': 'Engineer', 'adaptive': 'How many years of experience do you have?'}
}

# Track survey metrics
surveys_completed = 0
quality_score = 0.0

# Simple auto-coding rules
def auto_code_response(response):
    response = response.lower()
    if any(word in response for word in ['engineer', 'developer', 'technician']):
        return 'Technical'
    elif any(word in response for word in ['teacher', 'professor']):
        return 'Education'
    else:
        return 'Other'

@app.route('/', methods=['GET', 'POST'])
def home():
    global surveys_completed, quality_score
    language = request.args.get('lang', 'en')
    trans = translations.get(language, translations['en'])

    if request.method == 'POST':
        identifier = request.form.get('identifier')
        response = request.form.get('response', '')
        question = request.form.get('question', '')

        if identifier and identifier in mock_data:
            question_text = mock_data[identifier]['question']
            adaptive_question = mock_data[identifier].get('adaptive', '')

            if not response or len(response.strip()) < 2:
                return f'<h1>{trans["validation_error"]}</h1><a href="/?lang={language}">Back</a>'

            category = auto_code_response(response)
            surveys_completed += 1
            quality_score = min(1.0, quality_score + 0.1)

            return f'''
                <h1>{trans["prepopulate"]}</h1>
                <p>Pre-filled Question: {question_text}</p>
                <p>{trans["adaptive"]}: {adaptive_question}</p>
                <p>{trans["response_label"]} {response}</p>
                <p>{trans["auto_coded"]} {category}</p>
                <a href="/dashboard?lang={language}">View Dashboard</a> |
                <a href="/chat?lang={language}">Chat with AI</a>
            '''

        if not question or len(question.strip()) < 5:
            return f'<h1>{trans["error"]}</h1><a href="/?lang={language}">Back</a>'

        return f'<h1>{trans["added"]}</h1><p>{question}</p><a href="/?lang={language}">Back</a>'

    # GET method form
    return f'''
        <h1>{trans["welcome"]}</h1>
        <form method="POST">
            <label>{trans["question_label"]}</label><br>
            <input type="text" name="question"><br><br>

            <label>{trans["id_label"]}</label><br>
            <input type="text" name="identifier"><br><br>

            <label>{trans["response_label"]}</label><br>
            <input type="text" name="response"><br><br>

            <button type="submit">{trans["submit"]}</button>
        </form>
        <br>
        <a href="/dashboard?lang={language}">View Dashboard</a> |
        <a href="/chat?lang={language}">Chat with AI</a>
    '''

@app.route('/dashboard')
def dashboard():
    language = request.args.get('lang', 'en')
    trans = translations.get(language, translations['en'])

    return f'''
        <h1>{trans["dashboard"]}</h1>
        <p>{trans["progress"]}{surveys_completed}</p>
        <p>{trans["quality"]}{quality_score:.2f}</p>
        <a href="/?lang={language}">Back to Home</a>
    '''

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    language = request.args.get('lang', 'en')
    trans = translations.get(language, translations['en'])

    if request.method == 'POST':
        user_input = request.form.get('user_input', '')
        return f'''
            <h1>{trans["chat_welcome"]}</h1>
            <p>{trans["chat_message"]}</p>
            <p><strong>User:</strong> {user_input}</p>
            <p><strong>AI:</strong> {trans["chat_response"]}</p>
            <a href="/chat?lang={language}">Chat Again</a> |
            <a href="/?lang={language}">Back</a>
        '''

    return f'''
        <h1>{trans["chat_welcome"]}</h1>
        <p>{trans["chat_message"]}</p>
        <form method="POST" action="/chat?lang={language}">
            <label for="user_input">Your Message:</label><br>
            <input type="text" id="user_input" name="user_input"><br><br>
            <input type="submit" value="Send">
        </form>
        <a href="/?lang={language}">Back to Home</a>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
