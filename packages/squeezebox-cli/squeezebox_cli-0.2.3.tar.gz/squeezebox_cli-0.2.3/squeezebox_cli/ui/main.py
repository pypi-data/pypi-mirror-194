import click
import sys
import os
import time
import tomllib
from tabulate import tabulate
import curses
import requests

from squeezebox_cli import __version__
import squeezebox_cli.player
import squeezebox_cli.display

player_id = None
sb_server = None


def safe_main():
    try:
        ui_main()
    except requests.exceptions.ConnectionError:
        host, port = sb_server
        click.echo(f'ERROR: could not connect to {host}:{port}')
        sys.exit(1)


@click.group()
@click.version_option(__version__)
@click.option(
        '--host', type=str,
        help='hostname for squeezebox server')
@click.option(
        '--port', type=int,
        help='port for squeezebox server (default 9090)')
def ui_main(host, port):
    try:
        with open(os.path.expanduser('~/.squeezebox-cli.toml'), 'rb') as f:
            cfg = tomllib.load(f)
            if not host:
                try:
                    host = cfg['server']['host']
                except KeyError:
                    pass
            if not port:
                try:
                    port = cfg['server']['port']
                except KeyError:
                    pass
    except FileNotFoundError:
        pass
    if not host:
        click.echo('ERROR: you must specify a host.'
                   ' Either in configuration (~/.squeezebox-cli.toml)'
                   ' or by argument (--host=).')
        sys.exit(1)
    if not port:
        port = 9000
    global sb_server
    sb_server = (host, port)


@ui_main.command(name='players', help='list the currently connected players')
def ui_players():
    # TODO: options for columns to show?
    ps = squeezebox_cli.player.players(sb_server)
    click.echo(tabulate(
        [(p['name'], 'yes' if p['isplaying'] else 'no')
            for p in ps],
        headers=['name', 'is playing?']))


@ui_main.command(name='search', help='search the music database')
@click.argument('term')
def ui_search(term):
    reply = squeezebox_cli.database.search(sb_server, term)
    artists = reply['artists']
    click.echo(tabulate(
        [(artist, id) for id, artist in artists.items()],
        headers=['artist', 'id']))
    click.echo()
    albums = reply['albums']
    click.echo(tabulate(
        [(album, id) for id, album in albums.items()],
        headers=['album', 'id']))
    click.echo()
    tracks = reply['tracks']
    click.echo(tabulate(
        [(track, id) for id, track in tracks.items()],
        headers=['track', 'id']))


@ui_main.group(name='player',
               help='view and control a player by name or index')
@click.argument('player-name')
def player(player_name):
    if player_name not in {p['name'] for p
                           in squeezebox_cli.player.players(
                               sb_server)}:
        click.echo(f'ERROR: no such player: {player_name}')
        sys.exit(2)
    global player_id
    player_id = player_name


@player.command(name='stop', help='stop the specified player')
def ui_stop():
    squeezebox_cli.player.stop(sb_server, player_id)


SHUFFLE_BY_STRING = {
        'none': squeezebox_cli.player.Shuffle.NONE,
        'song': squeezebox_cli.player.Shuffle.SONG,
        'album': squeezebox_cli.player.Shuffle.ALBUM,
        }

SHUFFLE_TO_STRING = {v: k for k, v in SHUFFLE_BY_STRING.items()}


@player.command(help='query shuffle state on the specified player')
def shuffled():
    click.echo(SHUFFLE_TO_STRING[squeezebox_cli.player.playlist_query_shuffle(
        sb_server, player_id)])


@player.command(help='set the shuffle state on the specified player')
@click.argument('shuffle-type',
                type=click.Choice(['none', 'song', 'album']),
                required=False)
def shuffle(shuffle_type):
    try:
        squeezebox_cli.player.playlist_set_shuffle(
                sb_server, player_id, SHUFFLE_BY_STRING[shuffle_type])
    except KeyError:
        squeezebox_cli.player.playlist_toggle_shuffle(sb_server,
                                                      player_id)


@player.command(help='query the repeat state of the specified player')
def repeating():
    click.echo(REPEAT_TO_STRING[squeezebox_cli.player.playlist_query_repeat(
        sb_server, player_id)])


