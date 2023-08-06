import json
from datetime import timedelta, datetime

from .helpers import set_response, assert_post, assert_posts, \
        sb_server
import squeezebox_cli.database as database


#########
# Tests #
#########

def test_rescan_action(mocker, requests_post):
    set_response(mocker, requests_post, ['rescan'], {})
    database.rescan(sb_server)
    assert_post(requests_post, ['rescan'])


def test_rescan_query_scanning_true(mocker, requests_post):
    set_response(mocker, requests_post, ['rescan', '?'], {'_rescan': 1})
    assert database.rescanning(sb_server)
    assert_post(requests_post, ['rescan', '?'])


def test_rescan_query_scanning_false(mocker, requests_post):
    set_response(mocker, requests_post, ['rescan', '?'], {'_rescan': 0})
    assert not database.rescanning(sb_server)
    assert_post(requests_post, ['rescan', '?'])


def test_rescan_playlists(mocker, requests_post):
    set_response(mocker, requests_post, ['rescan', 'playlists'], {})
    database.rescan_playlists(sb_server)
    assert_post(requests_post, ['rescan', 'playlists'])


def test_rescan_progress_in_progress(mocker, requests_post):
    set_response(mocker,
                 requests_post,
                 ['rescanprogress'],
                 {
                     'totaltime': '00:01:15',
                     'updateStandaloneArtwork': 100,
                     'steps': 'plugin_fulltext,updateStandaloneArtwork'
                              ',dboptimize',
                     'plugin_fulltext': 100,
                     'dboptimize': 50,
                     'rescan': 1,
                     })
    assert dict(
            totaltime=timedelta(minutes=1, seconds=15),
            steps=[
                ('plugin_fulltext', 100),
                ('updateStandaloneArtwork', 100),
                ('dboptimize', 50),
                ]) == database.rescan_progress(sb_server)
    assert_post(requests_post, ['rescanprogress'])


def test_rescan_progress_not_in_progress(mocker, requests_post):
    set_response(mocker,
                 requests_post,
                 ['rescanprogress'],
                 {'rescan': 0})
    assert database.rescan_progress(sb_server) is None
    assert_post(requests_post, ['rescanprogress'])


def test_totals_genres(mocker, requests_post):
    set_response(mocker,
                 requests_post,
                 ['info', 'total', 'genres', '?'],
                 {'_genres': 54})
    assert 54 == database.total_genres(sb_server)
    assert_post(requests_post, ['info', 'total', 'genres', '?'])


def test_totals_artists(mocker, requests_post):
    set_response(mocker,
                 requests_post,
                 ['info', 'total', 'artists', '?'],
                 {'_artists': 123})
    assert 123 == database.total_artists(sb_server)
    assert_post(requests_post, ['info', 'total', 'artists', '?'])


def test_totals_songs(mocker, requests_post):
    set_response(mocker,
                 requests_post,
                 ['info', 'total', 'songs', '?'],
                 {'_songs': 123})
    assert 123 == database.total_songs(sb_server)
    assert_post(requests_post, ['info', 'total', 'songs', '?'])


def test_totals_albums(mocker, requests_post):
    set_response(mocker,
                 requests_post,
                 ['info', 'total', 'albums', '?'],
                 {'_albums': 123})
    assert 123 == database.total_albums(sb_server)
    assert_post(requests_post, ['info', 'total', 'albums', '?'])


def test_genres_get_all_multiple_chunks(mocker, requests_post):
    mocker.patch('squeezebox_cli.database.commands.CHUNK_SIZE', 5)
    requests_post.side_effect = [
            mocker.MagicMock(content=json.dumps({
               'params': ['', ['genres', '0', '5']],
               'result': {
                   'count': 7,
                   'genres_loop': [
                       {'id': 351, 'genre': '255)'},
                       {'id': 325, 'genre': 'Acoustic'},
                       {'id': 357, 'genre': 'Alt Rock'},
                       {'id': 329, 'genre': 'Alternative'},
                       {'id': 356, 'genre': 'Alternative/Indie'},
                       ],
                   },
               'method': 'slim.request',
               })),
            mocker.MagicMock(content=json.dumps({
                'method': 'slim.request',
                'result': {
                    'genres_loop': [
                        {'genre': 'Alternative & Punk', 'id': 341},
                        {'genre': 'Alternative Rock', 'id': 347},
                        ],
                    'count': 7,
                    },
                'params': ['', ['genres', '5', '5']],
                })),
            mocker.MagicMock(content=json.dumps({
                'method': 'slim.request',
                'result': {},
                'params': ['', ['genres', '10', '5']],
                })),
            ]
    assert {
            351: '255)',
            325: 'Acoustic',
            357: 'Alt Rock',
            329: 'Alternative',
            356: 'Alternative/Indie',
            341: 'Alternative & Punk',
            347: 'Alternative Rock',
            } == database.genres(sb_server)
    assert_posts(requests_post, [
        ['genres', 0, 5],
        ['genres', 5, 5],
        ])


