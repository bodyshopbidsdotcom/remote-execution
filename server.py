import http.server
import socketserver
import json
import os
import sys
import datetime

PORT = 8000
ROOT_DIR = os.path.dirname(__file__)
PAYLOADS_DIRNAME = 'payloads'

class Handler(http.server.SimpleHTTPRequestHandler):
  def do_POST(self):
    length = int(self.headers['content-length'])
    body_dict = json.loads(self.rfile.read(length))

    payload_filepath = create_payload_file()
    with open(payload_filepath, 'w') as outfile:
      json.dump(body_dict, outfile, indent=2)

    # https://stackoverflow.com/a/73652631
    response = os.path.relpath(payload_filepath, start=ROOT_DIR)
    self.send_response(200)
    self.end_headers() # Not including this causes `Received HTTP/0.9 when not allowed` warning.
    self.wfile.write(response.encode(encoding='utf_8'))

def create_payload_file() -> str:
  basename = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')
  return os.path.join(create_payloads_directory_if_necessary(), f'{basename}.json')

def create_payloads_directory_if_necessary() -> str:
  payloads_dirpath = os.path.join(ROOT_DIR, PAYLOADS_DIRNAME)
  print(payloads_dirpath)
  os.makedirs(payloads_dirpath, exist_ok=True)
  return payloads_dirpath

def run() -> int:
  socketserver.TCPServer.allow_reuse_address = True
  with socketserver.TCPServer(('0.0.0.0', PORT), Handler) as httpd:
      print(f'Serving http://0.0.0.0:{PORT}')
      try:
        httpd.serve_forever()
      except KeyboardInterrupt:
        # Should be gracefully handled by the `with` block but for some reason it's not.
        print('Shutting down')
        httpd.shutdown()

  return 0

if __name__ == "__main__":
  sys.exit(run())
