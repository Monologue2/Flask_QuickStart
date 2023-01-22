from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def hello():
    return f"Hello World"

@app.route("/<name>")
def hello_world(name):
    print(name)
    return f"Hello, {escape(name)}!"

#default, String 값 허용, / 비허용
@app.route("/user/<username>")
def show_username(username):
    return f'User : {escape(username)}'

#int, 정수 사용 가능, 부동소수점 사용 불가
@app.route("/post/<int:post_id>")
def show_post(post_id):
    return f'Post {post_id}'

#float,부동소수점 사용 가능, 정수를 사용할 경우 허용되지 않음
@app.route("/float/<float:post_id>")
def show_float(post_id):
    return f'Post {post_id}'

#path, String과 / 를 허용, escape를 통해 injection 공격 예방
@app.route("/path/<path:subpath>")
def show_subpath(subpath):
    return f'Subpath {escape(subpath)}'


#아래 두 URL은 다른 의미를 가진다. 큰 차이는 / 의 유무이다
#/Project/ : (/project)로 접근할 경우 (/project/) 로 리다이렉트한다
#파일 시스템의 폴더와 유사하다
@app.route("/project/")
def project():
    return 'The Project Page'

#/about : (/about/)로 접근할 경우 404 Not Found Error을 return한다
#파일 시스템의 파일의 경로와 유사하다
@app.route('/about')
def about():
    return 'The about Page'