def test_genres_search_found(mocker, requests_post):
    mocker.patch('squeezebox_cli.database.commands.CHUNK_SIZE', 3)
    requests_post.side_effect = [
            mocker.MagicMock(content=json.dumps({
               'method': 'slim.request',
               'params': ['', ['genres', '0', 3, 'search:folk']],
               'result': {
                   'count': 5,
                   'genres_loop': [
                       {'id': 332, 'genre': 'Folk'},
                       {'id': 360, 'genre': 'Folk, acoustic'},
                       {'id': 371, 'genre': 'Folk, Acoustic'},
                       ],
                   },
               'method': 'slim.request',
               })),
            mocker.MagicMock(content=json.dumps({
               'method': 'slim.request',
               'params': ['', ['genres', '3', 3, 'search:folk']],
               'result': {
                   'count': 5,
                   'genres_loop': [
                       {'id': 327, 'genre': 'Pop-Folk'},
                       {'genre': 'Rock/Folk', 'id': 326}
                       ],
                   },
               'method': 'slim.request',
               })),
            mocker.MagicMock(content=json.dumps({
                'method': 'slim.request',
                'result': {},
                'params': ['', ['genres', '6', '3', 'search:folk']],
                })),
            ]
    assert {
            332: 'Folk',
            360: 'Folk, acoustic',
            371: 'Folk, Acoustic',
            327: 'Pop-Folk',
            326: 'Rock/Folk',
            } == database.genres(sb_server, search='folk')
    assert_posts(requests_post, [
        ['genres', 0, 3, 'search:folk'],
        ['genres', 3, 3, 'search:folk'],
        ])


def test_artists_get_all(mocker, requests_post):
    mocker.patch('squeezebox_cli.database.commands.CHUNK_SIZE', 3)
    requests_post.side_effect = [
            mocker.MagicMock(content=json.dumps({
               'method': 'slim.request',
               'params': ['', ['artists', '0', 3]],
               'result': {
                   'count': 5,
                   'artists_loop': [
                       {'id': 10283, 'artist': '5 Seconds of Summer'},
                       {'artist': '50 Cent', 'id': 9243},
                       {'artist': '6 Notes', 'id': 9129},
                       ],
                   },
               'method': 'slim.request',
               })),
            mocker.MagicMock(content=json.dumps({
               'method': 'slim.request',
               'params': ['', ['artists', '3', 3]],
               'result': {
                   'count': 5,
                   'artists_loop': [
                       {'artist': '702', 'id': 9949},
                       {'id': 10178, 'artist': '98 Degrees'},
                       ],
                   },
               'method': 'slim.request',
               })),
            mocker.MagicMock(content=json.dumps({
               'method': 'slim.request',
               'params': ['', ['artists', '6', 3]],
               'result': {},
               })),
            ]
    assert {
            10283: '5 Seconds of Summer',
            9243: '50 Cent',
            9129: '6 Notes',
            9949: '702',
            10178: '98 Degrees',
            } == database.artists(sb_server)
    assert_posts(requests_post, [
        ['artists', 0, 3],
        ['artists', 3, 3],
        ])


