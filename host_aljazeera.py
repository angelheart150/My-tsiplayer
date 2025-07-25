# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass, tscolor,tshost
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.tools.iptvtypes import strwithmeta
from Plugins.Extensions.IPTVPlayer.libs import ph
import os, re, json
try: from html import unescape  # Python 3
except ImportError:
    try: from HTMLParser import HTMLParser  # Python 2
    except ImportError: from html.parser import HTMLParser  # Python 3 alternative
    unescape = HTMLParser().unescape
def getinfo():
    info_={}
    name = 'Aljazeera'
    hst = 'https://ajnet.me'
    info_['old_host'] = hst
    hst_ = tshost(name)
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='2.0 18/07/2025'
    info_['dev']='MOHAMED_OS + Angel_heart'
    info_['cat_id']='21'
    info_['desc']='افلام وثائقية'
    info_['icon'] = 'https://banner2.cleanpng.com/20180615/ews/aa793z4va.webp'
    info_['recherche_all']='0'
    return info_
class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{})
        self.MAIN_URL   =  getinfo()['host']
        self.USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0'
    def showmenu(self,cItem):
        TAB = [('افلام وثائقية','/programs/investigative/','20',0),('مسلسلات وثائقية','/programs/documentaries/','20',0),('برامج حوارية','/programs/discussions/','20',0),('برامج رقمية','/programs/digital/','20',0),('جميع البرامج','/programs/all-shows/','20',0)]
        self.add_menu(cItem,'','','','','','',TAB=TAB,search=False)
    def showitms(self,cItem):
        sts, data = self.getPage(cItem.get('url'))
        if sts:
            Liste_els = re.findall(r'loading="lazy" src="(.+?)" srcSet.+?<h3 class="program-card__title"><a href="(.+?)"><span>(.+?)</span></a></h3><p', data, re.S)
            for (image,url,titre)in Liste_els:
                image_ = self.MAIN_URL+image.split("?")[0]
                info  = self.std_title(ph.clean_html(titre))
                self.addDir({'import':cItem['import'],'category' : 'host2','title':info.get('title_display'),'icon':self.std_url(image_),'desc':info.get('desc'),'mode':'21','url':self.MAIN_URL+url,'good_for_fav':True,'hst':'tshost'})
    def showelms(self, cItem):
        sts, data = self.getPage(cItem.get('url'))
        if not sts:
            self.addMarker({'title': 'فشل في تحميل البيانات','desc': 'تعذر الاتصال بالخادم','icon': cItem.get('icon', '')})
            return
        if 'graphql' in cItem.get('url', ''):
            try:
                json_data = json.loads(data)
                articles = json_data.get('data', {}).get('articles', [])
                current_urls = set()
                for item in self.currList:
                    if item.get('type') != 'category' and 'url' in item:
                        current_urls.add(item['url'])
                added_count = 0
                for article in articles:
                    if added_count >= 16:
                        break
                    title = article.get('title', '')
                    url = article.get('link', '')
                    if not url.startswith('http'):
                        url = self.MAIN_URL + url
                    if not title or not url or url in current_urls:
                        continue
                    clean_title = self._clean_title(title, cItem.get('title', ''))
                    desc = article.get('excerpt', '')
                    duration = article.get('video', {}).get('duration', '')
                    image = article.get('featuredImage', {}).get('sourceUrl', '')
                    final_desc = ph.clean_html(desc) if desc else ''
                    if duration:
                        final_desc += f"\n\nمدة الفيديو: {duration}" if final_desc else f"مدة الفيديو: {duration}"                        
                    self.addVideo({'import': cItem['import'],'hst': 'tshost','url': url,'title': clean_title,'desc': final_desc,'icon': self.std_url(self.MAIN_URL + image) if image else '','good_for_fav': True,'EPG': True})
                    added_count += 1
                    current_urls.add(url)                
                has_more = len(articles) > 16 or (len(articles) == 16 and added_count == 16)                
                if has_more:
                    current_offset = cItem.get('offset', 0)
                    next_offset = current_offset + 16
                    program_name = cItem['url'].split('category%22%3A%22')[-1].split('%22')[0]                    
                    next_url = (
                        f"{self.MAIN_URL}/graphql?wp-site=aja&"
                        f"operationName=ArchipelagoEpisodesQuery&"
                        f"variables=%7B%22category%22%3A%22{program_name}%22%2C%"
                        f"22quantity%22%3A16%2C%22offset%22%3A{next_offset}%7D&"
                        f"extensions=%7B%7D"
                    )                    
                    self.addDir({'import': cItem['import'],'category': 'host2','title': tscolor('\c00????30')+'اعرض المزيد (16 فيديو)','url': next_url,'offset': next_offset,'mode': '21','icon': cItem.get('icon', ''),'desc': 'تحميل 16 فيديو إضافي','hst': 'tshost'})
                elif added_count == 0 and not self.currList:
                    self.addMarker({'title': tscolor('\c00????30')+'لا توجد فيديوهات متاحة','icon': cItem.get('icon', '')})
                elif added_count == 0:
                    self.addMarker({'title': 'تم عرض كل الفيديوهات المتاحة','desc': 'لا توجد فيديوهات إضافية للعرض','icon': cItem.get('icon', '')})
            except Exception as e:
                printDBG(f'Error parsing JSON: {str(e)}')
                if not self.currList:
                    self.addMarker({'title': 'حدث خطأ في جلب البيانات','desc': 'تعذر تحميل قائمة الفيديوهات','icon': cItem.get('icon', '')})
                else:
                    self.addMarker({'title': 'تم عرض كل الفيديوهات المتاحة','desc': 'لا توجد فيديوهات إضافية للعرض','icon': cItem.get('icon', '')})
        else:
            self._extract_videos(data, cItem)
            load_more = re.search(
                r'<button[^>]*class="show-more-button[^"]*"[^>]*data-testid="show-more-button"[^>]*>.*?'
                r'<span[^>]*aria-hidden="true"[^>]*>(.*?)</span>.*?'
                r'(?:data-url="([^"]+)")?',
                data, re.S
            )
            if load_more:
                button_text = load_more.group(1).strip()
                load_more_url = load_more.group(2)
                if not load_more_url:
                    program_name = cItem['url'].split('/')[-1]
                    if program_name:
                        offset = cItem.get('offset', 0) + 16
                        load_more_url = (
                            f"{self.MAIN_URL}/graphql?wp-site=aja&"
                            f"operationName=ArchipelagoEpisodesQuery&"
                            f"variables=%7B%22category%22%3A%22{program_name}%22%2C%"
                            f"22quantity%22%3A16%2C%22offset%22%3A{offset}%7D&"
                            f"extensions=%7B%7D"
                        )
                if load_more_url:
                    if not load_more_url.startswith('http'):
                        load_more_url = self.MAIN_URL + load_more_url
                    self.addDir({'import': cItem['import'],'category': 'host2','title': tscolor('\c00????30')+ button_text if button_text else tscolor('\c00????30')+ 'اعرض المزيد (16 فيديو)','url': load_more_url,'page': cItem.get('page', 0) + 1,'offset': cItem.get('offset', 0) + 16,'mode': '21','icon': cItem.get('icon', ''),'desc': 'تحميل 16 فيديو إضافي','hst': 'tshost'})
    def getPage(self, url, params={}, post_data=None):
        if 'graphql' in url:
            headers = {'Accept': 'application/json','Content-Type': 'application/json','User-Agent': self.USER_AGENT,'Referer': self.MAIN_URL,'wp-site': 'aja','original-domain': 'www.ajnet.me'}
            params['header'] = headers
        return TSCBaseHostClass.getPage(self, url, params, post_data)
    def _extract_videos(self, data, cItem):
        if data.strip().startswith('{'):
            try:
                json_data = json.loads(data)
                for video in json_data.get('data', {}).get('articles', []):
                    title = video.get('title', '')
                    url = video.get('link', '')
                    desc = video.get('excerpt', '')
                    duration = video.get('video', {}).get('duration', '')
                    image = video.get('featuredImage', {}).get('sourceUrl', '')
                    if not all([title, url]):
                        continue
                    clean_title = self._clean_title(title, cItem['title'])
                    final_desc = ph.clean_html(desc) if desc else ''
                    if duration:
                        final_desc += f"\n\nمدة الفيديو: {duration}" if final_desc else f"مدة الفيديو: {duration}"
                    self.addVideo({'import': cItem['import'],'hst': 'tshost','url': self.MAIN_URL + url,'title': clean_title,'desc': final_desc,'icon': self.std_url(self.MAIN_URL + image) if image else '','good_for_fav': True,'EPG': True})
            except Exception as e:
                printDBG(f'Error parsing JSON: {str(e)}')
        else:
            all_blocks = []
            big_video_blocks = re.findall(r'(<article class="article-card[^"]*article-card--video[^"]*">.*?</article>)', data, re.S)
            all_blocks.extend(big_video_blocks)
            video_blocks = re.findall(r'(<article class="(?:gc|playlist-item-container)[^>]*>.*?</article>)', data, re.S)
            all_blocks.extend(video_blocks)
            for block in all_blocks:
                video_data = re.search(r'href="([^"]+)".*?<img[^>]*src="([^"]+)"', block, re.S)
                if not video_data:
                    continue
                url = video_data.group(1)
                image = video_data.group(2)
                title_match = re.search(r'<h3[^>]*>\s*<a[^>]*>\s*<span[^>]*>([^<]+)</span>', block, re.S) or \
                             re.search(r'<h3[^>]*>\s*<a[^>]*>([^<]+)</a>', block, re.S) or \
                             re.search(r'<span[^>]*>([^<]+)</span>', block, re.S)
                if not title_match or 'مدة الفيديو' in title_match.group(1):
                    continue
                title = unescape(title_match.group(1).strip())
                title = re.sub(r'^["\']+|["\']+$', '', title)
                desc_match = re.search(r'(?:<div class="(?:gc__excerpt|article-card__excerpt)">.*?<p>(.*?)</p>|<div class="playlist-item-description">(.*?)</div>)', block, re.S)
                desc = desc_match.group(1) or desc_match.group(2) or '' if desc_match else ''
                duration_match = re.search(r'<span class="screen-reader-text">مدة الفيديو\s*(.*?)\s*</span>', block)
                duration = duration_match.group(1).strip() if duration_match and duration_match.group(1).strip() else ''
                clean_title = self._clean_title(title, cItem['title'])
                final_desc = ph.clean_html(desc) if desc else ''
                if duration:
                    final_desc += f"\n\nمدة الفيديو: {duration}" if final_desc else f"مدة الفيديو: {duration}"
                self.addVideo({'import': cItem['import'],'hst': 'tshost','url': self.MAIN_URL + url,'title': clean_title,'desc': final_desc,'icon': self.std_url(self.MAIN_URL + image.split("?")[0]),'good_for_fav': True,'EPG': True})
    def _clean_title(self, title, program_title):
        patterns_to_remove = [
            program_title + " - ",
            program_title + "-",
            program_title + ": ",
            program_title + " ــ ",
            program_title + " – ",
            program_title
        ]
        clean_title = title
        for pattern in patterns_to_remove:
            clean_title = clean_title.replace(pattern, "")
        clean_title = re.sub(r'\s+', ' ', clean_title).strip()
        clean_title = re.sub(r'^\s*[-–—:]+\s*', '', clean_title).strip()
        return clean_title
    def get_links(self, cItem):
        urlTab = []
        js_url = "https://players.brightcove.net/665001584001/J84cZMVRPE_default/index.min.js"
        js_path = "/tmp/index.min.js"
        if not os.path.exists(js_path):
            sts_js = self.download_file(js_url, js_path)
            if not sts_js:
                printDBG("[aljazeera] Failed to download JS file for quality extraction")
                return urlTab
        try:
            with open(js_path, 'r', encoding='utf-8') as f:
                js_data = f.read()
            pattern = re.compile(r'{[^{}]*"src":"(https?://[^"]+\.(?:m3u8|mp4|ts))"[^{}]*"height":(\d+)[^{}]*}', re.I)
            matches = pattern.findall(js_data)
            found = {}
            for url, height in matches:
                base_url = re.sub(r'^https?:', '', url)
                if base_url not in found:
                    found[base_url] = {'url': url, 'height': int(height)}
            sorted_links = sorted(found.values(), key=lambda x: x['height'], reverse=True)
            for idx, item in enumerate(sorted_links, start=1):
                label = f'Aljazeera [{item["height"]}p]'
                urlTab.append({'name': label, 'url': strwithmeta(item['url'], {'Referer': cItem['url']}), 'need_resolve': 0})
        except Exception as e:
            printDBG(f"[aljazeera] Error reading JS file: {e}")
        if not urlTab:
            sts, data = self.getPage(cItem['url'])
            if not sts:
                return urlTab
            embed = re.search(r'"embedUrl"\s*:\s*"([^"]+)"', data)
            if not embed:
                return urlTab
            embed_url = embed.group(1)
            video_id = self.cm.ph.getSearchGroups(embed_url, r'videoId=(\d+)')[0]
            if not video_id:
                return urlTab
            api_url = f"https://edge.api.brightcove.com/playback/v1/accounts/665001584001/videos/{video_id}"
            headers = {'Accept': 'application/json;pk=BCpkADawqM2WV_cMXnGg7cQ_h8ZF7RlC8EyY4uVca2LT3ze4PrU4MCCuj3F7TA2rOsSXAXgLDcWKavBi2M5_R7HRDOAnsQ1OX4yzxA00cLv37ggu76kll4P_eX4','User-Agent': self.USER_AGENT}
            sts, json_data = self.getPage(api_url, {'header': headers})
            if not sts:
                return urlTab
            try:
                video_data = json.loads(json_data)
                sources = video_data.get('sources', [])
                found = set()
                sources.sort(key=lambda s: s.get('height', 0), reverse=True)
                idx = 1
                for source in sources:
                    src = source.get('src', '')
                    if not src or not any(x in src for x in ['.m3u8', '.mp4', '.ts']):
                        continue
                    base_src = re.sub(r'^https?:', '', src)
                    if base_src in found:
                        continue
                    found.add(base_src)
                    height = source.get('height')
                    quality = f'{height}p' if height else 'HLS'
                    if '.m3u8' in src:
                        proto = 'HLS'
                        if '/v3/' in src: proto += ' v3'
                        elif '/v4/' in src: proto += ' v4'
                    elif '.mp4' in src: proto = 'MP4'
                    elif '.ts' in src: proto = 'TS'
                    else: proto = 'Video'
                    label = f'{idx}- Aljazeera [{quality} - {proto}]'
                    urlTab.append({'name': label, 'url': strwithmeta(src, {'Referer': embed_url}), 'need_resolve': 0})
                    idx += 1
            except Exception as e:
                printDBG(f'[aljazeera] JSON parse error: {e}')
        return urlTab
    def download_file(self, url, filepath):
        try:
            import requests
            r = requests.get(url, headers={'User-Agent': self.USER_AGENT})
            if r.status_code == 200:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(r.text)
                return True
            return False
        except Exception as e:
            printDBG(f"[aljazeera] download_file error: {e}")
            return False
    def getArticle(self,cItem):
        Desc = [('Story','class="article-excerpt">(.*?)</','\n','')]
        desc = self.add_menu(cItem,'','article-header">(.*?)article-content-read-more','','desc',Desc=Desc)
        if desc =='': desc = cItem.get('desc','')
        return [{'title':cItem['title'], 'text': desc, 'images':[{'title':'', 'url':cItem.get('icon','')}], 'other_info':{}}]