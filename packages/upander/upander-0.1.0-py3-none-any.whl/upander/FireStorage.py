from upander import Uploader
from upander import UploaderPoster
from upander import UploaderPosterResponse

from requests.models import Response
from html.parser import HTMLParser
from typing import IO , Optional, Union
import urllib.parse
import requests
import datetime
import sys
import io
import random
import re

class FireStorage(Uploader):
  UPLOAD_FILE_SIZE_LIMIT = 2 * 1024 * 1024 * 1024
  def __init__(self):
    pass
  class Poster(UploaderPoster):
    FOLDER_IDS = ['f7e3285547f333e3be0d854a096c91d38be0b492b4028346b8884e4']
    SERVER_IDS = [41, 127]

    def __init__(
        self
        , file: Union[IO, str]
        , folder_id: str = None
        , server_id: int = None
        , ppass=''
        , dpass=''
        , thumbnail="normal"
        , top =  '1'
        , jqueryupload_1 =  '1'
        , max_size =  '2147483648'
        , max_sized =  '2'
        , max_size_photo_1 =  '15728640'
        , max_size_photod =  '15'
        , max_size_photo_2 =  '150'
        , max_count =  '20'
        , max_count_photo =  '150'
        , jqueryupload_2 =  '1'
        , eid =  ''
        , qst =  ''
        , comments =  ''
        , comment =  ''
        , arc =  ''
        , zips =  ''
        , file_queue =  '1'
        , pc =  '1'
        , exp =  '1'
      ):
      self._file = file
      self._folder_id = random.choice(FireStorage.Poster.FOLDER_IDS) if folder_id is None else folder_id
      self._server_id = random.choice(FireStorage.Poster.SERVER_IDS) if server_id is None else server_id
      self._ppass = ppass
      self._dpass = dpass
      self._thumbnail = thumbnail
      self._top = top
      self._jqueryupload_1 = jqueryupload_1
      self._max_size = max_size
      self._max_sized = max_sized
      self._max_size_photo_1 = max_size_photo_1
      self._max_size_photod = max_size_photod
      self._max_size_photo_2 = max_size_photo_2
      self._max_count = max_count
      self._max_count_photo = max_count_photo
      self._jqueryupload_2 = jqueryupload_2
      self._eid = eid
      self._qst = qst
      self._comments = comments
      self._comment = comment
      self._arc = arc
      self._zips = zips
      self._file_queue = file_queue
      self._pc = pc
      self._exp = exp

    def run(self) -> UploaderPosterResponse:
      url = 'https://server{0}.firestorage.jp/upload.cgi'.format(self._server_id)

      _file = self._file if type(self._file) is io.BufferedReader else open(self._file, "rb")
      pid = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+datetime.datetime.now().strftime("%f").ljust(7,"0")

      files = [
          ('folder_id', (None, self._folder_id)),
          ('ppass', (None, self._ppass)),
          ('dpass', (None, self._dpass)),
          ('thumbnail', (None, self._thumbnail)),
          ('top', (None, self._top)),
          ('jqueryupload', (None, self._jqueryupload_1)),
          ('max_size', (None, self._max_size)),
          ('max_sized', (None, self._max_sized)),
          ('max_size_photo', (None, self._max_size_photo_1)),
          ('max_size_photod', (None, self._max_size_photod)),
          ('max_size_photo', (None, self._max_size_photo_2)),
          ('max_count', (None, self._max_count)),
          ('max_count_photo', (None, self._max_count_photo)),
          ('jqueryupload', (None, self._jqueryupload_2)),
          ('eid', (None, self._eid)),
          ('processid', (None, pid)),
          ('qst', (None, self._qst)),
          ('comments', (None, self._comments)),
          ('comment', (None, self._comment)),
          ('arc', (None, self._arc)),
          ('zips', (None, self._zips)),
          ('file_queue', (None, self._file_queue)),
          ('pc', (None, self._pc)),
          ('exp', (None, self._exp)),
          ('Filename', _file),
      ]
      response = FireStorage.Poster.Response(requests.post(url, files=files))
      if type(self._file) is str: _file.close()
      return response

    class Response(UploaderPosterResponse):
      def __init__(self, response: Response):
        super().__init__()
        parser = FireStorage.Poster.Response.HtmlParser()
        parser.feed(urllib.parse.unquote(response.text))
        self._status = response.status_code
        self._url = response.url
        self._encoding = response.encoding
        self._headers = response.headers
        self._text = response.text
        self._content = response.content
        self._cookies = response.cookies
        self._dl_file_name = parser.dl_file_name
        self._dl_link = parser.dl_link
        self._dl_link_short = parser.dl_link_short
        if not(self._dl_file_name and self._dl_link and self._dl_link_short):
            raise Exception("Exception: \nFireStorage Post Response \n" + response.text)
      def dl_url(self) -> str:
        return self._dl_link
      def dl_file_name(self) -> str:
        return self._dl_file_name
      def dl_url_short(self) -> str:
        return self._dl_link_short
      def status(self) -> int:
        return self._status
      def url(self) -> str:
        return self._url
      def encoding(self) -> str:
        return self._encoding
      def headers(self) -> str:
        return self._headers
      def text(self) -> str:
        return self._text
      def content(self) -> bytes:
        return self._content
      def cookies(self) -> str:
        return self._cookies

      class HtmlParser(HTMLParser):
        def __init__(self):
          super().__init__()
          self.dl_link = None
          self.dl_link_short = None
          self.dl_file_name = None
          self.dl_file_name_flg = False

        def handle_starttag(self, tag, attrs):
          attrs_dict = {}
          for attr in attrs: attrs_dict[attr[0]] = attr[1]

          if tag == "form":
            if attrs_dict.get("name", None) == "embedForm":
              self.dl_file_name_flg = True
          if tag == "a":
            if attrs_dict.get("id", None) == "downloadlink":
              if not(self.dl_link):
                self.dl_link = attrs_dict["href"]
              else:
                self.dl_link_short = attrs_dict["href"]

        def handle_endtag(self, tag):
          pass
        def handle_data(self, data):
          if self.dl_file_name_flg :
            self.dl_file_name = re.match("\[ (.+) \].+", data.strip()).groups()[0]
            self.dl_file_name_flg = False