def test_artists_search(mocker, requests_post):
    mocker.patch('squeezebox_cli.database.commands.CHUNK_SIZE', 3)
    requests_post.side_effect = [
            mocker.MagicMock(content=json.dumps({
               'method': 'slim.request',
               'params': ['', ['artists', '0', 3, 'search:ben']],
               'result': {
                   'count': 5,
                   'artists_loop': [
                       {'id': 10035, 'artist': 'Bent'},
                       {'id': 10635, 'artist': 'Beny Moré'},
                       {'id': 9158, 'artist': 'Ben Howard'},
                       ],
                   },
               'method': 'slim.request',
               })),
            mocker.MagicMock(content=json.dumps({
               'method': 'slim.request',
               'params': ['', ['artists', '3', 3, 'search:ben']],
               'result': {
                   'count': 5,
                   'artists_loop': [
                       {'id': 10242, 'artist': 'Ben Pearce'},
                       {'id': 10575, 'artist': 'Ben Webster'},
                       ],
                   },
               'method': 'slim.request',
               })),
            mocker.MagicMock(content=json.dumps({
               'method': 'slim.request',
               'params': ['', ['artists', '6', 3, 'search:ben']],
               'result': {},
               })),
            ]
    assert {
            10035: 'Bent',
            10635: 'Beny Moré',
            9158: 'Ben Howard',
            10242: 'Ben Pearce',
            10575: 'Ben Webster',
            } == database.artists(sb_server, search='ben')
    assert_posts(requests_post, [
        ['artists', 0, 3, 'search:ben'],
        ['artists', 3, 3, 'search:ben'],
        ])


def test_albums_basic(mocker, requests_post):
    mocker.patch('squeezebox_cli.database.commands.CHUNK_SIZE', 10)
    requests_post.side_effect = [
            mocker.MagicMock(content=json.dumps({
                'method': 'slim.request',
                'params': ['', ['albums', '0', 10]],
                'result': {
                    'count': 5,
                    'albums_loop': [
                        {'id': 3794, 'album': '+'},
                        {'id': 3793, 'album': '÷'},
                        {'id': 4294, 'album': '='},
                        {'album': '100 Broken Windows', 'id': 3872},
                        {'album': '100 Hits: Christmas Legends', 'id': 4226}
                        ],
                    },
                'method': 'slim.request',
                })),
            mocker.MagicMock(content=json.dumps({
                'method': 'slim.request',
                'params': ['', ['albums', '10', 10]],
                'result': {},
                })),
            ]

    assert {
            3794: '+',
            3793: '÷',
            4294: '=',
            3872: '100 Broken Windows',
            4226: '100 Hits: Christmas Legends',
            } == database.albums(sb_server)
    assert_posts(requests_post, [
        ['albums', 0, 10],
        ['albums', 10, 10],
        ])


def test_albums_extended(mocker, requests_post):
    mocker.patch('squeezebox_cli.database.commands.CHUNK_SIZE', 10)
    requests_post.side_effect = [
            mocker.MagicMock(content=json.dumps({
                'method': 'slim.request',
                'params': ['', ['albums', '0', 10, 'tags:AywaSXl']],
                'result': {
                    'count': 5,
                    'albums_loop': [
                        {
                            'year': 2011,
                            'compilation': 0,
                            'artist_id': 9232,
                            'album': '+',
                            'artist': 'Ed Sheeran',
                            'album_replay_gain': -5.78,
                            'id': 3794,
                            },
                        {
                            'album_replay_gain': -9.66,
                            'id': 3793,
                            'artist_id': 9232,
                            'compilation': 0,
                            'album': '÷',
                            'artist': 'Ed Sheeran',
                            'year': 0,
                            },
                        {
                            'year': 2021,
                            'artist_id': 9232,
                            'compilation': 0,
                            'album': '=',
                            'artist': 'Ed Sheeran',
                            'album_replay_gain': -10.18,
                            'id': 4294,
                            },
                        {
                            'id': 3872,
                            'album_replay_gain': -9.12,
                            'album': '100 Broken Windows',
                            'artist': 'Idlewild',
                            'compilation': 0,
                            'artist_id': 9502,
                            'year': 2000,
                            },
                        {
                            'year': 0,
                            'artist': 'Various Artists',
                            'album': '100 Hits: Christmas Legends',
                            'compilation': 1,
                            'artist_id': 9130,
                            'id': 4226,
                            'album_replay_gain': -8.52,
                            },
                        ],
                    },
                'method': 'slim.request',
                })),
            mocker.MagicMock(content=json.dumps({
                'method': 'slim.request',
                'params': ['', ['albums', '10', 10, 'tags:AywaSXl']],
                'result': {},
                })),
            ]

    assert [
            dict(id=3794, year=2011, compilation=False,
                 album_replay_gain=-5.78, artist_id=9232,
                 artist='Ed Sheeran', album='+'),
            dict(id=3793, year=None, compilation=False, album='÷',
                 album_replay_gain=-9.66, artist_id=9232,
                 artist='Ed Sheeran'),
            dict(id=4294, year=2021, compilation=False, album='=',
                 album_replay_gain=-10.18, artist_id=9232,
                 artist='Ed Sheeran'),
            dict(id=3872, year=2000, compilation=False,
                 album_replay_gain=-9.12, artist_id=9502,
                 artist='Idlewild',
                 album='100 Broken Windows'),
            dict(id=4226, year=None, compilation=True,
                 album_replay_gain=-8.52, artist_id=9130,
                 artist='Various Artists',
                 album='100 Hits: Christmas Legends'),
        ] == database.albums(sb_server, extended=True)
    assert_posts(requests_post, [
        ['albums', 0, 10, 'tags:AywaSXl'],
        ['albums', 10, 10, 'tags:AywaSXl'],
        ])


