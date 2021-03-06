from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests, json, cloudscraper

app = Flask(__name__)


@app.route('/')
def get_root():
    print('sending root')
    return render_template('index.html')


@app.route('/api/docs')
def get_docs():
    print('sending docs')
    return render_template('swaggerui.html')


@app.route('/lk21', methods=['GET'])
def lk21():
    if request.args.get('q'):
        query = request.args.get('q')
        return {
            'success': False,
            'msg': 'Soonn..',
            'info': 'Join telegram channel @YasirPediaChannel for updates.',
        }
    else:
        return {
            'success': False,
            'msg': 'Isi parameter query gaes',
            'info': 'Join telegram channel @YasirPediaChannel for updates.',
        }


@app.route('/youtube', methods=['GET'])
def youtube():
    if request.args.get('url'):
        url = request.args.get('url')
        try:
            html = requests.get(url)
            soup = BeautifulSoup(html.text, 'html.parser')
            body = soup.find_all("body")[0]
            scripts = body.find_all("script")
            result = json.loads(scripts[0].string[30:-1])
            return {
                'info':
                'Join telegram channel @YasirPediaChannel for updates.',
                'result': result['streamingData']['adaptiveFormats']
            }
        except Exception as e:
            print(e)
    else:
        return {
            'success': False,
            'msg': 'Isi parameter query gaes',
            'info': 'Join telegram channel @YasirPediaChannel for updates.',
        }

@app.route('/subscene-search', methods=['GET'])
def sub_search():
    if request.args.get('q'):
        query = request.args.get('q')
        scraper = cloudscraper.create_scraper()
        param = {'query':query}
        r  = scraper.post("https://subscene.com/subtitles/searchbytitle", data=param).text
        soup2 = BeautifulSoup(r,"html.parser")
        list = soup2.find("div", {"class": "search-result"})
        a = list.find_all("div", {"class":"title"})
        
        data = []
        for i in a:
            title = i.find_all('a')[0].text
            url = f"https://subscene.com{i.find_all('a')[0].get('href')}"
            data.append({
                'title': title,
                'url': url,
            })
        return {
            'status':200,
            'info':
            'Join telegram channel @YasirPediaChannel for updates.',
            'result': data
        }
    else:
        return {
            'success': False,
            'msg': 'Isi parameter query gaes',
            'info': 'Join telegram channel @YasirPediaChannel for updates.',
        }

@app.route('/google', methods=['GET'])
def google():
    if request.args.get('q'):
        query = request.args.get('q')
        try:
            headers = {
                'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/61.0.3163.100 Safari/537.36'
            }
            html = requests.get(f'https://www.google.com/search?q={query}',
                                headers=headers)
            soup = BeautifulSoup(html.text, 'html.parser')

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
            return {
                'info':
                'Join telegram channel @YasirPediaChannel for updates.',
                'result': data
            }
        except Exception as e:
            print(e)
    else:
        return {
            'success': False,
            'msg': 'Isi parameter query gaes',
            'info': 'Join telegram channel @YasirPediaChannel for updates.',
        }


@app.route('/textpro', methods=['GET'])
def textpro():
    try:
        if request.args.get('q'):
            sesi = requests.Session()
            neh = request.args.get('q')
            url = request.args.get('url')
            new = {
                'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip',
                'DNT': '1',  # Do Not Track Request Header 
                'Connection': 'close'
            }
            rr = sesi.get(url, headers=new)
            htmlbytes = rr.text
            soup = BeautifulSoup(htmlbytes, 'html.parser')
            token = soup.find('input', {'name': 'token'})['value']
            putprm = (
                ('text[]', (None, neh)),
                ('submit', (None, 'Go')),
                ('token', (None, token)),
                ('build_server', (None, 'https://textpro.me')),
                ('build_id', (None, '1')),
            )
            gazbang = sesi.post(url, files=putprm, headers=new)
            soupp = BeautifulSoup(gazbang.text, 'html.parser')
            getdata = soupp.find("div", {"class": "sr-only"}).text
            jonson = json.loads(getdata)
            id = jonson['id']
            token = jonson['token']
            buildserver = jonson['build_server']
            buildid = jonson['build_id']
            dats = {
                "id": id,
                "text[]": neh,
                "token": token,
                "build_server": buildserver,
                "build_id": buildid
            }
            gaslagi = sesi.post('https://textpro.me/effect/create-image',
                                data=dats,
                                headers=new)
            dcode = json.loads(gaslagi.text)
            return {
                'success': True,
                'msg': 'Successfully',
                'link': 'https://textpro.me' + dcode['image']
            }
        else:
            return {
                'success': False,
                'msg': 'Isi parameter url sama query dulu',
                'info':
                'Join telegram channel @YasirPediaChannel for updates.',
            }
    except:
        print('eror')


@app.route('/result')
def result():
    dict = {'phy': 50, 'che': 60, 'maths': 70}
    return render_template('result.html', result=dict)
