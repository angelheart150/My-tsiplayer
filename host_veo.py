# -*- coding: utf8 -*-
from __future__ import print_function
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass, tscolor, tshost, T
from Plugins.Extensions.IPTVPlayer.tools.iptvtypes import strwithmeta
import re
import json
from Plugins.Extensions.IPTVPlayer.components.e2ivkselector import GetVirtualKeyboard
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin
def getinfo():
    info_ = {
        'name': 'VEO',
        'host': tshost('VEO') or 'https://veo.buzz',
        'version': '1.0 13/08/2025',
        'dev': 'Angel_heart',
        'cat_id': '21',
        'desc': 'قنوات رياضة وأفلام و ومسلسلات',
        'icon': 'https://i.ibb.co/MxgXvG78/veo.png',
        'recherche_all': '0'
    }
    return info_
class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self)
        self.MAIN_URL = getinfo()['host']
        self.HEADERS = {
            'Referer': 'https://veo.buzz/',
            'Origin': 'https://veo.buzz',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
        }
        self.ALL_SECTIONS = [11, 12, 15, 17, 18, 19]  # For searchChannels
    def showmenu(self, cItem):
        menu_items = [
            {'url': '/showCategory/18', 'title': 'Sport'},
            {'url': '/showCategory/15', 'title': 'News'},
            {'url': '/showCategory/11', 'title': 'Movies'},
            {'url': '/showCategory/19', 'title': 'Entertainment'},
            {'url': '/showCategory/17', 'title': 'Islamic'},
            {'url': '/showCategory/12', 'title': 'Series'},
            {'title': 'schedules', 'mode': 'schedules'},
            {'title': T('Search'), 'icon': 'https://i.ibb.co/HfPQ0BL0/search.png', 'mode': '50'}
        ]
        for item in menu_items:
            item.update({
                'import': cItem['import'],
                'category': 'host2',
                'icon': item.get('icon', 'https://i.ibb.co/MxgXvG78/veo.png'),
                'desc': '',
                'mode': item.get('mode', '10')
            })
            self.addDir(item)
    def showmenu1(self, cItem):
        URL = cItem.get('url', '')
        match = re.search(r'/showCategory/(\d+)', URL)
        if not match:
            return
        group_id = match.group(1)
        api_url = f"https://api.veo.buzz/api/channels?id_groups={group_id}"
        sts, data = self.getPage(api_url)
        if not sts:
            return
        try:
            json_data = json.loads(data)
            if json_data.get('api_status') != 1:
                return
            channels = json_data.get('data', [])
            channels.reverse()
            count_channels = len(channels)
            desc_colored = tscolor('\c00????FF') + str(count_channels) + tscolor('\c00????30') + ' : عدد قنوات هذا القسم'
            for ch in channels:
                title = ch.get('logo_name') or ch.get('name_ar') or ch.get('name_en')
                icon = ch.get('mobile_logo') or ch.get('logo', '')
                cItemLinks = {'link': ch.get("link", ''),'link2': ch.get("link2", ''),'link3': ch.get("link3", ''),'link4': ch.get("link4", '')}
                default_url = cItemLinks.get('link2') or cItemLinks.get('link') or cItemLinks.get('link3') or cItemLinks.get('link4')
                if default_url:
                    default_url = strwithmeta(default_url, self.HEADERS)
                    self.addVideo({'import': cItem['import'],'category': 'video','title': title.strip(),'icon': icon,'url': default_url,'need_resolve': 0,'custom_links': cItemLinks,'hst': 'direct','type': 'video','desc': desc_colored})
        except Exception as e:
            printDBG(f"Error parsing API: {e}")
    def getLinksForVideo(self, cItem):
        printDBG("VEO.getLinksForVideo")
        url_list = []
        links = cItem.get('custom_links', {})
        headers = {
            'Referer': 'https://veo.buzz/',
            'Origin': 'https://veo.buzz',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
        }
        for key, quality_name in [('link2', '720p'), ('link', '360p'), ('link3', 'adaptive'), ('link4', 'other')]:
            stream_url = links.get(key, '')
            if stream_url:
                stream_url = strwithmeta(stream_url, headers)
                url_list.append({'name': quality_name, 'url': stream_url, 'need_resolve': 0})
        return url_list
    def playVideo(self, cItem):
        url = cItem.get('url', '')
        if url:
            self.setResolvedUrl(url)  
    def searchChannels(self, str_ch='', cItem=None):
        if str_ch == '':
            ret = self.sessionEx.waitForFinishOpen(GetVirtualKeyboard(), title=('اسم القناة:'), text='')
            if not ret: 
                return []
            str_ch = ret[0]
        all_sections = [11, 12, 15, 17, 18, 19]
        headers = {
            'Referer': 'https://veo.buzz/',
            'Origin': 'https://veo.buzz',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
        }
        results = []
        for section_id in all_sections:
            api_url = "https://api.veo.buzz/api/channels?id_groups={}".format(section_id)
            sts, data = self.getPage(api_url)
            if not sts:
                continue
            try:
                json_data = json.loads(data)
                if json_data.get('api_status') != 1:
                    continue
                channels = json_data.get('data', [])
                for ch in channels:
                    title = ch.get('logo_name') or ch.get('name_ar') or ch.get('name_en')
                    if str_ch.lower() not in title.lower():
                        continue
                    icon = ch.get('mobile_logo') or ch.get('logo', '')
                    cItemLinks = {'link': ch.get("link", ''),'link2': ch.get("link2", ''),'link3': ch.get("link3", ''),'link4': ch.get("link4", ''),}
                    for key in ['link2','link','link3','link4']:
                        if cItemLinks.get(key):
                            default_url = strwithmeta(cItemLinks[key], headers)
                            results.append({'import': cItem['import'] if cItem else '','category': 'video','title': title.strip(),'icon': icon,'url': default_url,'need_resolve': 0,'custom_links': cItemLinks,'hst': 'direct','type': 'video'})
                            break
            except Exception as e:
                printDBG("Error parsing API in searchChannels: {}".format(e))
                
        for item in results:
            self.addVideo(item)
        return results
    def showsearch(self, cItem):
        try:
            ret = self.sessionEx.waitForFinishOpen(GetVirtualKeyboard(), title='اسم القناة:', text='')
            if not ret or not ret[0] or not ret[0].strip():
                return []
            str_ch = ret[0].strip()
            return self.searchChannels(str_ch, cItem)
        except Exception as e:
            printDBG("Error in showsearch: {}".format(e))
            return []
    def showSchedules(self, cItem):
        api_url = "https://api.veo.buzz/api/schedules?id_groups=0&id_channels=0"
        sts, data = self.getPage(api_url)
        if not sts:
            return
        try:
            json_data = json.loads(data)
            if json_data.get('api_status') != 1:
                return
            schedules = json_data.get('data', [])
            headers = {
                'Referer': 'https://veo.buzz/',
                'Origin': 'https://veo.buzz',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
            }
            for item in schedules:
                ch_name = item.get('channels_logo_name') or item.get('channels_name_ar') or item.get('channels_name_en')
                program = item.get('program_name', '')
                prog_time = item.get('program_time', '')
                title = "{} - {} ({})".format(ch_name, program, prog_time)
                icon = item.get('channels_mobile_logo') or item.get('channels_logo', '')

                cItemLinks = {'link': item.get("channels_link", ''),'link2': item.get("channels_link2", ''),'link3': item.get("channels_link3", ''),'link4': item.get("channels_link4", ''),}
                default_url = cItemLinks.get('link2') or cItemLinks.get('link') or cItemLinks.get('link3') or cItemLinks.get('link4')
                if default_url:
                    default_url = strwithmeta(default_url, headers)
                    self.addVideo({'import': cItem['import'],'category': 'video','title': title.strip(),'icon': icon,'url': default_url,'need_resolve': 0,'custom_links': cItemLinks,'hst': 'direct','type': 'video'})
        except Exception as e:
            printDBG("Error parsing schedules: {}".format(e))
    def start(self,cItem):
        mode=cItem.get('mode', None)
        if mode=='00':
            self.showmenu(cItem)
        elif mode=='10':
            self.showmenu1(cItem)	
        elif mode=='11':
            self.showmenu2(cItem)
        elif mode=='19':
            self.showfilter(cItem)                    
        elif mode=='20':
            self.showitms(cItem)
        elif mode=='21':
            self.showelms(cItem)		
        elif mode=='50':
            self.showsearch(cItem)
        elif mode=='51':
            self.searchResult(cItem)
        elif mode == 'schedules':
            self.showSchedules(cItem)
        return True