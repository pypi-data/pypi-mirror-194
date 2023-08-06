# MyPy8TML

<em><h6> A new way to create a html code inside python </em>

> Status of project: in progress...

<div align="center">
<a href="https://github.com/MikalROn/ApiOmie-nao-oficial" ><img alt="GitHub" src="https://img.shields.io/badge/Github-Open%20source-green?style=for-the-badge&amp;logo=github"></a>
<img src="https://img.shields.io/github/license/MikalROn/MyPy8TML?style=for-the-badge">
<a href="https://smokeshow.helpmanual.io/0c5m6z050r2w2d4t1n4n/"><img src="https://img.shields.io/badge/coverage-100%25-green?style=for-the-badge"></a>
</div>

## Download

````shell
$pip install mypy8tml
````

## Easy start

<em>Generating a simple code:</em>

````python
from mypy_8tml import MyPy8TML

html = MyPy8TML()
html.h1['Hello world']()
code = html.generate()
print(code)

````

- Use MyPy8TML( ) to start the class
- Call the property (name of tag)
- Put content betwen the tag using -> []
- close tag calling the class -> ()


## Using flask to render code

<h3> So let's do a form </h3>

<h6> Remember to download Flask firt</h6>

````shell
pip install flask
````

**Pyhton code:**

````python
from flask import Flask, render_template_string
from mypy_8tml import MyPy8TML

app = Flask(__name__)

register = MyPy8TML().init_html('Form', 'pt')

register.div.in_class('flex-box')\
        .form.in_class('form')\
            .h1[' Just a simple form']()\
            .p['e-mail :'](-1).input.in_type('email')()\
            .p['password :'](-1).input.in_type('password')()\
            .button.in_type('submit')['submit']()


@app.route('/')
def index():
    return render_template_string(register.generate())

app.run(debug=True)
````

<li>init_html creates a basic html structure </li>
<li>Call suports <em>int</em> values, and this values means, a number 
of times that tags will be closed</li>
<li><b>in_</b> prefix values puts contents inside tags like class, type, id and etc.</li>


