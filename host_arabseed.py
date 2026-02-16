# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.libs import ph
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,gethostname,tscolor,tshost
import re,json,base64,urllib,urllib.parse
from Components.config import config
from urllib.parse import quote
try:
    from html import unescape  # Python 3.4+
except ImportError:
    from HTMLParser import HTMLParser  # Python 2.x
    unescape = HTMLParser().unescape
############################################################################## 20260216
def getinfo():
    info_={}
    name = 'Arabseed'
    hst = 'https://asd.pics/'
    info_['old_host'] = hst
    hst_ = tshost(name)	
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='5.0 08/02/2026'    
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
        self.cacheLinks = {}
        self.seen_series_titles = set()
    def showmenu(self,cItem):
        hst='host2'
        self.Arabseed_TAB = [
                            {'category':hst, 'sub_mode':0, 'title': 'الأفـــلام', 'mode':'10'},
                            {'category':hst, 'sub_mode':1, 'title': 'مســلـســلات', 'mode':'10'},
                            {'category':hst, 'sub_mode':2, 'title': 'مواسم المسلسلات - البرامج - الأنمي', 'mode':'10'},
                            {'category':hst, 'sub_mode':3, 'title': 'رمـضـان', 'mode':'10'},
                            {'category':hst, 'sub_mode':4, 'title': 'انـمـي', 'mode':'10'},                            
                            {'category':hst, 'sub_mode':5, 'title': 'متنوع','mode':'10'},
                            {'category':'search','title':tscolor('\c00????30') + _('Search'), 'search_item':True,'page':1,'hst':'tshost'},
                            ]		
        self.listsTab(self.Arabseed_TAB, {'import':cItem.get('import',''),'icon':cItem.get('icon','')})
    def showmenu1(self, cItem):
        hst = 'host2'
        gnr = cItem['sub_mode']
        categories = {
            0: [
                ('/category/arabic-movies-6/','أفلام عربية'),
                ('/category/foreign-movies-6/','أفلام أجنبية'),
                ('/category/turkish-movies/','أفلام تركية'),
                ('/category/indian-movies/','أفلام هندية'),
                ('/category/netfilx/افلام-netfilx/','Netfilx أفلام'),
                ('/category/asian-movies/','أفلام اسيوية'),
                ('/category/افلام-كلاسيكيه/','افلام كلاسيكيه'),
                ('/category/افلام-مدبلجة/','افلام مدبلجة'),
            ],
            1: [
                ('/category/arabic-series-3/','مسلسلات عربية'),
                ('/category/مسلسلات-مصريه/','مسلسلات مصريه'),
                ('/category/foreign-series-3/','مسلسلات أجنبية'),
                ('/category/turkish-series-/','مسلسلات تركية'), 
                ('/category/مسلسلات-هندية/','مسلسلات هندية'), 
                ('/category/netfilx/مسلسلات-netfilz/','مسلسلات Netfilx'),
                ('/category/cartoon-series/','مسلسلات كرتون'),
                ('/category/مسلسلات-كوريه/','مسلسلات كوريه'),
                ('/category/مسلسلات-مدبلجة/','مسلسلات مدبلجة')
            ],
            2: [
                ('/category/arabic-series-8/packs/','مواسم مسلسلات عربية'),
                ('/category/مسلسلات-مصريه/packs/','مواسم مسلسلات مصرية'),
                ('/category/foreign-series-3/packs/','مواسم مسلسلات اجنبية'),
                ('/category/turkish-series-2/packs/','مواسم مسلسلات تركية'), 
                ('/category/مسلسلات-هندية/packs/','مواسم مسلسلات هندية'), 
                ('/category/netfilx/مسلسلات-netfilx-1/packs/','مواسم مسلسلات Netfilx'),
                ('/category/مسلسلات-كوريه/packs/','مواسم مسلسلات كورية'),
                ('/category/مسلسلات-مدبلجة/packs/','مواسم مسلسلات مدبلجة'),
                ('/category/مسلسلات-رمضان/ramadan-series-2026/packs/','مواسم مسلسلات رمضان 2026'),
                ('/category/مسلسلات-رمضان/ramadan-series-2025/packs/','مواسم مسلسلات رمضان 2025'),
                ('/category/مسلسلات-رمضان/ramadan-series-2024/packs/','مواسم مسلسلات رمضان 2024'),
                ('/category/مسلسلات-رمضان/ramadan-series-2023/packs/','مواسم مسلسلات رمضان 2023'),
                ('/category/مسلسلات-رمضان/مسلسلات-رمضان-2022/packs/','مواسم مسلسلات رمضان 2022'),
                ('/category/مسلسلات-رمضان/مسلسلات-رمضان-2021/packs/','مواسم مسلسلات رمضان 2021'),
                ('/category/مسلسلات-رمضان/مسلسلات-رمضان-2020-hd/packs/','مواسم مسلسلات رمضان 2020'),
                ('/category/مسلسلات-رمضان/مسلسلات-رمضان-2019/packs/','مواسم مسلسلات رمضان 2019'),
                ('/category/برامج-تلفزيونية/packs/','مواسم برامج تليفزيونية'),
                ('/category/cartoon-series/packs/','مواسم مسلسلات كرتون'),
            ],
            3: [
                ('/category/مسلسلات-رمضان/ramadan-series-2026/','مسلسلات رمضان 2026'),
                ('/category/مسلسلات-رمضان/ramadan-series-2025/','مسلسلات رمضان 2025'),
                ('/category/مسلسلات-رمضان/ramadan-series-2024/','مسلسلات رمضان 2024'),
                ('/category/مسلسلات-رمضان/ramadan-series-2023/','مسلسلات رمضان 2023'),
                ('/category/مسلسلات-رمضان/مسلسلات-رمضان-2022/','مسلسلات رمضان 2022'),
                ('/category/مسلسلات-رمضان/مسلسلات-رمضان-2021/','مسلسلات رمضان 2021'),
                ('/category/مسلسلات-رمضان/مسلسلات-رمضان-2020-hd/','مسلسلات رمضان 2020'),
                ('/category/مسلسلات-رمضان/مسلسلات-رمضان-2019/','مسلسلات رمضان 2019'),
            ],
            4: [
                ('/category/افلام-انيميشن/','افلام انيميشن'),
                ('/category/cartoon-series/','مسلسلات كرتون')
            ],
            5: [ 
                ('/category/اغاني-عربي/','اغاني عربي'),
                ('/category/wwe-shows/','مصارعه'),
                ('/category/برامج-تلفزيونية/','برامج تلفزيونية'),
                ('/category/مسرحيات-عربي/','مسرحيات عربيه'),
            ]
        }
        cat_list = categories.get(gnr, [])
        for url, title in cat_list:
            full_url = self.MAIN_URL + url
            item = {'import': cItem.get('import', ''),'category': 'host2','url': full_url,'title': title,'desc': '','good_for_fav':True,'icon': cItem.get('icon', ''),'mode': '20','sub_mode': gnr}
            if gnr in [0, 5]:
                item['direct_video'] = True
            self.addDir(item)
    def SearchResult(self, str_ch, page, extra):
        printDBG(f"SearchResult for: {str_ch}, page={page}")
        query = urllib.parse.quote(str_ch.encode('utf-8'))
        url = f"{self.MAIN_URL}/find/?word={query}&type=&page_number={page}"
        printDBG(f"Search URL: {url}")
        sts, data = self.cm.getPage(url, self.defaultParams)
        if not sts:
            printDBG('SearchResult: failed to get page')
            return []
        blocks = re.findall(r'(<a[^>]+class="movie__block[^"]*"[^>]*>.*?</a>)',data, re.S)
        printDBG(f"Found {len(blocks)} results")
        for block in blocks:
            url = self.cm.ph.getSearchGroups(block, r'href="([^"]+)"')[0]
            icon = self.cm.ph.getSearchGroups(block, r'(?:data-src|src)="([^"]+)"')[0]
            url = quote(url, safe=':/?&=%')
            icon = quote(icon, safe=':/?&=%')
            title = self.cm.ph.getSearchGroups(block, r'<h3>([^<]+)</h3>')[0]
            title = self.cleanHtmlStr(title)
            story = self.cm.ph.getSearchGroups(block, r'<p[^>]*>(.*?)</p>')[0]
            quality = self.cm.ph.getSearchGroups(block, r'class="__quality[^"]*">([^<]+)<')[0]
            genre = self.cm.ph.getSearchGroups(block, r'class="__genre[^"]*">([^<]+)<')[0]
            rating = self.cm.ph.getSearchGroups(block, r'class="post__ratings">([^<]+)<')[0]
            category = self.cm.ph.getSearchGroups(block, r'class="post__category[^"]*">([^<]+)<')[0]
            line1_parts = []
            if quality: line1_parts.append(tscolor('\c0000FF00') + "الجودة: " + tscolor('\c00FFFFFF') + self.cleanHtmlStr(quality))
            if genre:   line1_parts.append(tscolor('\c00FF00FF') + "النوع: " + tscolor('\c00FFFFFF') + self.cleanHtmlStr(genre))
            if rating:
                rating_text = self.cleanHtmlStr(rating).strip()
                rating_value = None
                match_num = re.search(r'(\d+(\.\d+)?)', rating_text)
                if match_num:rating_value = float(match_num.group(1))
                color = '\c00FFFFFF'
                if rating_value is not None:
                    if rating_value >= 7: color = '\c0000FF00'
                    elif rating_value >= 5: color = '\c00FFA500'
                    else: color = '\c00FF0000'
                line1_parts.append(tscolor('\c00FF6600') + "التقييم: " +tscolor(color) +rating_text +tscolor('\c00FFFFFF'))
            if category:line1_parts.append(tscolor('\c0066FFFF') + "الفئة: " + tscolor('\c00FFFFFF') + self.cleanHtmlStr(category))
            line1 = " | ".join(line1_parts)
            line2 = tscolor('\c00FFFF00') + "القصة: " + tscolor('\c00FFFFFF') + self.cleanHtmlStr(story) if story else ''
            desc = line1
            if line2: desc += "\n" + line2
            self.addVideo({'import': extra,'title': title,'url': url,'icon': icon,'desc': desc.strip(),'mode': '21','hst': 'tshost'})
        return []
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
    def showitms(self, cItem):
        seen_urls = set()
        fetch_all = cItem.get('fetch_all', False)
        url = cItem['url']
        is_packs = '/packs/' in url
        collected_items = []
        next_url = None
        sub_mode = cItem.get('sub_mode', -1)
        printDBG('showitms - URL: %s' % url)
        while True:
            sts, data = self.getPage(url)
            if not sts: break
            items_data = []
            items_pattern = r'<li class="box__xs__2[^>]*>.*?<a href="([^"]+)"[^>]*title="([^"]+)"[^>]*>.*?<img[^>]*src="([^"]+)"[^>]*>(.*?)</a>'
            items_matches = []
            if not is_packs:
                items_pattern = r'<li class="box__xs__2[^>]*>.*?<a href="([^"]+)"[^>]*title="([^"]+)"[^>]*>.*?<img[^>]*src="([^"]+)"[^>]*>(.*?)</a>'
                items_matches = re.findall(items_pattern, data, re.S)
            else:
                # ===== PACKS / SEASONS =====
                packs_pattern = r'(<li class="box__xs__1.*?)(?=<li class="box__xs__1|\Z)'
                items_matches = re.findall(packs_pattern, data, re.S)
            printDBG('showitms - Found %s items (packs=%s)' % (len(items_matches), is_packs))
            for item in items_matches:
                if not is_packs:
                    url1, title, image, content = item
                    clean_title = unescape(ph.clean_html(title))
                    if not url1.startswith('http'): url1 = self.MAIN_URL + url1
                    if image.startswith('//'): image = 'https:' + image
                    elif not image.startswith('http'): image = self.MAIN_URL + image
                    url1 = quote(url1, safe=':/?&=%')
                    image = quote(image, safe=':/?&=%')
                    description_match = re.search(r'<p[^>]*>(.*?)</p>', content, re.S)
                    quality_match     = re.search(r'<div class="__quality[^>]*>(.*?)</div>', content, re.S)
                    genre_match       = re.search(r'<div class="__genre[^>]*>(.*?)</div>', content, re.S)
                    rating_match      = re.search(r'<div class="post__ratings">(.*?)</div>', content, re.S)
                    category_match    = re.search(r'<div class="post__category[^>]*>(.*?)</div>', content, re.S)
                    first_line_parts = []
                    if quality_match and quality_match.group(1).strip():
                        first_line_parts.append(tscolor('\c0000FF00') + 'الجودة: ' + tscolor('\c00FFFFFF') + ph.clean_html(quality_match.group(1)))
                    if genre_match and genre_match.group(1).strip():
                        first_line_parts.append(tscolor('\c00FF00FF') + 'النوع: ' + tscolor('\c00FFFFFF') + ph.clean_html(genre_match.group(1)))
                    if rating_match and rating_match.group(1).strip():
                        rating_text = ph.clean_html(rating_match.group(1)).strip()
                        rating_value = None
                        match_num = re.search(r'(\d+(\.\d+)?)', rating_text)
                        if match_num: rating_value = float(match_num.group(1))
                        color = '\c00FFFFFF'  # افتراضي أبيض
                        if rating_value is not None:
                            if rating_value >= 7: color = '\c0000FF00'   # أخضر
                            elif rating_value >= 5: color = '\c00FFA500'   # برتقالي
                            else: color = '\c00FF0000'   # أحمر
                        first_line_parts.append(tscolor('\c00FF6600') + 'التقييم: ' +tscolor(color) +rating_text +tscolor('\c00FFFFFF'))

                    if category_match and category_match.group(1).strip():
                        first_line_parts.append(tscolor('\c0066FFFF') + 'الفئة: ' + tscolor('\c00FFFFFF') + ph.clean_html(category_match.group(1)))
                    first_line = ' | '.join(first_line_parts)
                    second_line = ''
                    if description_match and description_match.group(1).strip():
                        second_line = tscolor('\c00FFFF00') + 'القصة: ' + tscolor('\c00FFFFFF') + ph.clean_html(description_match.group(1))
                    desc = first_line
                    if second_line: desc += '\\n' + second_line
                    self.addVideo({'import': cItem.get('import', ''),'category': 'host2','title': clean_title,'url': url1,'desc': desc,'good_for_fav': True,'icon': image,'EPG': True,'hst': 'tshost','mode': '22','sub_mode': sub_mode})
                else:
                    content = item
                    url1   = ph.search(content, r'href="([^"]+)"')[0]
                    title  = ph.search(content, r'<div class="title___">([^<]+)</div>')[0]
                    image  = ph.search(content, r'(?:data-src|src)="([^"]+)"')[0]
                    clean_title = unescape(ph.clean_html(title))
                    if not url1.startswith('http'): url1 = self.MAIN_URL + url1
                    if image.startswith('//'): image = 'https:' + image
                    elif not image.startswith('http'): image = self.MAIN_URL + image
                    url1 = quote(url1, safe=':/?&=%')
                    image = quote(image, safe=':/?&=%')
                    desc_parts = []
                    hover_box = ph.search(content, r'<div class="hover__box.*?>(.*?)</div>', flags=re.S)[0]
                    dots_info = ph.search(hover_box, r'<ul class="dots__info">(.*?)</ul>', flags=re.S)[0]
                    line_parts = []
                    if dots_info:
                        spans = re.findall(r'<span>(.*?)</span>', dots_info)
                        if len(spans) > 0: line_parts.append(tscolor('\c00FFFF00') + 'السنة: ' + tscolor('\c00FFFFFF') + ph.clean_html(spans[0]))
                        if len(spans) > 1: line_parts.append(tscolor('\c00FFFF00') + 'الدولة: ' + tscolor('\c00FFFFFF') + ph.clean_html(spans[1]))
                    bottom_ul = ph.search(hover_box, r'<ul class="bottom__ul">(.*?)</ul>', flags=re.S)[0]
                    if bottom_ul:
                        lis = re.findall(r'<li>(.*?)</li>', bottom_ul)
                        if len(lis) > 0: line_parts.append(tscolor('\c0000FF00') + 'الجودة: ' + tscolor('\c00FFFFFF') + ph.clean_html(lis[0]))
                        if len(lis) > 1: line_parts.append(tscolor('\c00FF00FF') + 'النوع: ' + tscolor('\c00FFFFFF') + ph.clean_html(lis[1]))
                    if line_parts: desc_parts.append(' | '.join(line_parts))
                    story = ph.search(content, r'<p class="story">(.*?)</p>')[0]
                    if story: desc_parts.append(tscolor('\c00FFFF00') + 'القصة: ' + tscolor('\c00FFFFFF') + ph.clean_html(story))
                    desc = '\n'.join(desc_parts)
                    self.addDir({'import': cItem.get('import', ''),'category': 'host2','title': clean_title,'url': url1,'icon': image,'desc': desc,'good_for_fav':True,'mode': '23','sub_mode': sub_mode})
            next_url = None
            pagination_match = re.search(r'class="pagination.*?<a[^>]*href="([^"]*)"[^>]*>.*?التالي', data, re.S | re.I)
            if pagination_match:
                next_url = pagination_match.group(1)
            if not next_url:
                next_match = re.search(r'<a[^>]*class="[^"]*next[^"]*"[^>]*href="([^"]*)"', data, re.I)
                if next_match:
                    next_url = next_match.group(1)
            if not next_url:
                current_page = re.search(r'class="[^"]*current[^"]*"[^>]*>(\d+)<', data)
                if current_page:
                    current_num = int(current_page.group(1))
                    next_num = current_num + 1
                    next_url = re.sub(r'/(\d+)/?$', '/' + str(next_num) + '/', url)
                    if next_url == url:
                        next_url = url + 'page/' + str(next_num) + '/' if not url.endswith('/') else url + 'page/' + str(next_num) + '/'
            printDBG('showitms - Next URL found: %s' % next_url)
            if not fetch_all:
                break
            if next_url:
                if not next_url.startswith('http'):
                    next_url = self.MAIN_URL + next_url if next_url.startswith('/') else self.MAIN_URL + '/' + next_url
                url = next_url
            else:
                break
            if is_packs and next_url:
                next_url = next_url.replace('/packs/packs/', '/packs/')
        if not fetch_all and len(seen_urls) > 0:
            self.addDir({'import': cItem.get('import', ''),'category': 'host2', 'title': tscolor('\c0000??66') + '◀ عرض الكل فى قائمة واحدة ▶','url': cItem['url'],'desc': tscolor('\c0000??66') + 'يجمع كل محتويات القسم بدون تكرار ومرتب أبجديا .. لكنه يأخذ وقت أطول للتحميل فكن صبورا.','icon': cItem.get('icon', ''),'mode': '20','fetch_all': True,'sub_mode': sub_mode})
        if next_url and not fetch_all:
            clean_current = url.rstrip('/')
            clean_next = next_url.rstrip('/')
            if clean_next != clean_current:
                self.addDir({'import': cItem.get('import', ''),'category': 'host2','title': tscolor('\c00FFFF00') + '<< الصفحة التالية','url': next_url,'desc': '','icon': cItem.get('icon', ''),'mode': '20','page': cItem.get('page', 1) + 1,'sub_mode': sub_mode})
    def showelms(self, cItem):
        url = cItem.get('url')
        season_id = cItem.get('season_id', '')
        desc = cItem.get('desc', '')
        icon = cItem.get('icon', '')
        if not url:
            return
        if season_id:
            post_url = self.getFullUrl("/season__episodes/")
            post_data = {'season_id': season_id,'csrf_token': cItem.get('csrf_token', '')}
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': url
            }
            sts, response = self.cm.getPage(post_url, {'header': headers}, post_data)
            if not sts: return
            try: result = json_loads(response)
            except: return
            if result.get('type') != 'success': return
            html = result.get('html', '')
        else:
            sts, html = self.getPage(url)
            if not sts: return
        episodes_section = re.findall(r'class="ContainerEpisodesList(.*?)</div>', html, re.S)
        episodes = []
        if episodes_section:
            raw_episodes = re.findall(r'href="(.*?)".*?>(.*?)</a>', episodes_section[0], re.S)
            for ep_url, title in raw_episodes:
                clean_title = ph.clean_html(title)
                match = re.search(r'الحلقة\s+(\d+)', clean_title)
                ep_num = int(match.group(1)) if match else 0
                ep_url = quote(ep_url, safe=':/?&=%')
                ep_icon = quote(icon, safe=':/?&=%')
                episodes.append({'url': ep_url, 'title': clean_title, 'num': ep_num, 'icon': ep_icon})
            episodes.sort(key=lambda x: x['num'])
            for ep in episodes:
                self.addVideo({'import': cItem.get('import', ''),'title': ep['title'],'url': ep['url'],'icon': ep['icon'],'desc': desc,'good_for_fav':True,'EPG': True,'hst': 'tshost'})
        else:
            self.addVideo({'import': cItem.get('import', ''),'title': cItem['title'],'url': quote(url, safe=':/?&=%'),'icon': quote(icon, safe=':/?&=%'),'desc': desc,'EPG': True,'hst': 'tshost'})
    def listSeasons(self, cItem):
        printDBG('ArabSeed.listSeasons >>> %s' % cItem)
        url = cItem.get('url')
        sts, data = self.getPage(url)
        if not sts or not data: return
        # ================= TRAILER =================
        trailer_url = self.cm.ph.getSearchGroups(data,r'data-iframe="([^"]+)"')[0]
        if trailer_url:
            # YouTube
            if 'youtube.com/embed/' in trailer_url: trailer_url = trailer_url.replace('youtube.com/embed/','youtube.com/watch?v=')
            # IMDb
            elif 'imdb.com/video/' in trailer_url: pass
            self.addVideo({'title': tscolor('\c0000??00') + "TRAILER",'url': trailer_url,'type': 'video','icon': cItem.get('icon', ''),'need_resolve': 1,'hst': 'tshost'})
        printDBG('[ArabSeed] trailer_url = %s' % trailer_url)
        # ================= CSRF TOKEN =================
        csrf_token = self.cm.ph.getSearchGroups(data, r'csrf__token["\']\s*:\s*["\']([^"\']+)')[0]
        if not csrf_token: csrf_token = self.cm.ph.getSearchGroups(data, r'name="csrf_token" value="([^"]+)"')[0]
        # ================= SEASONS =================
        seasons_block = self.cm.ph.getDataBeetwenMarkers(data, 'id="seasons__list"', '</div></div>', False)[1]
        if seasons_block:
            season_items = self.cm.ph.getAllItemsBeetwenMarkers(seasons_block, '<li', '</li>')
            for s in season_items:
                season_id = self.cm.ph.getSearchGroups(s, r'data-term="([^"]+)"')[0]
                title = self.cm.ph.getSearchGroups(s, r'<span>([^<]+)</span>')[0]
                if not season_id or not title: continue
                params = dict(cItem)
                params.update({'title': title.strip(),'season_id': season_id,'csrf_token': csrf_token,'mode': '24','hst': 'tshost'})
                self.addDir(params)
        # ================= NO SEASONS → DIRECT EPISODES =================
        else:
            printDBG('[ArabSeed] No seasons → listing episodes directly')
            episodes_block = self.cm.ph.getDataBeetwenMarkers(data, '<ul class="episodes__list', '</ul>', False)[1]
            promo_url = self.cm.ph.getSearchGroups(data, r'<div class="watch__and__download.*?<a href="([^"]+/watch/)"',)[0]
            if promo_url:
                printDBG('[ArabSeed] Single promo detected')
                params = dict(cItem)
                params.update({'title': tscolor('\c00????00') + "برومو المسلسل",'url': promo_url,'type': 'video','mode': '22','hst': 'tshost','icon': cItem.get('icon', '')})
                self.addVideo(params)
            if episodes_block:
                episodes = self.cm.ph.getAllItemsBeetwenMarkers(episodes_block, '<li', '</li>')
                episodes.reverse()
                for ep in episodes:
                    ep_num = self.cm.ph.getSearchGroups(ep, r'<b>(\d+)</b>')[0]
                    if not ep_num: continue
                    ep_url = self.cm.ph.getSearchGroups(ep, r'href="([^"]+)"')[0]
                    if not ep_url: continue
                    if '/watch/' not in ep_url: ep_url += 'watch/'
                    self.addVideo({'title': u'الحلقة %s' % ep_num,'url': ep_url,'icon': cItem.get('icon', ''),'mode': '22','hst': 'tshost'})
            elif 'watch__area' in data:
                printDBG('[ArabSeed] Found watch__area → trying encoded video')
                m = re.search(r'data-post="(\d+)".+?data-qu="(\d+)".+?data-link="([^"]+)"', data, re.S)
                if m:
                    post_id, quality, link = m.groups()
                    try:
                        encoded = re.search(r'(?:url=|id=)([A-Za-z0-9+/=]+)', link).group(1)
                        padding = 4 - len(encoded) % 4
                        if padding != 4: encoded += '=' * padding
                        video_url = base64.b64decode(encoded).decode('utf-8')
                    except:
                        video_url = self.MAIN_URL + link if link.startswith('/') else link
                    self.addVideo({'title': u'برومو / مشاهدة [%sP]' % quality,'url': video_url,'icon': cItem.get('icon', ''),'mode': '22','hst': 'tshost'})

    def listEpisodes(self, cItem):
        printDBG('ArabSeed.listEpisodes >>> %s' % cItem)
        url = cItem.get('url')
        season_id = cItem.get('season_id')
        csrf_token = cItem.get('csrf_token')
        if not url or not season_id or not csrf_token: return
        # ========= CHECK FIRST SEASON =========
        sts, data = self.getPage(url)
        if sts:
            selected = self.cm.ph.getSearchGroups(data,r'<li[^>]+class="selected"[^>]+data-term="(\d+)"')[0]
            if selected == season_id:
                episodes = self.cm.ph.getAllItemsBeetwenMarkers(data, '<li', '</li>')
                episodes.reverse()
                for ep in episodes:
                    ep_num = self.cm.ph.getSearchGroups(ep, r'<b>(\d+)</b>')[0]
                    if not ep_num: continue
                    ep_url = self.cm.ph.getSearchGroups(ep, r'href="([^"]+)"')[0]
                    if not ep_url: continue
                    if '/watch/' not in ep_url: ep_url += 'watch/'
                    self.addVideo({'title': u'الحلقة %s' % ep_num,'url': ep_url,'mode': '22','hst': 'tshost'})
                return
        # ========= AJAX OTHER SEASONS =========
        post_url = self.getFullUrl('/season__episodes/')
        post_data = {'season_id': season_id,'csrf_token': csrf_token}
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': url,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        sts, response = self.cm.getPage(post_url, {'header': headers}, post_data)
        if not sts: return
        try: result = json.loads(response)
        except: return
        if result.get('type') != 'success': return
        episodes = self.cm.ph.getAllItemsBeetwenMarkers(result.get('html', ''), '<li', '</li>')
        episodes.reverse()
        for ep in episodes:
            ep_num = self.cm.ph.getSearchGroups(ep, r'<b>(\d+)</b>')[0]
            if not ep_num: continue
            ep_url = self.cm.ph.getSearchGroups(ep, r'href="([^"]+)"')[0]
            if not ep_url: continue
            if '/watch/' not in ep_url: ep_url += 'watch/'
            self.addVideo({'title': u'الحلقة %s' % ep_num,'url': ep_url,'mode': '22','hst': 'tshost'})

    def get_links(self, cItem):
        urlTab = []
        url = cItem['url']
        if not url: return []
        # ===== IMDb DIRECT =====
        if 'imdb.com/video/' in url:
            printDBG("Detected IMDb trailer")
            return self.getIMDBTrailer(url)
        # ===== YOUTUBE DIRECT =====
        if 'youtube.com' in url or 'youtu.be' in url:
            urlTab.append({'name': 'YouTube','url': url,'need_resolve': 1})
            return urlTab
        if '/watch/' not in url: url = url.rstrip('/') + '/watch/'
        sts, watch_data = self.getPage(url)
        if not sts: return urlTab
        printDBG('get_links - Watch page loaded')
        servers_pattern = r'data-qu="(\d+)"[^>]+data-link="([^"]+)"[^>]*>\s*<i[^>]*></i>\s*<span>([^<]+)</span>'
        servers = re.findall(servers_pattern, watch_data, re.S)
        server_domains = {}
        for quality, link, name in servers:
            if 'عرب' in name and quality == '480': continue
            try:
                encoded = re.search(r'(?:url=|id=)([A-Za-z0-9+/=]+)', link).group(1)
                padding = 4 - len(encoded) % 4
                if padding != 4: encoded += '=' * padding
                video_url = base64.b64decode(encoded).decode('utf-8')
            except:
                video_url = self.MAIN_URL + link if link.startswith('/') else link
            domain_match = re.search(r'https?://([^/]+)', video_url)
            if domain_match:
                domain = domain_match.group(1)
                server_id = name.strip()
                if server_id not in ['سيرفر عرب سيد']:
                    server_domains[server_id] = domain
        post_id = self.cm.ph.getSearchGroups(watch_data, r"psot_id['\s:]+['\"](\d+)")[0] or \
                  self.cm.ph.getSearchGroups(watch_data, r"post_id['\s:]+['\"](\d+)")[0]
        csrf_token = self.cm.ph.getSearchGroups(watch_data, r"csrf__token['\"]:\s*['\"]([^'\"]+)")[0]
        printDBG('get_links - post_id: {}, csrf_token: {}'.format(post_id, csrf_token))
        if post_id and csrf_token:
            for quality in ['1080', '720', '480']:
                for server_id in range(0, 6):
                    server_url = self.get_server_link(post_id, quality, server_id, csrf_token, url)
                    if server_url:
                        if server_id == 0:
                            server_name = 'سيرفر عرب سيد'
                            domain_name = 'm.reviewrate.net'
                        else:
                            server_name = 'سيرفر {}'.format(server_id)
                            domain_match = re.search(r'https?://([^/]+)', server_url)
                            domain_name = domain_match.group(1) if domain_match else 'unknown'
                            if server_name in server_domains:
                                domain_name = server_domains[server_name]
                        if server_id == 0:
                            label = '[{}P] {}'.format(quality, server_name)
                        else:
                            label = '[{}P] {} - {}'.format(quality, server_name, domain_name)
                        urlTab.append({'name': label, 'url': server_url, 'need_resolve': 1})
                        printDBG('get_links - Added: {}'.format(label))
        def sort_key(item):
            name = item['name']
            if '1080' in name and 'عرب سيد' in name: return 10
            elif '720' in name and 'عرب سيد' in name: return 9
            elif '480' in name and 'عرب سيد' in name: return 8
            elif '1080' in name: return 7
            elif '720' in name: return 6
            else: return 5
        urlTab.sort(key=sort_key, reverse=True)
        printDBG('get_links - Total servers found: {}'.format(len(urlTab)))
        return urlTab
    def get_server_link(self, post_id, quality, server_id, csrf_token, referer):
        """استخراج رابط سيرفر معين لجودة معينة - مع تحسينات السرعة"""
        try:
            ajax_url = 'https://asd.pics/get__watch__server/'
            post_data = {'post_id': post_id,'quality': quality,'server': server_id,'csrf_token': csrf_token}
            headers = {
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': referer,
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
            }
            params = self.defaultParams.copy()
            params['header'] = headers
            params['timeout'] = 7
            params['connect_timeout'] = 3
            printDBG('get_server_link - Fetching server {} quality {}...'.format(server_id, quality))
            sts, response = self.cm.getPage(ajax_url, params, post_data)
            if sts and response:
                try:
                    res = json.loads(response)
                    if res.get('type') == 'success' and res.get('server'):
                        server_url = res['server']
                        if 'url=' in server_url or 'id=' in server_url:
                            try:
                                encoded = re.search(r'(?:url=|id=)([A-Za-z0-9+/=]+)', server_url).group(1)
                                padding = 4 - len(encoded) % 4
                                if padding != 4: encoded += '=' * padding
                                server_url = base64.b64decode(encoded).decode('utf-8')
                            except: pass
                        return server_url
                except: pass
        except Exception as e: printDBG('get_server_link - Error: {}'.format(str(e)))
        return None
    def getVideos(self, videoUrl):
        printDBG('getVideos - Processing: {}'.format(videoUrl))
        try: return self.up.getVideoLinkExt(videoUrl)
        except Exception as e:
            printDBG('getVideos - Resolver error: {}'.format(str(e)))
            return []
    # ==========================================
    # IMDb Trailer Resolver
    # ==========================================
    def getIMDBTrailer(self, url):
        printDBG('IMDB resolver start >>> %s' % url)
        links = []
        vid = self.cm.ph.getSearchGroups(url, r'(vi\d+)')[0]
        if not vid:
            printDBG('IMDB: video id not found')
            return []
        embed_url = 'https://www.imdb.com/video/embed/%s/' % vid
        printDBG('IMDB embed URL >>> %s' % embed_url)
        sts, data = self.getPage(embed_url)
        if not sts:
            printDBG('IMDB: failed to load embed page')
            return []
        json_data = self.cm.ph.getSearchGroups(data,r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>')[0]
        if not json_data:
            printDBG('IMDB: __NEXT_DATA__ not found')
            return []
        try:
            json_data = json.loads(json_data)
            videoData = json_data['props']['pageProps'].get('videoEmbedPlaybackData')
            if not videoData:
                printDBG('IMDB: videoEmbedPlaybackData not found')
                return []
            qualities = []
            for item in videoData.get('playbackURLs', []):
                mime = item.get('videoMimeType', '').lower()
                video_url = item.get('url')
                if not video_url: continue
                if mime != 'mp4': continue
                display = item.get('displayName', {})
                quality_txt = display.get('value', '')
                try: quality = int(quality_txt.replace('p', '').strip())
                except: continue
                qualities.append({'q': quality,'name': 'IMDb %dp' % quality,'url': video_url,'need_resolve': 0})
            qualities.sort(key=lambda x: x['q'], reverse=True)
            for q in qualities:
                links.append({'name': q['name'],'url': q['url'],'need_resolve': 0})
        except Exception as e:
            printDBG('IMDB extraction error: %s' % e)
        return links

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
    def start(self, cItem):
        mode = cItem.get('mode', None)
        printDBG('Arabseed start mode = %s' % mode)
        printDBG('cItem: %s' % str(cItem))
        if mode == '10': self.showmenu1(cItem)
        elif mode == '20': self.showitms(cItem)
        elif mode == '21': self.showelms(cItem)
        elif mode == '22': return self.get_links(cItem)
        elif mode == '23': return self.listSeasons(cItem)
        elif mode == '24': return self.listEpisodes(cItem)
        elif mode == '50': self.showsearch(cItem)
        elif mode == '51': self.SearchResult(cItem.get('search_pattern', ''), cItem.get('page', 1), cItem.get('import', ''))
        else: self.showmenu(cItem)
        return True