import flask
app = flask.Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>AI-Powered Survey Tool</h1>
    <form action="/create_survey" method="post">
        <label for="question">Enter Survey Question:</label><br>
        <input type="text" id="question" name="question"><br><br>
        <input type="submit" value="Add Question">
    </form>
    '''

@app.route('/create_survey', methods=['POST'])
def create_survey():
    question = flask.request.form['question']
    return f'<h1>Survey Question Added</h1><p>{question}</p><a href="/">Back</a>'

if __name__ == '__main__':
    app.run(debug=True)