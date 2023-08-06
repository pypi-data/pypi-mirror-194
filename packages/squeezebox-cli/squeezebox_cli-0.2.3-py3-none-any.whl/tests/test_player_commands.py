from .helpers import set_response, assert_post, assert_posts, \
        sb_server, set_responses
import squeezebox_cli.player


def test_stop_player(mocker, requests_post):
    squeezebox_cli.player.stop(sb_server, 'Garden')
    assert_post(requests_post, ['stop'], player='Garden')


def test_player_status_radio_playing(mocker, requests_post):
    mocker.patch('squeezebox_cli.player.commands.CHUNK_SIZE', 3)
    set_responses(mocker,
                  requests_post,
                  [{
                      'params': ['status', '0', '3'],
                      'result': {
                          'digital_volume_control': 1,
                          'current_title': 'Radio X London',
                          'rate': 1,
                          'player_name': 'Lounge',
                          'time': 86.372361831665,
                          'playlist repeat': 0,
                          'mode': 'play',
                          'signalstrength': 0,
                          'playlist_cur_index': '0',
                          'playlist mode': 'off',
                          'playlist_tracks': 1,
                          'playlist shuffle': 0,
                          'seq_no': 0,
                          'player_connected': 1,
                          'playlist_timestamp': 1677600236.1468,
                          'remote': 1,
                          'remoteMeta': {
                              'id': '-99965232',
                              'title': 'Uprising',
                              },
                          'player_ip': '192.168.1.130:48150',
                          'mixer volume': 15,
                          'power': 1,
                          'playlist_loop': [
                              {'id': '-99965232',
                               'playlist index': 0,
                               'title': 'Uprising'
                               },
                              ],
                          },
                      },
                   {
                      'params': ['status', '3', '3'],
                      'result': {
                          'digital_volume_control': 1,
                          'current_title': 'Radio X London',
                          'rate': 1,
                          'player_name': 'Lounge',
                          'time': 86.372361831665,
                          'playlist repeat': 0,
                          'mode': 'play',
                          'signalstrength': 0,
                          'playlist_cur_index': '0',
                          'playlist mode': 'off',
                          'playlist_tracks': 1,
                          'playlist shuffle': 0,
                          'seq_no': 0,
                          'player_connected': 1,
                          'playlist_timestamp': 1677600236.1468,
                          'remote': 1,
                          'remoteMeta': {
                              'id': '-99965232',
                              'title': 'Uprising',
                              },
                          'player_ip': '192.168.1.130:48150',
                          'mixer volume': 15,
                          'power': 1,
                          },
                      },
                   ], player='Lounge')
    assert (dict(name='Lounge',
                 mode='play',
                 volume=15,
                 shuffle=squeezebox_cli.player.Shuffle.NONE,
                 repeat=squeezebox_cli.player.Repeat.NONE,
                 playlist_cur_index=0,
                 playlist=[(-99965232, 'Radio X London: Uprising')])
            == squeezebox_cli.player.status(sb_server, 'Lounge'))
    assert_posts(requests_post,
                 [
                        ['status', 0, 3],
                        ['status', 3, 3],
                        ],
                 player='Lounge')


