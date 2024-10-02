#!/usr/bin/env python3

from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
import os
from flask import Flask, request, current_app, g, make_response, redirect, abort

app = Flask(__name__)

# Hook to store the application's path in a global variable for the lifetime of the request
@app.before_request
def app_path():
    g.path = os.path.abspath(os.getcwd())

@app.route('/')
def index():
    host = request.headers.get('Host')
    appname = current_app.name
    response_body = f'''
        <h1>The host for this page is {host}</h1>
        <h2>The name of this application is {appname}</h2>
        <h3>The path of this application on the user's device is {g.path}</h3>
    '''
    return make_response(response_body, 200)

@app.route('/print/<parameter>')
def print_parameter(parameter):
    print(parameter)  # Print the parameter to the console
    return make_response(parameter, 200)

@app.route('/count/<int:parameter>')
def count(parameter):
    count_output = '\n'.join(str(i) for i in range(parameter)) + '\n'
    return make_response(count_output, 200)

@app.route('/math/<int:num1>/<operation>/<int:num2>')
def math_operation(num1, operation, num2):
    if operation == '+':
        result = num1 + num2
    elif operation == '-':
        result = num1 - num2
    elif operation == '*':
        result = num1 * num2
    elif operation == 'div':
        if num2 == 0:
            return abort(400, "Cannot divide by zero")
        result = num1 / num2
    elif operation == '%':
        result = num1 % num2
    else:
        return abort(400, "Unsupported operation")
    
    return make_response(str(result), 200)

# Redirect example (you can uncomment this route to test)
# @app.route('/old-url')
# def redirect_example():
#     return redirect('http://www.new-url.com', code=302)

# Example of handling a missing resource
@app.route('/<stage_name>')
def get_name(stage_name):
    # Simulate a query; replace with real database logic
    stages = ['Stage1', 'Stage2', 'Stage3']
    if stage_name not in stages:
        return abort(404, f"{stage_name} not found.")
    return make_response(f'<h1>{stage_name} is an existing stage name!</h1>', 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
