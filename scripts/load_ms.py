#!/usr/bin/env python3
import requests, json, argparse, meilisearch, os, hashlib
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('--file', required=True)
parser.add_argument('--start', required=True, help="Year-Month to read from file", metavar="1834-01")
parser.add_argument('--end', required=True, help="Year-Month to stop at", metavar="1834-02")
args = parser.parse_args()

output = 'completed-ms.txt'

# open data file
with open(args.file) as f: 
    data = json.load(f)

def get_entry(url):
    '''Get entry text from url'''

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    if 'tumblr' in url:
        try:
            txt = soup.find("div", class_="body-text").get_text()
            return txt
        except:
            u = url
        
            if 'tumblr' in u:
                try:
                    txt = soup.find("article", class_="text").get_text()
                    return txt
                except:
                    u2 = u
                
                    if 'tumblr' in u2:
                        try:
                            txt = soup.find("div", class_="template-post-content-body").get_text() 
                            return txt
                        except:
                            u3 = u2
                            
                        if 'tumblr' in u3:
                            try:
                                txt = soup.find("div", class_="text").get_text()
                                return txt
                            except:
                                u4 = u3
                                     
                            if 'tumblr' in u4:
                                try:
                                    txt = soup.find("div", class_="caption_content").get_text()
                                    return txt
                                except:                                
                                    print(f'ERROR_URL: {url}')



    if 'blogspot' in url:
        try:
            txt = soup.find("div", class_="post-body").get_text()
            return txt
        except:
            print(f'ERROR_URL: {url}')
        

def wyas_extract(data):
    '''Extract WYAS list data from file'''

    dt = dict()
    id_date = data['id']
    wyas = data['wyasLink'][0]
    dt['date'] = id_date.replace(',','-')
    dt['wyas_link'] = wyas['link']
    dt['type'] = wyas['type']
    return dt

def tr_extract(data):
    '''Extract TR list data from file'''

    dt = dict()
    dt['link'] = data['link'][0]
    dt['credit'] = data['credit']
    dt['type'] = data['type']
    return dt


   
def extract_fmt_push(c, index):
    
    for d in data:
        w = wyas_extract(d)
        date = w.get('date')
    
        if args.start in date:

            for x in d['Tr']:
                if x['link']:
                    t = tr_extract(x)
                    
                    # skipping these sources as the formatting is difficult to work with
                    if t.get('credit') == 'ISAW':
                        break
                    elif "insearchofannwalker.com" in t.get('link'):
                        break
                    elif "drive.google.com" in t.get('link'):
                        break
                    elif "annelisternorway.com" in t.get('link'):
                        break
                    elif "xldev.co.uk" in t.get('link'):
                        break
                    elif "tolerablygoodtranscriptions" in t.get('link'):
                        break

                    body = get_entry(t.get('link'))
                    entry = body.replace('\n', ' ').replace('\t', '').replace('\r', '').encode("ascii", "ignore").decode()
                    date = w.get('date')
                    wlink = w.get('wyas_link')
                    credit = t.get('credit')
                    type = t.get('type')
                    tlink = t.get('link')
                    hash = hashlib.md5(tlink.encode())
                    id = hash.hexdigest()
                    year = date[0:4]
                    doc = [{
                        'id': id, 
                        'date': date, 
                        'WYAS': wlink, 
                        'credit': credit, 
                        'type': type, 
                        'entry': entry,
                        'transcript': tlink,
                        'year': year
                    }]
                    
                    print(f"PUSH FOR {date} BY {credit}" )
                    c.index(index).update_documents(doc)
                    
    
        elif args.end in date:
            with open(output, 'a') as o:
                o.write(f'\nStopping at {date}')
            break


def main():
    sl = os.environ["URL"]
    key = os.environ["MASTER_KEY"]
    client = meilisearch.Client(sl, key)
    
    print(f'Starting {args.start}')
    extract_fmt_push(client, 'lister')

if __name__ == "__main__":
    main()