def test_albums_extended_search(mocker, requests_post):
    mocker.patch('squeezebox_cli.database.commands.CHUNK_SIZE', 10)
    requests_post.side_effect = [
            mocker.MagicMock(content=json.dumps({
                'method': 'slim.request',
                'params': [
                    '',
                    ['albums', '0', 10, 'search:bob', 'tags:AywaSXl']
                    ],
                'result': {
                    'count': 5,
                    'albums_loop': [
                        {
                            'id': 3728,
                            'album_replay_gain': -6.47,
                            'year': 2002,
                            'artist': 'Bob Marley & The Wailers',
                            'album': 'Legend: The Best of Bob Marley'
                                     ' and The Wailers',
                            'artist_id': 9170,
                            'compilation': 0,
                            },
                        {
                            'id': 3916,
                            'year': 2006,
                            'album_replay_gain': -8.77,
                            'album': 'Only Whispering',
                            'artist': 'Josh Woodward',
                            'compilation': 0,
                            'artist_id': 9522,
                            },
                        {
                            'artist_id': 9131,
                            'compilation': 0,
                            'artist': 'Adele',
                            'album': '19',
                            'album_replay_gain': -8.5,
                            'year': 2008,
                            'id': 3662,
                            },
                        {
                            'artist': 'Various Artists',
                            'album': 'Frukie',
                            'compilation': 1,
                            'artist_id': 9130,
                            'id': 3834,
                            'year': 0,
                            'album_replay_gain': 1.84,
                            },
                        {
                            'artist': 'Various Artists',
                            'album': 'Sunday Morning Songs',
                            'artist_id': 9130,
                            'compilation': 1,
                            'id': 4259,
                            'album_replay_gain': -7.02,
                            'year': 2006
                            },
                        ],
                    }
                })),
            mocker.MagicMock(content=json.dumps({
                'method': 'slim.request',
                'params': [
                    '',
                    ['albums', '10', 10, 'search:bob', 'tags:AywaSXl'],
                    ],
                'result': {},
                })),
            ]
    assert [
            dict(id=3728,
                 album='Legend: The Best of Bob Marley and The Wailers',
                 year=2002,
                 compilation=False,
                 album_replay_gain=-6.47,
                 artist_id=9170,
                 artist='Bob Marley & The Wailers'),
            dict(id=3916,
                 album='Only Whispering',
                 year=2006,
                 compilation=False,
                 album_replay_gain=-8.77,
                 artist_id=9522,
                 artist='Josh Woodward'),
            dict(id=3662,
                 album='19',
                 year=2008,
                 compilation=False,
                 album_replay_gain=-8.5,
                 artist_id=9131,
                 artist='Adele'),
            dict(id=3834,
                 album='Frukie',
                 year=None,
                 compilation=True,
                 album_replay_gain=1.84,
                 artist_id=9130,
                 artist='Various Artists'),
            dict(id=4259,
                 album='Sunday Morning Songs',
                 year=2006,
                 compilation=True,
                 album_replay_gain=-7.02,
                 artist_id=9130,
                 artist='Various Artists')
            ] == database.albums(sb_server, extended=True, search='bob')
    assert_posts(requests_post,
                 [['albums', 0, 10, 'search:bob', 'tags:AywaSXl']])


def test_years_no_rescan(mocker, requests_post):
    mocker.patch('squeezebox_cli.database.commands.CHUNK_SIZE', 10)
    requests_post.side_effect = [
            mocker.MagicMock(content=json.dumps({
                'method': 'slim.request',
                'params': ['', ['years', '0', 10]],
                'result': {
                    'count': 5,
                    'years_loop': [
                        {'year': 2022},
                        {'year': 2021},
                        {'year': 2020},
                        {'year': 2002},
                        {'year': 1957},
                        ]
                    },
                })),
            mocker.MagicMock(content=json.dumps({
                'method': 'slim.request',
                'params': ['', ['years', '10', 10]],
                'result': {},
                })),
            ]
    assert [2022, 2021, 2020, 2002, 1957] == database.years(sb_server)
    assert_posts(requests_post, [['years', 0, 10]])


