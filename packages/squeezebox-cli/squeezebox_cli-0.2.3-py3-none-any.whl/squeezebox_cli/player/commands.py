from enum import Enum


from squeezebox_cli.core.protocol import send_receive, send_query, send


CHUNK_SIZE = 50

#
# public interface
#


Shuffle = Enum('Shuffle', {'NONE': 0, 'SONG': 1, 'ALBUM': 2})
Repeat = Enum('Repeat', {'NONE': 0, 'SONG': 1, 'ALL': 2})


def stop(host_port, player):
    send(host_port, ['stop'], player=player)


def play(server, player, track_id=None, album_id=None):
    id = None
    if track_id:
        id = f'track_id:{track_id}'
    elif album_id:
        id = f'album_id:{album_id}'
    if id:
        send(server, ['playlistcontrol', 'cmd:load', id], player=player)
    else:
        send(server, ['play'], player=player)


def pause(server, player):
    send(server, ['pause'], player=player)


def next(server, player):
    send(server, ['playlist', 'index', '+1'], player=player)


def previous(server, player):
    send(server, ['playlist', 'index', '-1'], player=player)


def status(server, player):
    result = send_receive(server,
                          ['status', 0, CHUNK_SIZE],
                          loops=['playlist'],
                          player=player)
    response = {
            'name': result['player_name'],
            'repeat': Repeat(result['playlist repeat']),
            'shuffle': Shuffle(result['playlist shuffle']),
            'volume': result['mixer volume'],
            'mode': result['mode'],
            'playlist_cur_index': int(result['playlist_cur_index']),
            }
    try:
        response['duration'] = result['duration']
    except KeyError:
        pass
    response['playlist'] = []
    for track in result['playlist_loop']:
        id = int(track['id'])
        title = track['title']
        if id < 0:
            response['playlist'].append(
                    (id, f"{result.get('current_title', '')}: {title}"))
        else:
            response['playlist'].append((id, title))
    return response


def sync_to(server, sync_to_player, player):
    send(server, ['sync', sync_to_player], player)


def sync_groups(server):
    result = send_receive(server, ['syncgroups', '?'])
    return [{p for p in group['sync_member_names'].split(',')}
            for group in result.get('syncgroups_loop', [])]


def get_volume(server, player):
    return int(send_receive(server,
                            ['mixer', 'volume', '?'],
                            player=player)['_volume'])


def set_volume(server, player, vol):
    send(server, ['mixer', 'volume', vol], player=player)


def change_volume(server, player, step):
    send(server, ['mixer', 'volume', f'{step:+}'], player=player)


def mute(server, player):
    send(server, ['mixer', 'muting', 1], player=player)


def unmute(server, player):
    send(server, ['mixer', 'muting', 0], player=player)


def toggle_mute(server, player):
    send(server, ['mixer', 'muting'], player=player)


def get_mute(server, player):
    return send_receive(server,
                        ['mixer', 'muting', '?'],
                        player=player)['_muting'] == '1'


def players(server):
    response = send_receive(server, ['players', 0, CHUNK_SIZE])
    tag_handlers = {
            'name': lambda v: str(v),
            'connected': lambda v: bool(v),
            'isplaying': lambda v: bool(v)
        }
    return [{k: h(player[k]) for k, h in tag_handlers.items()}
            for player in response['players_loop']]


def playlist_add(server, player, track_id=None, album_id=None, artist_id=None):
    playlist_cmd(server, player, 'add', track_id, album_id, artist_id)


def playlist_insert(
        server, player, track_id=None, album_id=None, artist_id=None):
    playlist_cmd(server, player, 'insert', track_id, album_id, artist_id)


def playlist_cmd(server, player, cmd, track_id, album_id, artist_id):
    if track_id:
        id = f'track_id:{track_id}'
    elif album_id:
        id = f'album_id:{album_id}'
    elif artist_id:
        id = f'artist_id:{artist_id}'
    send(server, ['playlistcontrol', f'cmd:{cmd}', id], player=player)


def playlist_remove(server, player, index):
    send(server, ['playlist', 'delete', index], player=player)


def playlist_query_shuffle(server, player):
    _playlist, _shuffle, state = send_query(server,
                                            ['playlist', 'shuffle', '?'],
                                            player=player)
    return Shuffle(int(state))


def playlist_set_shuffle(server, player, shuffle_type):
    send(server,
         ['playlist', 'shuffle', str(shuffle_type.value)],
         player=player)


def playlist_toggle_shuffle(server, player):
    send(server, ['playlist', 'shuffle'], player=player)


def playlist_query_repeat(server, player):
    match send_query(server, ['playlist', 'repeat', '?'], player=player):
        case ['playlist', 'repeat', state]:
            return Repeat(int(state))


def playlist_set_repeat(server, player, repeat_type):
    send(server, ['playlist', 'repeat', str(repeat_type.value)], player=player)


def playlist_toggle_repeat(server, player):
    send(server, ['playlist', 'repeat'], player=player)


def playlist_index(server, player, index):
    send(server, ['playlist', 'index', index], player=player)
