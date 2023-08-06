import os
import shutil
from typing import Any
from urllib.parse import urlparse, ParseResult

import requests
from plumbum import local
from torpy.http.requests import TorRequests


def mv(url: str, path: str, replace=False, recursive=True, **kwargs):
    if os.path.exists(path) and not replace:
        return False
    shutil.move(url, path)
    return True


def https(url: str, path: str, replace=False, recursive=True, **kwargs: str):
    if os.path.exists(path) and not replace:
        return False

    qs = urlparse(url)
    res = requests.get(url, stream=True)
    with open(path, "wb") as f:
        for chunk in res.iter_content(chunk_size=kwargs.get("chunk_size", 1024)):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


http = https


def ssh(url: str, path: str, replace=False, recursive=True, **kwargs: str):
    if os.path.exists(path) and not replace:
        return False

    qs = urlparse(url)

    # the url[6:] is to skip the ssh://
    scp = local["scp"]
    result = scp(url[6:], path).run()
    retcode = result[0]
    return retcode == 0


def ftp(url: str, path: str, replace: bool = False, recursive=True, **kwargs: str):
    raise NotImplementedError


def sftp(url: str, path: str, replace: bool = False, recursive=True, **kwargs: str):
    raise NotImplementedError


def torrent(url: str, path: str, replace: bool = False, recursive=True, **kwargs: str):
    raise NotImplementedError


def tor(
    url: str,
    path: str,
    replace: bool = False,
    recursive: bool = True,
    proto: str = "https",
    chunk_size: int = 1024,
    **kwargs: str,
):
    qs = urlparse(url)
    scheme, netloc, _path, params, query, fragment = proto, *qs[1:]
    fixed_url = ParseResult(scheme, netloc, _path, params, query, fragment).geturl()

    with TorRequests() as tor_requests:
        with tor_requests.get_session() as sess:

            res = sess.get(fixed_url, stream=True)
            with open(path, "wb") as f:
                for chunk in res.iter_content(
                    chunk_size=kwargs.get("chunk_size", chunk_size)
                ):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)


HANDLED_SUFFIXES = {
    "file": mv,
    "http": http,
    "https": https,
    "ssh": ssh,
    "ftp": ftp,
    "sftp": sftp,
    "torrent": torrent,
    "onion": tor,
    "tor": tor,
}


def _pick_downloader(url: str):
    qs = urlparse(url)
    scheme = qs.scheme
    return HANDLED_SUFFIXES.get(scheme)


def download(url: str, path: str, replace=False, recursive=True, **kwargs: Any):
    handler = _pick_downloader(url)
    if not handler:
        supported = "\n".join(HANDLED_SUFFIXES.keys())
        raise ValueError(
            f"protocol of {url} is not supported. The ones that are:\n{supported}"
        )

    return handler(url, path, replace, **kwargs)


def read(path: str, binary: bool = False):
    with open(path, mode="r" if not binary else "rb") as file:
        return file.read()
