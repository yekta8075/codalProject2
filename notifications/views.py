from django.shortcuts import render
import pandas as pd
import requests
import json
from django.http import HttpResponse
from .models import notification, attachment
import os
from datetime import datetime
from bs4 import BeautifulSoup


def get_notification(request):
    try:
        req = requests.Session()
        url = '''https://search.codal.ir/api/search/v2/q?&Audited=true&AuditorRef=-1&Category=-1&Childs=
                 true&CompanyState=-1&CompanyType=-1&Consolidatable=true&IsNotAudited=false&Length=-1&LetterType=
                 -1&Mains=true&NotAudited=true&NotConsolidatable=true&PageNumber=1&Publisher=false&TracingNo=
                 -1&search=true'''

        response = req.get(url, headers={'Accept': 'application/json; charset=utf-8', 'User-Agent': 'foo'})

    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    else:
        data = json.loads(response.content)
        l = data["Letters"]
        df = pd.DataFrame(l)
        df1 = df.loc[:, df.columns != 'SuperVision']
        df2 = df["SuperVision"].apply(pd.Series)
        result = pd.concat([df1, df2], axis=1, join='inner')

        for e in result.T.to_dict().values():
            if e['PdfUrl']:
                url1 = 'https://www.codal.ir/' + e['PdfUrl']
                filename = url1.split('?')[1]
                path = download_file(url1, 'pdf', filename)
                e['PdfUrl'] = path
            if e['ExcelUrl']:
                url1 = e['ExcelUrl']
                filename = url1.split('/')[6]
                path = download_file(url1, 'xls', filename)
                e['ExcelUrl'] = path
            if e['Url']:
                url1 = 'https://www.codal.ir/' + e['Url']
                filename = url1.split('=')[1]
                path = download_file(url1, 'html', filename)
                e['Url'] = path
            n = notification.objects.update_or_create(**e)

            if e['AttachmentUrl']:
                url1 = 'https://www.codal.ir/' + e['AttachmentUrl']
                url2, file_type = get_attachment_link(url1)

                for u in url2:
                    filename = u.split('=')[1]
                    path = download_file(u, file_type[url2.index(u)], filename)
                    attachment.objects.update_or_create(
                        AttachmentPath=path,
                        note=n[0]
                    )

        return HttpResponse("records saved successfully")


def get_attachment_link(url):
    try:
        req = requests.Session()
        r = req.get(url, headers={'Accept': 'application.json ;charset=utf-8', 'User-Agent': 'foo'})

    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    else:
        soup = BeautifulSoup(r.content, 'html.parser')
        linkList = []
        typelist = []

        for a in soup.find_all("tr", {"class": "GridItem"}):
            onclick = a.attrs['onclick']
            left = onclick.find("'")
            right = onclick.find("'", left + 1)
            link = onclick[left + 1:right]
            url = 'https://www.codal.ir/Reports/' + link
            linkList.append(url)

        for i in soup.findAll('img'):
            src = i['src'].split('/')[-1]
            typelist.append(src.split('.')[0])

        return linkList, typelist


def download_file(url1, type, filename):
    today = datetime.now().strftime('%Y%m%d')
    save_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\files\\' + today + '\\'
    isExist = os.path.exists(save_path)
    if not isExist:
        os.makedirs(save_path)
    completeName = os.path.join(save_path, filename + '.' + type)
    try:
        req = requests.Session()
        response = req.get(url1, headers={'Accept': 'application/json; charset=utf-8', 'User-Agent': 'foo'})

    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    else:
        with open(completeName, 'wb') as r:
            r.write(response.content)
        return completeName
