# -*- coding: utf-8 -*-
import asyncio
import logging
import os
import posixpath
from typing import List, Tuple, Union
import mimetypes

use_pygments = False
try:
  from pygments import highlight
  from pygments.lexers import get_lexer_for_mimetype, get_lexer_by_name, get_lexer_for_filename
  from pygments.formatters import HtmlFormatter
  use_pygments = True
except:
  pass

req_log = logging.getLogger('request')
req_log.setLevel(logging.INFO)

dir_template = '''<html>
<head>
<title>目录 {dir_name}</title>
</head>
<body>
<h2>{nav}</h2>
<hr>
{content}
</body>
</html>'''

highlight_template = '''<html>
<head>
<title>文件: {file_name}</title>
<link rel="stylesheet"
      href="//cdn.jsdelivr.net/gh/highlightjs/cdn-release@10.2.1/build/styles/default.min.css">
<script src="//cdn.jsdelivr.net/gh/highlightjs/cdn-release@10.2.1/build/highlight.min.js"></script>
<script>hljs.initHighlightingOnLoad();</script>
</head>
<body>
<h2>{nav}</h2>
<hr>
<pre>
<code class="{lang}">{content}</code>
</pre>
</body>
</html>'''

pygments_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
      {style}
    </style>
</head>
<body>
  <h2>{nav}</h2>
  <hr>
  {content}
</body>
</html>'''

def is_text(type: Union[str]) -> Union[bool]:
  return type.startswith('text/')

class BasicHttpResponse(object):
  protocol: Union[str] = 'HTTP'
  protocol_version: Union[str] = '1.1'
  status_code: Union[int] = 200
  headers: List[Tuple[str, str]] = [
    ('Server', 'asyncio-server')
  ]
  
  body: Union[str] = ''
  
  template = '''{}/{} {} OK
{}