REPEAT_BY_STRING = {
        'none': squeezebox_cli.player.Repeat.NONE,
        'song': squeezebox_cli.player.Repeat.SONG,
        'all': squeezebox_cli.player.Repeat.ALL,
        }

REPEAT_TO_STRING = {v: k for k, v in REPEAT_BY_STRING.items()}


@player.command(help='set the repeat state on the specified player')
@click.argument('repeat-type',
                type=click.Choice(['none', 'song', 'all']),
                required=False)
def repeat(repeat_type):
    try:
        squeezebox_cli.player.playlist_set_repeat(
                sb_server, player_id, REPEAT_BY_STRING[repeat_type])
    except KeyError:
        squeezebox_cli.player.playlist_toggle_repeat(sb_server,
                                                     player_id)


@player.group(name='play', help='play a track or album')
def ui_play():
    pass


@ui_play.command(name='track', help='play the specified track')
@click.argument('track_id', type=int)
def play_track(track_id):
    squeezebox_cli.player.play(sb_server, player_id, track_id=track_id)


@ui_play.command(name='album', help='play the specified album')
@click.argument('album_id', type=int)
def play_album(album_id):
    squeezebox_cli.player.play(sb_server, player_id, album_id=album_id)


@player.command(name='pause', help='pause/unpause the specified player')
def ui_pause():
    squeezebox_cli.player.pause(sb_server, player_id)


@player.command(name='status', help='status of the specified player')
@click.option(
        '--long/--short', default=False,
        help='verbose output, playlist etc.')
@click.option('--max-tracks', type=int)
def ui_status(long, max_tracks):
    s = squeezebox_cli.player.status(sb_server, player_id)
    click.echo(squeezebox_cli.display.format_status(s))
    if long:
        click.echo(squeezebox_cli.display.format_playlist(
            [squeezebox_cli.database.songinfo(sb_server, id)
                if id > 0
                else dict(title=t, album='[Radio]', artist=None)
             for id, t in s['playlist']],
            s['playlist_cur_index'],
            max_tracks))


@player.command(help='monitor the specified player')
def monitor():

    def do_tui(screen):
        curses.curs_set(0)
        while True:
            squeezebox_cli.display.show(screen, sb_server, player_id)
            time.sleep(0.5)

    curses.wrapper(do_tui)


@player.command(name='next',
                help='play the next track in the current playlist')
def ui_next():
    squeezebox_cli.player.next(sb_server, player_id)


@player.command(name='previous',
                help='play the previous track in the current playlist')
def ui_previous():
    squeezebox_cli.player.previous(sb_server, player_id)


@player.group(help=('add a track or album to the end of the current playlist'))
def add():
    pass


@add.command(name='track',
             help='add a track to the end of the current playlist')
@click.argument('track_id')
def add_track(track_id):
    squeezebox_cli.player.playlist_add(sb_server, player_id, track_id=track_id)


@add.command(name='album',
             help='add an album to the end of the current playlist')
@click.argument('album_id')
def add_album(album_id):
    squeezebox_cli.player.playlist_add(sb_server, player_id, album_id=album_id)


@player.group(help='insert a track or album after the current track')
def insert():
    pass


@insert.command(name='track', help='insert a track after the current one')
@click.argument('track_id')
def insert_track(track_id):
    squeezebox_cli.player.playlist_insert(sb_server,
                                          player_id,
                                          track_id=track_id)


@insert.command(name='album', help='insert an album after the current track')
@click.argument('album_id')
def insert_album(album_id):
    squeezebox_cli.player.playlist_insert(sb_server,
                                          player_id,
                                          album_id=album_id)


@player.command(help='set or change the player volume N, +N or -- -N')
@click.argument('vol', type=str)
def volume(vol):
    squeezebox_cli.player.set_volume(sb_server, player_id, vol)


@player.command(help='remove a track from the current playlist by index')
@click.argument('index', type=int)
def remove(index):
    squeezebox_cli.player.playlist_remove(sb_server, player_id, index - 1)


@player.command(
        name='index',
        help='set or modify the current track by playlist index N, +N, -- -N')
@click.argument('index')
def ui_index(index):
    squeezebox_cli.player.playlist_index(sb_server, player_id, index)