def test_years_rescan_in_progress(mocker, requests_post):
    mocker.patch('squeezebox_cli.database.commands.CHUNK_SIZE', 10)
    requests_post.side_effect = [
            mocker.MagicMock(content=json.dumps({
                'method': 'slim.request',
                'params': ['', ['years', '0', 10]],
                'result': {
                    'rescan': 1,
                    'count': 5,
                    'years_loop': [
                        {'year': 2022},
                        {'year': 2021},
                        {'year': 2020},
                        {'year': 2002},
                        {'year': 1957},
                        ]
                    },
                })),
            mocker.MagicMock(content=json.dumps({
                'method': 'slim.request',
                'params': ['', ['years', '10', 10]],
                'result': {},
                })),
            ]
    assert [2022, 2021, 2020, 2002, 1957] == database.years(sb_server)
    assert_posts(requests_post, [['years', 0, 10]])


def test_songinfo_default_tags(mocker, requests_post):
    mocker.patch('squeezebox_cli.database.commands.CHUNK_SIZE', 10)
    requests_post.side_effect = [
            mocker.MagicMock(content=json.dumps({
                'method': 'slim.request',
                'params': [
                    '',
                    [
                        'songinfo',
                        '0',
                        10,
                        'track_id:56743',
                        'tags:aCDdegilpqstuy',
                        ],
                    ],
                'result': {
                    'songinfo_loop': [
                        {'id': 56743},
                        {'title': 'Azalea Flower'},
                        {'artist': 'Karine Polwart'},
                        {'compilation': '0'},
                        {'duration': 319},
                        {'album_id': '3925'},
                        {'genre': 'Folk'},
                        {'album': 'Faultlines'},
                        {'genre_id': '332'},
                        {'artist_id': '9334'},
                        ],
                    },
                })),
            mocker.MagicMock(content=json.dumps({
                'method': 'slim.request',
                'result': {
                    'songinfo_loop': [
                        {'tracknum': '11'},
                        {'url': 'file:///media/2yyusb0/music/Karine%20Polwart'
                                '/Faultlines/11%20-%20Azalea%20Flower.flac'},
                        {'year': '2004'},
                        {'addedTime': 'Tuesday, September 21, 2021, 10:46 am'},
                        ],
                    },
                'params': [
                    '',
                    [
                        'songinfo',
                        '10',
                        10,
                        'track_id:56743',
                        'tags:aCDdegilpqstuy',
                        ],
                    ],
                })),
            mocker.MagicMock(content=json.dumps({
                'method': 'slim.request',
                'result': {},
                'params': [
                    '',
                    [
                        'songinfo',
                        '20',
                        10,
                        'track_id:56743',
                        'tags:aCDdegilpqstuy',
                        ],
                    ],
                })),
            ]
    assert dict(id=56743,
                title='Azalea Flower',
                artist='Karine Polwart',
                compilation=False,
                duration=319,
                album_id=3925,
                genre='Folk',
                album='Faultlines',
                genre_id=332,
                artist_id=9334,
                tracknum=11,
                addedTime=datetime(
                    year=2021, month=9, day=21, hour=10, minute=46),
                url='file:///media/2yyusb0/music/Karine%20Polwart'
                    '/Faultlines/11%20-%20Azalea%20Flower.flac',
                year=2004) == database.songinfo(sb_server, 56743)
    assert_posts(requests_post, [
        ['songinfo', 0, 10, 'track_id:56743', 'tags:aCDdegilpqstuy'],
        ['songinfo', 10, 10, 'track_id:56743', 'tags:aCDdegilpqstuy'],
        ['songinfo', 20, 10, 'track_id:56743', 'tags:aCDdegilpqstuy'],
        ])


