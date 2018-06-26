from run import main_func, parse_func, grep_email
from flask import Flask, request, render_template
app = Flask(__name__)


@app.route("/", methods=('GET', 'POST'))
def hello():
    error = 'введите валидный URL'
    if request.method == 'POST':
        url = request.form['url']
        if url == '':
            return render_template('main.html', error=error)
        text = main_func(url)
        zvr = parse_func(text)
        if zvr in ['Ошибка соединения', '', 'Таблица ЗВР не найдена']:
            return render_template('main.html', error=zvr)
        email = grep_email(text)
        return render_template('main.html', text=zvr, email=email)
    return render_template('main.html')

