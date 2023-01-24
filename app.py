from flask import Flask
from flask import url_for
from flask import request
from flask import render_template
from markupsafe import escape
from markupsafe import Markup


#cmd : flask run // flask --app <filename> run
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

'''
아래 두 URL은 다른 의미를 가진다. 큰 차이는 / 의 유무다
이는 검색 엔진이 같은 페이지를 두 번 이상 인덱싱하는 것을 방지할 수 있다.
'''

#/Project/ : (/project)로 접근할 경우 (/project/) 로 리다이렉트한다
#파일 시스템의 폴더와 유사하다
@app.route("/project/")
def project():
    return 'The Project Page'

#/about : (/about/)로 접근할 경우 404 Not Found Error을 return한다
#파일 시스템의 파일의 경로와 유사하다
@app.route("/about")
def about():
    return 'The about Page'



'''
url_for()
특정 기능을 위한 URL을 생성하려면 url_for() 함수를 사용한다

url_for('route 함수 명', *변수명)
해당 route가 가지는 url 주소와 변수명을 포함한 주소값을 return 한다.

URL을 하드코딩하여 직접 구성하는 일보다 url_for을 이용하는 이유?
    1. 더 설명하기 쉬움
    2. URL을 수동으로 변경하지 않고 자동으로 변경 가능
    3. 특수 문자의 이스케이프 처리
    4. 생성 경로는 항상 절대 경로이며 상대 경로의 예상못한 동작을 방지
    5. URL 외부에 애플리케이션이 배치될 경우 
'''

@app.route("/testname/<testname>")
def testname(testname):
    url_result = url_for('testname', testname = 'shogle')
    return f'{testname}\'s files, URL:{url_result}'

with app.test_request_context():
    print(url_for('testname', testname = testname))


'''
HTTP Methods

app.route() 데코레이터는 기본적으로 GET 요청만 응답한다.
app.route() 데코레이터의 method 매개변수를 통해 다른 HTTP Method들을 제어할 수 있다.
'''

def do_the_login():
    return "Access Allow"

def fail_the_login():
    return "Access Denied"



'''
동적 웹 애플리케이션을 위해 정적 파일(Static files)들이 필요하다.
CSS, Js 등이 위치하게된다.
웹 서버가 이를 지원하는게 제일 이상적인 방법이지만 개발 도중엔 Flask도 이 기능을 지원한다.
패키지 또는 모듈 옆에 static 폴더를 만들면 /static 을 통해 사용할 수 있다.
url_for('static', filename='style.css')
'''

#Rendering Templates
#Python에서 HTML을 생성하는건 매우 고된 일이고, HTML 이스케이프를 일일히 수행해야하므로 번거롭다.
#이 때문에 Flask는 자동으로 Jinja2 Templete Engine을 구성했다.
#템플릿을 사용하여 모든 유형의 텍스트 파일을 생성할 수 있고 Markdown, 메일을 위한 평문이나 여러 것들도 당연히 생성할 수 있으며 주로 HTML파일을 생성할 것이다.
#templates 폴더에서 문서를 찾는다
@app.route("/hello/")
@app.route("/hello/<name>")
def hello_html(name=None):
    #name=escape()를 사용하였으나, render_template 함수는 자동으로 escape를 지원한다
    return render_template('hello.html', name=escape(name))


'''
Context Local과 Request 전역 변수
Flask의 Context는 request를 처리하거나 CLI 명령어를 처리하기 위해 필요한 정보를 저장하고 제공하기 위해 사용한다

아래 예제에서, 모든 요청에 대해 Request 전역 변수를 활용하는 것 같으나, Request 객체를 전역 변수로 사용할 수 없다
멀티 Thread 환경으로 어플리케이션이 동작할 때 모든 Thread가 같은 Request 객체에 접근시 Thread-Safe 하지 않다.
이때 Context 개념이 등장한다, Context를 활용하여 특정 변수를 전역 변수처럼 사용하지만 특정 단위(Thread, Process, Conrutine) 만 접근할 수 있다.
이를 Context Local이라 한다.
'''

with app.test_request_context('/hello', method='POST'):
    #with block을 사용하여 Request를 받으며 다른 작업을 할 수있다.
    assert request.path =='/hello'
    assert request.method == 'POST'

#Post http 구현 후 사용해볼 것
def valid_login(**krg):
    return 0

def log_the_user_in(**krg):
    return 0

@app.route("/login", methods = ['GET', 'POST'])
def login(): 
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    return render_template('login.html', error=error)



