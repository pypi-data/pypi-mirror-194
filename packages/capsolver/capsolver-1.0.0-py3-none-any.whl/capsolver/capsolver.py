import time

import capsolver.error
from capsolver.capsolver_object import CapsolverObject


class CapsolverRequest(CapsolverObject):

    @classmethod
    def get_retries(self):
        raise NotImplementedError()

    @classmethod
    def get_interval(self):
        raise NotImplementedError()

    @classmethod
    def post(cls, **params):
        return cls().request("post", "/createTask", {"task":params})

    @classmethod
    def get(cls, **params):
        for _ in range(cls.get_retries()):
            time.sleep(cls.get_interval())
            result = cls().request("post", "/getTaskResult", params)
            if result["status"]=="processing":
                continue
            return result
        raise capsolver.error.Timeout('Failed to get results')

    @classmethod
    def solve(cls, **params):
        r = cls.post(**params)
        if isinstance(r, capsolver.error.CapsolverError):
            raise r
        if r['status']=="ready":
            return r['solution']
        r = cls.get(taskId=r['taskId'])
        if isinstance(r, capsolver.error.CapsolverError):
            raise r
        return r['solution']

class RecognitionTask(CapsolverRequest):

    @classmethod
    def get_retries(self):
        return 120

    @classmethod
    def get_interval(self):
        return 1


class TokenTask(CapsolverRequest):

    @classmethod
    def get_retries(self):
        return 180

    @classmethod
    def get_interval(self):
        return 1


class Balance(CapsolverObject):

    @classmethod
    def get(cls, **params):
        r = cls().request("post", "/getBalance", params)
        if isinstance(r, capsolver.error.CapsolverError):
            raise r
        return r
