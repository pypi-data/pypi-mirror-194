import sys
from itertools import count
import curses

import squeezebox_cli.player
import squeezebox_cli.database
from .status import shuffle_display_string, repeat_display_string


def show(screen, sb_server, player_id):
    num_rows, num_cols = screen.getmaxyx()
    screen.clear()
    status = squeezebox_cli.player.status(sb_server, player_id)
    len_playlist = len(status['playlist'])
    summary = (
        f"{status['name']}"
        f" {status['playlist_cur_index'] + 1}/{len_playlist}"
        f" {status['playlist'][status['playlist_cur_index']][1]}"
        f" <{status['mode']}>"
        f" vol:{status['volume']}/100")
    try:
        summary += f" s:{shuffle_display_string[status['shuffle']]}"
    except KeyError:
        pass
    try:
        summary += f" r:{repeat_display_string[status['repeat']]}"
    except KeyError:
        pass
    sys.stdout.write(f'\x1b]2;Squeezebox: {summary}\x07')
    sys.stdout.flush()
    tracks_to_show = min(len_playlist, num_rows - 2)
    first_track_to_show = (
        max(0, min(status['playlist_cur_index'],
            len_playlist - tracks_to_show))
        if tracks_to_show < len_playlist else 0)
    playlist_to_show = \
        status['playlist'][first_track_to_show:
                           first_track_to_show + tracks_to_show]
    tracks = [squeezebox_cli.database.songinfo(sb_server, id) if id > 0
              else {'title': t, 'album': '', 'artist': ''}
              for id, t
              in playlist_to_show]
    title_width = max([len(t['title']) for t in tracks])
    album_width = max([len(t['album']) for t in tracks])
    artist_width = max([len(t['artist']) for t in tracks])
    screen.addstr(0, 4, 'Track:', curses.A_BOLD | curses.A_UNDERLINE)
    screen.addstr(
            0, 4 + title_width + 3,
            'Album:', curses.A_BOLD | curses.A_UNDERLINE)
    screen.addstr(
            0, 4 + title_width + 3 + album_width + 3,
            'Artist:', curses.A_BOLD | curses.A_UNDERLINE)
    for i, row, track in zip(
            count(first_track_to_show),
            range(1, num_rows - 1),
            tracks):
        screen.addstr(
                row,
                0,
                f"{i + 1:3}: {track['title']:<{title_width}} :"
                f" {track['album']:<{album_width}} :"
                f" {track['artist']:<{artist_width}}",
                curses.A_STANDOUT if i == status['playlist_cur_index']
                else curses.A_NORMAL)
    screen.addstr(
        num_rows - 1, 0,
        summary,
        curses.A_STANDOUT)
    screen.refresh()
