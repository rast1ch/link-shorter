from flask import Flask
import flask
import requests
import json

from werkzeug.exceptions import abort

from wtforms import validators, Form, StringField

app = Flask(__name__)


class CreationForm(Form):
    url_to = StringField('URL', [validators.Lenght(min=5,max=200)])


@app.route('/',methods=['GET', 'POST'])
def home():
    form = CreationForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            ready_json = json.dumps({"link_to":form.url_to.data})
        except Exception:
            pass
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
        return flask.redirect(link_to)
    else:
        abort(404)

        
@app.route('/info/<tocken>')
def info(tocken):
    r = requests.get(url=f'http://127.0.0.1:8000/api/info/{tocken}')
    if r.status_code == 200:
        api_dict = json.loads(r.content)
        data = {'tocken' : api_dict['tocken'],
                'url' : 'http://127.0.0.1:5000/'+api_dict['url_tocken'],
                'link_to' : api_dict['link_to']}
        return flask.render_template('', data=data)

@app.route('/delete/<tocken>')
def delete(tocken):
    
    r = requests.delete(url=f'http://127.0.0.1:8000/api/delete/{tocken}')
    if r.status_code == 204:
        return flask.redirect('http://127.0.0.1:5000/')
    else:
        abort(404)
    


if __name__ == '__main__':
    app.run(debug=True)
    