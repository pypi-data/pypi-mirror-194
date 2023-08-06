import pytest
from click.testing import CliRunner

import squeezebox_cli.ui.main


@pytest.fixture()
def min_config(mocker):
    return mocker.patch('squeezebox_cli.ui.main.open',
                        mocker.mock_open(read_data=b'[server]\n'
                                                   b"host = 'my-host'\n"))


@pytest.fixture()
def player_status(mocker):
    return mocker.patch(
            'squeezebox_cli.ui.main.squeezebox_cli.player.status',
            return_value={
                 'name': 'office',
                 'mode': 'stop',
                 'volume': 53,
                 'playlist_cur_index': 1,
                 'playlist': [
                     (52734, 'City of Love'),
                     (52807, 'the 1'),
                     (52816, 'cardigan'),
                     (52818, 'exile'),
                     (52819, 'hoax'),
                     ],
                 })


@pytest.fixture()
def database_songinfo(mocker):
    stub_songinfo = {
            52734: {
                'title': 'City of Love',
                'album': 'City of Love',
                'artist': 'Deacon Blue',
                },
            52807: {
                'title': 'the 1',
                'album': 'folklore',
                'artist': 'Taylor Swift',
                },
            52816: {
                'title': 'cardigan',
                'album': 'folklore',
                'artist': 'Taylor Swift',
                },
            52818: {
                'title': 'exile',
                'album': 'folklore',
                'artist': 'Taylor Swift',
                },
            52819: {
                'title': 'hoax',
                'album': 'folklore',
                'artist': 'Taylor Swift',
                },
            }
    return mocker.patch(
            'squeezebox_cli.ui.main.squeezebox_cli.database.songinfo',
            lambda host_port, track_id: stub_songinfo[track_id])


@pytest.fixture()
def playlist_add(mocker):
    return mocker.patch(
            'squeezebox_cli.ui.main.squeezebox_cli.player.playlist_add')


@pytest.fixture()
def playlist_insert(mocker):
    return mocker.patch(
            'squeezebox_cli.ui.main.squeezebox_cli.player.playlist_insert')


@pytest.fixture()
def player_set_volume(mocker):
    return mocker.patch(
            'squeezebox_cli.ui.main.squeezebox_cli.player.set_volume')


@pytest.fixture()
def players_list_all(mocker):
    return mocker.patch(
            'squeezebox_cli.ui.main.squeezebox_cli.player.players',
            return_value=[
                dict(playerindex=0,
                     connected=True,
                     name='office',
                     isplaying=False),
                dict(playerindex=1,
                     connected=True,
                     name='lounge',
                     isplaying=True),
                ])


def test_players_valid_connection_args(mocker, players_list_all):
    runner = CliRunner()
    result = runner.invoke(squeezebox_cli.ui.main.ui_main,
                           ['--host=my-host', '--port=1234', 'players'])
    players_list_all.assert_called_once_with(('my-host', 1234))
    assert 0 == result.exit_code
    assert ('name    is playing?\n'
            '------  -------------\n'
            'office  no\n'
            'lounge  yes\n') == result.output


def test_players_valid_connection_config(mocker, players_list_all):
    open_config = mocker.patch('squeezebox_cli.ui.main.open',
                               mocker.mock_open(read_data=b'[server]\n'
                                                          b"host = 'my-host'\n"
                                                          b'port = 1234\n'))
    runner = CliRunner()
    result = runner.invoke(squeezebox_cli.ui.main.ui_main, ['players'])
    open_config.assert_called_once()
    players_list_all.assert_called_once_with(('my-host', 1234))
    assert 0 == result.exit_code
    assert ('name    is playing?\n'
            '------  -------------\n'
            'office  no\n'
            'lounge  yes\n') == result.output


def test_players_valid_connection_config_default_port(
        mocker, players_list_all):
    open_config = mocker.patch('squeezebox_cli.ui.main.open',
                               mocker.mock_open(
                                   read_data=b'[server]\n'
                                             b"host = 'my-host'\n"))
    runner = CliRunner()
    result = runner.invoke(squeezebox_cli.ui.main.ui_main, ['players'])
    open_config.assert_called_once()
    players_list_all.assert_called_once_with(('my-host', 9000))
    assert 0 == result.exit_code
    assert ('name    is playing?\n'
            '------  -------------\n'
            'office  no\n'
            'lounge  yes\n') == result.output


