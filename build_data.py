import json,re
def load(p):
    d=json.load(open('raw/'+p))
    return json.loads(d) if isinstance(d,str) else d
out=[];seen=set()
def add(b,n,kg,cup,url,date):
    n=re.sub(r'\s+',' ',n).strip()
    k=(b,n.lower(),kg,cup)
    if k in seen or not kg or not (2500<=kg<=5200) or not (150<=cup<=600): return
    seen.add(k); out.append(dict(brand=b,name=n,kcal_kg=kg,kcal_cup=cup,url=url,checked=date))
d=load('dogfood-hills.json')
for r in d['records']:
    slug=r['url'].rstrip('/').split('/')[-1]
    line='Prescription Diet' if slug.startswith(('prescription','pd-')) else 'Science Diet'
    n=r['product_name']
    n=re.sub(r'\s*Dry Dog Food$|\s*Dog Food$','',n)
    if r['kcal_per_cup'] is None: continue
    add("Hill's",f'{line} {n}',r['kcal_per_kg'],r['kcal_per_cup'],r['url'],d['checked'])
d=load('dogfood-royalcanin.json')
for r in d['records']:
    line='Veterinary Diet' if '/vet-products/' in r['url'] else ''
    n=re.sub(r'\s*Dry Dog Food$','',r['product_name']).replace('®','').replace('™','')
    if re.search(r'loaf|canned|stew|pate|wet|pouch',n,re.I): continue
    n=n.title() if n.isupper() else n
    add('Royal Canin',(line+' '+n).strip(),r['kcal_per_kg'],r['kcal_per_cup'],r['url'],d['checked'])
d=load('dogfood-diamond.json')
for r in d['records']:
    if 'quiz' in r['url']: continue
    parts=r['url'].rstrip('/').split('/')
    line=parts[-2].replace('-',' ').title().replace('Pro89','Pro89'); sl=parts[-1].replace('-',' ').title()
    add('Diamond',f'{line}: {sl}',r['kcal_per_kg'],r['kcal_per_cup'],r['url'],d['checked'])
d=load('dogfood-bluebuffalo.json')
for r in d['records']:
    parts=r['url'].rstrip('/').split('/')
    add('Blue Buffalo','BLUE '+parts[-2].replace('-',' ').title()+': '+parts[-1].replace('-',' ').title(),r['kcal_per_kg'],r['kcal_per_cup'],r['url'],d['checked'])
d=load('dogfood-fromm.json')
for r in (d if isinstance(d,list) else d.get('records',d)):
    if r.get('kcal_per_cup') and r.get('kcal_per_kg'):
        add('Fromm',r['product_name'],r['kcal_per_kg'],r['kcal_per_cup'],r['url'],r['checked'])
d=load('dogfood-canidae.json')
for r in d['records']:
    n=re.sub(r'\s*[-\u2013]\s*Canidae$','',r['product_name']).replace('Canidae ','').strip()
    if 'Grass-Fed Beef' in n: continue  # 414 kcal/cup is inconsistent with its kcal/kg; likely a typo on the page
    add('Canidae',n,r['kcal_per_kg'],r['kcal_per_cup'],r['url'],d['checked'])
d=load('dogfood-merrick.json')
import html
for r in d['records']:
    if '/canada/' in r['url']: continue
    add('Merrick',html.unescape(r['product_name']),r['kcal_per_kg'],r['kcal_per_cup'],r['url'],d['checked'])
d=load('dogfood-acana.json')
for r in d['records']:
    n=re.sub(r'\s+Dry Dog Food.*$','',r['product_name']).replace('Dog Food for Healthy Dogs','').strip()
    add('Acana',n,r['kcal_per_kg'],r['kcal_per_cup'],r['url'],d['checked'])
d=load('dogfood-totw.json')
for r in d['records']:
    add('Taste of the Wild',r['product_name'].replace(' Canine Recipe',''),r['kcal_per_kg'],r['kcal_per_cup'],r['url'],d['checked'])
out.sort(key=lambda r:(r['brand'],r['name']))
json.dump(out,open('foods.json','w'),separators=(',',':'),ensure_ascii=False)
from collections import Counter;print(len(out),Counter(r['brand'] for r in out))
