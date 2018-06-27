from parse import main_func, parse_func, grep_email, get_forms_internet
from flask import Flask, request, render_template
app = Flask(__name__)


@app.route("/phone", methods=('GET', 'POST'))
def phone():
    error = 'введите валидный URL'
    if request.method == 'POST':
        url = request.form['url']
        if url == '':
            return render_template('phone_page.html', error=error)
        # collect zvr
        zvr = main_func(url)
        if 'error' in zvr:
            return render_template('phone_page.html', error=zvr['error'])
        if 'text' in zvr:
            text = parse_func(zvr['text'])
            if text == 'Таблица ЗВР не найдена':
                return render_template('phone_page.html', error=text)
            email = grep_email(zvr['text'])
            return render_template('phone_page.html', text=text, email=email)
    return render_template('phone_page.html')


@app.route("/", methods=('GET', 'POST'))
def internet():
    error = 'введите валидный URL'
    if request.method == 'POST':
        url = request.form['url']
        if url == '':
            return render_template('internet_page.html', error=error)
        zvr = main_func(url)
        if 'error' in zvr:
            return render_template('internet_page.html', error=zvr['error'])
        if 'text' in zvr:
            text = get_forms_internet(zvr['text'])
            if text == 'Таблица ЗВР не найдена':
                return render_template('internet_page.html', error=text)
            email = grep_email(zvr['text'])
            return render_template('internet_page.html', email=email, text=text)
    return render_template('internet_page.html')


