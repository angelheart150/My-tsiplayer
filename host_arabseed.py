# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.libs import ph
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,gethostname,tscolor,tshost
import urllib
import re
from Components.config import config
try:
    from html import unescape  # Python 3.4+
except ImportError:
    from HTMLParser import HTMLParser  # Python 2.x
    unescape = HTMLParser().unescape
    
def getinfo():
    info_={}
    name = 'Arabseed'
    hst = 'https://a.asd.homes'
    info_['old_host'] = hst
    hst_ = tshost(name)	
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='3.0 12/07/2025'    
    info_['dev']='RGYSoft+Angel_heart'
    info_['cat_id']='21'
    info_['desc']='أفلام و مسلسلات عربية و اجنبية'
    info_['icon']='https://i.ibb.co/7S7tWYb/arabseed.png'
    info_['recherche_all']='1'
    return info_
class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':'arabseed.cookie'})
        self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
        self.MAIN_URL = getinfo()['host']
        self.SiteName   = 'Arabseed'
        self.HEADER = {'User-Agent': self.USER_AGENT, 'Connection': 'keep-alive', 'Accept-Encoding':'gzip', 'Content-Type':'application/x-www-form-urlencoded','Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
        self.defaultParams = {'header':self.HEADER, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
        #self.getPage = self.cm.getPage
        self.cacheLinks = {}
        self.seen_series_titles = set()
    def showmenu(self,cItem):
        hst='host2'
        self.Arablionz_TAB = [
                            {'category':hst, 'sub_mode':0, 'title': 'الأفـــلام', 'mode':'10'},
                            {'category':hst, 'sub_mode':1, 'title': 'مســلـســلات', 'mode':'10'},
                            {'category':hst, 'sub_mode':2, 'title': 'مســلـســلات رمـضـان', 'mode':'10'},
                            {'category':hst, 'sub_mode':3, 'title': 'نيتفليكس - Netfilx', 'mode':'10'},                            
                            {'category':hst, 'sub_mode':4, 'title': 'المــصـارعــة','url':self.MAIN_URL+'/category/wwe-shows/', 'mode':'20'},
                            {'category':hst, 'title': tscolor('\c0000????') + 'حسب التصنيف' , 'mode':'19','count':1,'data':'none','code':''},	
                            {'category':'search','title':tscolor('\c00????30') + _('Search'), 'search_item':True,'page':1,'hst':'tshost'},
                            ]		
        self.listsTab(self.Arablionz_TAB, {'import':cItem.get('import',''),'icon':cItem.get('icon','')})
    def showmenu1(self,cItem):
        hst='host2'
        gnr=cItem['sub_mode']
        sts, data = self.getPage(self.MAIN_URL+'/main/')
        if sts:
            cat_film_data=re.findall('<ul class="sub-menu">(.*?)</ul>', data, re.S) 
            if cat_film_data:
                data2=re.findall('<li.*?href="(.*?)".*?>(.*?)<', cat_film_data[gnr], re.S)
                for (url,titre) in data2:
                    if not url.startswith('http'): url=self.MAIN_URL+url
                    item = {'import': cItem.get('import',''),'category': 'host2','url': url,'title': titre,'desc': '','icon': cItem.get('icon',''),'mode': '20','sub_mode': gnr,}
                    if gnr in [0, 3]:
                        item['direct_video'] = True
                    self.addDir(item)
    def showfilter(self, cItem):
        count = cItem['count']
        data1 = cItem['data']	
        codeold = cItem['code']	
        if count == 1:
            sts, data = self.getPage(self.MAIN_URL + '/category/foreign-movies/')
            if sts:
                data1 = re.findall('TaxPageFilterItem.*?<ul>(.*?)</ul', data, re.S)
            else:
                data1 = None
        mode_ = '20' if count == 5 else '19'
        headers = ['إختر أحد الأقسام','إختر أحد الانواع','إختر الجودة','إختر سنة الاصدار','إختر اللغة','إختر الدولة']
        if data1:
                lst_data1 = re.findall('<li.*?data-tax="(.*?)".*?data-term="(.*?)">(.*?)</li>', data1[count - 1], re.S)
                for (x1, x2, x3) in lst_data1:
                    if not ((x1 == 'category') and (x2.strip() == '')):
                        code = codeold + x1 + '=' + x2.strip() + '&'
                    else:
                        code = codeold
                    title = ph.clean_html(x3)
                    if x2.strip() == '':
                        title += '  (كل التصنيفات)'
                    desc = tscolor('\c00FFFF00') + '▣❖ ' + headers[count - 1] + ' ❖▣'
                    self.addDir({'import': cItem.get('import', ''),'category': 'host2','url': code,'title': title,'desc': desc,'icon': cItem.get('icon', ''),'mode': mode_,'count': count + 1,'data': data1,'code': code,'sub_mode': 'item_filter','page': -1})
    def showitms(self, cItem):
        seen_titles = set()
        fetch_all = cItem.get('fetch_all', False)
        url = cItem['url']
        collected_items = []
        next_url = None
        sub_mode = cItem.get('sub_mode', -1)
        direct_video = bool(cItem.get('direct_video', False) or sub_mode in [0, 3, 4])
        while True:
            sts, data = self.getPage(url)
            if not sts:
                break
            matches = re.findall(r'class="MovieBlock.*?href="(.*?)".*?(?:image=|data-src=)"(.*?)".*?<h4>(.*?)</h4>', data, re.S)
            for url1, image, title in matches:
                title = unescape(title)
                clean_title = re.sub(r'الحلقة\s+\d+.*', '', title).strip()
                if clean_title in seen_titles:
                    continue
                seen_titles.add(clean_title)
                item_data = {'import': cItem.get('import', ''),'category': 'host2','title': clean_title,'url': url1,'desc': '','icon': image,'EPG': True,'hst': 'tshost','sub_mode': sub_mode,'direct_video': direct_video}
                if direct_video:
                    item_data['mode'] = '22'
                    self.addVideo(item_data)
                else:
                    item_data['mode'] = '21'
                    collected_items.append(item_data)
            if not fetch_all:
                match = re.findall(r'class="next page-numbers"\s*href="(.*?)"', data)
                if match:
                    next_url = match[0]
                    if not next_url.startswith('http'):
                        next_url = self.MAIN_URL + next_url
                break
            match = re.findall(r'class="next page-numbers"\s*href="(.*?)"', data)
            if match:
                next_url = match[0]
                if not next_url.startswith('http'):
                    next_url = self.MAIN_URL + next_url
                url = next_url
            else:
                break
        if collected_items:
            for item in sorted(collected_items, key=lambda x: x['title'].lower()):
                self.addDir(item)
        if not fetch_all:
            self.addDir({'import': cItem.get('import', ''),'category': 'host2','title': tscolor('\c0000??66') + '◀ عرض الكل فى قائمة واحدة ▶','url': cItem['url'],'desc': tscolor('\c0000??66') + 'يجمع كل محتويات القسم بدون تكرار ومرتب أبجديا .. لكنه يأخذ وقت أطول للتحميل فكن صبورا.','icon': cItem.get('icon', ''),'mode': '20','fetch_all': True,'sub_mode': sub_mode,'direct_video': direct_video})
            if next_url:
                self.addDir({'import': cItem.get('import', ''),'category': 'host2','title': tscolor('\c00FFFF00') + '<< الصفحة التالية','url': next_url,'desc': '','icon': cItem.get('icon', ''),'mode': '20','page': cItem.get('page', 1) + 1,'sub_mode': sub_mode,'direct_video': direct_video})
    def showelms(self, cItem):
        sts, data = self.getPage(cItem['url'])
        if not sts:
            return
        episodes_section = re.findall(r'class="ContainerEpisodesList(.*?)</div>', data, re.S)
        if episodes_section:
            episodes = []
            raw_episodes = re.findall(r'href="(.*?)".*?>(.*?)</a>', episodes_section[0], re.S)
            for url, title in raw_episodes:
                clean_title = ph.clean_html(title)
                match = re.search(r'الحلقة\s+(\d+)', clean_title)
                ep_num = int(match.group(1)) if match else 0
                episodes.append({'url': url, 'title': clean_title, 'num': ep_num})
            episodes.sort(key=lambda x: x['num'])
            for ep in episodes:
                self.addVideo({'import': cItem.get('import', ''),'title': ep['title'],'url': ep['url'],'icon': cItem.get('icon', ''),'desc': '','EPG': True,'hst': 'tshost'})
        else:
            self.addVideo({'import': cItem.get('import', ''),'title': cItem['title'],'url': cItem['url'],'icon': cItem.get('icon', ''),'desc': '','EPG': True,'hst': 'tshost'})
    def SearchResult(self,str_ch,page,extra):
        elms = []
        url = self.MAIN_URL+'/find/?find='+str_ch+'&offset='+str(page)
        desc = [('Info','Ribbon">(.*?)</div>','',''),('Story','Story">(.*?)</div>','','')]
        data = self.add_menu({'import':extra,'url':url},'','class="MovieBlock.*?href="(.*?)".*?(?:image=|img src=)"(.*?)"(.*?)<h4>(.*?)</h4>(.*?)</a>','','21',ind_0 = -1,ord=[0,3,1,2,4],Desc=desc,u_titre=True,year_op=1,EPG=True)		
        return data[2]
    def MediaBoxResult1(self,str_ch,year_,extra):
        urltab=[]
        str_ch_o = str_ch
        str_ch = urllib.quote(str_ch_o+' '+year_)	
        url_=self.MAIN_URL+'/?s='+str_ch+'&page='+str(1)
        sts, data = self.getPage(url_)
        if sts:		
            data1=re.findall('class="BlockItem.*?href="(.*?)".*?src="(.*?)".*?Title">(.*?)<(.*?)</div>', data, re.S)		
            i=0
            for (url,image,titre,desc) in data1:
                desc=ph.clean_html(desc)
                titre=ph.clean_html(titre)
                desc0,titre = self.uniform_titre(titre,year_op=1)
                if desc.strip()!='':
                    desc = tscolor('\c00????00')+'Desc: '+tscolor('\c00??????')+desc
                desc=desc0+desc	
                titre0='|'+tscolor('\c0060??60')+'ArabSeeD'+tscolor('\c00??????')+'| '+titre				
                urltab.append({'titre':titre,'import':extra,'good_for_fav':True,'EPG':True,'category' : 'host2','url': url,'title':titre0,'desc':desc,'icon':image,'mode':'31','hst':'tshost'})			
        return urltab
    def get_links(self, cItem): 	
        urlTab = []	
        if config.plugins.iptvplayer.ts_dsn.value:
            urlTab = self.cacheLinks.get(str(cItem['url']), [])		
        if urlTab == []:		
            url = cItem['url']
            sts, data = self.getPage(url)
            if sts:
                server_data = re.findall('WatchButtons">.*?<a href="(.*?)"', data, re.S)
                if server_data:
                    URL = server_data[0]
                    addParams = dict(self.defaultParams)
                    addParams['header']['Referer'] = self.MAIN_URL
                    sts, data = self.getPage(URL, addParams)
                    if sts:
                        quality_order = ['1080', '720', '480']
                        blocks = re.split(r'<h3>مشاهدة (\d+)</h3>', data)
                        quality_map = {}
                        for i in range(1, len(blocks), 2):
                            quality = blocks[i]
                            block_data = blocks[i+1]
                            matches = re.findall(r'data-link="([^"]+)"[^>]*>.*?<span>([^<]+)</span>', block_data, re.S)
                            for url_, server_name in matches:
                                domain = re.findall(r'https?://([^/]+)/', url_)
                                domain_str = ''
                                if domain:
                                    domain_str = domain[0].split('.')[0]
                                if 'عرب سيد' in server_name:
                                    server_label = 'Server [ Arabseed ]'
                                else:
                                    server_name = server_name.replace('سيرفر', 'Server').strip()
                                    server_label = '{} ( {} )'.format(server_name, domain_str)
                                label = '[{}] {}'.format(quality, server_label)
                                if quality not in quality_map:
                                    quality_map[quality] = []
                                quality_map[quality].append({'name': label, 'url': url_, 'need_resolve': 1})
                        for q in quality_order:
                            urlTab.extend(quality_map.get(q, []))
            if config.plugins.iptvplayer.ts_dsn.value:
                self.cacheLinks[str(cItem['url'])] = urlTab
        return urlTab
    def getVideos(self,videoUrl):
        urlTab = []	
        code1,code2,qu=videoUrl.split('|')
        url=self.MAIN_URL+'/wp-content/themes/ArbSeed/Server.php'
        url=self.MAIN_URL+'/wp-content/themes/Elshaikh2021/Ajaxat/Single/Server.php'
        post_data = {'post_id':code2,'server':code1,'qu':qu}
        sts, data = self.getPage(url,post_data=post_data)
        if sts:
            print(data)
            Liste_els = re.findall('src.*?["\'](.*?)["\']', data, re.S|re.IGNORECASE)
            if Liste_els:
                URL_ = Liste_els[0]
                if URL_.startswith('//'): URL_ = 'http:'+URL_
                urlTab.append((URL_,'1'))
        return urlTab	
    def getArticle(self, cItem):
        otherInfo1 = {}
        desc = cItem['desc']
        sts, data = self.getPage(cItem['url'])
        if sts:
            lst_dat=re.findall('class="HoldINfo(.*?)class="topBar', data, re.S)
            if lst_dat:
                lst_dat0=re.findall("<li>(.*?):(.*?)</li>", lst_dat[0], re.S)
                for (x1,x2) in lst_dat0:
                    if 'الجودة'     in x1: otherInfo1['quality'] = ph.clean_html(x2)
                    if 'تاريخ'      in x1: otherInfo1['year'] = ph.clean_html(x2)				
                    if 'اللغة'      in x1: otherInfo1['language'] = ph.clean_html(x2)	
                    if 'النوع'      in x1: otherInfo1['genres'] = ph.clean_html(x2)				
                    if 'الدولة'      in x1: otherInfo1['country'] = ph.clean_html(x2)	
                    if 'السنه'      in x1: otherInfo1['year'] = ph.clean_html(x2)	                         
            lst_dat=re.findall('StoryLine">(.*?)</div>', data, re.S)
            if lst_dat: desc = ph.clean_html(lst_dat[0])
        icon = cItem.get('icon')
        title = cItem['title']	
        return [{'title':title, 'text': desc, 'images':[{'title':'', 'url':icon}], 'other_info':otherInfo1}]
