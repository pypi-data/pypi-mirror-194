import pytest

from squeezebox_cli.player import Shuffle
from squeezebox_cli.display import format_status, format_playlist


def test_format_status_one_track():
    status = dict(
            name='Kitchen',
            mode='pause',
            volume=49,
            playlist_cur_index=0,
            playlist=[(12345, 'One For The Ditch')],
            )
    assert ('[Kitchen] <pause> vol:49/100 1/1 One For The Ditch'
            == format_status(status))


def test_format_status_three_tracks():
    status = dict(
            name='Kitchen',
            mode='play',
            volume=49,
            playlist_cur_index=1,
            playlist=[
                (12345, 'cardigan'),
                (12345, 'One For The Ditch'),
                (12345, 'Vincent Black Lightning'),
                ],
            )
    assert ('[Kitchen] <play> vol:49/100 2/3 One For The Ditch'
            ' [>>Vincent Black Lightning]' == format_status(status))


def test_format_status_three_tracks_shuffle_song():
    status = dict(
            name='Kitchen',
            mode='play',
            volume=49,
            shuffle=Shuffle.SONG,
            playlist_cur_index=1,
            playlist=[
                (12345, 'cardigan'),
                (12345, 'One For The Ditch'),
                (12345, 'Vincent Black Lightning'),
                ],
            )
    assert ('[Kitchen] <play> s:song vol:49/100 2/3 One For The Ditch'
            ' [>>Vincent Black Lightning]' == format_status(status))


@pytest.fixture()
def playlist():
    return [
            dict(title='the 1',
                 album='folklore',
                 artist='Taylor Swift'),
            dict(title='cardigan',
                 album='folklore',
                 artist='Taylor Swift'),
            dict(title='the last great american dynasty',
                 album='folklore',
                 artist='Taylor Swift'),
            dict(title='exile',
                 album='folklore',
                 artist='Taylor Swift'),
            dict(title='my tears ricochet',
                 album='folklore',
                 artist='Taylor Swift'),
            dict(title='mirrorball',
                 album='folklore',
                 artist='Taylor Swift'),
            dict(title='seven',
                 album='folklore',
                 artist='Taylor Swift'),
            dict(title='august',
                 album='folklore',
                 artist='Taylor Swift'),
            dict(title='this is me trying',
                 album='folklore',
                 artist='Taylor Swift'),
            dict(title='illicit affairs',
                 album='folklore',
                 artist='Taylor Swift'),
            dict(title='invisible string',
                 album='folklore',
                 artist='Taylor Swift'),
            dict(title='mad woman',
                 album='folklore',
                 artist='Taylor Swift'),
            dict(title='epiphany',
                 album='folklore',
                 artist='Taylor Swift'),
            dict(title='betty',
                 album='folklore',
                 artist='Taylor Swift'),
            dict(title='peace',
                 album='folklore',
                 artist='Taylor Swift'),
            dict(title='hoax',
                 album='folklore',
                 artist='Taylor Swift'),
            dict(title='the lakes',
                 album='folklore',
                 artist='Taylor Swift'),
            ]


def test_format_playlist_three_tracks():
    playlist = [
        dict(title='cardigan',
             album='folklore',
             artist='Taylor Swift'),
        dict(title='One For The Ditch',
             album='Some Kind of Certainty',
             artist='Ewan Robertson'),
        dict(title='Vincent Black Lightning',
             album='Some Kind of Certainty',
             artist='Ewan Robertson'),
        ]
    assert (
        '         index  title                    album                   '
        'artist\n'
        '-----  -------  -----------------------  ----------------------  '
        '--------------\n'
        '             1  cardigan                 folklore                '
        'Taylor Swift\n'
        '>>>          2  One For The Ditch        Some Kind of Certainty  '
        'Ewan Robertson\n'
        '             3  Vincent Black Lightning  Some Kind of Certainty  '
        'Ewan Robertson' == format_playlist(playlist, 1))


def test_format_playlist_all(playlist):
    assert (
            '         index  title                            album    '
            ' artist\n'
            '-----  -------  -------------------------------  -------- '
            ' ------------\n'
            '             1  the 1                            folklore '
            ' Taylor Swift\n'
            '             2  cardigan                         folklore '
            ' Taylor Swift\n'
            '             3  the last great american dynasty  folklore '
            ' Taylor Swift\n'
            '             4  exile                            folklore '
            ' Taylor Swift\n'
            '>>>          5  my tears ricochet                folklore '
            ' Taylor Swift\n'
            '             6  mirrorball                       folklore '
            ' Taylor Swift\n'
            '             7  seven                            folklore '
            ' Taylor Swift\n'
            '             8  august                           folklore '
            ' Taylor Swift\n'
            '             9  this is me trying                folklore '
            ' Taylor Swift\n'
            '            10  illicit affairs                  folklore '
            ' Taylor Swift\n'
            '            11  invisible string                 folklore '
            ' Taylor Swift\n'
            '            12  mad woman                        folklore '
            ' Taylor Swift\n'
            '            13  epiphany                         folklore '
            ' Taylor Swift\n'
            '            14  betty                            folklore '
            ' Taylor Swift\n'
            '            15  peace                            folklore '
            ' Taylor Swift\n'
            '            16  hoax                             folklore '
            ' Taylor Swift\n'
            '            17  the lakes                        folklore '
            ' Taylor Swift' == format_playlist(playlist, 4))


def test_format_playlist_limit_start(playlist):
    assert (
            '         index  title              album    '
            ' artist\n'
            '-----  -------  -----------------  -------- '
            ' ------------\n'
            '[-3]\n'
            '             4  exile              folklore '
            ' Taylor Swift\n'
            '>>>          5  my tears ricochet  folklore '
            ' Taylor Swift\n'
            '             6  mirrorball         folklore '
            ' Taylor Swift\n'
            '             7  seven              folklore '
            ' Taylor Swift\n'
            '             8  august             folklore '
            ' Taylor Swift\n'
            '             9  this is me trying  folklore '
            ' Taylor Swift\n'
            '            10  illicit affairs    folklore '
            ' Taylor Swift\n'
            '            11  invisible string   folklore '
            ' Taylor Swift\n'
            '            12  mad woman          folklore '
            ' Taylor Swift\n'
            '            13  epiphany           folklore '
            ' Taylor Swift\n'
            '[+4]' == format_playlist(playlist, 4, 10))


def test_format_playlist_limit_end(playlist):
    assert (
            '         index  title      album    '
            ' artist\n'
            '-----  -------  ---------  -------- '
            ' ------------\n'
            '[-12]\n'
            '            13  epiphany   folklore '
            ' Taylor Swift\n'
            '            14  betty      folklore '
            ' Taylor Swift\n'
            '            15  peace      folklore '
            ' Taylor Swift\n'
            '>>>         16  hoax       folklore '
            ' Taylor Swift\n'
            '            17  the lakes  folklore '
            ' Taylor Swift' == format_playlist(playlist, 15, 5))
