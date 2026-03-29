# -*- coding: utf8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.libs import ph
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor
from Plugins.Extensions.IPTVPlayer.libs.e2ijson import loads as json_loads
from Components.config import config
import re
def getinfo():
    info_={}
    info_['name']='MP3Quran.Net'
    info_['version']='1.2 15/03/2026'
    info_['dev']='RGYSoft + Angel_heart'
    info_['cat_id']='24'
    info_['desc']='Quran Audio Library'
    info_['icon']='https://i.ibb.co/4M5FBQR/logo2.png'
    info_['recherche_all']='0'
    return info_
class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':'mp3quran.cookie'})
        self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
        self.MAIN_URL = 'https://www.mp3quran.net'
        self.HEADER = {'User-Agent': self.USER_AGENT, 'Connection': 'keep-alive', 'Accept-Encoding':'gzip', 'Content-Type':'application/x-www-form-urlencoded','Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
        self.defaultParams = {'header':self.HEADER, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
    def showmenu(self,cItem):			
        self.addDir({'import':cItem['import'],'category' :'host2','title':'Reciters | القراء Ar','icon':cItem['icon'],'mode': '20','lng':'ar'})
        self.addDir({'import':cItem['import'],'category' :'host2','title':'Reciters | القراء En','icon':cItem['icon'],'mode': '20','lng':'eng'})
        self.addDir({'import': cItem['import'],'category':'host2','title':'Videos | تلاوات مرئية','icon':cItem['icon'],'mode': '60','lng': 'ar'})
        self.addDir({'import': cItem['import'],'category':'host2','title':'Videos | Video Recitations','icon':cItem['icon'],'mode': '60','lng': 'eng'})
        self.addDir({'import': cItem['import'],'category':'host2','title':'Tafsir | التفسير','icon':cItem['icon'],'mode': '80','lng': 'ar'})
        self.addDir({'import': cItem['import'],'category':'host2','title':'Tadabor | تدبر','icon': cItem['icon'],'mode': '90'})
        self.addDir({'import':cItem['import'],'category' :'host2','title':'Radios','icon':cItem['icon'],'mode': '21'})
        self.addDir({'import': cItem['import'], 'category': 'host2', 'title': 'Live | مباشر', 'icon': cItem['icon'], 'mode': '70'})
    def showmenu1(self, cItem):
        lng = cItem.get('lng','ar')
        url = 'https://www.mp3quran.net/api/v3/reciters?language=' + lng
        sts, data = self.getPage(url)
        if not sts:
            return
        data = json_loads(data)
        reciters = data.get('reciters', [])
        reciters = sorted(reciters, key=lambda x: x.get('name',''))
        for reciter in reciters:
            name = reciter.get('name','')
            recent = reciter.get('date','')
            moshafs = reciter.get('moshaf', [])
            moshafs = sorted(moshafs, key=lambda x: x.get('name',''))
            for moshaf in moshafs:
                title = name + ' - ' + moshaf.get('name','')
                surah_total = int(moshaf.get('surah_total','0'))
                # إذا كان عدد السور 114، نعرض "المصحف كاملاً"
                if surah_total == 114:
                    if lng == 'eng':
                        desc = tscolor('\c00FFFF00') + 'Number of Suras: '
                        desc += tscolor('\c00FFFFFF') + 'Full Quran' + '\n'
                        desc += tscolor('\c00FFFF00') + 'Update Date: '
                        desc += tscolor('\c00FFFFFF') + recent[:10]
                    else:
                        desc = tscolor('\c00FFFF00') + 'عدد السور : '
                        desc += tscolor('\c00FFFFFF') + 'المصحف كاملاً' + '\n'
                        desc += tscolor('\c00FFFF00') + 'تاريخ التحديث : '
                        desc += tscolor('\c00FFFFFF') + recent[:10]
                else:
                    if lng == 'eng':
                        desc = tscolor('\c00FFFF00') + 'Number of Suras: '
                        desc += tscolor('\c00FFFFFF') + str(surah_total) + '\n'
                        desc += tscolor('\c00FFFF00') + 'Update Date: '
                        desc += tscolor('\c00FFFFFF') + recent[:10]
                    else:
                        desc = tscolor('\c00FFFF00') + 'عدد السور : '
                        desc += tscolor('\c00FFFFFF') + str(surah_total) + '\n'
                        desc += tscolor('\c00FFFF00') + 'تاريخ التحديث : '
                        desc += tscolor('\c00FFFFFF') + recent[:10]
                self.addDir({
                    'import': cItem['import'],
                    'category': 'host2',
                    'title': title,
                    'icon': cItem['icon'],
                    'desc': desc,
                    'mode': '40',
                    'server': moshaf.get('server',''),
                    'surah_list': moshaf.get('surah_list',''),
                    'lng': lng
                })
    def showmenu2(self, cItem):
        url = 'https://api.mp3quran.net/api_2/atheer/radios_cats?language=ar'
        addParams = dict(self.defaultParams)
        addParams['header'].update({
            'Accept': 'application/json',
            'Origin': 'https://www.atheer-radio.com',
            'Referer': 'https://www.atheer-radio.com/'
        })
        sts, data = self.getPage(url, addParams)
        if sts:
            data = json_loads(data)
            for elm in data.get('reads', []):
                title = elm.get('name', '')
                cat_id = elm.get('id', '')
                link = 'https://api.mp3quran.net/api_2/atheer/radios?radio_cat=%s' % cat_id
                self.addDir({'import': cItem['import'],'category': 'host2','title': title,'url': link,'icon':cItem['icon'],'mode': '22'})
    def showmenu3(self, cItem):
        url = cItem['url']
        addParams = dict(self.defaultParams)
        addParams['header'].update({
            'Accept': 'application/json',
            'Origin': 'https://www.atheer-radio.com',
            'Referer': 'https://www.atheer-radio.com/'
        })
        sts, data = self.getPage(url, addParams)
        if not sts:
            return
        try:
            data = json_loads(data)
        except Exception:
            printDBG("JSON ERROR")
            printDBG(data)
            return
        for elm in data.get('reads', []):
            name = elm.get('name', '')
            radio_url = elm.get('URL', '')
            lst = elm.get('list')
            if not lst:
                self.addAudio({'import': cItem['import'],'title': name,'url': radio_url,'icon':cItem['icon'],'desc': tscolor('\c00??0000')+'LIVE','hst': 'direct'})
            else:
                self.addDir({'import': cItem['import'],'category': 'host2','title': name,'icon':cItem['icon'],'list': lst,'mode': '23'})
    def showmenu4(self, cItem):
        for sora in cItem.get('list', []):
            self.addAudio({'import': cItem['import'],'title': sora.get('name',''),'url': sora.get('url',''),'icon':cItem['icon'],'hst':'direct'})
    def showitms(self,cItem):		
        Url=cItem['url']
        page=cItem.get('page',1)
        url_=Url+'?page='+str(page)
        sts, data = self.getPage(url_) 	
        if sts:
            data_ = re.findall('class="thumbnail">.*?href="(.*?)".*?src="(.*?)".*?<h5>(.*?)</h5>', data, re.S)
            for (url,image,titre) in data_:
                url='https://videos.mp3quran.net'+url.replace('//','/')
                image='https://videos.mp3quran.net'+image
                self.addVideo({'import':cItem['import'],'category' :'host2','title':titre,'url':url,'icon':image,'hst': 'tshost'})			
            self.addDir({'import':cItem['import'],'category' : 'host2','title':'Next','url':Url,'page':page+1,'mode':'30'})
    def showitms1(self, cItem):
        server = cItem.get('server','')
        surahs = cItem.get('surah_list','').split(',')
        lng = cItem.get('lng','ar')
        for s in surahs:
            num = int(s)
            sura = "%03d" % num
            url = server + sura + ".mp3"
            if lng == 'ar':
                title  = tscolor('\c00FFFF00') + "سورة " + str(num)
                title += tscolor('\c00FFFFFF') + " - " + self.SURA_NAMES[num]
            else:
                title  = tscolor('\c00FFFF00') + "Surah " + str(num)
                title += tscolor('\c00FFFFFF') + " - " + self.SURA_NAMES_EN[num]
            self.addAudio({'import': cItem['import'],'title': title,'url': url,'icon': cItem['icon'],'hst': 'direct'})
    def showVideos(self, cItem):
        lng = cItem.get('lng', 'ar')
        url = f'https://www.mp3quran.net/api/v3/videos?language={lng}'
        sts, data = self.getPage(url)
        if not sts:
            return
        data = json_loads(data)
        reciters = data.get('videos', [])
        reciters = sorted(reciters, key=lambda x: x.get('reciter_name',''))
        for reciter in reciters:
            self.addDir({'import': cItem['import'],'category': 'host2','title': reciter.get('reciter_name',''),'icon': cItem['icon'],'list': reciter.get('videos', []),'mode': '61'})
    def showVideosItems(self, cItem):
        videos = cItem.get('list', [])
        for video in videos:
            self.addVideo({'import': cItem['import'],'title': cItem['title'],'url': video.get('video_url',''),'icon': video.get('video_thumb_url',''),'hst': 'direct'})
    def showLive(self, cItem):
        self.addAudio({
            'import': cItem['import'],
            'title': 'LIVE Radio',
            'url': 'http://live.mp3quran.net:8006/;',
            'icon': cItem['icon'],
            'desc': tscolor('\c00??0000')+'LIVE',
            'hst': 'direct'
        })
        url = 'https://www.mp3quran.net/api/v3/live-tv'
        sts, data = self.getPage(url)
        if not sts:
            return
        data = json_loads(data)
        for tv in data.get('livetv', []):
            self.addAudio({'import': cItem['import'],'title': tv.get('name',''),'url': tv.get('url',''),'icon': cItem['icon'],'desc': tscolor('\c00??0000')+'LIVE','hst': 'direct'})
    def showTafsir(self, cItem):
        url = 'https://mp3quran.net/api/v3/tafasir?language=ar'
        sts, data = self.getPage(url)
        if not sts:
            return
        data = json_loads(data)
        tafasir = data.get('tafasir', [])
        if isinstance(tafasir, dict):
            tafasir = [tafasir]
        for tafsir in tafasir:
            self.addDir({'import': cItem['import'],'category': 'host2','title': tafsir.get('name',''),'icon': cItem['icon'],'tafsir_id': tafsir.get('id',1),'mode': '81'})
    def showTafsirSuras(self, cItem):
        tafsir_id = cItem.get('tafsir_id','1')
        url = 'https://www.mp3quran.net/api/v3/tafsir?tafsir=%s&language=ar' % tafsir_id
        sts, data = self.getPage(url)
        if not sts:
            return
        data = json_loads(data)
        soar = data.get('tafasir', {}).get('soar', [])
        sura_map = {}
        for item in soar:
            sid = item.get('sura_id')
            if sid not in sura_map:
                sura_map[sid] = []
            sura_map[sid].append(item)
        for sid in sorted(sura_map.keys()):
            title = tscolor('\c00FFFF00') + "سورة " + tscolor('\c00FFFFFF') + self.SURA_NAMES[sid]
            self.addDir({'import': cItem['import'],'category': 'host2','title': title,'icon': cItem['icon'],'list': sura_map[sid],'mode': '82'})
    def showTafsirItems(self, cItem):
        items = cItem.get('list', [])
        for item in items:
            title = tscolor('\c00FFFF00') + item.get('name','')
            self.addAudio({'import': cItem['import'],'title': title,'url': item.get('url',''),'icon': cItem['icon'],'hst': 'direct'})
    def showTadabor(self, cItem):
        url = 'https://mp3quran.net/api/v3/tadabor'
        sts, data = self.getPage(url)
        if not sts:
            return
        data = json_loads(data)
        tadabor = data.get('tadabor', {})
        for sid in sorted(tadabor.keys(), key=int):
            items = tadabor.get(sid, [])
            if not items:
                continue
            sura = items[0].get('sora_name','')
            title = tscolor('\c00FFFF00') + "سورة " + tscolor('\c00FFFFFF') + sura
            self.addDir({'import': cItem['import'],'category': 'host2','title': title,'icon': items[0].get('image_url',''),'list': items,'mode': '91'})
    def showTadaborVideos(self, cItem):
        items = cItem.get('list', [])
        for item in items:
            title = tscolor('\c00FFFF00') + item.get('title','')
            if item.get('reciter_name'):
                title += tscolor('\c00FFFFFF') + " | " + item.get('reciter_name')
            self.addVideo({'import': cItem['import'],'title': title,'url': item.get('video_url',''),'icon': item.get('image_url',''),'hst': 'direct'})
    def get_links(self,cItem): 	
        urlTab = []
        URL=cItem['url']	
        sts, data = self.getPage(URL)
        if sts:
            _data = re.findall('video-grid">.*?src="(.*?)"', data, re.S)
            if _data:
                url='https://videos.mp3quran.net'+_data[0]
                url=url.replace('&#39;',"'")
                urlTab.append({'name':cItem['title'], 'url':url, 'need_resolve':0})
        return urlTab
    SURA_NAMES = [
        "", "الفاتحة","البقرة","آل عمران","النساء","المائدة","الأنعام","الأعراف",
        "الأنفال","التوبة","يونس","هود","يوسف","الرعد","إبراهيم","الحجر","النحل",
        "الإسراء","الكهف","مريم","طه","الأنبياء","الحج","المؤمنون","النور",
        "الفرقان","الشعراء","النمل","القصص","العنكبوت","الروم","لقمان","السجدة",
        "الأحزاب","سبأ","فاطر","يس","الصافات","ص","الزمر","غافر","فصلت","الشورى",
        "الزخرف","الدخان","الجاثية","الأحقاف","محمد","الفتح","الحجرات","ق",
        "الذاريات","الطور","النجم","القمر","الرحمن","الواقعة","الحديد","المجادلة",
        "الحشر","الممتحنة","الصف","الجمعة","المنافقون","التغابن","الطلاق","التحريم",
        "الملك","القلم","الحاقة","المعارج","نوح","الجن","المزمل","المدثر",
        "القيامة","الإنسان","المرسلات","النبأ","النازعات","عبس","التكوير",
        "الانفطار","المطففين","الانشقاق","البروج","الطارق","الأعلى","الغاشية",
        "الفجر","البلد","الشمس","الليل","الضحى","الشرح","التين","العلق",
        "القدر","البينة","الزلزلة","العاديات","القارعة","التكاثر","العصر",
        "الهمزة","الفيل","قريش","الماعون","الكوثر","الكافرون","النصر",
        "المسد","الإخلاص","الفلق","الناس"
    ]
    SURA_NAMES_EN = [
        "", "Al-Fatihah","Al-Baqarah","Aal-i-Imran","An-Nisa","Al-Ma'idah","Al-An'am","Al-A'raf",
        "Al-Anfal","At-Tawbah","Yunus","Hud","Yusuf","Ar-Ra'd","Ibrahim","Al-Hijr","An-Nahl",
        "Al-Isra","Al-Kahf","Maryam","Ta-Ha","Al-Anbiya","Al-Hajj","Al-Mu'minun","An-Nur",
        "Al-Furqan","Ash-Shu'ara","An-Naml","Al-Qasas","Al-Ankabut","Ar-Rum","Luqman","As-Sajda",
        "Al-Ahzab","Saba","Fatir","Ya-Sin","As-Saffat","Sad","Az-Zumar","Ghafir","Fussilat","Ash-Shura",
        "Az-Zukhruf","Ad-Dukhan","Al-Jathiya","Al-Ahqaf","Muhammad","Al-Fath","Al-Hujurat","Qaf",
        "Adh-Dhariyat","At-Tur","An-Najm","Al-Qamar","Ar-Rahman","Al-Waqi'a","Al-Hadid","Al-Mujadila",
        "Al-Hashr","Al-Mumtahina","As-Saff","Al-Jumua","Al-Munafiqun","At-Taghabun","At-Talaq","At-Tahrim",
        "Al-Mulk","Al-Qalam","Al-Haaqqa","Al-Ma'arij","Nuh","Al-Jinn","Al-Muzzammil","Al-Muddaththir",
        "Al-Qiyama","Al-Insan","Al-Mursalat","An-Naba","An-Nazi'at","Abasa","At-Takwir",
        "Al-Infitar","Al-Mutaffifin","Al-Inshiqaq","Al-Buruj","At-Tariq","Al-A'la","Al-Ghashiya",
        "Al-Fajr","Al-Balad","Ash-Shams","Al-Lail","Ad-Duha","Ash-Sharh","At-Tin","Al-'Alaq",
        "Al-Qadr","Al-Bayyina","Az-Zalzalah","Al-Adiyat","Al-Qari'a","At-Takathur","Al-Asr",
        "Al-Humaza","Al-Fil","Quraish","Al-Ma'un","Al-Kawthar","Al-Kafirun","An-Nasr",
        "Al-Masad","Al-Ikhlas","Al-Falaq","An-Nas"
    ]
    def start(self,cItem):
        mode=cItem.get('mode', None)
        if mode=='00':
            self.showmenu(cItem)
        if mode=='20':
            self.showmenu1(cItem)
        if mode=='21':
            self.showmenu2(cItem)
        if mode=='22':
            self.showmenu3(cItem)
        if mode=='23':
            self.showmenu4(cItem)
        if mode=='30':
            self.showitms(cItem)
        if mode=='40':
            self.showitms1(cItem)
        if mode=='60':
            self.showVideos(cItem)
        if mode=='61':
            self.showVideosItems(cItem)
        if mode=='70':
            self.showLive(cItem)
        if mode=='80':
            self.showTafsir(cItem)
        if mode=='81':
            self.showTafsirSuras(cItem)
        if mode=='82':
            self.showTafsirItems(cItem)
        if mode=='90':
            self.showTadabor(cItem)
        if mode=='91':
            self.showTadaborVideos(cItem)
        return True