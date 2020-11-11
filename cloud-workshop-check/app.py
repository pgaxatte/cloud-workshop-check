import os

from abc import ABC, abstractmethod
from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class WorkshopValidator(ABC):
    def __init__(self, expected, msg):
        self.expected = expected
        self.msg = msg

    @abstractmethod
    def validate(self, answer):
        pass

class StringValidator(WorkshopValidator):
    def validate(self, answer):
        if answer == self.expected:
            return True, "OK"
        return False, self.msg

class ListValidator(WorkshopValidator):
    def validate(self, answer):
        if answer in self.expected:
            return True, "OK"
        return False, self.msg

class Workshop(Resource):
    validators = {}

    def _results(messages, status):
        return make_response(jsonify({"results": messages}), status)

    def post(self):
        data = request.get_json()

        if data.get("project_id", "") == "":
            return results(["Empty project ID"], 400)
        del data["project_id"]

        errors = []
        for k, v in data.items():
            if k not in self.validators:
                errors.append("Unexpected answer type {}".format(k))
                continue

            ok, msg = self.validators[k].validate(v)
            if not ok:
                errors.append(msg)

        if len(errors) > 0:
            return self._results(errors, 400)
        return self._results(["OK"], 200)

class Workshop101(Workshop):
    validators = {
        "flavor": StringValidator("c2-7", "You used the wrong flavor"),
        "release": StringValidator("buster", "You used the wrong image"),
        "hostname": ListValidator(["vm01", "vm02"], "The name of your instance is incorrect"),
    }

class Workshop102(Workshop):
    validators = {
        "disk": StringValidator("c2-7", "You used the wrong flavor"),
        "mounts": StringValidator("buster", "You used the wrong image"),
        "hostname": ListValidator(["vm01", "vm02"], "The name of your instance is incorrect"),
    }

api.add_resource(Workshop101, '/101')

#if __name__ == "__main__":
#    app.run(debug=(os.environ.get("DEBUG", "0") == "1"))
