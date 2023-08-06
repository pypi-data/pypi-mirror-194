from .helpers import set_responses, assert_posts, \
        sb_server
from squeezebox_cli.core.protocol import send_receive


def test_send_receive(mocker, requests_post):
    set_responses(
            mocker,
            requests_post,
            [
                {
                    'result': {
                        'players_loop': [
                            {
                                'ip': '192.168.1.100:47935',
                                'model': 'fab4',
                                'playerindex': '0',
                                'isplayer': 1,
                                'playerid': '00:04:20:23:30:7f',
                                'displaytype': 'none',
                                'name': 'Lounge',
                                'power': 1,
                                'canpoweroff': 1,
                                'firmware': '7.8.0-r16754',
                                'uuid': 'b0ff501bdcff1d6a18e0965b23844c94',
                                'isplaying': 1,
                                'seq_no': '10',
                                'modelname': 'Squeezebox Touch',
                                'connected': 1
                                },
                            ],
                        'count': 1,
                        },
                    'params': ['players', '0', '100'],
                    },
                {
                    'result': {'count': 1},
                    'params': ['players', '100', '100'],
                    },
                ])
    assert {
            'players_loop': [
                {
                    'ip': '192.168.1.100:47935',
                    'model': 'fab4',
                    'playerindex': '0',
                    'isplayer': 1,
                    'playerid': '00:04:20:23:30:7f',
                    'displaytype': 'none',
                    'name': 'Lounge',
                    'power': 1,
                    'canpoweroff': 1,
                    'firmware': '7.8.0-r16754',
                    'uuid': 'b0ff501bdcff1d6a18e0965b23844c94',
                    'isplaying': 1,
                    'seq_no': '10',
                    'modelname': 'Squeezebox Touch',
                    'connected': 1
                    },
                ],
            'count': 1
            } == send_receive(
                    sb_server, ['players', 0, 100], loops=['players'])
    assert_posts(
            requests_post,
            [
                ['players', 0, 100],
                ['players', 100, 100],
                ])


def test_send_receive_chunked(mocker, requests_post):
    set_responses(mocker,
                  requests_post,
                  [
                      {
                          'result': {
                              'players_loop': [
                                  {'p': 0},
                                  {'p': 1},
                                  ],
                              'count': 5,
                              },
                          'params': ['players', 0, 2],
                          },
                      {
                          'result': {
                              'players_loop': [
                                  {'p': 2},
                                  {'p': 3},
                                  ],
                              'count': 5,
                              },
                          'params': ['players', 2, 2],
                          },
                      {
                          'result': {
                              'players_loop': [
                                  {'p': 4},
                                  ],
                              'count': 5,
                              },
                          'params': ['players', 4, 2],
                          },
                      {
                          'result': {
                              'count': 5,
                              },
                          'params': ['players', 6, 2],
                          },
                      ])
    assert {
            'players_loop': [
                {'p': 0},
                {'p': 1},
                {'p': 2},
                {'p': 3},
                {'p': 4},
            ],
            'count': 5,
            } == send_receive(sb_server, ['players', 0, 2], loops=['players'])
    assert_posts(requests_post,
                 [
                     ['players', 0, 2],
                     ['players', 2, 2],
                     ['players', 4, 2],
                     ['players', 6, 2],
                     ])

# TODO: params mismatch -> ProtocolException
