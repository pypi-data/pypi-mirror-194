import json
from unittest.mock import call


sb_server = ('my-host', 1234)


###########
# Helpers #
###########

def set_response(mocker, requests_post, params, result=None, player=''):
    content = {
                'method': 'slim.request',
                'params': [player, params],
                }
    if result is not None:
        content['result'] = result
    requests_post.return_value = mocker.MagicMock(content=json.dumps(content))


def set_responses(mocker, requests_post, params_results, player=''):
    responses = []
    for p_r in params_results:
        content = {
                'method': 'slim.request',
                'params': [player, p_r['params']],
                }
        try:
            content['result'] = p_r['result']
        except KeyError:
            pass
        responses.append(json.dumps(content))
    requests_post.side_effect = [mocker.MagicMock(content=r)
                                 for r in responses]


def assert_post(requests_post, params, player=''):
    host, port = sb_server
    requests_post.assert_called_once_with(
            f'http://{host}:{port}/jsonrpc.js',
            json={
                'method': 'slim.request',
                'params': [player, params],
                })


def assert_posts(requests_post, list_params, player=''):
    host, port = sb_server
    requests_post.assert_has_calls(
            [call(f'http://{host}:{port}/jsonrpc.js',
                  json={
                      'method': 'slim.request',
                      'params': [player, params],
                      })
             for params in list_params])