def test_player_status_with_playlist(mocker, requests_post):
    mocker.patch('squeezebox_cli.player.commands.CHUNK_SIZE', 3)
    set_responses(mocker,
                  requests_post,
                  [{
                      'params': ['status', '0', '3'],
                      'result': {
                          'power': 1,
                          'mixer volume': 53,
                          'sync_slaves': '00:04:20:23:30:7f,dc:a6:32:f6:ff:4b',
                          'player_ip': '192.168.1.100:38135',
                          'playlist_timestamp': 1677592623.47087,
                          'player_connected': 1,
                          'duration': 279.693,
                          'can_seek': 1,
                          'playlist_tracks': 21,
                          'playlist mode': 'off',
                          'seq_no': '16',
                          'playlist shuffle': 0,
                          'sync_master': 'b8:27:eb:0c:89:b6',
                          'signalstrength': 100,
                          'playlist repeat': 0,
                          'mode': 'stop',
                          'playlist_cur_index': '8',
                          'rate': 1,
                          'player_name': 'Lounge',
                          'time': 0,
                          'playlist_loop': [
                              {
                                  'playlist index': 0,
                                  'id': 53780,
                                  'title': 'Harvest Home',
                                  },
                              {
                                  'title': 'In A Big Country',
                                  'id': 53789,
                                  'playlist index': 1,
                                  },
                              {
                                  'playlist index': 2,
                                  'id': 53790,
                                  'title': 'Close Action',
                                  },
                              ],
                          'digital_volume_control': 1,
                          },
                      },
                   {
                       'result': {
                           'player_ip': '192.168.1.100:38135',
                           'power': 1,
                           'mixer volume': 53,
                           'sync_slaves': '00:04:20:23:30:7f'
                                          ',dc:a6:32:f6:ff:4b',
                           'playlist_tracks': 21,
                           'playlist mode': 'off',
                           'seq_no': '16',
                           'playlist shuffle': 0,
                           'player_connected': 1,
                           'playlist_timestamp': 1677592623.47087,
                           'duration': 279.693,
                           'can_seek': 1,
                           'signalstrength': 100,
                           'mode': 'stop',
                           'playlist repeat': 0,
                           'playlist_cur_index': '8',
                           'sync_master': 'b8:27:eb:0c:89:b6',
                           'digital_volume_control': 1,
                           'rate': 1,
                           'player_name': 'Lounge',
                           'time': 0,
                           'playlist_loop': [
                               {
                                   'title': 'The Storm',
                                   'playlist index': 3,
                                   'id': 53791,
                                   },
                               {
                                   'title': 'Wonderland',
                                   'id': 53792,
                                   'playlist index': 4,
                                   },
                               {
                                   'id': 53793,
                                   'playlist index': 5,
                                   'title': 'Belief In The Small Man',
                                   },
                               ],
                           },
                       'params': ['status', '3', '3'],
                       },
                   {
                       'result': {
                           'player_ip': '192.168.1.100:38135',
                           'power': 1,
                           'mixer volume': 53,
                           'sync_slaves': '00:04:20:23:30:7f'
                                          ',dc:a6:32:f6:ff:4b',
                           'playlist_tracks': 21,
                           'playlist mode': 'off',
                           'seq_no': '16',
                           'playlist shuffle': 0,
                           'player_connected': 1,
                           'playlist_timestamp': 1677592623.47087,
                           'duration': 279.693,
                           'can_seek': 1,
                           'signalstrength': 100,
                           'mode': 'stop',
                           'playlist repeat': 0,
                           'playlist_cur_index': '8',
                           'sync_master': 'b8:27:eb:0c:89:b6',
                           'digital_volume_control': 1,
                           'rate': 1,
                           'player_name': 'Lounge',
                           'time': 0,
                           },
                       'params': ['status', '6', '3'],
                       },
                   ], player='Lounge')
    assert dict(name='Lounge',
                mode='stop',
                volume=53,
                shuffle=squeezebox_cli.player.Shuffle.NONE,
                repeat=squeezebox_cli.player.Repeat.NONE,
                duration=279.693,
                playlist_cur_index=8,
                playlist=[
                     (53780, 'Harvest Home'),
                     (53789, 'In A Big Country'),
                     (53790, 'Close Action'),
                     (53791, 'The Storm'),
                     (53792, 'Wonderland'),
                     (53793, 'Belief In The Small Man'),
                     ]) == squeezebox_cli.player.status(sb_server, 'Lounge')
    assert_posts(requests_post, [
        ['status', 0, 3],
        ['status', 3, 3],
        ['status', 6, 3],
        ],
                 player='Lounge')


def test_sync_to(requests_post):
    squeezebox_cli.player.sync_to(sb_server, 'Kitchen', player='Lounge')
    assert_post(requests_post, ['sync', 'Kitchen'], 'Lounge')


def test_syncgroups_none(mocker, requests_post):
    set_response(mocker,
                 requests_post,
                 ['syncgroups', '?'],
                 result={})
    assert [] == squeezebox_cli.player.sync_groups(sb_server)
    assert_post(requests_post, ['syncgroups', '?'])


def test_syncgroups_one(mocker, requests_post):
    set_response(mocker,
                 requests_post,
                 ['syncgroups', '?'],
                 result={
                     'syncgroups_loop': [
                         {
                             'sync_member_names': 'Kitchen,Lounge',
                             'sync_members': 'b8:27:eb:0c:89:b6'
                                             ',00:04:20:23:30:7f',
                             },
                         ],
                     })
    assert ([{'Kitchen', 'Lounge'}]
            == squeezebox_cli.player.sync_groups(sb_server))
    assert_post(requests_post, ['syncgroups', '?'])


def test_get_volume(mocker, requests_post):
    set_response(mocker,
                 requests_post,
                 ['mixer', 'volume', '?'],
                 result={'_volume': '57'},
                 player='office')
    assert 57 == squeezebox_cli.player.get_volume(sb_server, 'office')
    assert_post(requests_post, ['mixer', 'volume', '?'], player='office')


def test_set_volume(requests_post):
    squeezebox_cli.player.set_volume(sb_server, 'office', 75)
    assert_post(requests_post, ['mixer', 'volume', 75], player='office')


def test_inc_volume(requests_post):
    squeezebox_cli.player.change_volume(sb_server, 'office', 7)
    assert_post(requests_post, ['mixer', 'volume', '+7'], player='office')


