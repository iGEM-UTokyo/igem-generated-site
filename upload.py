import sys
import os
import igem_wikisync.wikisync as wikisync

print('preparing browser')
# Browser system only uses the config below.
config = {
  'team': 'UTokyo',
  'year': '2021',
}

credentials = {
  'username': os.environ.get('IGEM_USERNAME'),
  'password': os.environ.get('IGEM_PASSWORD')
}

browser, _ = wikisync.get_browser_with_cookies()
login = wikisync.iGEM_login(browser, credentials, config)
if not login:
  print('Failed to login.')

for line in sys.stdin:
  path = line[:-1] # 最後は\nがくる。
  url = ''
  if path == 'Team-UTokyo(index)':
    url = 'Team:UTokyo'
  elif path.startswith('Team-UTokyo/'):
    start = len('Team-UTokyo/')
    url = 'Team:UTokyo/' + path[start:]
  elif path.startswith('Template-UTokyo/'):
    start = len('Template-UTokyo/')
    url = 'Template:UTokyo/' + path[start:]
  else:
    print('ignore file: ' + path)
    continue
  content = ''
  with open(path, encoding='utf-8') as f:
    content = f.read()
  url = 'https://2021.igem.org/wiki/index.php?title=' + url + '&action=edit'
  print('uploading ' + url)
  wikisync.iGEM_upload_page(browser, content, url)


