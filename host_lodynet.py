# -*- coding: utf8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor,tshost,T
import base64,urllib,re,time,os,requests,hashlib,subprocess,threading,json,sys
from PIL import Image
from io import BytesIO
try:
    from urllib.parse import quote_plus  # Python 3
except ImportError:
    from urllib import quote_plus        # Python 2
#################################################
def getinfo():
    info_={}
    name='Lodynet'
    hst = 'https://lodynet.watch'
    info_['old_host'] = hst
    hst_ = tshost(name)
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='5.0 25/10/2025'
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
        TAB = [('مسلسلات','','10',0),('أفلام','','10',1),('برامج و حفلات','/category/البرامج-و-حفلات-tv/','20',''),('أغاني','','10',2),
        # ('الممثلين','/الممثلين/','20',''),
        ('المضاف حديثاً','/','20','newly'),]
        self.add_menu(cItem,'','','','','',TAB=TAB,search=False)
        self.addDir({'import':cItem['import'],'category' :'host2','title':T('Search')  ,'icon':'https://i.ibb.co/dQg0hSG/search.png','mode':'50'})
    def showmenu1(self,cItem):
        gnr = cItem.get('sub_mode','')
        if gnr == 0 : 
            TAB = [
                ('مسلسلات هندية','/category/مسلسلات-هندية-مترجمة/','20',''),
                ('مسلسلات هندية مدبلجة','/dubbed-indian-series-p5/','20',''),
                ('مسلسلات ويب هندية','/category/مسلسل-ويب-هندية/','20',''),
                ('مسلسلات هندية 2020','/release-year/مسلسلات-هندية-2020-a/','20',''),
                ('مسلسلات هندية 2019','/release-year/مسلسلات-هندية-2019/','20',''),
                ('مسلسلات هندية 2018','/release-year/مسلسلات-هندية-2018/','20',''),
                ('مسلسلات تركية','/category/مسلسلات-تركي/','20',''),
                ('مسلسلات تركية مدبلجة','/dubbed-turkish-series-g/','20',''),
                ('مسلسلات كورية','/korean-series-b/','20',''),
                ('مسلسلات صينية','/category/مسلسلات-صينية-مترجمة/','20',''),
                ('مسلسلات تايلاندية','/مشاهدة-مسلسلات-تايلندية/','20',''),
                ('مسلسلات باكستانية','/category/المسلسلات-باكستانية/','20',''),
                ('مسلسلات آسيوية حديثة','/tag/new-asia/','20',''),
                ('مسلسلات مكسيكية','/category/مسلسلات-مكسيكية-a/','20',''),
                ('مسلسلات أجنبية','/category/مسلسلات-اجنبية/','20',''),
            ]
        elif gnr == 1:
            TAB = [
                ('افلام هندية', '/category/افلام-هندية/', '20', ''),
                ('أفلام هندية مدبلجة', '/category/أفلام-هندية-مدبلجة/', '20', ''),
                ('افلام هندية جنوبية', '/tag/الافلام-الهندية-الجنوبية/', '20', ''),
                ('أفلام هندي 2025', '/release-year/أفلام-هندي-2025/', '20', ''),
                ('أفلام هندي 2024', '/release-year/أفلام-هندي-2024/', '20', ''),
                ('أفلام هندي 2023', '/release-year/أفلام-هندية-2023/', '20', ''),
                ('أفلام هندي 2021', '/release-year/movies-hindi-2021/', '20', ''),
                ('أفلام هندي 2020', '/release-year/افلام-هندي-2020-a/', '20', ''),
                ('افلام هندي 2019', '/release-year/افلام-هندي-2019/', '20', ''),
                ('افلام هندي 2018', '/release-year/افلام-هندي-2018/', '20', ''),
                ('افلام هندي 2017', '/release-year/افلام-هندي-2017/', '20', ''),
                ('افلام هندي 2016', '/release-year/2016/', '20', ''),
                ('افلام هندية 4K', '/tag/افلام-هندية-مترجمة-بجودة-4k/', '20', ''),
                ('أميتاب باتشان', '/actor/أميتاب-باتشان/', '20', ''),
                ('اعمال شاروخان', '/actor/شاه-روخ-خان-a/', '20', ''),
                ('أعمال سلمان خان', '/actor/سلمان-خان-a/', '20', ''),
                ('أعمال عامر خان', '/actor/عامر-خان-a/', '20', ''),
                ('أعمال شاهد كابور', '/actor/شاهيد-كابور/', '20', ''),
                ('أعمال رانبير كابور', '/actor/رانبير-كابور/', '20', ''),
                ('أعمال ديبيكا بادكون', '/actor/ديبيكا-بادكون/', '20', ''),
                ('أعمال جينيفر ونجت', '/actor/جينيفر-ونجت/', '20', ''),
                ('أعمال هريتيك روشان', '/actor/هريتيك-روشان/', '20', ''),
                ('أعمال اكشاي كومار', '/actor/اكشاي-كومار/', '20', ''),
                ('أعمال تابسي بانو', '/actor/تابسي-بانو/', '20', ''),
                ('أعمال سانجاي دوت', '/actor/سانجاي-دوت-a/', '20', ''),
                ('ترجمات احمد بشير', '/tag/جميع-الأفلام-في-هذا-القسم-من-ترجمة-أحمد/', '20', ''),
                ('افلام تركية مترجم', '/category/افلام-تركية-مترجم/', '20', ''),
                ('افلام باكستانية', '/tag/افلام-باكستانية-مترجمة/', '20', ''),
                ('افلام اسيوية', '/category/افلام-اسيوية-a/', '20', ''),
                ('افلام اجنبي', '/category/افلام-اجنبية-مترجمة-a/', '20', ''),
                ('انيمي', '/category/انيمي/', '20', ''),
            ]
        elif gnr == 2:
            TAB = [
                ('أغاني المسلسلات', '/category/اغاني/اغاني-المسلسلات-الهندية/','20',''),
                ('تصاميم مسلسلات هندية', '/category/تصاميم-مسلسلات-هندية/','20',''),
                ('أغاني الأفلام','/category/اغاني-الافلام/','20',''),
                ('اغاني هندية mp3', '/category/اغاني/اغاني-هندية-mp3/','20',''),
            ]
        self.add_menu(cItem,'','','','','',TAB=TAB)
    def showsearch(self,cItem):
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'البحث في الموقع','icon':'https://i.ibb.co/2nztSQz/all.png','mode':'51','section':''})
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'البحث عن فيلم','icon':'https://i.ibb.co/k56BbCm/aflam.png','mode':'51','section':'فيلم'})
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'البحث عن مسلسل','icon':'https://i.ibb.co/3M38qkV/mousalsalat.png','mode':'51','section':'مسلسل'})
    def extract_series_episodes(self, url):
        episodes = []
        sts, data = self.getPage(url)
        if not sts or not data:
            return episodes
        block = re.search(r'<div id="ListEpisodes".*?>(.*?)</div>\s*</div>', data, re.S)
        if not block:
            return episodes
        links = re.findall(r'<a[^>]+href="([^"]+)"[^>]*>([^<]+)</a>', block.group(1))
        for ep_url, ep_title in links:
            ep_url = self.std_url(ep_url)
            title = ep_title.strip()
            if not title:
                continue
            episodes.append({'title': title,'url': ep_url,'category': 'video','mode': '21','good_for_fav': True,'hst': 'tshost'})
        return episodes
    def SearchAll(self, str_ch, page, extra, section=None, type_=''):
        if section and section.strip() != '':
            str_ch = section + " " + str_ch
        printDBG("SearchAll: كلمة البحث [%s], صفحة [%s], القسم [%s]" % (str_ch, page, section))
        url = "https://lodynet.watch/wp-content/themes/Lodynet2020/Api/RequestSearch.php?value=%s" % quote_plus(str_ch)
        sts, data = self.getPage(url)
        results = []
        if not sts or not data:
            return results
        try:
            js = json.loads(data)
            if isinstance(js, list) and len(js) > 1:
                for item in js[1]:
                    title = item.get("Title", "").strip()
                    link = item.get("Url", "").replace("\\/", "/")
                    cover = item.get("Cover", "").replace("\\/", "/")
                    cat = item.get("Category", "").strip()
                    if not link.startswith("http"):
                        link = self.MAIN_URL.rstrip('/') + '/' + link.lstrip('/')
                    params = {'title': title,'url': link,'icon': cover,'desc': cat,'section': section,'category': 'host2','hst': 'tshost','import': 'from Plugins.Extensions.IPTVPlayer.tsiplayer.host_lodynet import ',}
                    if '/actor/' in link or 'ممثل' in cat or 'نجم' in cat:
                        params.update({'mode': '20','type_': 'actor','sub_mode': 'actor','desc': 'ممثل هندي'})
                        results.append(params)
                        continue
                    if 'مسلسل' in title or 'series' in link:
                        episodes = self.extract_series_episodes(link)
                        if episodes:
                            folder = {'title': tscolor('\c0090??00') + title,'category': 'host2','url': link,'icon': cover,'desc': 'حلقات المسلسل','mode': '20','sub_mode': 'episodes','good_for_fav': True,'hst': 'tshost','import': 'from Plugins.Extensions.IPTVPlayer.tsiplayer.host_lodynet import ','episodes': episodes}
                            results.append(folder)
                            continue
                    params.update({'mode': '20', 'type_': 'video'})
                    results.append(params)
        except Exception as e:
            printDBG("SearchAll exception: %s" % str(e))
        return results
    def SearchMovies(self, str_ch, page=1, extra=''):
        return self.SearchAll(str_ch, page, extra=extra, type_='فيلم')
    def SearchSeries(self, str_ch, page=1, extra=''):
        return self.SearchAll(str_ch, page, extra=extra, type_='مسلسل')
    def get_items(self, cItem={}):
        elms = []
        extra = cItem.get('import')
        str_ch = cItem.get('str_ch')
        page = cItem.get('page', 1)
        url_ = cItem.get('url', '')
        type_ = cItem.get('type_', '')
        if not url_:
            return elms
        url0 = url_.strip('/')
        if not url0.startswith('http'):
            if url0.startswith(('tag/', 'release-year/', 'actor/', 'category/', 'مشاهدة-')):
                url0 = self.MAIN_URL + '/' + url0
            else:
                url0 = self.MAIN_URL + '/category/' + url0
        if page > 1:
            url0 = url0 + '/page/' + str(page)
        sts, data = self.getPage(url0)
        if not sts or not data:
            return elms
        items = re.findall(
            r'<div class="ItemNewly">\s*<a title="([^"]+)" href="([^"]+)".*?data-src="([^"]+)".*?(?:<div class="NewlyRibbon">([^<]*)</div>).*?(?:<div class="NewlyTimeAgo">([^<]*)</div>)',
            data, re.S)
        for title, url, img, ribbon, timeago in items:
            url = self.std_url(url)
            img = self.fix_image_url(self.std_url(img))
            desc = ""
            if ribbon.strip():
                desc += tscolor('\c00??????') + ribbon.strip() + '\n'
            if timeago.strip():
                desc += tscolor('\c0090??00') + timeago.strip()
            elms.append({'import': cItem['import'],'category': 'host2','title': title.strip(),'url': url,'desc': desc,'icon': img,'mode': '21','good_for_fav': True,'sub_mode': '1','EPG': True,'hst': 'tshost'})
        if 'الصفحة التالية' in data or 'class="next"' in data:
            elms.append({'import': extra,'category': 'host2','title': T('Next'),'url': url_,'desc': 'Next','icon': '','hst': 'tshost','mode': '20','page': page + 1,'str_ch': str_ch,'type_': type_})
        return elms
    def fix_image_url(self, url):
        DEFAULT_IMAGE = 'https://lodynet.watch/wp-content/uploads/2015/12/logo-1.png'
        if not url or not isinstance(url, str) or url.strip() == '':
            return DEFAULT_IMAGE
        cache_folder = '/etc/IPTVCache/webp/'
        if not os.path.exists(cache_folder): os.makedirs(cache_folder)
        try:
            file_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
        except Exception as e:
            print("خطأ في إنشاء hash للصورة:", e)
            return DEFAULT_IMAGE
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
        page = cItem.get('page', 1)
        sub_mode = cItem.get('sub_mode', '')
        sts, data = self.getPage(url)
        if not sts:
            return
        items_added = 0
        item_blocks = re.findall(r'(<div class="ItemNewly">.*?</div>\s*</a>\s*</div>)', data, re.S)
        if item_blocks:
            for item_block in item_blocks:
                title_match = re.search(r'<a title="([^"]+)"', item_block)
                url_match = re.search(r'href="([^"]+)"', item_block)
                img_match = re.search(r'data-src="([^"]+)"', item_block)
                new_title_match = re.search(r'<div class="NewlyTitle">([^<]+)</div>', item_block)
                if not all([title_match, url_match, img_match]):
                    continue
                title = title_match.group(1)
                item_url = url_match.group(1)
                img = img_match.group(1)
                new_title = new_title_match.group(1) if new_title_match else ''
                if any(x in str(value) for value in [title, item_url, img] for x in ["+ CategoryItem.", "CategoryItem."]):
                    printDBG("تخطي عنصر غير صالح: " + title)
                    continue
                icon = self.fix_image_url(self.std_url(img))
                content_type = self.determine_content_type(title, url)
                desc = self.extract_desc_from_newly(item_block)
                if content_type == 'series':
                    self.addDir({'import': cItem.get('import'),'category': 'host2','title': title.strip(),'url': item_url,'icon': icon,'desc': desc,'good_for_fav': True,'hst': 'tshost','mode': '21'})
                else:
                    self.addVideo({'import': cItem.get('import'),'title': title.strip(),'url': item_url,'icon': icon,'desc': desc,'good_for_fav': True,'hst': 'tshost'})
                items_added += 1
        more_match = False
        pick_up_order = ''
        pick_up_id = ''
        more_match1 = re.search(r'onclick="[^"]*GetMoreCategory\(\'([^\']+)\',\s*\'([^\']+)\'\)"', data)
        if more_match1:
            pick_up_order = more_match1.group(1)
            pick_up_id = more_match1.group(2)
            more_match = True
            printDBG(f"تم اكتشاف زر تحميل المزيد - النمط 1: order={pick_up_order}, id={pick_up_id}")
        if not more_match:
            more_match2 = re.search(r'onclick="[^"]*GetMoreCategory\(\'([^\']+)\',\s*\'([^\']+)\'\)[^"]*"', data)
            if more_match2:
                pick_up_order = more_match2.group(1)
                pick_up_id = more_match2.group(2)
                more_match = True
                printDBG(f"تم اكتشاف زر تحميل المزيد - النمط 2: order={pick_up_order}, id={pick_up_id}")
        if more_match and pick_up_order and pick_up_id:
            parent_id = ''
            parent_match1 = re.search(r"DataPosting\.append\('parent',\s*'(\d+)'\)", data)
            if parent_match1:
                parent_id = parent_match1.group(1)
                printDBG(f"تم اكتشاف parent_id - النمط 1: {parent_id}")
            if not parent_id:
                parent_match2 = re.search(r"append\('parent',\s*'(\d+)'\)", data)
                if parent_match2:
                    parent_id = parent_match2.group(1)
                    printDBG(f"تم اكتشاف parent_id - النمط 2: {parent_id}")
            type_match = re.search(r"DataPosting\.append\('type',\s*'([^']+)'\)", data)
            taxonomy_match = re.search(r"DataPosting\.append\('taxonomy',\s*'([^']+)'\)", data)
            data_type = type_match.group(1) if type_match else 'Category'
            taxonomy = taxonomy_match.group(1) if taxonomy_match else 'category'
            if parent_id:
                self.addDir({'import': cItem.get('import'),'category': 'host2','title': tscolor('\c00????20') + 'تحميل المزيد','url': url,'icon': '','desc': '','good_for_fav': False,'hst': 'tshost','mode': '22','pick_up_order': pick_up_order,'pick_up_id': pick_up_id,'parent_id': parent_id,'data_type': data_type,'taxonomy': taxonomy})
                printDBG(f"تم إضافة زر تحميل المزيد: order={pick_up_order}, id={pick_up_id}, parent={parent_id}")
            else:
                printDBG("لم يتم العثور على parent_id، لا يمكن إضافة زر تحميل المزيد")
        else:
            printDBG("لم يتم العثور على زر تحميل المزيد في الصفحة")
            next_match = re.search(r'class="next page-numbers".*?href="([^"]+)"', data)
            if next_match:
                next_url = next_match.group(1)
                if not next_url.startswith('http'):
                    next_url = self.MAIN_URL + '/' + next_url.lstrip('/')
                self.addDir({'import': cItem.get('import'),'category': 'host2','title': tscolor('\c00????20') + 'الصفحة التالية','url': next_url,'desc': '','icon': '','hst': 'tshost','mode': '20'})
            elif sub_mode == 'newly' and items_added > 0:
                is_newly_section = (url == self.MAIN_URL + '/' or 
                                   url.startswith(self.MAIN_URL + '/page/'))
                if is_newly_section:
                    next_page = page + 1
                    next_url = self.MAIN_URL + '/page/' + str(next_page) + '/'
                    self.addDir({'import': cItem.get('import'),'category': 'host2', 'title': tscolor('\c00????20') + 'Page (' + str(next_page) + ')','url': next_url,'icon': '','desc': tscolor('\c00????20') + 'الانتقال إلى الصفحة ' + str(next_page),'good_for_fav': False,'hst': 'tshost','mode': '20','page': next_page,'sub_mode': 'newly'})
    def determine_content_type(self, title, url=''):
        title_lower = title.lower()
        url_lower = url.lower() if url else ''
        episode_keywords = [
            'حلقة', 'الحلقة', 'episode', 'الحلقة الأخيرة', 'حلقة جديدة',
        ]
        series_keywords = [
            'مسلسل', 'المسلسل', 'series', 'مسلسلات', 'المسلسلات',
            'season', 'موسم', 'الموسم', 'سلسلة', 'برنامج'
        ]
        movie_keywords = [
            'فيلم', 'الفيلم', 'movie', 'film', 'أفلام', 'الأفلام', 
            'أغنية', 'اغنية', 'أغاني', 'اغاني',
            'كليب', 'تصميم', 'تصاميم', 'مقطع', 'مقاطع'
        ]
        if any(keyword in url_lower for keyword in ['/اغاني/', '/أغاني/', '/music/', '/songs/', '/تصاميم-', '/design/']):
            return 'movie'
        if any(keyword in title_lower for keyword in ['أغنية', 'اغنية', 'أغاني', 'اغاني', 'music', 'كليب', 'كلب', 'تصميم', 'تصاميم']):
            return 'movie'
        for keyword in episode_keywords:
            if keyword in title_lower:
                return 'episode'
        for keyword in series_keywords:
            if keyword in title_lower:
                return 'series'
        for keyword in movie_keywords:
            if keyword in title_lower:
                return 'movie'
        if re.search(r'(season|موسم|s)\s*\d+', title_lower):
            return 'series'
        if any(keyword in url_lower for keyword in ['/series/', '/مسلسلات/', '/مسلسل/', '/seasons/']):
            return 'series'
        if any(keyword in url_lower for keyword in ['/movies/', '/أفلام/', '/فيلم/', '/film/']):
            return 'movie'
        if '/category/مسلسلات-اجنبية' in url_lower or '/series' in url_lower:
            return 'series'
        if '/أفلام' in url_lower or '/movies' in url_lower:
            return 'movie'
        return 'movie'
    def extract_desc_from_newly(self, html_block):
        desc_parts = []
        type_match = re.search(r'NewlyRibbon">([^<]+)</div>', html_block)
        if type_match:
            desc_parts.append(tscolor('\c00????00') + 'النوع: ' + tscolor('\c00????FF') + type_match.group(1))
        time_match = re.search(r'NewlyTimeAgo">([^<]+)</div>', html_block)
        if time_match:
            desc_parts.append(tscolor('\c00????00') + 'وقت النشر: ' + tscolor('\c00????FF') + time_match.group(1))
        episode_match = re.search(r'NewlyEpNumber[^>]*>.*?(\d+)</div>', html_block)
        if episode_match:
            desc_parts.append(tscolor('\c00????00') + 'الحلقة: ' + tscolor('\c00????FF') + episode_match.group(1))
        return '\n'.join(desc_parts) if desc_parts else tscolor('\c00????00') + 'محتوى مضاف حديثاً'
    def load_more(self, cItem):
        pick_up_order = cItem.get('pick_up_order', 'category')
        pick_up_id = cItem.get('pick_up_id')
        parent_id = cItem.get('parent_id')
        data_type = cItem.get('data_type', 'Category')
        taxonomy = cItem.get('taxonomy', 'category')
        is_episodes = cItem.get('is_episodes', False)
        if not pick_up_id or not parent_id:
            self.addDir({'import': cItem.get('import'),'category': 'host2','title': tscolor('\c00????20') + 'لا يمكن تحميل المزيد','url': '','icon': '','desc': '','good_for_fav': False,'hst': 'tshost','mode': ''})
            return
        API_URL = self.MAIN_URL + "/wp-content/themes/Lodynet2020/Api/RequestMoreCategory.php"
        try:
            post_data = urllib.parse.urlencode({"order": pick_up_order,"parent": parent_id,"type": data_type,"taxonomy": taxonomy,"id": pick_up_id}).encode('utf-8')
            printDBG(f"طلب تحميل المزيد: order={pick_up_order}, parent={parent_id}, type={data_type}, taxonomy={taxonomy}, id={pick_up_id}")
            headers = {"User-Agent": "Mozilla/5.0","X-Requested-With": "XMLHttpRequest","Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            }
            req = urllib.request.Request(API_URL, data=post_data, headers=headers)
            response = urllib.request.urlopen(req, timeout=30)
            response_text = response.read().decode('utf-8')
            if response_text:
                try:
                    items = json.loads(response_text)
                    if isinstance(items, list) and items:
                        valid_items = []
                        for item in items:
                            if not isinstance(item, dict):
                                continue
                            if 'name' not in item or 'url' not in item:
                                continue
                            valid_items.append(item)
                        for item in valid_items:
                            title = item.get("name", "")
                            url_path = item.get("url", "")
                            image = item.get("cover", "")
                            ribbon = item.get("ribbon", "")
                            ago = item.get("ago", "")
                            episode = item.get("episode", "")
                            item_id = item.get("ID", "")
                            if url_path and not url_path.startswith('http'):
                                if url_path.startswith('/'):
                                    url = self.MAIN_URL + url_path
                                else:
                                    url = self.MAIN_URL + '/' + url_path
                            else:
                                url = url_path
                            icon = self.fix_image_url(self.std_url(image)) if image else ''
                            desc_parts = []
                            if ribbon: 
                                desc_parts.append(tscolor('\c00????00') + 'النوع: ' + tscolor('\c00????FF') + ribbon)
                            if ago: 
                                desc_parts.append(tscolor('\c00????00') + 'وقت النشر: ' + tscolor('\c00????FF') + ago)
                            if episode: 
                                desc_parts.append(tscolor('\c00????00') + 'الحلقة: ' + tscolor('\c00????FF') + str(episode))
                            desc = '\n'.join(desc_parts) if desc_parts else ''
                            content_type = self.determine_content_type(title, url)
                            if is_episodes or content_type == 'episode' or content_type == 'movie':
                                self.addVideo({'import': cItem.get('import'),'title': title,'url': url,'icon': icon,'desc': desc,'good_for_fav': True,'hst': 'tshost'})
                            else:
                                self.addDir({'import': cItem.get('import'),'category': 'host2','title': title,'url': url,'icon': icon,'desc': desc,'good_for_fav': True,'hst': 'tshost','mode': '21'})
                        if len(valid_items) >= 20 and valid_items[-1].get("ID"):
                            last_item = valid_items[-1]
                            new_pick_up_id = str(last_item.get("ID", ""))
                            if new_pick_up_id and new_pick_up_id != pick_up_id:
                                self.addDir({'import': cItem.get('import'),'category': 'host2','title': tscolor('\c00????20') + 'تحميل المزيد','url': cItem.get('url', ''),'icon': '','desc': '','good_for_fav': False,'hst': 'tshost','mode': '22','pick_up_order': pick_up_order,'pick_up_id': new_pick_up_id,'parent_id': parent_id,'data_type': data_type,'taxonomy': taxonomy,'is_episodes': is_episodes})
                    else:
                        self.addDir({'import': cItem.get('import'),'category': 'host2','title': tscolor('\c00????20') + 'لا توجد عناصر إضافية','url': '','icon': '','desc': 'الاستجابة فارغة أو غير صالحة','good_for_fav': False,'hst': 'tshost','mode': ''})
                except Exception as e:
                    printDBG("Error parsing JSON: " + str(e))
                    printDBG("Response content: " + response_text)
                    self.addDir({'import': cItem.get('import'),'category': 'host2','title': tscolor('\c00????20') + 'خطأ في تنسيق البيانات','url': '','icon': '','desc': str(e),'good_for_fav': False,'hst': 'tshost','mode': ''})
            else:
                self.addDir({'import': cItem.get('import'),'category': 'host2','title': tscolor('\c00????20') + 'استجابة فارغة من الخادم','url': '','icon': '','desc': '','good_for_fav': False,'hst': 'tshost','mode': ''})
        except urllib.error.URLError as e:
            printDBG("URL Error in load_more: " + str(e))
            self.addDir({'import': cItem.get('import'),'category': 'host2','title': tscolor('\c00????20') + 'خطأ في الاتصال','url': '','icon': '','desc': str(e),'good_for_fav': False,'hst': 'tshost','mode': ''})
        except Exception as e:
            printDBG("Error in load_more: " + str(e))
            self.addDir({'import': cItem.get('import'),'category': 'host2','title': tscolor('\c00????20') + 'خطأ في النظام','url': '','icon': '','desc': str(e),'good_for_fav': False,'hst': 'tshost','mode': ''})
    def show_actors(self, cItem):
        url = cItem.get('url', '')
        if not url.startswith('http'):
            url = self.MAIN_URL + '/' + url.lstrip('/')
        sts, data = self.getPage(url)
        if not sts:
            return
        actors = []
        actor_blocks = re.findall(r'<li[^>]*class="ActorItem"[^>]*>(.*?)</li>', data, re.S)
        for block in actor_blocks:
            url_match = re.search(r'href="([^"]+)"', block)
            actor_url = url_match.group(1) if url_match else ''
            img_match = re.search(r'<img[^>]*src="([^"]*)"', block)
            actor_img = img_match.group(1) if img_match else ''
            title_match = re.search(r'title="([^"]+)"', block)
            actor_title = title_match.group(1) if title_match else ''
            name_match = re.search(r'ActorName">([^<]+)</div>', block)
            actor_name = name_match.group(1) if name_match else actor_title
            if actor_url and actor_name:
                actors.append((actor_url, actor_img, actor_name))
        if not actors:
            actors_section = re.search(r'<div class="ActorsList">(.*?)</div>', data, re.S)
            if actors_section:
                actors_content = actors_section.group(1)
                actor_links = re.findall(r'<a href="([^"]+)"[^>]*title="([^"]+)"[^>]*>', actors_content, re.S)
                for actor_url, actor_title in actor_links:
                    if not actor_url.startswith('http'):
                        actor_url = self.MAIN_URL + '/' + actor_url.lstrip('/')
                    actors.append((actor_url, '', actor_title))
        actors_sorted = sorted(actors, key=lambda x: x[2])
        for actor_url, actor_img, actor_name in actors_sorted:
            if not actor_url.startswith('http'):
                actor_url = self.MAIN_URL + '/' + actor_url.lstrip('/')
            icon = self.fix_image_url(self.std_url(actor_img)) if actor_img and actor_img.strip() else cItem.get('icon', '')
            self.addDir({'import': cItem.get('import'),'category': 'host2','title': actor_name.strip(),'url': actor_url,'icon': icon,'mode': '21','hst': 'tshost','good_for_fav': True})
        next_match = re.search(r'class="next page-numbers".*?href="([^"]+)"', data)
        if next_match:
            next_url = next_match.group(1)
            if not next_url.startswith('http'):
                next_url = self.MAIN_URL + '/' + next_url.lstrip('/')
            self.addDir({'import': cItem.get('import'),'category': 'host2','title': 'Next','url': next_url,'desc': 'Next','icon': cItem.get('icon', ''),'hst': 'tshost','mode': '20'})
    def show_actor_movies(self, cItem):
        url = cItem.get('url', '')
        if not url.startswith('http'):
            url = self.MAIN_URL + '/' + url.lstrip('/')
        sts, data = self.getPage(url)
        if not sts:
            return
        matches = re.findall(r'<div class="ItemNewly">.*?<a title="([^"]+)" href="([^"]+)".*?<div class="NewlyCover[^>]+(?:data-src|src)="([^"]+)".*?<div class="NewlyTitle">([^<]+)</div>', data, re.S)
        for (title, url_, img, new_title) in matches:
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
            self.addDir({'import': cItem.get('import'),'category': 'host2', 'title': tscolor('\c00????20') + 'خطأ في تحميل الصفحة','url': '','icon': '','desc': 'تعذر تحميل الصفحة، يرجى المحاولة لاحقاً','good_for_fav': False,'hst': 'tshost','mode': ''})
            return
        items_added = 0
        item_blocks = re.findall(r'(<div class="ItemNewly">.*?</div>\s*</a>\s*</div>)', data, re.S)
        if item_blocks:
            for item_block in item_blocks:
                title_match = re.search(r'<a title="([^"]+)"', item_block)
                url_match = re.search(r'href="([^"]+)"', item_block)
                img_match = re.search(r'data-src="([^"]+)"', item_block)
                ribbon_match = re.search(r'NewlyRibbon">([^<]+)</div>', item_block)
                time_match = re.search(r'NewlyTimeAgo">([^<]+)</div>', item_block)
                episode_match = re.search(r'NewlyEpNumber[^>]*>.*?<small>[^<]*</small>.*?(\d+)</div>', item_block)
                if not all([title_match, url_match, img_match]):
                    continue
                title = title_match.group(1)
                item_url = url_match.group(1)
                img = img_match.group(1)
                if any(x in str(value) for value in [title, item_url, img] for x in ["+ CategoryItem.", "CategoryItem."]):
                    printDBG("تخطي عنصر غير صالح في الحلقات: " + title)
                    continue
                icon = self.fix_image_url(self.std_url(img))
                desc_parts = []
                if ribbon_match and ribbon_match.group(1).strip():
                    desc_parts.append(tscolor('\c00????00') + 'النوع: ' + tscolor('\c00????FF') + ribbon_match.group(1).strip())
                if time_match and time_match.group(1).strip():
                    desc_parts.append(tscolor('\c00????00') + 'وقت النشر: ' + tscolor('\c00????FF') + time_match.group(1).strip())
                if episode_match and episode_match.group(1).strip():
                    desc_parts.append(tscolor('\c00????00') + 'الحلقة: ' + tscolor('\c00????FF') + episode_match.group(1).strip())
                desc = '\n'.join(desc_parts) if desc_parts else ''
                self.addVideo({'import': cItem.get('import'),'title': title.strip(),'url': item_url,'desc': desc,'icon': icon,'good_for_fav': True,'hst': 'tshost'})
                items_added += 1
        if items_added == 0:
            self.addDir({'import': cItem.get('import'),'category': 'host2','title': tscolor('\c00????20') + 'لا توجد حلقات متاحة','url': '','icon': '','desc': 'لا توجد حلقات متاحة لهذا المسلسل حالياً.\nقد يكون السبب:\n- الحلقات غير متوفرة بعد\n- المشكلة مؤقتة من الموقع\n- المسلسل قديم ولم يعد متاحاً','good_for_fav': False,'hst': 'tshost','mode': ''})
        more_match = re.search(r'<span id="ItemMoreBtn"[^>]*onclick="[^"]*GetMoreCategory\(\'([^\']+)\',\s*\'([^\']+)\'\)"', data)
        if more_match:
            pick_up_order = more_match.group(1)
            pick_up_id = more_match.group(2)
            parent_match = re.search(r"DataPosting\.append\('parent',\s*'(\d+)'\)", data)
            parent_id = parent_match.group(1) if parent_match else ''
            if pick_up_id and parent_id:
                self.addDir({'import': cItem.get('import'),'category': 'host2','title': tscolor('\c00????20') + 'تحميل المزيد من الحلقات','url': url,'icon': '','desc': '','good_for_fav': False,'hst': 'tshost','mode': '22','pick_up_order': pick_up_order,'pick_up_id': pick_up_id,'parent_id': parent_id,'data_type': 'Category','taxonomy': 'category','is_episodes': True})
        else:
            next_match = re.search(r'class="nextpage-numbers".*?href="([^"]+)"', data)
            if next_match:
                next_url = next_match.group(1)
                if not next_url.startswith('http'):
                    next_url = self.MAIN_URL + '/' + next_url.lstrip('/')
                self.addDir({'import': cItem.get('import'),'category': 'host2','title': tscolor('\c00????20') + 'الصفحة التالية للحلقات','url': next_url,'desc': '','icon': '','hst': 'tshost','mode': '21'})
    def SearchResult(self,str_ch,page,extra):
        url = self.MAIN_URL+'/search/'+str_ch+'/page/'+str(page)
        desc = [('Info','Ribbon">(.*?)</div>','',''),('Time','<time>(.*?)</time>','','')]
        self.add_menu({'import':extra,'url':url},'','<div class="ItemNewly">.*?<a title="(.*?)" href="(.*?)".*?<div class="NewlyCover[^>]+(?:data-src|src)="(.*?)".*?<div class="NewlyTitle">(.*?)</div>','','21',ord=[0,1,2,3],Desc=desc,u_titre=True)
    def getArticle(self,cItem):
        Desc = [('Date','PublishDate">(.*?)</div>','',''),('Story','BoxContentInner">(.*?)</div>','\n','')]
        desc = self.add_menu(cItem,'','DetailsBox">(.*?)<ul','','desc',Desc=Desc)
        if desc =='': desc = cItem.get('desc','')
        return [{'title':cItem['title'], 'text': desc, 'images':[{'title':'', 'url':cItem.get('icon','')}], 'other_info':{}}]
    def get_links(self, cItem):
        printDBG("LodyNet.get_links --------------------------------")
        url = cItem.get('url', '')
        sts, data = self.getPage(url)
        if not sts:
            return []
        links = []
        servers = re.findall(r"SwitchServer\(this,\s*'([^']+)'\).*?>([^<]+)<", data)
        if servers:
            for srv_url, srv_name in servers:
                srv_url = self.std_url(srv_url)
                srv_name = self.cleanHtmlStr(srv_name).strip()
                links.append({'name': srv_name, 'url': srv_url, 'need_resolve': 1})
                printDBG("  >> Found server: %s (%s)" % (srv_name, srv_url))
        else:
            old_servers = re.findall(r'<li[^>]+data-embed=["\']([^"\']+)["\'][^>]*>([^<]+)<', data)
            for srv_url, srv_name in old_servers:
                srv_url = self.std_url(srv_url)
                srv_name = self.cleanHtmlStr(srv_name).strip()
                links.append({'name': srv_name, 'url': srv_url, 'need_resolve': 1})
                printDBG("  >> Found old server: %s (%s)" % (srv_name, srv_url))
        return links
    def start(self, cItem):
        mode = cItem.get('mode', None)
        if mode == '00':
            self.showmenu(cItem)
        elif mode == '10':
            self.showmenu1(cItem)	
        elif mode == '11':
            self.showmenu2(cItem)
        elif mode == '19':
            self.showfilter(cItem)                    
        elif mode == '20':
            self.showitms(cItem)
        elif mode == '21':
            self.showelms(cItem)
        elif mode == '22':
            self.load_more(cItem)
        elif mode == '50':
            self.showsearch(cItem)
        elif mode == '51':
            self.searchResult(cItem)
        elif mode == 'schedules':
            self.showSchedules(cItem)
        return True