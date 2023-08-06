# dwnld

![dwnld.png](https://raw.githubusercontent.com/4thel00z/logos/master/dwnld.png)

## Motivation

A library to download stuff given urls with different protocols, like `ftp://...` or `ssh://...`.

## Usage

There is only one interesting module level function in this repo, it can download (or move) stuff from A to B:

```python
from dwnld import download

download("file://stuff.txt", "somewhere_else.txt")
download("ssh://some-remote-server:/home/reptile/stuff.txt", "here.txt")
download("https://cool.com/nice.pdf", "here.pdf")
download("http://cool.com/nice.pdf", "here.pdf")
# supports tor via
download("onion://cool.onion/here.pdf", "here.pdf", proto="https")
```

## Todos

- Support ftp/sftp
- Support torrent
- Support non-default ports for tor/socks4/socks5 server

## License

This project is licensed under the GPL-3 license.
