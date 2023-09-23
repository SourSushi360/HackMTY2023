from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Here, you can save the form data to a file, database, or perform any other actions.
        # For simplicity, we'll just print the data.
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Message: {message}")

        return "Form submitted successfully!"

if __name__ == '__main__':
    app.run(debug=True)
