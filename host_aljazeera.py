# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass, tscolor,tshost
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.tools.iptvtypes import strwithmeta
from Plugins.Extensions.IPTVPlayer.libs import ph
import os
import re
import json
import io
try:
    from html import unescape
except ImportError:
    from HTMLParser import HTMLParser
    _html_parser = HTMLParser()
    unescape = _html_parser.unescape
try:
    from urllib import quote
except:
    from urllib.parse import quote
def getinfo():
    info_={}
    name = 'Aljazeera'
    hst = 'https://www.ajnet.me'
    info_['old_host'] = hst
    hst_ = tshost(name)
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='2.0 18/07/2025'
    info_['dev']='MOHAMED_OS + Angel_heart'
    info_['cat_id']='21'
    info_['desc']='افلام وثائقية'
    info_['icon'] = 'https://iconape.com/wp-content/png_logo_vector/al-jazeera-logo-2.png'
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
    def showitms(self, cItem):
        url = cItem['url']
        offset = cItem.get('offset', 0)
        is_all = '/programs/all-shows/' in url
        if is_all and offset == 0:
            sts, data = self.getPage(url)
            if not sts:
                self.addMarker({'title': 'فشل في تحميل البيانات'})
                return
            items = re.findall(
                r'<article class="program-card.*?">.*?href="([^"]+)".*?'
                r'src="([^"]+)".*?<span>(.*?)</span>.*?'
                r'<p class="program-card__description">(.*?)</p>',
                data, re.S
            )
            for link, img, title, desc in items:
                self.addDir({'import': cItem['import'],'category': 'host2','title': ph.clean_html(title),'url': self.MAIN_URL + link,'icon': self.std_url(self.MAIN_URL + img.split('?')[0]),'desc': ph.clean_html(desc),'mode': '21','hst': 'tshost'})
            self.addDir({'import': cItem['import'],'category': 'host2','title': tscolor('\c00????30') + 'اعرض المزيد','url': url,'offset': 20,'mode': '20','hst': 'tshost'})
            return
        category = ''
        if not is_all and '/programs/' in url:
            category = url.split('/programs/')[-1].strip('/')
        variables = {
            "quantity": 20,
            "offset": offset
        }
        if category and not is_all:
            variables["category"] = category
        vars_json = json.dumps(variables, separators=(',', ':'))
        vars_enc = quote(vars_json)
        gql_url = (
            self.MAIN_URL +
            "/graphql?wp-site=aja&operationName=ArchipelagoProgramsQuery"
            "&variables=" + vars_enc +
            "&extensions=%7B%7D"
        )
        sts, data = self.getPage(gql_url)
        if not sts:
            self.addMarker({'title': 'فشل في تحميل البيانات'})
            return
        try:
            j = json.loads(data)
            programs = j.get('data', {}).get('programs') or []
            if isinstance(programs, dict):
                nodes = programs.get('nodes', [])
            else:
                nodes = programs
            added = 0
            for pr in nodes:
                title = pr.get('title')
                link = pr.get('link')
                img = pr.get('featuredImage', {}).get('sourceUrl')
                if img:
                    if img.startswith('/'): img = self.MAIN_URL + img
                    icon = self.std_url(img)
                else: icon = cItem.get('icon', '')  
                desc = pr.get('excerpt', '')
                if not title or not link: continue
                self.addDir({'import': cItem['import'],'category': 'host2','title': ph.clean_html(title),'url': self.MAIN_URL + link,'icon': icon,'desc': ph.clean_html(desc),'mode': '21','hst': 'tshost'})
                added += 1
            if added == 20:
                self.addDir({'import': cItem['import'],'category': 'host2','title': tscolor('\c00????30') + 'اعرض المزيد','url': url,'offset': offset + 20,'mode': '20','hst': 'tshost'})
            if added == 0:
                self.addMarker({'title': 'لا توجد برامج متاحة'})
        except Exception as e:
            printDBG("showitms JSON error: %s" % e)
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
                    if duration: final_desc += "\n\nمدة الفيديو: {}".format(duration) if final_desc else "مدة الفيديو: {}".format(duration)
                    if sys.version_info[0] == 2:
                        if isinstance(clean_title, unicode): clean_title = clean_title.encode('utf-8', 'ignore')
                        if isinstance(final_desc, unicode): final_desc = final_desc.encode('utf-8', 'ignore')
                    self.addVideo({'import': cItem['import'],'hst': 'tshost','url': url,'title': clean_title,'desc': final_desc,'icon': self.std_url(self.MAIN_URL + image) if image else '','good_for_fav': True,'EPG': True})
                    added_count += 1
                    current_urls.add(url)                
                has_more = len(articles) > 16 or (len(articles) == 16 and added_count == 16)                
                if has_more:
                    current_offset = cItem.get('offset', 0)
                    next_offset = current_offset + 16
                    program_name = ''
                    if 'category%22%3A%22' in cItem['url']:
                        parts = cItem['url'].split('category%22%3A%22')
                        if len(parts) > 1:
                            program_part = parts[-1]
                            program_name = program_part.split('%22')[0]
                            if 'graphql' in program_name or 'http' in program_name or '?' in program_name:
                                program_name = ''
                    if not program_name:
                        original_url = ''
                        if 'original_url' in cItem:
                            original_url = cItem['original_url']
                        elif 'page' in cItem and cItem['page'] > 1:
                            for item in self.currList:
                                if item.get('type') == 'category' and item.get('page') == 1:
                                    original_url = item.get('url', '')
                                    break
                        if original_url and '/video/' in original_url:
                            match = re.search(r'/video/([^/]+)/', original_url)
                            if match: program_name = match.group(1)
                    if not program_name:
                        program_name = 'private-investigation'
                    if program_name:
                        program_name = re.sub(r'[^\w\-]', '', program_name)
                        next_url = (
                            "{}/graphql?wp-site=aja&"
                            "operationName=ArchipelagoEpisodesQuery&"
                            "variables=%7B%22category%22%3A%22{}%22%2C%"
                            "22quantity%22%3A16%2C%22offset%22%3A{}%7D&"
                            "extensions=%7B%7D"
                        ).format(self.MAIN_URL, program_name, next_offset)
                        params = {'import': cItem['import'],'category': 'host2','title': tscolor('\c00????30') + 'اعرض المزيد (16 فيديو)','url': next_url,'offset': next_offset,'mode': '21','icon': cItem.get('icon', ''),'desc': 'تحميل 16 فيديو إضافي','hst': 'tshost','page': cItem.get('page', 1) + 1}
                        if cItem.get('page', 1) >= 2:
                            for item in self.currList:
                                if item.get('type') == 'category' and item.get('page') == 1:
                                    params['original_url'] = item.get('url', '')
                                    break
                        self.addDir(params)
                elif added_count == 0 and not self.currList:
                    self.addMarker({'title': tscolor('\c00????30') + 'لا توجد فيديوهات متاحة','icon': cItem.get('icon', '')})
                elif added_count == 0:
                    self.addMarker({'title': 'تم عرض كل الفيديوهات المتاحة','desc': 'لا توجد فيديوهات إضافية للعرض','icon': cItem.get('icon', '')})
            except Exception as e:
                printDBG("Error parsing JSON: {}".format(str(e)))
                if not self.currList:
                    self.addMarker({'title': 'حدث خطأ في جلب البيانات','desc': 'تعذر تحميل قائمة الفيديوهات','icon': cItem.get('icon', '')})
                else:
                    self.addMarker({'title': 'تم عرض كل الفيديوهات المتاحة','desc': 'لا توجد فيديوهات إضافية للعرض','icon': cItem.get('icon', '')})
        else:
            self._extract_videos(data, cItem)
            program_name = ''
            if '/video/' in cItem['url']:
                match = re.search(r'/video/([^/]+)/', cItem['url'])
                if match:
                    program_name = match.group(1)
            if program_name:
                current_offset = cItem.get('offset', 0)
                next_offset = current_offset + 16
                next_url = (
                    "{}/graphql?wp-site=aja&"
                    "operationName=ArchipelagoEpisodesQuery&"
                    "variables=%7B%22category%22%3A%22{}%22%2C%"
                    "22quantity%22%3A16%2C%22offset%22%3A{}%7D&"
                    "extensions=%7B%7D"
                ).format(self.MAIN_URL, program_name, next_offset)
                self.addDir({'import': cItem['import'],'category': 'host2','title': tscolor('\c00????30') + 'اعرض المزيد (16 فيديو)','url': next_url,'offset': next_offset,'mode': '21','icon': cItem.get('icon', ''),'desc': 'تحميل 16 فيديو إضافي','hst': 'tshost','page': 2,'original_url': cItem['url'],'program_name': program_name})
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
                    if not all([title, url]): continue
                    clean_title = self._clean_title(title, cItem['title'])
                    final_desc = ph.clean_html(desc) if desc else ''
                    if duration: final_desc += "\n\nمدة الفيديو: {}".format(duration) if final_desc else "مدة الفيديو: {}".format(duration)
                    if sys.version_info[0] == 2:
                        if isinstance(clean_title, unicode): clean_title = clean_title.encode('utf-8', 'ignore')
                        if isinstance(final_desc, unicode): final_desc = final_desc.encode('utf-8', 'ignore')
                    self.addVideo({'import': cItem['import'],'hst': 'tshost','url': self.MAIN_URL + url,'title': clean_title,'desc': final_desc,'icon': self.std_url(self.MAIN_URL + image) if image else '','good_for_fav': True,'EPG': True})
            except Exception as e:
                printDBG("Error parsing JSON: {}".format(str(e)))
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
                title_bytes = title_match.group(1).strip()
                if sys.version_info[0] == 2:
                    title_str = title_bytes.decode('utf-8', 'ignore') if isinstance(title_bytes, str) else title_bytes
                else:
                    title_str = title_bytes.decode('utf-8', 'ignore') if isinstance(title_bytes, bytes) else title_bytes
                title = unescape(title_str)
                title = re.sub(r'^["\']+|["\']+$', '', title)
                title = re.sub(r'\s*["\']\s*', ' ', title)
                title = re.sub(r'\s+', ' ', title).strip()
                desc_match = re.search(r'(?:<div class="(?:gc__excerpt|article-card__excerpt)">.*?<p>(.*?)</p>|<div class="playlist-item-description">(.*?)</div>)', block, re.S)
                desc = desc_match.group(1) or desc_match.group(2) or '' if desc_match else ''
                duration_match = re.search(r'<span class="screen-reader-text">مدة الفيديو\s*(.*?)\s*</span>', block)
                duration = duration_match.group(1).strip() if duration_match and duration_match.group(1).strip() else ''
                clean_title = self._clean_title(title, cItem['title'])
                final_desc = ph.clean_html(desc) if desc else ''
                if duration:
                    final_desc += "\n\nمدة الفيديو: {}".format(duration) if final_desc else "مدة الفيديو: {}".format(duration)
                if sys.version_info[0] == 2:
                    if isinstance(clean_title, unicode): clean_title = clean_title.encode('utf-8', 'ignore')
                    if isinstance(final_desc, unicode): final_desc = final_desc.encode('utf-8', 'ignore')
                self.addVideo({'import': cItem['import'],'hst': 'tshost','url': self.MAIN_URL + url,'title': clean_title,'desc': final_desc,'icon': self.std_url(self.MAIN_URL + image.split("?")[0]),'good_for_fav': True,'EPG': True})
    def _clean_title(self, title, program_title):
        if sys.version_info[0] == 2:
            if isinstance(title, str):
                title = title.decode('utf-8', 'ignore')
            if isinstance(program_title, str):
                program_title = program_title.decode('utf-8', 'ignore')
        else:
            if isinstance(title, bytes):
                title = title.decode('utf-8', 'ignore')
            if isinstance(program_title, bytes):
                program_title = program_title.decode('utf-8', 'ignore')
        patterns_to_remove = [
            program_title + " - ",
            program_title + "-",
            program_title + ": ",
            program_title + " ــ ",
            program_title + " – ",
            program_title
        ]
        clean_title = title
        for pattern in patterns_to_remove: clean_title = clean_title.replace(pattern, "")
        clean_title = re.sub(r'["\']', '', clean_title)
        clean_title = re.sub(r'\s+', ' ', clean_title).strip()
        clean_title = re.sub(r'^\s*[-–—:]+\s*', '', clean_title).strip()
        return clean_title
    def get_links(self, cItem):
        urlTab = []
        sts, data = self.getPage(cItem['url'])
        if not sts: return urlTab
        embed = re.search(r'"embedUrl"\s*:\s*"([^"]+)"', data)
        if not embed: return urlTab
        embed_url = embed.group(1).replace('\\/', '/')
        m = re.search(r'players\.brightcove\.net/(\d+)/([^/]+)/', embed_url)
        if not m: return urlTab
        account_id, player_id = m.groups()
        vid = re.search(r'videoId=(\d+)', embed_url)
        if not vid: return urlTab
        video_id = vid.group(1)
        js_url = 'https://players.brightcove.net/{}/{}/index.min.js'.format(account_id, player_id)
        sts, js = self.getPage(js_url)
        if not sts: return urlTab
        pk = re.search(r'policyKey\s*:\s*"([^"]+)"', js)
        if not pk: return urlTab
        policy_key = pk.group(1)
        api_url = 'https://edge.api.brightcove.com/playback/v1/accounts/{}/videos/{}'.format(account_id, video_id)
        headers = {
            'Accept': 'application/json;pk={}'.format(policy_key),
            'Origin': 'https://players.brightcove.net',
            'User-Agent': self.USER_AGENT
        }
        sts, json_data = self.getPage(api_url, {'header': headers})
        if not sts: return urlTab
        try:
            video = json.loads(json_data)
            sources = video.get('sources', [])
            seen_urls = set()
            mp4_list = []
            hls_urls = []
            for s in sources:
                src = s.get('src') or s.get('src_alt')
                if not src: continue
                skip_keywords = ['preview', 'image', 'thumbnail', '.jpg', '.png', '.webvtt', '.mpd', 'dash']
                should_skip = False
                for keyword in skip_keywords:
                    if keyword in src.lower():
                        should_skip = True
                        break
                if should_skip: continue
                url_base = src.split('?')[0] if '?' in src else src
                url_key = url_base.replace('https://', '').replace('http://', '').strip('/')
                if url_key in seen_urls: continue
                seen_urls.add(url_key)
                container = (s.get('container') or '').lower()
                mime = (s.get('type') or '').lower()
                height = s.get('height')
                bitrate = s.get('avg_bitrate', 0)
                is_mp4 = (
                    container == 'mp4' or 
                    'video/mp4' in mime or
                    ('codec' in s and s['codec'] == 'H264')
                )
                if is_mp4:
                    quality = height or 0
                    if quality >= 1080: quality_prefix = ' HD 1080p '
                    elif quality >= 720: quality_prefix = ' HD 720p '
                    elif quality >= 480: quality_prefix = ' SD 480p '
                    elif quality >= 360: quality_prefix = ' SD 360p '
                    else: quality_prefix = ' MP4 '
                    if bitrate:
                        bitrate_mbps = bitrate / 1000000.0
                        quality_label = '{} ({:.1f} Mbps)'.format(quality_prefix, bitrate_mbps)
                    else: quality_label = quality_prefix
                    if src.startswith('http:'): final_src = src.replace('http:', 'https:', 1)
                    else: final_src = src
                    mp4_list.append((quality, final_src, quality_label))
                elif 'm3u8' in src or 'application/x-mpegurl' in mime:
                    if src.startswith('http:'): final_src = src.replace('http:', 'https:', 1)
                    else:
                        final_src = src
                    hls_urls.append(final_src)
            def add_link(name, url):
                return {'name': name,'url': strwithmeta(url, {'Referer': embed_url}),'need_resolve': 0}
            mp4_list.sort(reverse=True)
            for _, src, label in mp4_list: urlTab.append(add_link('Aljazeera [{}]'.format(label), src))
            hls_streams = {}
            for hls_url in hls_urls[:1]:
                try:
                    sts, hls_data = self.getPage(hls_url)
                    if sts:
                        lines = hls_data.split('\n')
                        for i, line in enumerate(lines):
                            line = line.strip()
                            if line.startswith('#EXT-X-STREAM-INF:'):
                                resolution = None
                                bandwidth = None
                                height_val = None
                                res_match = re.search(r'RESOLUTION=(\d+x\d+)', line)
                                if res_match:
                                    resolution = res_match.group(1)
                                    try: height_val = int(resolution.split('x')[1])
                                    except: height_val = None
                                bw_match = re.search(r'BANDWIDTH=(\d+)', line)
                                if bw_match: bandwidth = int(bw_match.group(1))
                                if i + 1 < len(lines):
                                    stream_url = lines[i + 1].strip()
                                    if stream_url and not stream_url.startswith('#'):
                                        if not stream_url.startswith('http'):
                                            if '://' in hls_url:
                                                base_url = '/'.join(hls_url.split('/')[:-1])
                                                stream_url = base_url + '/' + stream_url
                                        if resolution:
                                            if height_val:
                                                if height_val >= 1080: label = ' HLS 1920x1080 '
                                                elif height_val >= 720: label = ' HLS 1280x720 '
                                                elif height_val >= 540: label = ' HLS 960x540 '
                                                elif height_val >= 480: label = ' HLS 854x480 '
                                                elif height_val >= 360: label = ' HLS 640x360 '
                                                elif height_val >= 270: label = ' HLS 480x270 '
                                                else: label = ' HLS {} '.format(resolution)
                                            else: label = ' HLS {} '.format(resolution)
                                        elif bandwidth:
                                            bandwidth_mbps = bandwidth / 1000000.0
                                            label = ' HLS ({:.1f} Mbps) '.format(bandwidth_mbps)
                                        else: label = ' HLS '
                                        stream_key = label
                                        if stream_key not in hls_streams: hls_streams[stream_key] = stream_url
                except Exception as e:
                    printDBG('[aljazeera] HLS parsing error: {}'.format(str(e)))
            if hls_streams:
                sorted_streams = []
                for label, url in hls_streams.items():
                    height_match = re.search(r'(\d+)x(\d+)', label)
                    if height_match:
                        height = int(height_match.group(2))
                        sorted_streams.append((height, label, url))
                    else: sorted_streams.append((0, label, url))
                sorted_streams.sort(reverse=True)
                for _, label, url in sorted_streams:
                    urlTab.append(add_link('Aljazeera [{}]'.format(label), url))
            elif hls_urls: urlTab.append(add_link('Aljazeera [HLS]', hls_urls[0]))
        except Exception as e:
            printDBG('[aljazeera] get_links error: {}'.format(str(e)))
        if not urlTab and 'sources' in locals().get('video', {}):
            for s in video['sources']:
                src = s.get('src') or s.get('src_alt')
                if src and ('mp4' in src or 'm3u8' in src):
                    if src.startswith('http:'): src = src.replace('http:', 'https:', 1)
                    urlTab.append({'name': 'Aljazeera [Default]','url': strwithmeta(src, {'Referer': embed_url}),'need_resolve': 0})
                    break
        return urlTab
    def download_file(self, url, filepath):
        try:
            import requests
            r = requests.get(url, headers={'User-Agent': self.USER_AGENT})
            if r.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(r.content)
                return True
            return False
        except Exception as e:
            printDBG("[aljazeera] download_file error: {}".format(e))
            return False
    def getArticle(self,cItem):
        Desc = [('Story','class="article-excerpt">(.*?)</','\n','')]
        desc = self.add_menu(cItem,'','article-header">(.*?)article-content-read-more','','desc',Desc=Desc)
        if desc =='': desc = cItem.get('desc','')
        return [{'title':cItem['title'], 'text': desc, 'images':[{'title':'', 'url':cItem.get('icon','')}], 'other_info':{}}]