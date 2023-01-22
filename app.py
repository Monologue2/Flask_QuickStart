from flask import Flask
from flask import url_for
from markupsafe import escape

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