#coding=utf-8
#
# from flask import Flask
#
# app = Flask("test")
#
# @app.route("/")
# def test(a):
#     return "haha"
#
# app.run(host="127.0.0.1",port=12321)

def test(a,b,c, d=5):
    x=5
    y=6
    print(a,b,c)

import inspect
sig = inspect.signature(test)
print()