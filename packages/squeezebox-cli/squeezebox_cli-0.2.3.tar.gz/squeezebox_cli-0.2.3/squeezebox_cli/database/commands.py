from datetime import timedelta
import dateparser

from squeezebox_cli.core.protocol import send_receive

CHUNK_SIZE = 50


def rescan(server):
    send_receive(server, ['rescan'])


def rescanning(server):
    return 1 == send_receive(server, ['rescan', '?'])['_rescan']


def rescan_playlists(server):
    send_receive(server, ['rescan', 'playlists'])


def rescan_progress(server):
    response = send_receive(server, ['rescanprogress'])
    if response['rescan'] == 0:
        return None
    result = {}
    result['steps'] = [(step, response[step])
                       for step in response['steps'].split(',')]
    hours, minutes, seconds = [int(n)
                               for n in response['totaltime'].split(':')]
    result['totaltime'] = timedelta(
            hours=hours, minutes=minutes, seconds=seconds)
    return result


def total_genres(server):
    return send_receive(server, ['info', 'total', 'genres', '?'])['_genres']


def total_artists(server):
    return send_receive(server, ['info', 'total', 'artists', '?'])['_artists']


def total_albums(server):
    return send_receive(server, ['info', 'total', 'albums', '?'])['_albums']


def total_songs(server):
    return send_receive(server, ['info', 'total', 'songs', '?'])['_songs']


def query_args(search, artist_id, album_id, track_id, genre_id):
    args = []
    if search:
        args.append(f'search:{search}')
    if artist_id:
        args.append(f'artist_id:{artist_id}')
    if album_id:
        args.append(f'album_id:{album_id}')
    if track_id:
        args.append(f'track_id:{track_id}')
    if genre_id:
        args.append(f'genre_id:{genre_id}')
    return args


def genres(
        server, search=None, artist_id=None, album_id=None, track_id=None,
        genre_id=None):
    params = ['genres', 0, CHUNK_SIZE] + query_args(
            search, artist_id, album_id, track_id, genre_id)
    return {g['id']: g['genre']
            for g in send_receive(server,
                                  params,
                                  loops=['genres'])['genres_loop']}


def artists(
        server, search=None, artist_id=None, album_id=None, track_id=None,
        genre_id=None):
    params = ['artists', 0, CHUNK_SIZE] + query_args(
            search, artist_id, album_id, track_id, genre_id)
    return {g['id']: g['artist']
            for g in send_receive(server,
                                  params,
                                  loops=['artists'])['artists_loop']}


def albums(
        server, search=None, artist_id=None, album_id=None, track_id=None,
        genre_id=None, year=None, compilation=None, sort=None,
        extended=False):
    params = ['albums', 0, CHUNK_SIZE] + query_args(
            search, artist_id, album_id, track_id, genre_id)
    if year is not None:
        params.append(f'year:{year}')
    if compilation is not None:
        params.append(f'compilation:{1 if compilation else 0}')
    if sort is not None:
        params.append(f'sort:{sort}')
    if extended:
        params.append('tags:AywaSXl')
    result = send_receive(server, params, loops=['albums'])['albums_loop']
    if extended:
        return [{
            'id': r['id'],
            'album': r['album'],
            'album_replay_gain': r['album_replay_gain'],
            'artist': r['artist'],
            'artist_id': r['artist_id'],
            'compilation': r['compilation'] == 1,
            'year': None if r['year'] == 0 else r['year'],
            } for r in result]
    return {g['id']: g['album'] for g in result}


def years(server):
    return [y['year']
            for y in send_receive(server,
                                  ['years', 0, CHUNK_SIZE],
                                  loops=['years'])['years_loop']]


BOOLEAN_FIELDS = ['compilation']
DATETIME_FIELDS = ['addedTime']
FLOAT_FIELDS = ['duration']
INT_FIELDS = ['album_id', 'artist_id', 'genre_id', 'id',
              'tracknum', 'year']


def apply_types(fields):
    typed_fields = {}
    for k, v in fields.items():
        if k in INT_FIELDS:
            typed_fields[k] = int(v)
        elif k in BOOLEAN_FIELDS:
            typed_fields[k] = (v == 1)
        elif k in DATETIME_FIELDS:
            typed_fields[k] = dateparser.parse(v)
        else:
            typed_fields[k] = v
    return typed_fields


def field_list_to_dict(fields):
    return {k: v for [(k, v)] in [list(f.items()) for f in fields]}


def songinfo(server, track_id):
    fields = send_receive(server,
                          ['songinfo', 0, CHUNK_SIZE,
                           f'track_id:{track_id}',
                           'tags:aCDdegilpqstuy'],
                          loops=['songinfo'])['songinfo_loop']
    return apply_types(field_list_to_dict(fields))


def tracks(
        server, search=None, artist_id=None, album_id=None, track_id=None,
        genre_id=None, year=None, sort=None, extended=False):
    params = ['tracks', 0, CHUNK_SIZE] + query_args(
            search, artist_id, album_id, track_id, genre_id)
    if extended:
        params.append('tags:AytsplgedCa')
    if album_id or artist_id:
        params.append('sort:albumtrack')
    response = send_receive(server, params, loops=['titles'])
    return [apply_types(t) for t in response['titles_loop']]


def id_pairs_to_dict(type, pairs):
    return {pair[f'{type}_id']: pair[f'{type}'] for pair in pairs}


def search(server, term):
    response = send_receive(server,
                            ['search', 0, CHUNK_SIZE, f'term:{term}'],
                            loops=['tracks', 'albums', 'contributors'])
    return dict(artists=id_pairs_to_dict('contributor',
                                         response.get('contributors_loop',
                                                      [])),
                tracks=id_pairs_to_dict('track',
                                        response.get('tracks_loop', [])),
                albums=id_pairs_to_dict('album',
                                        response.get('albums_loop', [])))