def test_tracks_default(mocker, requests_post):
    mocker.patch('squeezebox_cli.database.commands.CHUNK_SIZE', 5)
    requests_post.side_effect = [
            mocker.MagicMock(content=json.dumps({
                'params': ['', ['tracks', '0', '5']],
                'result': {
                    'titles_loop': [
                        {
                            'id': 59144,
                            'title': '-',
                            'genre': 'Rock/Pop',
                            'artist': 'Snow Patrol',
                            'album': 'Eyes Open',
                            'duration': 235.373,
                            },
                        {
                            'id': 58059,
                            'title': '?',
                            'genre': 'Punk',
                            'artist': 'Plaster Caster',
                            'album': '"Promo 2007"',
                            'duration': 182.36,
                            },
                        {
                            'id': 59736,
                            'title': '0.28',
                            'genre': 'Rock/Pop',
                            'artist': 'Texas',
                            'album': 'White on Blonde',
                            'duration': 28.466,
                            },
                        {
                            'id': 59734,
                            'title': '0.34',
                            'genre': 'Rock/Pop',
                            'artist': 'Texas',
                            'album': 'White on Blonde',
                            'duration': 34.666,
                            },
                        {
                            'id': 59681,
                            'title': '036',
                            'genre': 'Rock/Pop',
                            'artist': 'Texas',
                            'album': 'Red Book',
                            'duration': 36.213,
                            },
                        ],
                    'count': 5},
                'method': 'slim.request',
                })),
            mocker.MagicMock(content=json.dumps({
                'params': ['', ['tracks', '5', '5']],
                'method': 'slim.request',
                'result': {},
                })),
            ]
    assert [
            dict(id=59144,
                 title='-',
                 genre='Rock/Pop',
                 artist='Snow Patrol',
                 album='Eyes Open',
                 duration=235.373),
            dict(id=58059,
                 title='?',
                 genre='Punk',
                 artist='Plaster Caster',
                 album='"Promo 2007"',
                 duration=182.36),
            dict(id=59736,
                 title='0.28',
                 genre='Rock/Pop',
                 artist='Texas',
                 album='White on Blonde',
                 duration=28.466),
            dict(id=59734,
                 title='0.34',
                 genre='Rock/Pop',
                 artist='Texas',
                 album='White on Blonde',
                 duration=34.666),
            dict(id=59681,
                 title='036',
                 genre='Rock/Pop',
                 artist='Texas',
                 album='Red Book',
                 duration=36.213),
            ] == database.tracks(sb_server)
    assert_posts(requests_post, [
        ['tracks', 0, 5],
        ['tracks', 5, 5],
        ])


def test_tracks_default_search(mocker, requests_post):
    mocker.patch('squeezebox_cli.database.commands.CHUNK_SIZE', 3)
    requests_post.side_effect = [
            mocker.MagicMock(content=json.dumps({
                'method': 'slim.request',
                'result': {
                    'count': 3,
                    'titles_loop': [
                        {
                            'id': 53499,
                            'title': 'Deep & Wide & Tall',
                            'genre': 'Pop',
                            'artist': 'Aztec Camera',
                            'album': 'Love',
                            'duration': 247.266,
                            },
                        {
                            'id': 53518,
                            'title': 'Deep & Wide & Tall',
                            'genre': 'Pop',
                            'artist': 'Aztec Camera',
                            'album': 'The Best of Aztec Camera',
                            'duration': 245.106,
                            },
                        {
                            'id': 59003,
                            'title': 'Tall Ships',
                            'genre': 'Folk',
                            'artist': 'Show of Hands',
                            'album': 'Roots: The Best of Show of Hands',
                            'duration': 1316.32,
                            }
                        ]
                    },
                'params': ['', ['tracks', '0', 3, 'search:tall']],
                })),
            mocker.MagicMock(content=json.dumps({
                'method': 'slim.request',
                'params': ['', ['tracks', '3', 3, 'search:tall']],
                'result': {},
                })),
            ]
    assert [
            dict(id=53499,
                 title='Deep & Wide & Tall',
                 genre='Pop',
                 artist='Aztec Camera',
                 album='Love',
                 duration=247.266),
            dict(id=53518,
                 title='Deep & Wide & Tall',
                 genre='Pop',
                 artist='Aztec Camera',
                 album='The Best of Aztec Camera',
                 duration=245.106),
            dict(id=59003,
                 title='Tall Ships',
                 genre='Folk',
                 artist='Show of Hands',
                 album='Roots: The Best of Show of Hands',
                 duration=1316.32),
            ] == database.tracks(sb_server, search='tall')
    assert_posts(requests_post, [
        ['tracks', 0, 3, 'search:tall'],
        ])


