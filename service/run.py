import argparse
import json
import logging
import time

from sanic import Sanic
from sanic.exceptions import InvalidUsage
from sanic.response import json

from tipsi_tools.tipsi_logging import setup_logger

from service.functions import ackermann, factorial, fibonacci

app = Sanic()
setup_logger('interview_service')
log = logging.getLogger('service')


def validate_int(n, _min, _max):
    return _max >= n >= _min


def validate_params(*args):
    for params in args:
        if not validate_int(*params):
            nums = ', '.join([str(x[0]) for x in args])
            log.warning(f'Param is out of range: {nums}')
            raise InvalidUsage(json.dumps({'error': f'invalid number: {params[0]}'}))


def generic_response(what):
    """
    we're converting int's to string due json limitations for int values
    """
    return json({'response': str(what)})


@app.middleware('request')
def before_request(request):
    request.headers['start_time'] = time.time()


@app.middleware('response')
def after_request(request, response):
    total_time = time.time() - request.headers['start_time']
    extra = {'total_time': total_time}
    log.info(f'Request served {total_time:.4}', extra=extra)


@app.route("/fibonacci/<n:int>/")
async def fibonacci_view(request, n):
    """
    We're limiting n to 400 to not deal with stack things.
    In general, because of caching we can do bigger numbers in several attempts
    or increase by calling sys.setrecursionlimit
    """
    validate_params([n, 0, 400])
    log.debug(f'Calculate fibonacci for {n}')
    return generic_response(fibonacci(n))


@app.route("/ackermann/<m:int>/<n:int>/")
async def ackermann_view(request, m, n):
    """
    We don't want to deal with deeply nested recursion stack for this particular task
    So we're doing quite restricted subset of caluclations: 0 <= m <= 3 and 0 <= n <= 4
    """
    validate_params([m, 0, 3], [n, 0, 4])
    log.debug(f'Calculate ackermann for {m}, {n}')
    return generic_response(ackermann(m, n))


@app.route("/factorial/<n:int>/")
async def factorial_view(request, n):
    """
    We're limiting values to 0 <= n <= 400 to make response time acceptable
    """
    validate_params([n, 0, 400])
    log.debug(f'Calculate factorial for {n}')
    return generic_response(factorial(n))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=80)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    app.run(host="0.0.0.0", port=args.port)
