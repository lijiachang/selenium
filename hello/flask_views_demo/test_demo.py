# coding=utf-8
from flask import Flask, views, render_template, jsonify, request

app = Flask(__name__)
app.config.update({
    'DEBUG': True,
    'TEMPLATES_AUTO_RELOAD': True
})


@app.route('/')
def hello_world():
    return 'hello world!'


class CommonView(views.View):
    def __init__(self):
        self.context = {
            'username': 'dasheng',
            'age': 18
        }


class RegisterView(CommonView):
    def dispatch_request(self):
        self.context.update({
            'dasheng': '大圣'
        })
        return render_template('register.html', **self.context)


class LoginView(CommonView):
    def dispatch_request(self):
        return render_template('login.html', **self.context)


app.add_url_rule('/login/', view_func=LoginView.as_view('login'))
app.add_url_rule('/register/', view_func=RegisterView.as_view('register'))


# 如果url 想返回 json 数据
class JsonView(views.View):
    def get_data(self):
        raise NotImplementedError

    def dispatch_request(self):
        return jsonify(self.get_data())


class ListView(JsonView):
    def get_data(self):
        print request.values.to_dict()
        return request.values


app.add_url_rule('/list/', view_func=ListView.as_view('list123'))

if __name__ == '__main__':
    app.run()