def test_tracks_default_artist(mocker, requests_post):
    mocker.patch('squeezebox_cli.database.commands.CHUNK_SIZE', 3)
    requests_post.side_effect = [
            mocker.MagicMock(content=json.dumps({
                'params': [
                    '',
                    ['tracks', '0', 3, 'artist_id:3238', 'sort:albumtrack']],
                'result': {
                    'titles_loop': [
                        {
                            'id': 54751,
                            'title': 'The A Team',
                            'genre': 'Pop',
                            'artist': 'Ed Sheeran',
                            'album': '+',
                            'duration': 261.026,
                            'tracknum': '1',
                            },
                        {
                            'id': 54755,
                            'title': 'Drunk',
                            'genre': 'Pop',
                            'artist': 'Ed Sheeran',
                            'album': '+',
                            'duration': 199.133,
                            'tracknum': '2',
                            },
                        {
                            'id': 54756,
                            'title': 'U.N.I.',
                            'genre': 'Pop',
                            'artist': 'Ed Sheeran',
                            'album': '+',
                            'duration': 228.773,
                            'tracknum': '3',
                            },
                        ],
                    'count': 3
                    },
                'method': 'slim.request',
                })),
            mocker.MagicMock(content=json.dumps({
                'method': 'slim.request',
                'params': [
                    '',
                    ['tracks', '3', 3, 'artist_id:3238', 'sort:albumtrack']],
                'result': {},
                })),
            ]
    assert [dict(id=54751,
                 title='The A Team',
                 genre='Pop',
                 artist='Ed Sheeran',
                 album='+',
                 tracknum=1,
                 duration=261.026),
            dict(id=54755,
                 title='Drunk',
                 genre='Pop',
                 artist='Ed Sheeran',
                 album='+',
                 tracknum=2,
                 duration=199.133),
            dict(id=54756,
                 title='U.N.I.',
                 genre='Pop',
                 artist='Ed Sheeran',
                 album='+',
                 tracknum=3,
                 duration=228.773),
            ] == database.tracks(sb_server, artist_id=3238)
    assert_posts(requests_post, [
        ['tracks', 0, 3, 'artist_id:3238', 'sort:albumtrack'],
        ])


def test_tracks_default_album(mocker, requests_post):
    mocker.patch('squeezebox_cli.database.commands.CHUNK_SIZE', 3)
    requests_post.side_effect = [
            mocker.MagicMock(content=json.dumps({
                'method': 'slim.request',
                'params': [
                    '',
                    ['tracks', '0', 3, 'album_id:3238', 'sort:albumtrack']],
                'result': {
                    'count': 3,
                    'titles_loop': [
                        {
                            'id': 56733,
                            'title': 'Only One Way',
                            'genre': 'Folk',
                            'artist': 'Karine Polwart',
                            'album': 'Faultlines',
                            'duration': 173.16,
                            'tracknum': '1',
                            },
                        {
                            'id': 56734,
                            'title': 'Faultlines',
                            'genre': 'Folk',
                            'artist': 'Karine Polwart',
                            'album': 'Faultlines',
                            'duration': 196.546,
                            'tracknum': '2',
                            },
                        {
                            'id': 56735,
                            'title': 'Four Strong Walls',
                            'genre': 'Folk',
                            'artist': 'Karine Polwart',
                            'album': 'Faultlines',
                            'duration': 227.573,
                            'tracknum': '3',
                            },
                        ],
                    },
                })),
            mocker.MagicMock(content=json.dumps({
                'method': 'slim.request',
                'params': [
                    '',
                    ['tracks', '3', 3, 'album_id:3238', 'sort:albumtrack']],
                'result': {},
                })),
            ]
    assert [
            dict(id=56733,
                 title='Only One Way',
                 genre='Folk',
                 artist='Karine Polwart',
                 album='Faultlines',
                 tracknum=1,
                 duration=173.16),
            dict(id=56734,
                 title='Faultlines',
                 genre='Folk',
                 artist='Karine Polwart',
                 album='Faultlines',
                 tracknum=2,
                 duration=196.546),
            dict(id=56735,
                 title='Four Strong Walls',
                 genre='Folk',
                 artist='Karine Polwart',
                 album='Faultlines',
                 tracknum=3,
                 duration=227.573),
            ] == database.tracks(sb_server, album_id=3238)
    assert_posts(requests_post, [
        ['tracks', 0, 3, 'album_id:3238', 'sort:albumtrack'],
        ])


