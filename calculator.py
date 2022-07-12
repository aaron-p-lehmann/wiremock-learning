from flask import Flask, render_template, request
import re
from requests import get

app = Flask(__name__)
paren_re = re.compile(r"\((?P<paren>[-+*/\d]+)\)")
mult_re = re.compile(r"(?P<mult>[\d]+[*\][\d]+)")
add_re = re.compile(r"(?P<add>[\d]+[-+][\d]+)")


@app.route("/add")
def add():
    expression = request.args.get("expression", "")
    if expression:
        add_matches = add_re.search(expression)
        while add_matches:
            expression = expression[0:add_matches.start()] + str(eval(add_matches.groupdict()["add"])) + expression[add_matches.end():]
            add_matches = add_re.search(expression)
    else:
        expression = "0"
    return expression


@app.route("/mult")
def mult():
    expression = request.args.get("expression", "")
    if expression:
        mult_matches = mult_re.search(expression)
        while mult_matches:
            expression = expression[0:mult_matches.start()] + str(eval(mult_matches.groupdict()["mult"])) + expression[mult_matches.end():]
            mult_matches = mult_re.search(expression)
    else:
        expression = "0"
    return expression


@app.route("/parens")
def parens():
    expression = request.args.get("expression", "")
    if expression:
        paren_matches = paren_re.search(expression)
        while paren_matches:
            no_mult = get(
                "http://mult/mult",
                params={"expression": paren_matches.groupdict()["paren"]}).text
            no_add = get(
                "http://add/add",
                params={"expression": no_mult}).text
            expression = expression[0:paren_matches.start()] + no_add + expression[paren_matches.end():]
            paren_matches = paren_re.search(expression)
    else:
        expression = "0"
    return expression


@app.route("/calculate")
def calculate():
    expression = request.args.get("expression", "")
    if expression:
        expression = get("http://parens/parens", params={"expression": expression}).text
        app.logger.debug("after parens: {}".format(expression))
        expression = get("http://mult/mult", params={"expression": expression}).text
        app.logger.debug("after mult: {}".format(expression))
        expression = get("http://add/add", params={"expression": expression}).text
        app.logger.debug("after add: {}".format(expression))
    else:
        expression = "0"
    return expression


@app.route("/", methods=["GET", "POST"])
def ui():
    expression = "".join(request.form.get("expression", "").split())
    if expression:
        app.logger.debug("ui: {}".format(expression))
        expression = get("http://calculate/calculate", params={"expression": expression}).text
    return render_template(
        "index.html",
        result=expression)
