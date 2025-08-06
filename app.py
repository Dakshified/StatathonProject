import flask
import time
from flask import request

app = flask.Flask(__name__)

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
        'chat_response': 'Thank you for your input!',
        'paradata': 'Paradata Collected:',
        'quality_flag': 'Quality Flag: '
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
        'chat_response': 'आपकी प्रतिक्रिया के लिए धन्यवाद!',
        'paradata': 'पैराडेटा एकत्र किया गया:',
        'quality_flag': 'गुणवत्ता ध्वज: '
    }
}

# Mock database
mock_data = {
    '123456789012': {'question': 'What is your age?', 'answer': '30', 'adaptive': 'Are you employed?'},
    '9876543210': {'question': 'What is your occupation?', 'answer': 'Engineer', 'adaptive': 'How many years of experience do you have?'}
}

# Metrics
surveys_completed = 0
quality_score = 0.0

# Auto-coding
def auto_code_response(response):
    if any(word.lower() in response.lower() for word in ['engineer', 'developer', 'technician']):
        return 'Technical'
    elif any(word.lower() in response.lower() for word in ['teacher', 'professor']):
        return 'Education'
    else:
        return 'Other'

# Paradata collection
def collect_paradata():
    start_time = time.time()
    device = request.user_agent.string
    return {'time_taken': time.time() - start_time, 'device': device}

# Home page
@app.route('/', methods=['GET', 'POST'])
def home():
    global surveys_completed, quality_score
    language = request.args.get('lang', 'en')
    trans = translations.get(language, translations['en'])

    if request.method == 'POST':
        identifier = request.form.get('identifier')
        response = request.form.get('response', '')

        if identifier and identifier in mock_data:
            question = mock_data[identifier]['question']
            adaptive_question = mock_data[identifier].get('adaptive', '')
            if not response or len(response) < 2:
                return f'<h1>{trans["validation_error"]}</h1><a href="/?lang={language}">Back</a>'
            category = auto_code_response(response)
            paradata = collect_paradata()
            quality_flag = 'Good' if paradata['time_taken'] < 5 else 'Review'
            surveys_completed += 1
            quality_score = min(1.0, quality_score + 0.1)

            return f'''
                <h1>{trans["prepopulate"]}</h1>
                <p>Pre-filled Question: {question}</p>
                <p>{trans["adaptive"]} {adaptive_question}</p>
                <p>{trans["response_label"]} {response}</p>
                <p>{trans["auto_coded"]} {category}</p>
                <p>{trans["paradata"]} Time: {paradata["time_taken"]:.2f}s, Device: {paradata["device"]}</p>
                <p>{trans["quality_flag"]} {quality_flag}</p>
                <a href="/dashboard?lang={language}">View Dashboard</a> | <a href="/chat?lang={language}">Chat with AI</a>
            '''
        else:
            question = request.form.get('question')
            if not question or len(question) < 5:
                return f'<h1>{trans["error"]}</h1><a href="/?lang={language}">Back</a>'
            return f'<h1>{trans["added"]}</h1><p>{question}</p><a href="/?lang={language}">Back</a>'

    return f'''
        <h1>{trans["welcome"]}</h1>
        <form method="post">
            <label>{trans["id_label"]}</label><br>
            <input type="text" name="identifier"><br>
            <label>{trans["response_label"]}</label><br>
            <input type="text" name="response"><br><br>
            <input type="submit" value="{trans["prepopulate"]}">
        </form>
        <hr>
        <form method="post">
            <label>{trans["question_label"]}</label><br>
            <input type="text" name="question"><br><br>
            <input type="submit" value="{trans["submit"]}">
        </form>
        <a href="/dashboard?lang={language}">Dashboard</a> | <a href="/chat?lang={language}">Chat with AI</a>
    '''

# Dashboard route
@app.route('/dashboard')
def dashboard():
    global surveys_completed, quality_score
    language = request.args.get('lang', 'en')
    trans = translations.get(language, translations['en'])
    return f'''
        <h1>{trans["dashboard"]}</h1>
        <p>{trans["progress"]}{surveys_completed}</p>
        <p>{trans["quality"]}{quality_score:.2f}</p>
        <a href="/?lang={language}">Back to Home</a>
    '''

# Chat route
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    language = request.args.get('lang', 'en')
    trans = translations.get(language, translations['en'])

    if request.method == 'POST':
        user_input = request.form.get('user_input', '')
        return f'''
            <h1>{trans["chat_welcome"]}</h1>
            <p>{trans["chat_message"]}</p>
            <p>User: {user_input}</p>
            <p>AI: {trans["chat_response"]}</p>
            <a href="/chat?lang={language}">Chat Again</a> | <a href="/?lang={language}">Back</a>
        '''

    return f'''
        <h1>{trans["chat_welcome"]}</h1>
        <p>{trans["chat_message"]}</p>
        <form method="post" action="/chat?lang={language}">
            <label for="user_input">Your Message:</label><br>
            <input type="text" id="user_input" name="user_input"><br><br>
            <input type="submit" value="Send">
        </form>
        <a href="/?lang={language}">Back to Home</a>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