def test_tracks_extended_track(mocker, requests_post):
    mocker.patch('squeezebox_cli.database.commands.CHUNK_SIZE', 3)
    requests_post.side_effect = [
            mocker.MagicMock(content=json.dumps({
                'method': 'slim.request',
                'params': [
                    '',
                    ['tracks', '0', 3, 'track_id:56733', 'tags:AytsplgedCa'],
                    ],
                'result': {
                    'titles_loop': [
                        {
                            'id': 56733,
                            'title': 'Only One Way',
                            'artist': 'Karine Polwart',
                            'year': '2004',
                            'tracknum': '1',
                            'artist_id': '9334',
                            'genre_id': '332',
                            'album': 'Faultlines',
                            'genre': 'Folk',
                            'album_id': '3925',
                            'duration': 173.16,
                            'compilation': '0',
                            },
                        ],
                    'count': 1,
                    },
                })),
            mocker.MagicMock(content=json.dumps({
                'method': 'slim.request',
                'params': [
                    '',
                    ['tracks', '3', 3, 'track_id:56733', 'tags:AytsplgedCa'],
                    ],
                'result': {},
                })),
            ]
    assert [
            dict(id=56733,
                 title='Only One Way',
                 year=2004,
                 tracknum=1,
                 artist_id=9334,
                 genre_id=332,
                 album='Faultlines',
                 genre='Folk',
                 album_id=3925,
                 duration=173.16,
                 compilation=False,
                 artist='Karine Polwart'),
            ] == database.tracks(sb_server, track_id=56733, extended=True)
    assert_posts(requests_post, [
        ['tracks', 0, 3, 'track_id:56733', 'tags:AytsplgedCa'],
        ])


def test_search_no_match(mocker, requests_post):
    mocker.patch('squeezebox_cli.database.commands.CHUNK_SIZE', 3)
    requests_post.side_effect = [
            mocker.MagicMock(content=json.dumps({
                'method': 'slim.request',
                'params': ['', ['search', '0', 3, 'term:zzzzz']],
                'result': {},
                })),
            ]
    assert (dict(albums={}, artists={}, tracks={})
            == database.search(sb_server, 'zzzzz'))
    assert_posts(requests_post, [
        ['search', 0, 3, 'term:zzzzz'],
        ])


def test_search_matches_multiple_chunks(mocker, requests_post):
    mocker.patch('squeezebox_cli.database.commands.CHUNK_SIZE', 3)
    requests_post.side_effect = [
            mocker.MagicMock(content=json.dumps({
                'method': 'slim.request',
                'params': ['', ['search', '0', 3, 'term:tall']],
                'result': {
                    'albums_loop': [
                        {'album_id': 3674, 'album': 'Secrets (originals)'},
                        {'album_id': 3691, 'album': 'Love'},
                        {
                            'album_id': 3693,
                            'album': 'The Best of Aztec Camera',
                            },
                        ],
                    'count': 26,
                    'tracks_loop': [
                        {'track_id': 54373, 'track': 'Tall Trees'},
                        {'track': 'Tall Ships', 'track_id': 59003},
                        {
                            'track_id': 53493,
                            'track': "Love will find it's own way",
                            },
                        ],
                    'tracks_count': 16,
                    'albums_count': 10,
                    'contributors_loop': [
                        {'contributor_id': 1234, 'contributor': 'A Singer'},
                        {'contributor_id': 1235, 'contributor': 'A Band'},
                        ],
                    'contributors_count': 2,
                    },
                })),
            mocker.MagicMock(content=json.dumps({
                'method': 'slim.request',
                'params': ['', ['search', '3', 3, 'term:tall']],
                'result': {
                    'tracks_loop': [
                        {'track_id': 2345, 'track': 'A Song'},
                        ],
                    },
                })),
            mocker.MagicMock(content=json.dumps({
                'method': 'slim.request',
                'params': ['', ['search', '6', 3, 'term:tall']],
                'result': {},
                })),
            ]
    assert dict(albums={
                    3674: 'Secrets (originals)',
                    3691: 'Love',
                    3693: 'The Best of Aztec Camera',
                    },
                tracks={
                    54373: 'Tall Trees',
                    59003: 'Tall Ships',
                    53493: "Love will find it's own way",
                    2345: 'A Song',
                    },
                artists={
                    1234: 'A Singer',
                    1235: 'A Band',
                    }) == database.search(sb_server, 'tall')
    assert_posts(requests_post, [
        ['search', 0, 3, 'term:tall'],
        ['search', 3, 3, 'term:tall'],
        ])