def test_players_invalid_connection_no_config(mocker):
    open_config = mocker.patch('squeezebox_cli.ui.main.open',
                               mocker.MagicMock(
                                   side_effect=FileNotFoundError()))
    runner = CliRunner()
    result = runner.invoke(squeezebox_cli.ui.main.ui_main, ['players'])
    open_config.assert_called_once()
    assert 1 == result.exit_code
    assert ('ERROR: you must specify a host.'
            ' Either in configuration (~/.squeezebox-cli.toml)'
            ' or by argument (--host=).\n') == result.output


def test_search_nothing_found(mocker, min_config):
    search = mocker.patch(
            'squeezebox_cli.ui.main.squeezebox_cli.database.search',
            return_value={
                'artists': {},
                'albums': {},
                'tracks': {},
                })
    runner = CliRunner()
    result = runner.invoke(squeezebox_cli.ui.main.ui_main, ['search', 'toast'])
    search.assert_called_once_with(('my-host', 9000), 'toast')
    assert 0 == result.exit_code
    assert ('artist    id\n'
            '--------  ----\n'
            '\n'
            'album    id\n'
            '-------  ----\n'
            '\n'
            'track    id\n'
            '-------  ----\n') == result.output


def test_search_something_found(mocker, min_config):
    search = mocker.patch(
            'squeezebox_cli.ui.main.squeezebox_cli.database.search',
            return_value={
                'artists': {
                    1234: 'A Singer',
                    1235: 'A Band',
                    1236: 'A Group',
                    },
                'albums': {
                    2345: 'A Rock Album',
                    2346: 'A Jazz Album',
                    },
                'tracks': {
                    3456: 'A Song',
                    3457: 'Another Song',
                    },
                })
    runner = CliRunner()
    result = runner.invoke(squeezebox_cli.ui.main.ui_main, ['search', 'toast'])
    search.assert_called_once_with(('my-host', 9000), 'toast')
    assert 0 == result.exit_code
    assert ('artist      id\n'
            '--------  ----\n'
            'A Singer  1234\n'
            'A Band    1235\n'
            'A Group   1236\n'
            '\n'
            'album           id\n'
            '------------  ----\n'
            'A Rock Album  2345\n'
            'A Jazz Album  2346\n'
            '\n'
            'track           id\n'
            '------------  ----\n'
            'A Song        3456\n'
            'Another Song  3457\n'
            ) == result.output


def test_player_no_such_name(mocker, min_config, players_list_all):
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'garden',
        'stop',
        ])
    assert 'ERROR: no such player: garden\n' == result.output
    assert 2 == result.exit_code


def test_player_stop(mocker, min_config, players_list_all):
    player_stop = mocker.patch(
            'squeezebox_cli.ui.main.squeezebox_cli.player.stop')
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'stop',
        ])
    player_stop.assert_called_once_with(('my-host', 9000), 'office')
    assert 0 == result.exit_code


def test_player_shuffled_none(mocker, min_config, players_list_all):
    player_shuffled = mocker.patch(
            'squeezebox_cli.ui.main'
            '.squeezebox_cli.player.playlist_query_shuffle',
            return_value=squeezebox_cli.player.Shuffle.NONE)
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'shuffled',
        ])
    player_shuffled.assert_called_once_with(('my-host', 9000), 'office')
    assert 0 == result.exit_code
    assert 'none\n' == result.output


def test_player_shuffled_song(mocker, min_config, players_list_all):
    player_shuffled = mocker.patch(
            'squeezebox_cli.ui.main'
            '.squeezebox_cli.player.playlist_query_shuffle',
            return_value=squeezebox_cli.player.Shuffle.SONG)
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'shuffled',
        ])
    player_shuffled.assert_called_once_with(('my-host', 9000), 'office')
    assert 0 == result.exit_code
    assert 'song\n' == result.output


def test_player_shuffled_album(mocker, min_config, players_list_all):
    player_shuffled = mocker.patch(
            'squeezebox_cli.ui.main'
            '.squeezebox_cli.player.playlist_query_shuffle',
            return_value=squeezebox_cli.player.Shuffle.ALBUM)
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'shuffled',
        ])
    player_shuffled.assert_called_once_with(('my-host', 9000), 'office')
    assert 0 == result.exit_code
    assert 'album\n' == result.output


def test_player_shuffle_none(mocker, min_config, players_list_all):
    player_shuffle = mocker.patch(
            'squeezebox_cli.ui.main'
            '.squeezebox_cli.player.playlist_set_shuffle')
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'shuffle',
        'none',
        ])
    player_shuffle.assert_called_once_with(
            ('my-host', 9000),
            'office',
            squeezebox_cli.player.Shuffle.NONE)
    assert 0 == result.exit_code


