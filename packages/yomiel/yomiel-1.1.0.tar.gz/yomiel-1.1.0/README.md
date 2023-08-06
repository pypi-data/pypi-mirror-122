# yomiel

[![pypi-pyversions](https://img.shields.io/pypi/pyversions/yomiel?color=%230a66dc)][pypi]
[![pypi-v](https://img.shields.io/pypi/v/yomiel?color=%230a66dc)][pypi]
[![pypi-wheel](https://img.shields.io/pypi/wheel/yomiel?color=%230a66dc)][pypi]
[![pypi-status](https://img.shields.io/pypi/status/yomiel?color=%230a66dc)][pypi]
[![code-style](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi]: https://pypi.org/project/yomiel
[black]: https://pypi.org/project/black

The pretty printer for [jomiel] messages.

![Example (yomiel)](./docs/demo.svg)

## Features

- **Secure**. It can authenticate and encrypt connections with [jomiel]
  by using [CURVE] and [SSH].

- **Flexible.** It prints in different output formats (raw/json/yaml).

- **Configurable**. Many of the options are configurable.

[jomiel]: https://github.com/guendto/jomiel/
[curve]: http://curvezmq.org/
[ssh]: https://en.wikipedia.org/wiki/ssh

## Installation

```shell
pip install yomiel
```

Install from the repository, e.g. for development:

```shell
git clone https://github.com/guendto/jomiel-yomiel
cd jomiel-yomiel
pip install -e .  # Install a project in editable mode
```

Or, if you'd rather not install in "editable mode":

```shell
pip install git+https://github.com/guendto/jomiel-yomiel
```

Be sure to check out `jomiel` [HOWTO], also.

[howto]: https://github.com/guendto/jomiel/blob/master/docs/HOWTO.md#howto-jomiel

## Usage

```text
usage: yomiel [-h] [--version] [-v] [--config-file FILE] [-D] [-E] [-P]
              [--logger-config FILE] [-L] [--logger-idents-verbose] [-l IDENT]
              [-o [raw|json|yaml|terse]] [-r ADDR] [-t TIME] [-m]
              [--auth-mode [none|curve|ssh]]
              [--curve-server-public-key-file FILE]
              [--curve-client-key-file FILE] [--ssh-server user@server:port]
              [--ssh-key-file FILE] [--ssh-password PASSWD]
              [--ssh-timeout TIME] [--ssh-paramiko]
              [<uri> ...]

positional arguments:
  <uri>                 the URIs to parse (default: None)

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v, --version-long    show version information about program's environment
                        and exit (default: False)
  --config-file FILE    Read configuration from the specified file [env var:
                        CONFIG_FILE] (default: None)
  -D, --print-config    Show the configuration values and exit (default:
                        False)
  -E, --report-config   Report keys, values and where they were set (default:
                        False)
  -P, --config-paths    Print default configuration file paths (default:
                        False)
  -o [raw|json|yaml|terse], --output-format [raw|json|yaml|terse]
                        Print messages in the specified data serialization
                        format (default: raw)

logger:
  --logger-config FILE  Logger configuration file to read [env var:
                        LOGGER_CONFIG] (default: None)
  -L, --logger-idents   Print logger identities and exit (default: False)
  --logger-idents-verbose
                        Print logger identities in detail, use together with
                        --logger-idents (default: False)
  -l IDENT, --logger-ident IDENT
                        Use the logger identity [env var: LOGGER_IDENT]
                        (default: default)

jomiel:
  -r ADDR, --router-endpoint ADDR
                        jomiel router endpoint address to connect to (default:
                        tcp://localhost:5514)
  -t TIME, --connect-timeout TIME
                        Maximum time in seconds that the program should allow
                        the connection to the service to take (default: 60)

debug:
  -m, --debug-minify-json
                        Minify JSON messages in the logger (default: False)

auth:
  --auth-mode [none|curve|ssh]
                        Select authentication mode (default: none)

auth: curve:
  --curve-server-public-key-file FILE
                        Public CURVE certificate key file to use for
                        connecting to jomiel (default: .curve/server.key)
  --curve-client-key-file FILE
                        Secret client CURVE key file to use for connecting to
                        jomiel (default: .curve/client.key_secret)

auth: ssh:
  --ssh-server user@server:port
                        SSH server to connect to (default: None)
  --ssh-key-file FILE   Path to the key file to use (default: None)
  --ssh-password PASSWD
                        Password to the SSH server (default: None)
  --ssh-timeout TIME    Time (in seconds) after which no activity will result
                        in the tunnel closing (default: 60)
  --ssh-paramiko        Use paramiko instead of pexpect (default: False)

 If an arg is specified in more than one place, then commandline values
override environment variables which override defaults.
```

## License

`yomiel` is licensed under the [Apache License version 2.0][aplv2].

[aplv2]: https://www.tldrlegal.com/l/apache2

## Acknowledgements

- [pre-commit] is used for linting and reformatting, see the
  [.pre-commit-config.yaml] file

[.pre-commit-config.yaml]: https://github.com/guendto/jomiel-yomiel/blob/master/.pre-commit-config.yaml
[pre-commit]: https://pre-commit.com/
