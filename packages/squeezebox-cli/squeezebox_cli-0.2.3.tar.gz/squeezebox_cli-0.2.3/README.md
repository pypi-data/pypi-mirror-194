# squeezebox-cli [![pipeline status](https://gitlab.com/OldIronHorse/squeezebox-cli/badges/master/pipeline.svg)](https://gitlab.com/OldIronHorse/squeezebox-cli/-/commits/master) [![coverage report](https://gitlab.com/OldIronHorse/squeezebox-cli/badges/master/coverage.svg)](https://gitlab.com/OldIronHorse/squeezebox-cli/-/commits/master)


A command line interface to control Squeezebox players.

## Installation

```
% pip install squeezebox-cli
```

## Configuration

Optionally, the host and port for your Logitech Media Server instance can be configured in ~/.squeezebox-cli.toml

```
[server]
host = your-hostname
port = your-port
```

## Usage

Try:

```
% squeezebox-cli --help
```

and explore from there.

List the connected players:
```
% squeezebox-cli players
  index  name         is playing?
-------  -----------  -------------
      0  Dining Room  no
      1  Kitchen      no
      2  Lounge       no
%
```

Show a player's status (short):
```
% squeezebox-cli player 0 status
[Dining Room] <stop> vol:23/100 2/13 The Goodman [>>The Daughter of Megan]
```

Show a player's status (long):
```
% squeezebox-cli player 0 status
[Dining Room] <stop> vol:23/100 2/11 The Goodman [>>The Daughter of Megan]
         index  title                                   album                 artist
-----  -------  --------------------------------------  --------------------  ----------
             1  The Village Green Preservation Society  Awkward Annie         Kate Rusby
>>>          2  The Goodman                             Underneath the Stars  Kate Rusby
             3  The Daughter of Megan                   Underneath the Stars  Kate Rusby
             4  Cruel                                   Underneath the Stars  Kate Rusby
             5  The Blind Harper                        Underneath the Stars  Kate Rusby
             6  The White Cockade                       Underneath the Stars  Kate Rusby
             7  Falling                                 Underneath the Stars  Kate Rusby
             8  Bring Me a Boat                         Underneath the Stars  Kate Rusby
             9  Polly                                   Underneath the Stars  Kate Rusby
            10  Sweet William's Ghost                   Underneath the Stars  Kate Rusby
            11  Underneath the Stars                    Underneath the Stars  Kate Rusby
%
```

Monitor a player:

```
% squeezebox-cli player 0 monitor
```

```
    Track:                                   Album:                 Artist:
  1: The Village Green Preservation Society : Awkward Annie        : Kate Rusby
  2: The Goodman                            : Underneath the Stars : Kate Rusby
  3: The Daughter of Megan                  : Underneath the Stars : Kate Rusby
  4: Cruel                                  : Underneath the Stars : Kate Rusby
  5: The Blind Harper                       : Underneath the Stars : Kate Rusby
  6: The White Cockade                      : Underneath the Stars : Kate Rusby
  7: Falling                                : Underneath the Stars : Kate Rusby
  8: Bring Me a Boat                        : Underneath the Stars : Kate Rusby
  9: Polly                                  : Underneath the Stars : Kate Rusby
 10: Sweet William's Ghost                  : Underneath the Stars : Kate Rusby
 11: Underneath the Stars                   : Underneath the Stars : Kate Rusby



Dining Room 2/11 The Goodman <stop> vol:23/100
```
