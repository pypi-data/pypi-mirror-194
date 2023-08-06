import json
import requests


class ProtocolError(Exception):
    pass


def equal_convert_ints(lhs, rhs):
    if len(lhs) != len(rhs):
        return False
    for ls, r in zip(lhs, rhs):
        if ls == r:
            continue
        if int(ls) == int(r):
            continue
        return False
    return True


def send(server, params, player=''):
    host, port = server
    requests.post(
            f'http://{host}:{port}/jsonrpc.js',
            json={
                'method': 'slim.request',
                'params': [player, params],
                })
    # TODO: validate response?


def send_query(server, params, player=''):
    host, port = server
    response = requests.post
    response = requests.post(
            f'http://{host}:{port}/jsonrpc.js',
            json={
                'method': 'slim.request',
                'params': [player, params],
                })
    response = json.loads(response.content)
    return response['params'][-1]


def send_receive(server, params, loops=tuple(), player=''):
    host, port = server
    result = None
    while True:
        response = requests.post(
                f'http://{host}:{port}/jsonrpc.js',
                json={
                    'method': 'slim.request',
                    'params': [player, params],
                    })
        # TODO: check response.status or response.ok here?
        response = json.loads(response.content)
        match response['params']:
            case [player_, params_] if (player == player_
                                        and equal_convert_ints(params,
                                                               params_)):
                pass
            case [player_, [command_, start_, size_, *fields]] if (
                    player == player_
                    and [command_, int(start_), int(size_)] == params[:3]
                    and fields == params[3:]):
                pass
            case _:
                raise ProtocolError
        this_result = response.get('result', None)
        if not this_result:
            return result if result else {}
        try:
            command, start, size = params[:3]
            start = int(start)
            size = int(size)
            if result:
                loops_found = 0
                for loop_name in [f'{loop}_loop' for loop in loops]:
                    try:
                        result[loop_name].extend(this_result[loop_name])
                        loops_found += 1
                    except KeyError:
                        pass
                if loops_found == 0:
                    return result
            else:
                result = this_result
            params = [command, start + size, size] + params[3:]
        except ValueError:
            return this_result
