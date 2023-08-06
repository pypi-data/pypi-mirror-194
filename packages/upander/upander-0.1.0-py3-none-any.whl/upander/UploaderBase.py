from typing import Optional

class Uploader:
  def __init__(self):
    pass

class UploaderPosterResponse:
  def dl_url(self) -> str       : raise NotImplementedError("未実装エラー")
  def dl_file_name(self) -> str : raise NotImplementedError("未実装エラー")
  def status(self) -> int       : raise NotImplementedError("未実装エラー")
  def url(self) -> str          : raise NotImplementedError("未実装エラー")
  def encoding(self) -> str     : raise NotImplementedError("未実装エラー")
  def headers(self) -> str      : raise NotImplementedError("未実装エラー")
  def text(self) -> str         : raise NotImplementedError("未実装エラー")
  def content(self) -> bytes    : raise NotImplementedError("未実装エラー")
  def cookies(self) -> str      : raise NotImplementedError("未実装エラー")

class UploaderPoster:
  def run(self) -> UploaderPosterResponse: raise NotImplementedError("未実装エラー")

class UploaderDownloaderResponse:
  def dl_file_name(self) -> str: raise NotImplementedError("未実装エラー")
  def status(self) -> int      : raise NotImplementedError("未実装エラー")
  def url(self) -> str         : raise NotImplementedError("未実装エラー")
  def encoding(self) -> str    : raise NotImplementedError("未実装エラー")
  def headers(self) -> str     : raise NotImplementedError("未実装エラー")
  def content(self) -> bytes   : raise NotImplementedError("未実装エラー")
  def cookies(self) -> dict    : raise NotImplementedError("未実装エラー")

class UploaderDownloader:
  def download(self) -> Optional[UploaderDownloaderResponse] : raise NotImplementedError("未実装エラー")
  def check_url(self, url) -> bool                                : raise NotImplementedError("未実装エラー")