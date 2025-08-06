import flask
app = flask.Flask(__name__)

# Simple translation dictionary
translations = {
    'en': {'welcome': 'Welcome to the AI-Powered Survey Tool', 'question_label': 'Enter Survey Question:', 'submit': 'Add Question', 'added': 'Survey Question Added', 'error': 'Error: Question cannot be empty or less than 5 characters.'},
    'hi': {'welcome': 'एआई-पावर्ड सर्वे टूल में आपका स्वागत है', 'question_label': 'सर्वे प्रश्न दर्ज करें:', 'submit': 'प्रश्न जोड़ें', 'added': 'सर्वे प्रश्न जोड़ा गया', 'error': 'त्रुटि: प्रश्न खाली नहीं हो सकता या 5 अक्षरों से कम नहीं हो सकता।'}
}

@app.route('/', methods=['GET', 'POST'])
def home():
    language = flask.request.args.get('lang', 'en')
    trans = translations.get(language, translations['en'])
    if flask.request.method == 'POST':
        question = flask.request.form['question']
        if not question or len(question) < 5:
            return f'<h1>{trans["error"]}</h1><a href="/?lang={language}">Back</a>'
        return f'<h1>{trans["added"]}</h1><p>{question}</p><a href="/?lang={language}">Back</a>'
    return '''
    <h1>{welcome}</h1>
    <form action="/?lang={lang}" method="post">
        <label for="question">{question_label}</label><br>
        <input type="text" id="question" name="question"><br><br>
        <input type="submit" value="{submit}">
    </form>
    <a href="/?lang=en">English</a> | <a href="/?lang=hi">हिंदी</a>
    '''.format(welcome=trans['welcome'], question_label=trans['question_label'], submit=trans['submit'], lang=language)

if __name__ == '__main__':
    app.run(debug=True)