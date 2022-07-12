from flask import Flask, render_template
from bs4 import BeautifulSoup
from flask import request
import requests

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, gaess'


@app.route('/test')
def test():
    return 'Test'

@app.route('/google/', methods=['GET'])
def google():
  if request.args.get('q'):
      try:
        headers = {   
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '   
         'Chrome/61.0.3163.100 Safari/537.36'   
        }
        html = requests.get(f'https://www.google.com/search?q={q}')
        soup = BeautifulSoup(html.text, 'lxml')

        # collect data
        data = []

        for result in soup.select('.tF2Cxc'):
           title = result.select_one('.DKV0Md').text
           link = result.select_one('.yuRUbf a')['href']
           try:
             snippet = result.select_one('#rso .lyLwlc').text
           except:
             snippet = "-"

           # appending data to an array
           data.append({
             'title': title,
             'link': link,
             'snippet': snippet,
           })
        return data
      except Exception as e:
        {
        'success' : False, 
        'msg' : e
       } 
  else:
      return {
        'success' : False, 
        'msg' : 'Isi parameter,'
      } 

@app.route('/textpro/', methods=['GET'])
def textpro():
  try:
    if request.args.get('q'):
      sesi = requests.Session()
      neh = request.args.get('q')
      url = request.args.get('url')
      new = {
        'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
        'Accept-Language' : 'en-US,en;q=0.5',
        'Accept-Encoding' : 'gzip', 
        'DNT' : '1', # Do Not Track Request Header 
        'Connection' : 'close' 
      }
      rr = sesi.get(url, headers=new) 
      htmlbytes = rr.text
      soup = bs4(htmlbytes, 'html.parser')
      token = soup.find('input', {'name':'token'})['value']
      putprm = (
        ('text[]', (None, neh)), 
        ('submit', (None, 'Go')), 
        ('token', (None, token)), 
        ('build_server', (None, 'https://textpro.me')), 
        ('build_id', (None, '1')),
        )
      gazbang = sesi.post(url, files=putprm, headers=new)
      soupp = bs4(gazbang.text, 'html.parser')
      getdata = soupp.find("div", {"class": "sr-only"}).text
      jonson = json.loads(getdata)
      id = jonson['id']
      token = jonson['token']
      buildserver = jonson['build_server']
      buildid = jonson['build_id']
      dats = {"id" : id, "text[]" : neh, "token" : token, "build_server" : buildserver, "build_id" : buildid}
      gaslagi = sesi.post('https://textpro.me/effect/create-image', data=dats, headers=new)
      dcode = json.loads(gaslagi.text)
      return {
        'success' : True, 
        'msg' : 'Successfully', 
        'link' : 'https://textpro.me'+dcode['image']
      } 
    else:
      return {
        'success' : False, 
        'msg' : 'Isi parameter,'
      } 
  except:
	  print('eror')

@app.route('/result')
def result():
   dict = {'phy':50,'che':60,'maths':70}
   return render_template('result.html', result = dict)
