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
############################################################################## 20251108
def getinfo():
    info_={}
    name = 'Arabseed'
    hst = 'https://a.asd.homes'
    info_['old_host'] = hst
    hst_ = tshost(name)	
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='4.0 08/11/2025'    
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
                            {'category':hst, 'sub_mode':2, 'title': 'رمـضـان', 'mode':'10'},
                            {'category':hst, 'sub_mode':3, 'title': 'انـمـي', 'mode':'10'},                            
                            {'category':hst, 'sub_mode':4, 'title': 'متنوع','mode':'10'},
                            {'category':'search','title':tscolor('\c00????30') + _('Search'), 'search_item':True,'page':1,'hst':'tshost'},
                            ]		
        self.listsTab(self.Arabseed_TAB, {'import':cItem.get('import',''),'icon':cItem.get('icon','')})
    def showmenu1(self, cItem):
        hst = 'host2'
        gnr = cItem['sub_mode']
        categories = {
            0: [
                ('/category/arabic-movies-6/', 'أفلام عربية'),
                ('/category/foreign-movies-6/', 'أفلام أجنبية'),
                ('/category/turkish-movies/', 'أفلام تركية'),
                ('/category/indian-movies/', 'أفلام هندية'),
                ('/category/netfilx/افلام-netfilx/', 'Netfilx أفلام'),
                ('/category/asian-movies/', 'أفلام اسيوية'),
                ('/category/افلام-كلاسيكيه/', 'افلام كلاسيكيه'),
                ('/category/افلام-مدبلجة/', 'افلام مدبلجة'),
            ],
            1: [
                ('/category/arabic-series-3/', 'مسلسلات عربية'),
                ('/category/مسلسلات-مصريه/', 'مسلسلات مصريه'),
                ('/category/foreign-series-3/', 'مسلسلات أجنبية'),
                ('/category/turkish-series-2/', 'مسلسلات تركية'), 
                ('/category/مسلسلات-هندية/', 'مسلسلات هندية'), 
                ('/category/netfilx/مسلسلات-netfilz/', 'مسلسلات Netfilx'),
                ('/category/cartoon-series/', 'مسلسلات كرتون'),
                ('/category/مسلسلات-كوريه/', 'مسلسلات كوريه'),
                ('/category/مسلسلات-مدبلجة/', 'مسلسلات مدبلجة')
            ],
            2: [
                ('/category/مسلسلات-رمضان/ramadan-series-2025/', 'رمضان 2025'),
                ('/category/مسلسلات-رمضان/ramadan-series-2024/', 'رمضان 2024'),
                ('/category/مسلسلات-رمضان/ramadan-series-2023/', 'رمضان 2023'),
                ('/category/مسلسلات-رمضان/مسلسلات-رمضان-2022/', 'مسلسلات رمضان 2022'),
                ('/category/مسلسلات-رمضان/مسلسلات-رمضان-2021/', 'مسلسلات رمضان 2021'),
                ('/category/مسلسلات-رمضان/مسلسلات-رمضان-2020-hd/', 'مسلسلات رمضان 2020'),
                ('/category/مسلسلات-رمضان/مسلسلات-رمضان-2019/', 'مسلسلات رمضان 2019'),
            ],
            3: [
                ('/category/افلام-انيميشن/', 'افلام انيميشن'),
                ('/category/cartoon-series/', 'مسلسلات كرتون')
            ],
            4: [ 
                ('/category/اغاني-عربي/', 'اغاني عربي'),
                ('/category/wwe-shows/', 'مصارعه'),
                ('/category/برامج-تلفزيونية/', 'برامج تلفزيونية'),
                ('/category/مسرحيات-عربي/', 'مسرحيات عربيه'),
            ]
        }
        cat_list = categories.get(gnr, [])
        for url, title in cat_list:
            full_url = self.MAIN_URL + url
            item = {'import': cItem.get('import', ''),'category': 'host2','url': full_url,'title': title,'desc': '','icon': cItem.get('icon', ''),'mode': '20','sub_mode': gnr}
            if gnr in [0, 4]:
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
        blocks = re.findall(
            r'(<a[^>]+class="movie__block[^"]*"[^>]*>.*?</a>)',
            data, re.S
        )
        printDBG(f"Found {len(blocks)} results")
        for block in blocks:
            url = self.cm.ph.getSearchGroups(block, r'href="([^"]+)"')[0]
            icon = self.cm.ph.getSearchGroups(block, r'(?:data-src|src)="([^"]+)"')[0]
            title = self.cm.ph.getSearchGroups(block, r'<h3>([^<]+)</h3>')[0]
            title = self.cleanHtmlStr(title)
            desc = ""
            story = self.cm.ph.getSearchGroups(block, r'<p[^>]*>(.*?)</p>')[0]
            quality = self.cm.ph.getSearchGroups(block, r'class="__quality[^"]*">([^<]+)<')[0]
            genre = self.cm.ph.getSearchGroups(block, r'class="__genre[^"]*">([^<]+)<')[0]
            rating = self.cm.ph.getSearchGroups(block, r'class="post__ratings">([^<]+)<')[0]
            category = self.cm.ph.getSearchGroups(block, r'class="post__category[^"]*">([^<]+)<')[0]
            if story:
                desc += tscolor('\c00FFFF00') + "القصة: " + tscolor('\c00FFFFFF') + self.cleanHtmlStr(story) + "\n"
            if category:
                desc += tscolor('\c0066FFFF') + "القسم: " + tscolor('\c00FFFFFF') + self.cleanHtmlStr(category) + "\n"
            if genre:
                desc += tscolor('\c00FF00FF') + "النوع: " + tscolor('\c00FFFFFF') + self.cleanHtmlStr(genre) + "\n"
            if quality:
                desc += tscolor('\c0000FF00') + "الجودة: " + tscolor('\c00FFFFFF') + self.cleanHtmlStr(quality) + "\n"
            if rating:
                desc += tscolor('\c00FF6600') + "التقييم: " + tscolor('\c00FFFFFF') + self.cleanHtmlStr(rating)
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
        collected_items = []
        next_url = None
        sub_mode = cItem.get('sub_mode', -1)
        printDBG('showitms - URL: %s' % url)
        while True:
            sts, data = self.getPage(url)
            if not sts:
                break
            items_data = []
            items_pattern = r'<li class="box__xs__2[^>]*>.*?<a href="([^"]+)"[^>]*title="([^"]+)"[^>]*>.*?<img[^>]*src="([^"]+)"[^>]*>(.*?)</a>'
            items_matches = re.findall(items_pattern, data, re.S)
            printDBG('showitms - Found %s items with basic info' % len(items_matches))
            for (url1, title, image, content) in items_matches:
                if any(x in url1 for x in ['/category/', '/tag/', 'wp-login', 'wp-admin']):
                    continue
                if url1 in seen_urls:
                    continue
                seen_urls.add(url1)
                h3_match = re.search(r'<h3>(.*?)</h3>', content, re.S)
                clean_title = unescape(ph.clean_html(h3_match.group(1))) if h3_match else unescape(ph.clean_html(title))
                if not clean_title or len(clean_title.strip()) < 2:
                    continue
                category_match = re.search(r'<div class="post__category[^>]*>(.*?)</div>', content, re.S)
                genre_match = re.search(r'<div class="__genre[^>]*>(.*?)</div>', content, re.S)
                rating_match = re.search(r'<div class="post__ratings">(.*?)</div>', content, re.S)
                quality_match = re.search(r'<div class="__quality[^>]*>(.*?)</div>', content, re.S)
                description_match = re.search(r'<p[^>]*>(.*?)</p>', content, re.S)
                if not url1.startswith('http'):
                    url1 = self.MAIN_URL + url1
                if image.startswith('//'):
                    image = 'https:' + image
                elif not image.startswith('http'):
                    image = self.MAIN_URL + image
                try:
                    parsed = image.split('/')
                    encoded_parts = []
                    for part in parsed:
                        try:
                            part.encode('ascii')
                            encoded_parts.append(part)
                        except UnicodeEncodeError:
                            encoded_parts.append(quote(part))
                    image = '/'.join(encoded_parts)
                except:
                    pass
                desc_lines = []
                if description_match and description_match.group(1).strip():
                    desc_lines.append(tscolor('\c00FFFF00') + 'القصة: ' + tscolor('\c00FFFFFF') + ph.clean_html(description_match.group(1)))
                if quality_match and quality_match.group(1).strip():
                    desc_lines.append(tscolor('\c0000FF00') + 'الجودة: ' + tscolor('\c00FFFFFF') + ph.clean_html(quality_match.group(1)))
                if genre_match and genre_match.group(1).strip():
                    desc_lines.append(tscolor('\c00FF00FF') + 'النوع: ' + tscolor('\c00FFFFFF') + ph.clean_html(genre_match.group(1)))
                if rating_match and rating_match.group(1).strip():
                    desc_lines.append(tscolor('\c00FF6600') + 'التقييم: ' + tscolor('\c00FFFFFF') + ph.clean_html(rating_match.group(1)))
                if category_match and category_match.group(1).strip():
                    desc_lines.append(tscolor('\c0066FFFF') + 'الفئة: ' + tscolor('\c00FFFFFF') + ph.clean_html(category_match.group(1)))
                desc = '\\n'.join(desc_lines) if desc_lines else ''
                self.addVideo({'import': cItem.get('import', ''),'category': 'host2','title': clean_title,'url': url1,'desc': desc,'icon': image,'EPG': True,'hst': 'tshost','mode': '22','sub_mode': sub_mode})
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
        if not fetch_all and len(seen_urls) > 0:
            self.addDir({'import': cItem.get('import', ''),'category': 'host2', 'title': tscolor('\c0000??66') + '◀ عرض الكل فى قائمة واحدة ▶','url': cItem['url'],'desc': tscolor('\c0000??66') + 'يجمع كل محتويات القسم بدون تكرار ومرتب أبجديا .. لكنه يأخذ وقت أطول للتحميل فكن صبورا.','icon': cItem.get('icon', ''),'mode': '20','fetch_all': True,'sub_mode': sub_mode})
        if next_url and not fetch_all:
            clean_current = url.rstrip('/')
            clean_next = next_url.rstrip('/')
            if clean_next != clean_current:
                self.addDir({'import': cItem.get('import', ''),'category': 'host2','title': tscolor('\c00FFFF00') + '<< الصفحة التالية','url': next_url,'desc': '','icon': cItem.get('icon', ''),'mode': '20','page': cItem.get('page', 1) + 1,'sub_mode': sub_mode})
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
                self.addVideo({'import': cItem.get('import', ''),'title': ep['title'],'url': ep['url'],'icon': cItem.get('icon', ''),'desc': cItem.get('desc', ''),'EPG': True,'hst': 'tshost'})
        else:
            self.addVideo({'import': cItem.get('import', ''),'title': cItem['title'],'url': cItem['url'],'icon': cItem.get('icon', ''),'desc': cItem.get('desc', ''),'EPG': True,'hst': 'tshost'})  
    def get_links(self, cItem):
        urlTab = []
        if config.plugins.iptvplayer.ts_dsn.value:
            urlTab = self.cacheLinks.get(str(cItem['url']), [])
            if urlTab:
                return urlTab
        url = cItem['url']
        sts, data = self.getPage(url)
        if not sts:
            return urlTab
        printDBG('get_links - Processing page for servers')
        watch_url = None
        watch_patterns = [
            r'href="([^"]*watch[^"]*)"',
            r'href="([^"]*/watch/)"',
            r'<a[^>]*class="[^"]*watch[^"]*"[^>]*href="([^"]*)"',
            r'<a[^>]*href="([^"]*)"[^>]*class="[^"]*watch[^"]*"'
        ]
        for pattern in watch_patterns:
            watch_match = re.search(pattern, data, re.I)
            if watch_match:
                watch_url = watch_match.group(1)
                if not watch_url.startswith('http'):
                    watch_url = self.MAIN_URL + watch_url
                break
        if not watch_url:
            if '/watch/' not in url:
                watch_url = url + '/watch/' if not url.endswith('/') else url + 'watch/'
            else:
                watch_url = url
        printDBG('get_links - Watch URL: {}'.format(watch_url))
        sts, watch_data = self.getPage(watch_url)
        if not sts:
            urlTab.append({'name': 'مشاهدة', 'url': watch_url, 'need_resolve': 1})
            return urlTab
        printDBG('get_links - Watch page data length: {}'.format(len(watch_data)))
        post_id = None
        post_id_match = re.search(r'data-post="(\d+)"', watch_data)
        if post_id_match:
            post_id = post_id_match.group(1)
            printDBG('get_links - Found post ID: {}'.format(post_id))
        csrf_token = self.extract_csrf_token(watch_data)
        printDBG('get_links - Found CSRF token: {}'.format(csrf_token))
        qualities = self.extract_qualities(watch_data)
        printDBG('get_links - Found qualities: {}'.format(qualities))
        servers_list = self.extract_servers(watch_data)
        printDBG('get_links - Found {} servers'.format(len(servers_list)))
        if post_id and csrf_token:
            for quality in qualities:
                if quality in ['720', '1080']:
                    printDBG('get_links - Fetching servers for quality {} via AJAX'.format(quality))
                    quality_servers = self.get_quality_servers_ajax(post_id, quality, csrf_token)
                    if quality_servers:
                        for server in quality_servers:
                            full_url = self.process_server_link(server['link'])
                            label = '[{}] {}'.format(quality + 'p', server['name'])
                            urlTab.append({'name': label, 'url': full_url, 'need_resolve': 1})
                            printDBG('get_links - Added quality server: {}'.format(label))
        if not urlTab:
            printDBG('get_links - Using servers with all qualities')
            for server in servers_list:
                for quality in qualities:
                    if post_id and csrf_token:
                        watch_link = self.get_watch_link_ajax(post_id, quality, server['server_id'], csrf_token)
                        if watch_link:
                            full_url = self.process_server_link(watch_link)
                            label = '[{}] {}'.format(quality + 'p', server['name'])
                            urlTab.append({'name': label, 'url': full_url, 'need_resolve': 1})
                            printDBG('get_links - Added server with quality: {}'.format(label))
                            continue
                    if quality == '480':
                        full_url = self.process_server_link(server['link'])
                        label = '[{}] {}'.format(quality + 'p', server['name'])
                        urlTab.append({'name': label, 'url': full_url, 'need_resolve': 1})
                        printDBG('get_links - Added default server: {}'.format(label))
        if not urlTab:
            printDBG('get_links - Using fallback method')
            asd_links = re.findall(r'https?://[^"\']*asd\.php\?url=[^"\']+', watch_data)
            for asd_link in asd_links:
                printDBG('get_links - Found ASD link: {}'.format(asd_link))
                sts, asd_data = self.getPage(asd_link)
                if sts:
                    iframe_match = re.search(r'<iframe[^>]+src="([^"]+)"', asd_data)
                    if iframe_match:
                        iframe_url = iframe_match.group(1)
                        printDBG('get_links - Extracted iframe URL: {}'.format(iframe_url))
                        urlTab.append({'name': '[480p] Direct iframe', 'url': iframe_url, 'need_resolve': 1})
        unique_servers = {}
        for server in urlTab:
            key = server['name'] + server['url']
            if key not in unique_servers:
                unique_servers[key] = server
        urlTab = list(unique_servers.values())
        def quality_sort(item):
            name = item['name']
            if '1080' in name:
                return 3
            elif '720' in name:
                return 2
            elif '480' in name:
                return 1
            else:
                return 0
        urlTab.sort(key=quality_sort, reverse=True)
        printDBG('get_links - Total unique servers found: {}'.format(len(urlTab)))
        for server in urlTab:
            printDBG('get_links - Server: {} -> {}'.format(server['name'], server['url']))
        if urlTab and config.plugins.iptvplayer.ts_dsn.value:
            self.cacheLinks[str(cItem['url'])] = urlTab
        return urlTab
    def extract_qualities(self, data):
        """استخراج الجودات المتاحة من الصفحة"""
        qualities = []
        qualities_section = re.search(r'<ul class="qualities__list">(.*?)</ul>', data, re.S)
        if qualities_section:
            qualities = re.findall(r'data-quality="([^"]*)"', qualities_section.group(1))
        if not qualities:
            qualities = re.findall(r'data-quality="([^"]*)"', data)
        filtered_qualities = []
        for q in qualities:
            if q in ['480', '720', '1080']:
                filtered_qualities.append(q)
        filtered_qualities = list(set(filtered_qualities))
        if not filtered_qualities:
            filtered_qualities = ['480', '720', '1080']
        return filtered_qualities
    def extract_servers(self, data):
        """استخراج السيرفرات من الصفحة"""
        servers_list = []
        servers_section = re.search(r'<ul class="d__flex gap__20 flex__wrap[^>]*>(.*?)</ul>', data, re.S)
        if servers_section:
            servers = re.findall(r'data-post="[^"]*"\s+data-server="([^"]*)"\s+data-qu="([^"]*)"\s+data-link="([^"]*)"[^>]*>\s*<i[^>]*></i>\s*<span>([^<]*)</span>', servers_section.group(1), re.S)
            for server_id, quality, server_link, server_name in servers:
                servers_list.append({
                    'server_id': server_id,
                    'quality': quality.strip() if quality.strip() else '480',
                    'link': server_link,
                    'name': ph.clean_html(server_name).strip()
                })
        return servers_list
    def extract_csrf_token(self, data):
        """استخراج CSRF token من الصفحة"""
        patterns = [
            r"csrf__token['\"]?\s*:\s*['\"]([^'\"]+)",
            r"<meta[^>]*name=['\"]csrf-token['\"][^>]*content=['\"]([^'\"]+)",
            r"<input[^>]*name=['\"]csrf_token['\"][^>]*value=['\"]([^'\"]+)",
            r"<input[^>]*name=['\"]_token['\"][^>]*value=['\"]([^'\"]+)",
            r"csrf_token['\"]?\s*:\s*['\"]?([^'\"\s]+)",
            r"_token['\"]?\s*:\s*['\"]?([^'\"\s]+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, data)
            if match:
                token = match.group(1)
                printDBG('extract_csrf_token - Found token via pattern: {}'.format(pattern))
                return token
        printDBG('extract_csrf_token - No token found, using fallback value')
        return '5408486120'
    def get_quality_servers_ajax(self, post_id, quality, csrf_token):
        """الحصول على السيرفرات لجودة محددة عبر AJAX"""
        servers = []
        post_data = {
            'post_id': post_id,
            'quality': quality
        }
        ajax_url = self.MAIN_URL + '/get__quality__servers/'
        headers = self.HEADER.copy()
        headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        headers['X-Requested-With'] = 'XMLHttpRequest'
        headers['Referer'] = self.MAIN_URL
        printDBG('get_quality_servers_ajax - Sending request to: {}'.format(ajax_url))
        params = self.defaultParams.copy()
        params['header'] = headers
        sts, response = self.getPage(ajax_url, params, post_data)
        if sts and response:
            try:
                data = json.loads(response)
                if data.get('type') == 'success':
                    html_content = data.get('html', '')
                    servers_data = re.findall(r'data-post="[^"]*"\s+data-server="([^"]*)"\s+data-qu="([^"]*)"\s+data-link="([^"]*)"[^>]*>\s*<i[^>]*></i>\s*<span>([^<]*)</span>', html_content, re.S)
                    for server_id, server_quality, server_link, server_name in servers_data:
                        servers.append({'server_id': server_id,'quality': server_quality,'link': server_link,'name': ph.clean_html(server_name).strip()})
                    printDBG('get_quality_servers_ajax - Found {} servers for quality {}'.format(len(servers), quality))
            except Exception as e:
                printDBG('get_quality_servers_ajax - Error: {}'.format(str(e)))
        return servers
    def get_watch_link_ajax(self, post_id, quality, server_id, csrf_token):
        """الحصول على رابط المشاهدة عبر AJAX"""
        post_data = 'post_id={}&quality={}&server={}&csrf_token={}'.format(
            post_id, quality, server_id, csrf_token
        ).encode('utf-8')
        ajax_url = self.MAIN_URL + '/get__watch__server/'
        headers = self.HEADER.copy()
        headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        headers['X-Requested-With'] = 'XMLHttpRequest'
        headers['Referer'] = self.MAIN_URL
        printDBG('get_watch_link_ajax - Sending request for quality {} server {}'.format(quality, server_id))
        params = self.defaultParams.copy()
        params['header'] = headers
        params['raw_post_data'] = True
        sts, response = self.getPage(ajax_url, params, post_data)
        if sts and response:
            try:
                data = json.loads(response)
                if data.get('type') == 'success':
                    watch_link = data.get('server')
                    printDBG('get_watch_link_ajax - Found watch link: {}'.format(watch_link))
                    return watch_link
                else:
                    printDBG('get_watch_link_ajax - Server responded but not success: {}'.format(data))
            except Exception as e:
                printDBG('get_watch_link_ajax - JSON parse error: {}'.format(str(e)))
        else:
            printDBG('get_watch_link_ajax - Request failed (sts={}, len={})'.format(sts, len(response) if response else 0))
        return None
    def process_server_link(self, server_link):
        """معالجة رابط السيرفر"""
        if server_link.startswith('/asd.php?url='):
            try:
                encoded_part = server_link.split('url=')[1]
                padding = 4 - len(encoded_part) % 4
                if padding != 4:
                    encoded_part += '=' * padding
                decoded_url = base64.b64decode(encoded_part).decode('utf-8')
                return decoded_url
            except Exception as e:
                printDBG('process_server_link - Base64 decode error: {}'.format(str(e)))
                return self.MAIN_URL + server_link
        elif server_link.startswith('/'):
            return self.MAIN_URL + server_link
        elif not server_link.startswith('http'):
            return self.MAIN_URL + '/' + server_link
        else:
            return server_link        
    def getVideos(self, videoUrl):
        urlTab = []
        printDBG('getVideos - Processing: {}'.format(videoUrl))
        if '/asd.php?url=' in videoUrl:
            try:
                encoded_part = videoUrl.split('url=')[1]
                decoded_url = base64.b64decode(encoded_part).decode('utf-8')
                printDBG('getVideos - Decoded URL: {}'.format(decoded_url))
                if decoded_url.startswith('http'):
                    urlTab.append((decoded_url, '1'))
                else:
                    urlTab.append((decoded_url, '1'))
            except Exception as e:
                printDBG('getVideos - Base64 decode error: {}'.format(str(e)))
                urlTab.append((videoUrl, '1'))
        elif any(domain in videoUrl for domain in ['voe.sx', 'filemoon.sx', 'bigwarp.pro', 'savefiles.com', 'gamehub.com']):
            urlTab.append((videoUrl, '1'))
        elif '/watch/' in videoUrl or 'embed' in videoUrl:
            urlTab.append((videoUrl, '1'))
        else:
            urlTab.append((videoUrl, '1' if any(x in videoUrl for x in ['.mp4', '.m3u8']) else '0'))
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
    def start(self, cItem):
        mode = cItem.get('mode', None)
        printDBG('Arabseed start mode = %s' % mode)
        printDBG('cItem: %s' % str(cItem))
        if mode == '10':
            self.showmenu1(cItem)
        elif mode == '20':
            self.showitms(cItem)
        elif mode == '21':
            self.showelms(cItem)
        elif mode == '22':
            return self.get_links(cItem)
        elif mode == '50':
            self.showsearch(cItem)
        elif mode == '51':
            self.SearchResult(cItem.get('search_pattern', ''), cItem.get('page', 1), cItem.get('import', ''))
        else:
            self.showmenu(cItem)
        return True