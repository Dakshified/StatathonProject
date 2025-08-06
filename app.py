import flask
app = flask.Flask(__name__)

# Simple translation dictionary
translations = {
    'en': {'welcome': 'Welcome to the AI-Powered Survey Tool', 'question_label': 'Enter Survey Question:', 'submit': 'Add Question', 'added': 'Survey Question Added', 'error': 'Error: Question cannot be empty or less than 5 characters.', 'id_label': 'Enter Identifier (e.g., Aadhaar/Phone):', 'prepopulate': 'Prepopulate Survey', 'adaptive': 'Adaptive Follow-up Added'},
    'hi': {'welcome': 'एआई-पावर्ड सर्वे टूल में आपका स्वागत है', 'question_label': 'सर्वे प्रश्न दर्ज करें:', 'submit': 'प्रश्न जोड़ें', 'added': 'सर्वे प्रश्न जोड़ा गया', 'error': 'त्रुटि: प्रश्न खाली नहीं हो सकता या 5 अक्षरों से कम नहीं हो सकता।', 'id_label': 'पहचानकर्ता दर्ज करें (जैसे, आधार/फोन):', 'prepopulate': 'सर्वे को पहले से भरें', 'adaptive': 'अनुकूली फॉलो-अप जोड़ा गया'}
}

# Mock database for prepopulation and adaptive logic
mock_data = {
    '123456789012': {'question': 'What is your age?', 'answer': '30', 'adaptive': 'Are you employed?'},
    '9876543210': {'question': 'What is your occupation?', 'answer': 'Engineer', 'adaptive': 'How many years of experience do you have?'}
}

@app.route('/', methods=['GET', 'POST'])
def home():
    language = flask.request.args.get('lang', 'en')
    trans = translations.get(language, translations['en'])
    if flask.request.method == 'POST':
        identifier = flask.request.form.get('identifier')
        if identifier and identifier in mock_data:
            question = mock_data[identifier]['question']
            adaptive_question = mock_data[identifier].get('adaptive', '')
            return f'<h1>{trans["prepopulate"]}</h1><p>Pre-filled Question: {question}</p><p>{trans["adaptive"]}: {adaptive_question}</p><a href="/?lang={language}">Back</a>'
        question = flask.request.form.get('question')
        if not question or len(question) < 5:
            return f'<h1>{trans["error"]}</h1><a href="/?lang={language}">Back</a>'
        return f'<h1>{trans["added"]}</h1><p>{question}</p><a href="/?lang={language}">Back</a>'
    return '''
    <h1>{welcome}</h1>
    <form action="/?lang={lang}" method="post">
        <label for="identifier">{id_label}</label><br>
        <input type="text" id="identifier" name="identifier"><br><br>
        <input type="submit" value="{prepopulate}">
    </form>
    <br>
    <form action="/?lang={lang}" method="post">
        <label for="question">{question_label}</label><br>
        <input type="text" id="question" name="question"><br><br>
        <input type="submit" value="{submit}">
    </form>
    <a href="/?lang=en">English</a> | <a href="/?lang=hi">हिंदी</a>
    '''.format(welcome=trans['welcome'], question_label=trans['question_label'], submit=trans['submit'], id_label=trans['id_label'], prepopulate=trans['prepopulate'], lang=language)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)