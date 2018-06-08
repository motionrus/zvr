from run import main_func, parse_func
from flask import Flask, request, render_template
app = Flask(__name__)


@app.route("/generate", methods=('GET', 'POST'))
def hello():
    error = 'введите валидный URL'
    if request.method == 'POST':
        url = request.form['url']
        if url == '':
            return render_template('main.html', text=error)
        text = parse_func(main_func(url))
        return render_template('main.html', text=text)
    return render_template('main.html')

