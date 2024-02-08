from flask import Flask,render_template,request
import requests
import json
from bs4 import BeautifulSoup

def get_links(url):
    headers={
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    data={
        "recaptchaToken": "",
        "q": url,
        "t": "media",
        "lang": "en"
    }
    response = requests.post(url="https://v3.igdownloader.app/api/ajaxSearch",data=data,headers=headers)
    res = json.loads(response.content)
    try:
        soup = BeautifulSoup(res['data'],'html5lib')
    except:
        return [0]
    op=[1]
    download_link=[]
    unwanted_links=["https://play.google.com/store/apps/details?id=saveinsta.download.video.instagram.photo.reels.story","/"]
    for link in soup.find_all('a'):
        url = link.get('href')
        if url not in unwanted_links:
            download_link.append(url)
        
    preview_link=[]
    for link in soup.find_all('img'):
        tlink = link.get('src')
        if tlink=='/imgs/loader.gif':
            tlink = link.get('data-src')
        preview_link.append(tlink)
    op.append(download_link)
    op.append(preview_link)
    return op
    
app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def main():
    if request.method=="POST":
        link=request.form['url']
        data=get_links(link)
        if(data[0]):
            return render_template('home.html',op=data[0],download_links=data[1],preview_links=data[2],length=len(data[1]))
        else:
            return render_template('home.html',info="Not Available")
    else:
        return render_template('home.html')
    
if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')