{}'''
  
  def __str__(self):
    headers = "\r\n".join(map(lambda h: h[0] + ':' + h[1], self.headers))
    return self.template.format(self.protocol, self.protocol_version, self.status_code, headers, self.body)
  

class HttpServerProtocol(asyncio.Protocol):
  base_dir: Union[str]
  extensions_map = _encodings_map_default = {
    '.gz': 'application/gzip',
    '.Z': 'application/octet-stream',
    '.bz2': 'application/x-bzip2',
    '.xz': 'application/x-xz',
    '.yml': 'text/x-yaml',
    '.cfg': 'text/x-ini',
  }
  file_map = _encodings_map_default
  def __init__(self, base_dir):
    super(HttpServerProtocol).__init__()
    self.base_dir = base_dir
  def connection_made(self, transport):
    peername = transport.get_extra_info('peername')
    req_log.debug('Connection from %s', peername)
    self.transport = transport

  def data_received(self, data):
    req_log.debug('http request body: %s', data)
    do_method, req_path, _, _ = self.parse_request(data.decode('utf-8'))
    method = getattr(self, 'do_' + do_method)
    body_html = ''
    if method is not None:
      body_html = method(req_path)
    else:
      r = BasicHttpResponse()
      r.body = '<h1>404</h1>'
      body_html = r
    self.transport.write(str(body_html).encode('utf-8'))

    req_log.debug('Close the client socket')
    self.transport.close()
    
  def do_GET(self, req_path: Union[str]) -> Union[BasicHttpResponse]:
    req_path = req_path[1:] if req_path.startswith('/') else req_path
    path = os.path.join(self.base_dir, req_path)
    r = BasicHttpResponse()
    if not os.path.exists(path):
      r.status_code = 404
      r.body = '<h1>404</h1>'
      return r
    ctype = self.guess_type(path)
    if os.path.isfile(path):
      has_lexer = True
      lexer = None
      try:
        lexer = get_lexer_for_mimetype(ctype)
        if lexer is None:
          has_lexer = False
      except:
        has_lexer = False
      if use_pygments and has_lexer:
        r.headers.append(('Content-Type', 'text/html; charset=utf-8'))
        r.body = self.do_text_file_by_pygments(path, req_path, lexer)
      elif is_text(ctype):
        r.headers.append(('Content-Type', 'text/html; charset=utf-8'))
        r.body = self.do_text_file(path, req_path)
      else:
        r.headers.append(('Content-Type', 'application/octet-stream'))
    else:
      r.headers.append(('Content-Type', 'text/html; charset=utf-8'))
      r.body = self.do_dir(path, req_path)
    return r
  
  def do_POST(self, req_path: Union[str]):
    pass
  
  def parse_request(self, data: Union[str]):
    method, path, _ = data.split('\r\n')[0].split(' ')
    req_log.info('%s %s', method, path)
    query_string, hash_string = None, None
    if '?' in path:
      path, query_string = path.split('?') 
      query_string = query_string.strip()
      query_string = query_string if len(query_string) > 0 else None
    
    qs_map = {}
    if query_string and '#' in query_string:
      query_string, hash_string = query_string.split('#')
      qs_map = dict(map(lambda it: it.split('='), query_string.split('&')))
      
    return method, path, qs_map, hash_string
 
  def guess_type(self, path):
        """Guess the type of a file.

        Argument is a PATH (a filename).

        Return value is a string of the form type/subtype,
        usable for a MIME Content-type header.

        The default implementation looks the file's extension
        up in the table self.extensions_map, using application/octet-stream
        as a default; however it would be permissible (if
        slow) to look inside the data to make a better guess.

        """
        _, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
          return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
          return self.extensions_map[ext]
        guess, _ = mimetypes.guess_type(path)
        if guess:
            return guess
        return 'application/octet-stream'
  
  def do_text_file(self, file_path, req_path):
    with open(file_path, 'r', encoding='utf-8') as f:
      content = f.read()
    ext = file_path.split('.')[-1]
    return highlight_template.format(file_name=file_path, nav=file_path, lang=ext, content=content)
  
  def do_text_file_by_pygments(self, file_path, req_path, lexer) -> Union[str]:
    formatter = HtmlFormatter(style='colorful')
    style = formatter.get_style_defs()
    with open(file_path, 'r', encoding='utf-8') as f:
      content = f.read()
    return pygments_template.format(
      title=file_path,
      nav=file_path,
      style=style,
      content=highlight(content, lexer, formatter)
    )
    
  
  def do_dir(self, dir_path, req_path):
    dir_html = self.list_dir(dir_path, req_path)
    
    return dir_template.format(dir_name=dir_path, nav=dir_path, content=dir_html)
  
  def nav(self, dir: Union[str]) -> Union[str, None]:
    pass
  
  def list_dir(self, dir_path: Union[str], req_path: Union[str]) -> Union[str]:
    return '<ul>' + "".join(map(lambda d: '<li><a href="'+os.path.join('/', req_path, d)+'">' + d + '</a></li>', os.listdir(dir_path))) + '</ul>'


async def main(bind: Union[str], port: Union[int], verbose: Union[bool], base_dir: Union[str]):
  loop = asyncio.get_running_loop()
  server = await loop.create_server(lambda: HttpServerProtocol(base_dir), bind, port)
  
  try:
    req_log.info('starting HTTP server: http://%s:%s', bind, port)
    await server.serve_forever()
  except:
    server.close()
    await server.wait_closed()
    
    
if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser('简易HTTP服务')
  parser.add_argument('-b', '--bind', type=str, default='127.0.0.1', help='host地址(default: 127.0.0.1)')
  parser.add_argument('-p', '--port', type=int, default=8888, help='端口号(default: 8888)')
  parser.add_argument('-d', '--directory', type=str, default=os.getcwd(), help='当前目录(default: %s)' % os.getcwd())
  parser.add_argument('--debug', default=False, action='store_true', help='debug日志')
  parser.add_argument('--verbose', action='store_true', default=False, help='打印详细日志')
  
  args = parser.parse_args()
  logging.basicConfig(level={True: logging.DEBUG, False: logging.INFO}[args.verbose | args.debug])
  try:
    asyncio.run(main(args.bind, args.port, args.verbose, args.directory))
  except:
    req_log.info('ctrl+c close server')