def test_dec_volume(requests_post):
    squeezebox_cli.player.change_volume(sb_server, 'office', -7)
    assert_post(requests_post, ['mixer', 'volume', '-7'], player='office')


def test_mute(requests_post):
    squeezebox_cli.player.mute(sb_server, 'office')
    assert_post(requests_post, ['mixer', 'muting', 1], player='office')


def test_unmute(requests_post):
    squeezebox_cli.player.unmute(sb_server, 'office')
    assert_post(requests_post, ['mixer', 'muting', 0], player='office')


def test_toggle_mute(requests_post):
    squeezebox_cli.player.toggle_mute(sb_server, 'office')
    assert_post(requests_post, ['mixer', 'muting'], player='office')


def test_get_mute_true(mocker, requests_post):
    set_response(mocker,
                 requests_post,
                 ['mixer', 'muting', '?'],
                 result={'_muting': '1'},
                 player='office')
    assert squeezebox_cli.player.get_mute(sb_server, 'office')
    assert_post(requests_post, ['mixer', 'muting', '?'], player='office')


def test_get_mute_false(mocker, requests_post):
    set_response(mocker,
                 requests_post,
                 ['mixer', 'muting', '?'],
                 result={'_muting': None},
                 player='office')
    assert not squeezebox_cli.player.get_mute(sb_server, 'office')
    assert_post(requests_post, ['mixer', 'muting', '?'], player='office')


def test_players(mocker, requests_post):
    mocker.patch('squeezebox_cli.player.commands.CHUNK_SIZE', 5)
    set_responses(
            mocker,
            requests_post,
            params_results=[
                {
                    'params': ['players', '0', '5'],
                    'result': {
                        'count': 3,
                        'players_loop': [
                            {
                                'seq_no': 0,
                                'playerid': 'dc:a6:32:f6:ff:4b',
                                'ip': '192.168.1.90:40338',
                                'canpoweroff': 1,
                                'modelname': 'HiFiBerry',
                                'displaytype': 'none',
                                'uuid': None,
                                'isplayer': 1,
                                'name': 'Dining Room',
                                'firmware': 'v1.9.1-1139',
                                'model': 'squeezelite',
                                'isplaying': 0,
                                'playerindex': '0',
                                'power': 1,
                                'connected': 1,
                                },
                            {
                                'connected': 1,
                                'playerindex': 1,
                                'power': 1,
                                'isplayer': 1,
                                'name': 'Lounge',
                                'uuid': 'b0ff501bdcff1d6a18e0965b23844c94',
                                'firmware': '7.8.0-r16754',
                                'isplaying': 0,
                                'model': 'fab4',
                                'playerid': '00:04:20:23:30:7f',
                                'seq_no': '15',
                                'ip': '192.168.1.100:52204',
                                'canpoweroff': 1,
                                'modelname': 'Squeezebox Touch',
                                'displaytype': 'none',
                                },
                            {
                                'connected': 1,
                                'playerindex': 2,
                                'power': 1,
                                'name': 'Kitchen',
                                'isplayer': 1,
                                'uuid': None,
                                'model': 'squeezelite',
                                'isplaying': 1,
                                'firmware': 'v1.9.9-1419-pCP',
                                'seq_no': 0,
                                'playerid': 'b8:27:eb:0c:89:b6',
                                'displaytype': 'none',
                                'modelname': 'SqueezeLite',
                                'canpoweroff': 1,
                                'ip': '192.168.1.99:55176',
                                },
                            ],
                        },
                    },
                {
                    'params': ['players', 5, 5],
                    'result': {},
                    },
                ])
    assert [
            {
                'name': 'Dining Room',
                'connected': True,
                'isplaying': False,
                },
            {
                'name': 'Lounge',
                'connected': True,
                'isplaying': False,
                },
            {
                'name': 'Kitchen',
                'connected': True,
                'isplaying': True,
                },
            ] == squeezebox_cli.player.players(sb_server)
    assert_posts(requests_post, [['players', 0, 5]])


def test_playlist_add_track(requests_post):
    squeezebox_cli.player.playlist_add(sb_server, 'office', track_id=3232)
    assert_post(requests_post,
                ['playlistcontrol', 'cmd:add', 'track_id:3232'],
                player='office')


def test_playlist_add_album(requests_post):
    squeezebox_cli.player.playlist_add(sb_server, 'office', album_id=3232)
    assert_post(requests_post,
                ['playlistcontrol', 'cmd:add', 'album_id:3232'],
                player='office')


def test_playlist_insert_track(requests_post):
    squeezebox_cli.player.playlist_insert(sb_server, 'office', track_id=3232)
    assert_post(requests_post,
                ['playlistcontrol', 'cmd:insert', 'track_id:3232'],
                player='office')


def test_playlist_insert_album(requests_post):
    squeezebox_cli.player.playlist_insert(sb_server, 'office', album_id=3232)
    assert_post(requests_post,
                ['playlistcontrol', 'cmd:insert', 'album_id:3232'],
                player='office')