def test_player_shuffle_song(mocker, min_config, players_list_all):
    player_shuffle = mocker.patch(
            'squeezebox_cli.ui.main'
            '.squeezebox_cli.player.playlist_set_shuffle')
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'shuffle',
        'song',
        ])
    player_shuffle.assert_called_once_with(
            ('my-host', 9000),
            'office',
            squeezebox_cli.player.Shuffle.SONG)
    assert 0 == result.exit_code


def test_player_shuffle_album(mocker, min_config, players_list_all):
    player_shuffle = mocker.patch(
            'squeezebox_cli.ui.main'
            '.squeezebox_cli.player.playlist_set_shuffle')
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'shuffle',
        'album',
        ])
    player_shuffle.assert_called_once_with(
            ('my-host', 9000),
            'office',
            squeezebox_cli.player.Shuffle.ALBUM)
    assert 0 == result.exit_code


def test_player_toggle_shuffle(mocker, min_config, players_list_all):
    player_shuffle = mocker.patch(
            'squeezebox_cli.ui.main'
            '.squeezebox_cli.player.playlist_toggle_shuffle')
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'shuffle',
        ])
    player_shuffle.assert_called_once_with(
            ('my-host', 9000),
            'office')
    assert 0 == result.exit_code


def test_player_repeating_none(mocker, min_config, players_list_all):
    player_repeating = mocker.patch(
            'squeezebox_cli.ui.main'
            '.squeezebox_cli.player.playlist_query_repeat',
            return_value=squeezebox_cli.player.Repeat.NONE)
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'repeating',
        ])
    player_repeating.assert_called_once_with(
            ('my-host', 9000),
            'office')
    assert 0 == result.exit_code
    assert 'none\n' == result.output


def test_player_repeating_song(mocker, min_config, players_list_all):
    player_repeating = mocker.patch(
            'squeezebox_cli.ui.main'
            '.squeezebox_cli.player.playlist_query_repeat',
            return_value=squeezebox_cli.player.Repeat.SONG)
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'repeating',
        ])
    player_repeating.assert_called_once_with(
            ('my-host', 9000),
            'office')
    assert 0 == result.exit_code
    assert 'song\n' == result.output


def test_player_repeating_all(mocker, min_config, players_list_all):
    player_repeating = mocker.patch(
            'squeezebox_cli.ui.main'
            '.squeezebox_cli.player.playlist_query_repeat',
            return_value=squeezebox_cli.player.Repeat.ALL)
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'repeating',
        ])
    player_repeating.assert_called_once_with(
            ('my-host', 9000),
            'office')
    assert 0 == result.exit_code
    assert 'all\n' == result.output


def test_player_repeat_none(mocker, min_config, players_list_all):
    player_repeat = mocker.patch(
            'squeezebox_cli.ui.main.squeezebox_cli.player.playlist_set_repeat')
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'repeat',
        'none',
        ])
    player_repeat.assert_called_once_with(
            ('my-host', 9000),
            'office',
            squeezebox_cli.player.Repeat.NONE)
    assert 0 == result.exit_code


def test_player_repeat_song(mocker, min_config, players_list_all):
    player_repeat = mocker.patch(
            'squeezebox_cli.ui.main.squeezebox_cli.player.playlist_set_repeat')
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'repeat',
        'song',
        ])
    player_repeat.assert_called_once_with(
            ('my-host', 9000),
            'office',
            squeezebox_cli.player.Repeat.SONG)
    assert 0 == result.exit_code


def test_player_repeat_all(mocker, min_config, players_list_all):
    player_repeat = mocker.patch(
            'squeezebox_cli.ui.main.squeezebox_cli.player.playlist_set_repeat')
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'repeat',
        'all',
        ])
    player_repeat.assert_called_once_with(
            ('my-host', 9000),
            'office',
            squeezebox_cli.player.Repeat.ALL)
    assert 0 == result.exit_code


def test_player_toggle_repeat(mocker, min_config, players_list_all):
    player_repeat = mocker.patch(
                'squeezebox_cli.ui.main'
                '.squeezebox_cli.player.playlist_toggle_repeat')
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'repeat',
        ])
    player_repeat.assert_called_once_with(
            ('my-host', 9000),
            'office')
    assert 0 == result.exit_code


def test_player_play_track(mocker, min_config, players_list_all):
    player_play = mocker.patch(
            'squeezebox_cli.ui.main.squeezebox_cli.player.play')
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'play',
        'track',
        '1234',
        ])
    player_play.assert_called_once_with(('my-host', 9000),
                                        'office',
                                        track_id=1234)
    assert 0 == result.exit_code


