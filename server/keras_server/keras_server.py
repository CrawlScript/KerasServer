#coding=utf-8

import flask
from flask import Flask
from flask import request
from flask_cors import CORS
import json
import tensorflow as tf

import keras
from keras import Input
from keras.layers import Dense
import inspect
import numpy as np

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


class KerasServer(Flask):
    # def __init__(self, flask_app=None, **kwargs):
    #     # self.flask_app = flask_app
    #     if flask_app is not None:
    #         self.flask_app=flask_app
    #     else:
    #         app = Flask(**kwargs)

    def __init__(self, *args, **kwargs):
        super(KerasServer, self).__init__(*args, **kwargs)
        self.default_graph = None



    def _wrap_response(self, result_data):
        response = {
            "data": result_data
        }
        return json.dumps(response, cls=NumpyEncoder)

    def remote_api(self, rule, data_param_name="data", **kwargs):
        def make_view_func(func):
            def created_api():
                json_params_str = request.args.get(data_param_name)
                json_params = json.loads(json_params_str)
                # var_names = func.__code__.co_varnames
                sig = inspect.signature(func)
                var_names = sig._parameters.keys()
                params = [json_params[var_name] for var_name in var_names]
                result_data = func(*params)
                return self._wrap_response(result_data)

            def created_api_with_graph():
                if self.default_graph is None:
                    return created_api()
                else:
                    with self.default_graph.as_default():
                        return created_api()

            self.route(rule=rule, **kwargs)(created_api)
            return func

            # self.add_url_rule(rule, endpoint=created_endpoint)
        return make_view_func


    def run(self, *args, **kwargs):
        self.default_graph = tf.get_default_graph()
        super(KerasServer, self).run(*args, **kwargs)



server = KerasServer("test")


# x = tf.get_variable("x", initializer=5.0)
# sess = tf.Session()
# sess.run(tf.initialize_all_variables())

model = keras.models.Sequential()
model.add(Dense(5, activation="sigmoid", input_shape=(10,)))





@server.remote_api(rule="/")
def predict_label(features):
    features = np.array(features)
    return {
        "predict": model.predict(features),#.astype(np.float64),
        "msg": "good"
    }



server.run(host="127.0.0.1")