def test_playlist_remove(requests_post):
    squeezebox_cli.player.playlist_remove(sb_server, 'office', 4)
    assert_post(requests_post,
                ['playlist', 'delete', 4],
                player='office')


def test_play_current(requests_post):
    squeezebox_cli.player.play(sb_server, 'office')
    assert_post(requests_post,
                ['play'],
                player='office')


def test_play_track(requests_post):
    squeezebox_cli.player.play(sb_server, 'office', track_id=1234)
    assert_post(requests_post,
                ['playlistcontrol', 'cmd:load', 'track_id:1234'],
                player='office')


def test_play_album(requests_post):
    squeezebox_cli.player.play(sb_server, 'office', album_id=1234)
    assert_post(requests_post,
                ['playlistcontrol', 'cmd:load', 'album_id:1234'],
                player='office')


def test_pause(requests_post):
    squeezebox_cli.player.pause(sb_server, 'office')
    assert_post(requests_post, ['pause'], player='office')


def test_next(requests_post):
    squeezebox_cli.player.next(sb_server, 'office')
    assert_post(requests_post, ['playlist', 'index', '+1'], player='office')


def test_previous(requests_post):
    squeezebox_cli.player.previous(sb_server, 'office')
    assert_post(requests_post, ['playlist', 'index', '-1'], player='office')


def test_playlist_suffle_query_none(mocker, requests_post):
    set_response(mocker,
                 requests_post,
                 ['playlist', 'shuffle', '0'],
                 player='office')
    assert (squeezebox_cli.player.Shuffle.NONE
            == squeezebox_cli.player.playlist_query_shuffle(sb_server,
                                                            'office'))
    assert_post(requests_post, ['playlist', 'shuffle', '?'], player='office')


def test_playlist_suffle_query_song(mocker, requests_post):
    set_response(mocker,
                 requests_post,
                 ['playlist', 'shuffle', '1'],
                 player='office')
    assert (squeezebox_cli.player.Shuffle.SONG
            == squeezebox_cli.player.playlist_query_shuffle(sb_server,
                                                            'office'))
    assert_post(requests_post, ['playlist', 'shuffle', '?'], player='office')


def test_playlist_suffle_query_album(mocker, requests_post):
    set_response(mocker,
                 requests_post,
                 ['playlist', 'shuffle', '2'],
                 player='office')
    assert (squeezebox_cli.player.Shuffle.ALBUM
            == squeezebox_cli.player.playlist_query_shuffle(sb_server,
                                                            'office'))
    assert_post(requests_post, ['playlist', 'shuffle', '?'], player='office')


def test_playlist_shuffle_set_song(requests_post):
    squeezebox_cli.player.playlist_set_shuffle(
            sb_server, 'office', squeezebox_cli.player.Shuffle.SONG)
    assert_post(requests_post, ['playlist', 'shuffle', '1'], player='office')


def test_playlist_shuffle_toggle(requests_post):
    squeezebox_cli.player.playlist_toggle_shuffle(sb_server, 'office')
    assert_post(requests_post, ['playlist', 'shuffle'], player='office')


def test_playlist_repeat_query_none(mocker, requests_post):
    set_response(mocker,
                 requests_post,
                 ['playlist', 'repeat', '0'],
                 player='office')
    assert (squeezebox_cli.player.Repeat.NONE
            == squeezebox_cli.player.playlist_query_repeat(sb_server,
                                                           'office'))
    assert_post(requests_post, ['playlist', 'repeat', '?'], player='office')


def test_playlist_repeat_set_song(requests_post):
    squeezebox_cli.player.playlist_set_repeat(
            sb_server,
            'office',
            squeezebox_cli.player.Repeat.SONG)
    assert_post(requests_post, ['playlist', 'repeat', '1'], player='office')


def test_playlist_repeat_set_all(requests_post):
    squeezebox_cli.player.playlist_set_repeat(
            sb_server,
            'office',
            squeezebox_cli.player.Repeat.ALL)
    assert_post(requests_post, ['playlist', 'repeat', '2'], player='office')


def test_playlist_repeat_set_none(requests_post):
    squeezebox_cli.player.playlist_set_repeat(
            sb_server,
            'office',
            squeezebox_cli.player.Repeat.NONE)
    assert_post(requests_post, ['playlist', 'repeat', '0'], player='office')


def test_playlist_repeat_toggle(requests_post):
    squeezebox_cli.player.playlist_toggle_repeat(sb_server, 'office')
    assert_post(requests_post, ['playlist', 'repeat'], player='office')


def test_playlist_index_set(requests_post):
    squeezebox_cli.player.playlist_index(sb_server, 'office', 5)
    assert_post(requests_post, ['playlist', 'index', 5], player='office')