def test_player_play_album(mocker, min_config, players_list_all):
    player_play = mocker.patch(
            'squeezebox_cli.ui.main.squeezebox_cli.player.play')
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'play',
        'album',
        '1234',
        ])
    player_play.assert_called_once_with(('my-host', 9000),
                                        'office',
                                        album_id=1234)
    assert 0 == result.exit_code


def test_player_pause(mocker, min_config, players_list_all):
    player_pause = mocker.patch(
            'squeezebox_cli.ui.main.squeezebox_cli.player.pause')
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'pause',
        ])
    player_pause.assert_called_once_with(('my-host', 9000), 'office')
    assert 0 == result.exit_code


def test_player_status(min_config, players_list_all, player_status):
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'status',
        ])
    player_status.assert_called_once_with(('my-host', 9000), 'office')
    assert ('[office] <stop> vol:53/100 2/5 the 1 [>>cardigan]\n' ==
            result.output)
    assert 0 == result.exit_code


def test_player_status_long(
        min_config, players_list_all, player_status,
        database_songinfo):
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'status',
        '--long',
        ])
    player_status.assert_called_once_with(('my-host', 9000), 'office')
    assert ('[office] <stop> vol:53/100 2/5 the 1 [>>cardigan]\n'
            '         index  title         album         artist\n'
            '-----  -------  ------------  ------------  ------------\n'
            '             1  City of Love  City of Love  Deacon Blue\n'
            '>>>          2  the 1         folklore      Taylor Swift\n'
            '             3  cardigan      folklore      Taylor Swift\n'
            '             4  exile         folklore      Taylor Swift\n'
            '             5  hoax          folklore      Taylor Swift\n'
            ) == result.output
    assert 0 == result.exit_code


def test_player_next(mocker, min_config, players_list_all):
    player_next = mocker.patch(
            'squeezebox_cli.ui.main.squeezebox_cli.player.next')
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'next',
        ])
    player_next.assert_called_once_with(('my-host', 9000), 'office')
    assert 0 == result.exit_code


def test_player_previous(
        mocker, min_config, players_list_all):
    player_previous = mocker.patch(
            'squeezebox_cli.ui.main.squeezebox_cli.player.previous')
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'previous',
        ])
    player_previous.assert_called_once_with(('my-host', 9000), 'office')
    assert 0 == result.exit_code


def test_player_add_track(
        min_config, players_list_all, playlist_add):
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'add',
        'track',
        '1234',
        ])
    playlist_add.assert_called_once_with(
            ('my-host', 9000), 'office', track_id='1234')
    assert 0 == result.exit_code


def test_player_add_album(
        min_config, players_list_all, playlist_add):
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'add',
        'album',
        '1234',
        ])
    playlist_add.assert_called_once_with(
            ('my-host', 9000), 'office', album_id='1234')
    assert 0 == result.exit_code


def test_player_insert_track(
        min_config, players_list_all, playlist_insert):
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'insert',
        'track',
        '1234',
        ])
    playlist_insert.assert_called_once_with(
            ('my-host', 9000), 'office', track_id='1234')
    assert 0 == result.exit_code


def test_player_insert_album(
        min_config, players_list_all, playlist_insert):
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'insert',
        'album',
        '1234',
        ])
    playlist_insert.assert_called_once_with(
            ('my-host', 9000), 'office', album_id='1234')
    assert 0 == result.exit_code


def test_player_volume_set(
        min_config, players_list_all, player_set_volume):
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'volume',
        '60',
        ])
    player_set_volume.assert_called_once_with(
            ('my-host', 9000), 'office', '60')
    assert 0 == result.exit_code


def test_playlist_remove(
        mocker, min_config, players_list_all):
    playlist_remove = mocker.patch(
        'squeezebox_cli.ui.main.squeezebox_cli.player.playlist_remove')
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'remove',
        '60',
        ])
    playlist_remove.assert_called_once_with(('my-host', 9000), 'office', 59)
    assert 0 == result.exit_code


def test_playlist_index(mocker, min_config, players_list_all):
    playlist_index = mocker.patch(
            'squeezebox_cli.ui.main.squeezebox_cli.player.playlist_index')
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'index',
        '+3',
        ])
    playlist_index.assert_called_once_with(('my-host', 9000), 'office', '+3')
    assert 0 == result.exit_code


def test_playlist_index_negative(mocker, min_config, players_list_all):
    playlist_index = mocker.patch(
            'squeezebox_cli.ui.main.squeezebox_cli.player.playlist_index')
    result = CliRunner().invoke(squeezebox_cli.ui.main.ui_main, [
        'player',
        'office',
        'index',
        '--',
        '-3',
        ])
    playlist_index.assert_called_once_with(('my-host', 9000), 'office', '-3')
    assert 0 == result.exit_code
