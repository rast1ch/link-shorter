

from flask import Flask
import flask
from flask import request
import requests
import json

from werkzeug.exceptions import abort

from wtforms import validators, Form, StringField

app = Flask(__name__)


class CreationForm(Form):
    url_to = StringField('URL', [validators.Length(min=5, max=200)])


class SearchForm(Form):
    tocken = StringField('tocken', [validators.Length(min=10, max=50)])


@app.route('/', methods=['GET', 'POST'])
def home():
    form = CreationForm(request.form)
    if request.method == 'POST' and form.validate():
        ready_json = {"link_to": form.url_to.data}
        r = requests.post(url='http://127.0.0.1:8000/api/create/', json=ready_json)
        if r.status_code == 201:
            api_dict = json.loads(r.content)
            tocken = api_dict['tocken']
            return flask.redirect(f'http://127.0.0.1:5000/info/{tocken}')

    return flask.render_template('index.html', form=form)


@app.route('/<slug>')
def redirect(slug):
    r = requests.get(url=f'http://127.0.0.1:8000/api/get_slug/{slug}')
    if r.status_code == 200:
        api_dict = json.loads(r.content)
        link_to = api_dict['link_to']
        requests.get(url=f'http://127.0.0.1:8000/api/jump/{slug}')
        return flask.redirect(link_to)
    else:
        abort(404)


@app.route('/info/<tocken>')
def info(tocken):
    r = requests.get(url=f'http://127.0.0.1:8000/api/info/{tocken}')
    if r.status_code == 200:
        api_dict = json.loads(r.content)
        format_time = lambda x: x[:10] + ' ' + x[11:19]
        jumps = []

        for i in api_dict['jumps']:
            jumps.append({'order': i['order'],
                          'time': format_time(i['time'])})
        data = {'tocken': api_dict['tocken'],
                'url': 'http://127.0.0.1:5000/' + api_dict['url_tocken'],
                'link_to': api_dict['link_to'],
                'jumps': jumps
                }

        return flask.render_template('info.html', data=data)


@app.route('/update/<tocken>', methods=['GET', 'POST'])
def update(tocken):
    r = requests.get(url=f'http://127.0.0.1:8000/api/info/{tocken}')
    if r.status_code == 200:
        api_dict = json.loads(r.content)
        form = CreationForm(request.form)
        if request.method == 'GET':
            form.url_to.data = api_dict['link_to']
        elif request.method == 'POST' and form.validate():
            data = json.dumps({'link_to': form.url_to.data})
            r = requests.put(url=f'http://127.0.0.1:8000/api/update/{tocken}', json=data)
            if r.status_code == 200:
                return flask.redirect(f'http://127.0.0.1:5000/info/{tocken}')
        return flask.render_template('update.html', data={'form': form,
                                                          'tocken': api_dict['tocken'],
                                                          'url': 'http://127.0.0.1:5000/' + api_dict['url_tocken']})
    else:
        abort(404)


@app.route('/delete/<tocken>')
def delete(tocken):
    r = requests.delete(url=f'http://127.0.0.1:8000/api/delete/{tocken}')
    if r.status_code == 204:
        return flask.redirect('http://127.0.0.1:5000/')
    else:
        abort(404)


@app.route('/search', methods=['GET','POST'])
def search_by_tocken():
    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate():
        r = requests.get(url=f'http://127.0.0.1:8000/api/info/{form.tocken.data}')
        if r.status_code == 200:
            return flask.redirect(f'http://127.0.0.1:5000/info/{form.tocken.data}')
        else:
            abort(404)

    return flask.render_template('search.html', data={'form':form})


if __name__ == '__main__':
    app.run(debug=True)
