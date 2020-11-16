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

class TrueValidator(WorkshopValidator):
    def validate(self, answer):
        return True, "OK"

class Workshop(Resource):
    validators = {}

    def _results(self, messages, status):
        return make_response(jsonify({"results": messages}), status)

    def _extra_validations(self, data):
        return (True, "")

    def post(self):
        data = request.get_json()

        if data.get("project_id", "") == "":
            return self._results(["Empty project ID"], 400)
        del data["project_id"]

        if set(data.keys()) != set(self.validators.keys()):
            return self._results(["Missing answers"], 400)

        errors = []
        for k, v in data.items():
            if k not in self.validators:
                # Ignore missing validators
                continue

            ok, msg = self.validators[k].validate(v)
            if not ok:
                errors.append(msg)

        ok, msg = self._extra_validations(data)
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
        "disks": StringValidator("sdb,sdb1", "Your volume is not attached or it does not have a single partition"),
        "mounts": StringValidator("/dev/sdb1", "Your volume is not mounted on /mnt"),
        "hostname": ListValidator(["vm01", "vm02"], "The name of your instance is incorrect"),
    }

class Workshop103(Workshop):
    validators = {
        "ip_eth1": TrueValidator(None, None),
        "hostname": ListValidator(["vm01", "vm02"], "The name of your instance is incorrect"),
    }

    def _extra_validations(self, data):
        if (data.get("hostname", "") == "vm01" and data.get("ip_eth1", "") == "10.0.0.100") or (data.get("hostname", "") == "vm02" and data.get("ip_eth1", "") == "10.0.0.101"):
            return True, "OK"
        return False, "eth1 does not have the correct IP address"


api.add_resource(Workshop101, '/101')
api.add_resource(Workshop102, '/102')
api.add_resource(Workshop103, '/103')
