# -*- coding: utf8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor,tshost,T
import base64,urllib,re,time,os,requests,hashlib,subprocess,threading
from PIL import Image
from io import BytesIO

def getinfo():
    info_={}
    name='Lodynet'
    hst = 'https://lodynet.watch'
    info_['old_host'] = hst
    hst_ = tshost(name)
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='3.0 26/06/2025'
    info_['dev']='RGYSoft + Angel_heart'
    info_['cat_id']='21'
    info_['desc']='افلام و مسلسلات وبرامج وحفلات وكرتون وأغاني وممثلين'
    info_['icon']='https://www.lodynet.co/wp-content/uploads/2015/12/logo-1.png'
    info_['recherche_all']='0'
    return info_
class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{})
        self.MAIN_URL = getinfo()['host']
    def showmenu(self,cItem):
        TAB = [('مسلسلات','','10',0),('أفلام','','10',1),('برامج و حفلات','/category/البرامج-و-حفلات-tv/','20',''),('أغاني','','10',2),('الممثلين','/الممثلين/','20','')]
        self.add_menu(cItem,'','','','','',TAB=TAB,search=False)
        self.addDir({'import':cItem['import'],'category' :'host2','title':T('Search')  ,'icon':'https://i.ibb.co/dQg0hSG/search.png','mode':'50'})
    def showmenu1(self,cItem):
        gnr = cItem.get('sub_mode','')
        if gnr == 0 : 
            TAB = [
                ('مسلسلات هندية','/category/مسلسلات-هنديه/','20',''),
                ('مسلسلات هندية مدبلجة','/category/1dubbed-indian-series/','20',''),
                ('مسلسلات ويب هندية','/category/مسلسل-ويب-هندية/','20',''),
                ('مسلسلات هندية 2020','/year/مسلسلات-هندية-2020-a/','20',''),
                ('مسلسلات هندية 2019','/year/مسلسلات-هندية-2019/','20',''),
                ('مسلسلات هندية 2018','/year/مسلسلات-هندية-2018/','20',''),
                ('مسلسلات تركية','/category/مشاهدة-مسلسلات-تركية/','20',''),
                ('مسلسلات تركية مدبلجة','/category/مشاهدة-مسلسلات-تركية-مدبلجة/','20',''),
                ('مسلسلات كورية','/category/مشاهدة-مسلسلات-كورية/','20',''),
                ('مسلسلات صينية مترجمة','/category/مسلسلات-صينية-مترجمة/','20',''),
                ('مسلسلات تايلاندية','/مشاهدة-مسلسلات-تايلندية/','20',''),
                ('مسلسلات مكسيكية','/category/مسلسلات-مكسيكية-a/','20','')
            ]
        elif gnr == 1:
            TAB = [
                ('افلام هندية', '/category/افلام-هندية/', '20', ''),
                ('أفلام هندية مدبلجة', '/category/أفلام-هندية-مدبلجة/', '20', ''),
                ('افلام هندية جنوبية', '/tag/الافلام-الهندية-الجنوبية/', '20', ''),
                ('أفلام هندي 2024', '/year/أفلام-هندي-2024/', '20', ''),
                ('أفلام هندي 2023', '/year/أفلام-هندية-2023/', '20', ''),
                ('أفلام هندي 2021', '/year/movies-hindi-2021/', '20', ''),
                ('أفلام هندي 2020', '/year/افلام-هندي-2020-a/', '20', ''),
                ('افلام هندي 2019', '/year/افلام-هندي-2019/', '20', ''),
                ('افلام هندي 2018', '/year/افلام-هندي-2018/', '20', ''),
                ('افلام هندي 2017', '/year/افلام-هندي-2017/', '20', ''),
                ('افلام هندي 2016', '/year/2016/', '20', ''),
                ('افلام هندية 4K', '/tag/افلام-هندية-مترجمة-بجودة-4k/', '20', ''),
                ('اعمال شاروخان', '/actor/شاه-روخ-خان-a/', '20', ''),
                ('أعمال سلمان خان', '/actor/سلمان-خان-a/', '20', ''),
                ('أعمال عامر خان', '/actor/عامر-خان-a/', '20', ''),
                ('أعمال شاهد كابور', '/actor/شاهيد-كابور/', '20', ''),
                ('أعمال رانبير كابور', '/actor/رانبير-كابور/', '20', ''),
                ('أعمال ديبيكا بادكون', '/actor/ديبيكا-بادكون/', '20', ''),
                ('أعمال هريتيك روشان', '/actor/هريتيك-روشان/', '20', ''),
                ('أعمال اكشاي كومار', '/actor/اكشاي-كومار/', '20', ''),
                ('أعمال تابسي بانو', '/actor/تابسي-بانو/', '20', ''),
                ('أعمال سانجاي دوت', '/actor/سانجاي-دوت-a/', '20', ''),
                ('ترجمات احمد بشير', '/tag/جميع-الأفلام-في-هذا-القسم-من-ترجمة-أحمد/', '20', ''),
                ('افلام تركية مترجم', '/category/افلام-تركية-مترجم/', '20', ''),
                ('افلام باكستانية', '/tag/افلام-باكستانية-مترجمة/', '20', ''),
                ('افلام اسيوية', '/category/افلام-اسيوية-a/', '20', ''),
                ('افلام اجنبي', '/category/افلام-اجنبية-مترجمة-a/', '20', ''),
                ('انيمي', '/category/انيمي/', '20', '')
            ]
        elif gnr == 2:
            TAB = [
                ('أغاني المسلسلات', '/category/اغاني/اغاني-المسلسلات-الهندية/','20',''),
                ('أغاني الأفلام','/category/اغاني-الافلام/','20','')
            ]
        self.add_menu(cItem,'','','','','',TAB=TAB)
    def showsearch(self,cItem):
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'البحث في الموقع','icon':'https://i.ibb.co/2nztSQz/all.png','mode':'51','section':''})
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'البحث عن فيلم','icon':'https://i.ibb.co/k56BbCm/aflam.png','mode':'51','section':'فيلم'})
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'البحث عن مسلسل','icon':'https://i.ibb.co/3M38qkV/mousalsalat.png','mode':'51','section':'مسلسل'})
    def SearchAll(self,str_ch,page=1,extra='',type_=''):
        return self.get_items({'page':page,'import':extra,'str_ch':str_ch,'type_':type_})
    def SearchMovies(self,str_ch,page=1,extra=''):
        elms = self.SearchAll(str_ch,page,extra=extra,type_='فيلم')
        return elms
    def SearchSeries(self,str_ch,page=1,extra=''):
        elms = self.SearchAll(str_ch,page,extra=extra,type_='مسلسل')
        return elms
    def get_items(self,cItem={}):
        elms    = []
        extra   = cItem.get('import')
        str_ch   = cItem.get('str_ch')
        page    = cItem.get('page', 1)
        url_    = cItem.get('url', '')
        type_   = cItem.get('type_', '')
        if url_ == '':
            with_type = True
            if type_ == 'مسلسل': url0 = self.MAIN_URL + '/search/' + str_ch
            elif type_ != '': url0 = self.MAIN_URL + '/search/' + str_ch + '+' + type_
            else: url0 = self.MAIN_URL + '/search/' + str_ch
            if page > 1: url0 = url0 + '/page/' + str(page)
        else:
            with_type = False
            url0 = url_.strip('/')
            if not url0.startswith('http'):
                if url0.startswith(('tag/', 'year/', 'actor/', 'category/', 'مشاهدة-')): url0 = self.MAIN_URL + '/' + url0
                else: url0 = self.MAIN_URL + '/category/' + url0
            if page > 1: url0 = url0 + '/page/' + str(page)
        sts, data = self.getPage(url0)
        if sts:
            lst_data=re.findall(r'class="LodyBlock.*?href="([^"]+)".*?<img[^>]+(?:data-src|src)="([^"]+)".*?<h2>([^<]+)</h2>(.*?)</li>', data, re.S)
            for (url,image,titre,desc) in lst_data:
                desc  = self.extract_desc(desc,[('info','Ribbon">(.*?)</div>'),('time','<time>(.*?)</time>')])
                info  = self.std_title(titre,desc=desc,with_type=with_type)
                desc  = info.get('desc')
                titre = info.get('title_display')
                image = self.fix_image_url(self.std_url(image))
                elms.append({'import':cItem['import'],'category' : 'host2','title':titre,'url':url,'desc':desc,'icon':image,'mode':'21','good_for_fav':True,'sub_mode':'1','EPG':True,'hst':'tshost','info':info})
        films_list = re.findall('(<a class="next|>الصفحة التالية</a>)', data, re.S)
        if films_list:
            if '/search/' in url0: mode = '51'
            else: mode = '20'
            elms.append({'import':extra,'category' : 'host2','title':T('Next'),'url':url_,'desc':'Next','icon':'','hst':'tshost','mode':mode,'page':page+1,'str_ch':str_ch,'type_':type_})
        return elms
    def fix_image_url(self, url):
        DEFAULT_IMAGE = 'https://lodynet.watch/wp-content/uploads/2015/12/logo-1.png'
        cache_folder = '/etc/IPTVCache/webp/'
        if not os.path.exists(cache_folder): os.makedirs(cache_folder)
        file_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
        jpg_path = os.path.join(cache_folder, file_hash + '.jpg')
        webp_path = os.path.join(cache_folder, file_hash + '.webp')
        if os.path.exists(jpg_path): return 'file://' + jpg_path
        def download_and_convert():
            try:
                r = requests.get(url, timeout=5, verify=False)
                if r.status_code == 200:
                    header = r.content[:10]
                    content = r.content
                    # JPEG
                    if header.startswith(b'\xff\xd8'):
                        with open(jpg_path, 'wb') as f: f.write(content)
                    # PNG
                    elif header.startswith(b'\x89PNG\r\n\x1a\n'):
                        with open(jpg_path, 'wb') as f: f.write(content)
                    # WebP
                    elif header.startswith(b'RIFF') and b'WEBP' in content[:20]:
                        with open(webp_path, 'wb') as f: f.write(content)
                        try:
                            subprocess.call(['ffmpeg', '-y', '-i', webp_path, jpg_path])
                            os.remove(webp_path)
                        except Exception as e: print("[lodynet] خطأ أثناء تحويل WebP:", e)
                    else:
                        if os.path.exists(jpg_path): os.remove(jpg_path)
            except Exception as e: print("[lodynet] خطأ تحميل صورة:", e)
        threading.Thread(target=download_and_convert).start()
        return 'file://' + jpg_path if os.path.exists(jpg_path) else DEFAULT_IMAGE
    def showitms(self, cItem):
        url = cItem.get('url', '')
        if not url.startswith('http'):
            url = self.MAIN_URL + '/' + url.lstrip('/')
        sts, data = self.getPage(url)
        if not sts:
            return
        actors = re.findall(r'<li[^>]*class="ActorItem"[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*>.*?(?:<img[^>]*src="([^"]+)")?.*?<div[^>]*class="ActorName"[^>]*>(.*?)<', data, re.S)
        if actors:
            actors_sorted = sorted(actors, key=lambda x: x[2])
            for link, img, name in actors_sorted:
                icon = self.fix_image_url(img) if img else 'https://www.lodynet.co/wp-content/uploads/2015/12/logo-1.png'
                self.addDir({'import': cItem.get('import'),'category': 'host2','title': name.strip(),'url': link,'icon': icon,'mode': '21','hst': 'tshost'})
            return
        if '/actor/' in url and 'ActorAvatar' in data:
            m = re.search(r'<div class="ActorAvatar">.*?<img[^>]+src="([^"]+)"', data, re.S)
            if m:
                actor_icon = self.fix_image_url(self.std_url(m.group(1)))
                cItem['icon'] = actor_icon
        matches = re.findall(r'class="LodyBlock.*?href="([^"]+)".*?<img[^>]+(?:data-src|src)="([^"]*)".*?<h2>([^<]+)</h2>(.*?)</li>', data, re.S)
        for url_, img, title, rest in matches:
            icon = self.fix_image_url(self.std_url(img)) if img and img.strip() else cItem.get('icon', '')
            desc = self.extract_desc(rest, [('Info', r'Ribbon">(.*?)</div>'), ('Time', r'<time>(.*?)</time>')])
            is_film = '/category/' not in url_ and '/actor/' not in url_
            item = {'import': cItem.get('import'),'title': title.strip(),'url': url_,'desc': desc,'icon': icon,'good_for_fav': True,'hst': 'tshost','mode': '21'}
            if is_film:
                self.addVideo(item)
            else:
                item['category'] = 'host2'
                self.addDir(item)
        next_match = re.search(r'class="next page-numbers".*?href="([^"]+)"', data)
        if next_match:
            self.addDir({'import': cItem.get('import'),'category': 'host2','title': 'Next','url': next_match.group(1),'desc': 'Next','icon': cItem.get('icon', ''),'hst': 'tshost','mode': '21'})
    def show_actor_movies(self, cItem):
        url = cItem.get('url', '')
        if not url.startswith('http'):
            url = self.MAIN_URL + '/' + url.lstrip('/')
        sts, data = self.getPage(url)
        if not sts:
            return
        matches = re.findall(r'class="LodyBlock.*?href="([^"]+)".*?<img[^>]+(?:data-src|src)="([^"]+)"[^>]*alt="([^"]+)".*?</a>', data, re.S)
        for url_, img, title in matches:
            icon = self.fix_image_url(self.std_url(img))
            self.addVideo({'import': cItem.get('import'),'title': title.strip(),'url': url_,'desc': '','icon': icon,'good_for_fav': True,'hst': 'tshost'})
        next_match = re.search(r'class="next page-numbers".*?href="([^"]+)"', data)
        if next_match:
            self.addDir({'import': cItem.get('import'),'category': 'host2','title': 'Next','url': next_match.group(1),'desc': 'Next','icon': '','hst': 'tshost','mode': '21'})
    def showelms(self, cItem):
        url = cItem.get('url', '')
        if not url.startswith('http'):
            url = self.MAIN_URL + '/' + url.lstrip('/')
        sts, data = self.getPage(url)
        if not sts:
            return
        matches = re.findall(r'class="LodyBlock.*?href="([^"]+)".*?<img[^>]+(?:data-src|src)="([^"]+)".*?<h2>([^<]+)</h2>(.*?)</li>', data, re.S)
        if matches:
            for url, img, title, rest in matches:
                icon = self.fix_image_url(self.std_url(img))
                desc = self.extract_desc(rest,[('Episode',r'NumberLayer">(.*?)</div>'),('Time',r'<time>(.*?)</time>')])
                self.addVideo({'import': cItem.get('import'),'title': title.strip(),'url': url,'desc': desc,'icon': icon,'good_for_fav': True,'hst': 'tshost'})
        else:
            self.addVideo({'import': cItem.get('import'),'title': cItem.get('title'),'url': url,'icon': cItem.get('icon'),'good_for_fav': True,'hst': 'tshost'})
        next_match = re.search(r'class="next page-numbers".*?href="([^"]+)"', data)
        if next_match:
            self.addDir({'import': cItem.get('import'),'category': 'host2','title': 'Next','url': next_match.group(1),'desc': 'Next','icon': '','hst': 'tshost','mode': '21'})
    def SearchResult(self,str_ch,page,extra):
        url = self.MAIN_URL+'/search/'+str_ch+'/page/'+str(page)
        desc = [('Info','Ribbon">(.*?)</div>','',''),('Time','<time>(.*?)</time>','','')]
        self.add_menu({'import':extra,'url':url},'','class="LodyBlock.*?href="(.*?)".*?>(.*?)<img.*?src="(.*?)".*?<h2>(.*?)</h2>(.*?)</li>','','21',ord=[0,3,2,1,4],Desc=desc,u_titre=True)
    def getArticle(self,cItem):
        Desc = [('Date','PublishDate">(.*?)</div>','',''),('Story','BoxContentInner">(.*?)</div>','\n','')]
        desc = self.add_menu(cItem,'','DetailsBox">(.*?)<ul','','desc',Desc=Desc)
        if desc =='': desc = cItem.get('desc','')
        return [{'title':cItem['title'], 'text': desc, 'images':[{'title':'', 'url':cItem.get('icon','')}], 'other_info':{}}]
    def get_links(self,cItem):
        local = [('vidlo.us','LoDyTo','0'),]
        result = self.add_menu(cItem,'ServersList">(.*?)</ul','<li.*?data-embed="(.*?)".*?>(.*?)</li>','','serv',local=local)
        return result[1]