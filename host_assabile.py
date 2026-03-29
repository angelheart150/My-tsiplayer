# -*- coding: utf8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.libs import ph
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor,tshost
from Plugins.Extensions.IPTVPlayer.libs.e2ijson import loads as json_loads
from Components.config import config
import re
def getinfo():
	info_={}
	name = 'Assabile'
	hst = 'https://ar.assabile.com'
	info_['old_host'] = hst
	hst_ = tshost(name)	
	if hst_!='': hst = hst_
	info_['host']= hst
	info_['name']=name
	info_['version']='1.1 29/03/2026'
	info_['dev']='RGYSoft + angel_heart'
	info_['cat_id']='24'
	info_['desc']='Quran Audio Library'
	info_['icon']='https://i.ibb.co/JpSLWz5/logo-assabile.png'
	info_['recherche_all']='0'
	return info_
class TSIPHost(TSCBaseHostClass):
	def __init__(self):
		TSCBaseHostClass.__init__(self,{'cookie':'mp3quran.cookie'})
		self.USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36'
		self.MAIN_URL = getinfo()['host']
		self.HEADER = {'User-Agent': self.USER_AGENT, 'X-Requested-With': 'XMLHttpRequest','Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
		self.defaultParams = {'header':self.HEADER,'with_metadata':True, 'use_cookie': False}
		self.getPage = self.cm.getPage
	def showmenu(self,cItem):
		self.addDir({'import':cItem['import'],'category' :'host2','title':'القرآن','icon':cItem['icon'],'mode': '10','sub_mode':'0'})
		self.addDir({'import':cItem['import'],'category' :'host2','title':'خطب','icon':cItem['icon'],'mode': '10','sub_mode':'1'})
		self.addDir({'import':cItem['import'],'category' :'host2','title':'اناشيد و اذان','icon':cItem['icon'],'mode': '10','sub_mode':'2'})				
	def showmenu1(self,cItem):
		sub_mode=cItem.get('sub_mode', '0')
		if sub_mode=='0':
			self.addDir({'import':cItem['import'],'category' :'host2','title':'القراء','icon':cItem['icon'],'url':self.MAIN_URL+'/quran','mode': '11'})
			self.addDir({'import':cItem['import'],'category' :'host2','title':'سور القرءان','icon':cItem['icon'],'url':self.MAIN_URL+'/quran/suwar','mode': '19'})
			self.addDir({'import':cItem['import'],'category' :'host2','title':'المصاحف المسموعة','icon':cItem['icon'],'mode': '15'})
			self.addDir({'import':cItem['import'],'category' :'host2','title':'الروايات','icon':cItem['icon'],'mode': '17'})
			self.addDir({'import':cItem['import'],'category' :'host2','title':'40 تلاوة الأكثر إستماعاً','icon':cItem['icon'],'url':self.MAIN_URL+'/quran/top','mode': '22'})
		elif sub_mode=='1':
			self.addDir({'import':cItem['import'],'category' :'host2','title':'دعاة','icon':cItem['icon'],'url':self.MAIN_URL+'/lesson','mode': '11'})
			self.addDir({'import':cItem['import'],'category' :'host2','title':'الدروس الاكثر مشاهدة','icon':cItem['icon'],'url':self.MAIN_URL+'/lesson/topseries','mode': '18'})
			self.addDir({'import':cItem['import'],'category' :'host2','title':'جديد الدروس','icon':cItem['icon'],'url':self.MAIN_URL+'/lesson/lastseries','mode': '18'})
		elif sub_mode=='2':
			self.addDir({'import':cItem['import'],'category' :'host2','title':'منشدون','icon':cItem['icon'],'url':self.MAIN_URL+'/anasheed','mode': '11'})
			self.addDir({'import':cItem['import'],'category' :'host2','title':'الأناشيد الأكثر استماعا','icon':cItem['icon'],'url':self.MAIN_URL+'/anasheed/top','mode': '22'})
			self.addDir({'import':cItem['import'],'category' :'host2','title':'تسجيلات الآذان بأجمل الأصوات','icon':cItem['icon'],'url':self.MAIN_URL+'/adhan-call-prayer','mode': '22'})
	def showmenu2(self,cItem):
		Url0=cItem.get('url',self.MAIN_URL)
		sts, data = self.getPage(Url0) 
		if sts:
			data_ = re.findall('<li class="activeFilter">(.*?)id="sort-container"', data, re.S)
			if data_:
				data_2 = re.findall('<li.*?href="(.*?)".*?">(.*?)<', '<li '+data_[0], re.S)
				for (url,name) in data_2:
					self.addDir({'import':cItem['import'],'category' :'host2','title':name,'url':self.MAIN_URL+url,'icon':cItem['icon'],'mode': '12'})
	def showmenu3(self,cItem):
		page = cItem.get('page',1)
		uRL	 = cItem['url']
		Url0 = uRL+'/page:'+str(page)
		sts, data = self.getPage(Url0) 
		if sts:
			data_ = re.findall('portfolio-image">.*?href="(.*?)".*?src="(.*?)".*?title="(.*?)"', data, re.S)
			i=0
			for (url,image,name) in data_:
				if name !='':
					self.addDir({'import':cItem['import'],'category' :'host2','title':name,'url':self.MAIN_URL+url,'icon':self.MAIN_URL+image,'mode': '20'})
					i=i+1
			if i>11:
				self.addDir({'import':cItem['import'],'category' : 'host2','title':'Next','url':uRL,'page':page+1,'mode':'12'})
	def showmenudourous(self,cItem):
		page = cItem.get('page',1)
		uRL	 = cItem['url']
		Url0 = uRL+'/page:'+str(page)
		sts, data = self.getPage(Url0) 
		if sts:
			data_ = re.findall('class="col_one_fourth .*?href="(.*?)".*?src="(.*?)".*?title="(.*?)".*?>(.*?)</div>.*?<ul class.*?>(.*?)</ul>', data, re.S)
			i=0
			for (url,image,name,desc1,desc2) in data_:
				mode_ = ''
				if '/series-audio/' in url: mode_ = '22'
				elif '/series/' in url: mode_ = '33'
				if 'audio-series.png' in image:
					image = cItem['icon']
				else:
					image = self.MAIN_URL+image
				self.addDir({'import':cItem['import'],'category' :'host2','title':name,'url':self.MAIN_URL+url,'icon':image,'mode': mode_})
				i=i+1
			if i>19:
				self.addDir({'import':cItem['import'],'category' : 'host2','title':'Next','url':uRL,'page':page+1,'mode':'18','icon':cItem['icon']})
	def showmenu4(self,cItem):
		url	 = cItem['url']
		sts, data = self.getPage(url) 
		if sts:
			data = re.findall('nav nav-tabs">(.*?)</ul>', data, re.S)
			if data:
				data = re.findall('<li.*?class="(.*?)".*?href="(.*?)">(.*?)<', data[0], re.S)
				for (class_,Url,titre) in data:
					titre = titre.strip()
					if titre!='':
						mode_=''
						if 'active' in class_: titre='>> '+titre
						if not ( (Url.endswith('/photos')) or (Url.endswith('/collection')) ):
							if Url.endswith('/quran'): mode_ = '21'
							elif Url.endswith('/series-audio'): mode_ = '31'
							elif Url.endswith('/series'): mode_ = '32'
							elif Url.endswith('/album'): mode_ = '32'
							self.addDir({'import':cItem['import'],'category' :'host2','title':titre,'url':self.MAIN_URL+Url,'icon':cItem['icon'],'desc':mode_,'mode': mode_})
	def showaudiomenu1(self,cItem):
		uRL = cItem['url']
		sts, data = self.getPage(uRL) 
		if sts:
			data = re.findall('riwaya">(.*?)</ul', data, re.S)
			if data:
				data = re.findall('<li.*?href="(.*?)">(.*?)<', data[0], re.S)
				for (url,name) in data:
					self.addDir({'import':cItem['import'],'category' :'host2','title':name,'desc':cItem['desc'],'url':self.MAIN_URL+url,'icon':cItem['icon'],'mode': '22'})
					printDBG('self.MAIN_URL+url='+name+'|'+self.MAIN_URL+url)
	def showaudio1(self,cItem):
		uRL = cItem['url']
		printDBG('uRL='+uRL)
		sts, data = self.getPage(uRL) 
		if sts:
			if data.startswith('{"'):
				data = json_loads(data)
				printDBG('data='+str(data))
				data = data.get('Recitation',[])
				for elm in data:
					desc=''
					name = elm.get('span_name','!!')
					url = elm.get('href','!!')
					duration = elm.get('duration','')
					statu = elm.get('stats-kind','')
					riwaya = elm.get('data-riwaya','')
					type_ = elm.get('stats-riwaya','').replace(')','-').replace('(','-')
					desc= desc+tscolor('\c00????00')+'Info: '+tscolor('\c00??????')+type_+'\n'
					desc= desc+tscolor('\c00????00')+'Duration: '+tscolor('\c00??????')+duration+'\n'
					desc= desc+tscolor('\c00????00')+'Kind: '+tscolor('\c00??????')+statu+'\n'
					desc= desc+tscolor('\c00????00')+'Riwaya: '+tscolor('\c00??????')+riwaya+'\n'
					self.addAudio({'import':cItem['import'],'category' :'host2','title':name,'desc':desc,'url':url,'icon':cItem['icon'],'hst': 'tshost'})
			else:
				data_ = re.findall('(class="link-media|itemprop="track").*?href="(.*?)"(.*?)">(.*?)</a(.*?)"timer">(.*?)</div>(.*?)</li>', data, re.S)
				for (x0,url,x2,name,x1,time_,desc) in data_:
					if 'data-title=' in x2: url = url.replace('#','@')
					name = ph.clean_html(name)	
					desc=time_+'\n'+ph.clean_html(desc)+'\n'+ph.clean_html('<'+x1+'>')
					self.addAudio({'import':cItem['import'],'category' :'host2','title':name,'desc':url,'url':url,'icon':cItem['icon'],'hst': 'tshost'})
	def showserieaudiomenu1(self,cItem):
		uRL = cItem['url']
		sts, data = self.getPage(uRL) 
		if sts:
			data = re.findall('<tr>.*?href="(.*?)">(.*?)<.*?>(.*?)</tr>', data, re.S)
			for (url,name,desc) in data:
				desc = ph.clean_html(desc)	
				self.addDir({'import':cItem['import'],'category' :'host2','title':name,'desc':desc,'url':self.MAIN_URL+url,'icon':cItem['icon'],'mode': '22'})
				printDBG('self.MAIN_URL+url='+name+'|'+self.MAIN_URL+url)
	def showserievidmenu1(self,cItem):
		uRL = cItem['url']
		sts, data = self.getPage(uRL) 
		if sts:
			data = re.findall('class="portfolio-item.*?href="(.*?)".*?src="(.*?)".*?title">(.*?)</div>', data, re.S)
			for (url,img,name) in data:
				desc =''
				name = ph.clean_html(name)
				mode_='33'
				if '/album/' in url: mode_='22'
				self.addDir({'import':cItem['import'],'category' :'host2','title':name,'desc':desc,'url':self.MAIN_URL+url,'icon':self.MAIN_URL+img,'mode': mode_})
	def showvid1(self,cItem):
		page = cItem.get('page',1)
		uRL	 = cItem['url']
		Url0 = uRL+'/page:'+str(page)
		sts, data = self.getPage(Url0) 
		if sts:
			i=0
			data_ = re.findall('entry clearfix.*?<h2>.*?href="(.*?)">(.*?)<.*?src="(.*?)"', data, re.S)
			for (url,name,img) in data_:
				self.addVideo({'import':cItem['import'],'category' :'host2','title':name,'desc':url,'url':self.MAIN_URL+url,'icon':self.MAIN_URL+img,'hst': 'tshost'})
				i=i+1
			if i>19:
				self.addDir({'import':cItem['import'],'category' : 'host2','title':'Next','url':uRL,'page':page+1,'mode':'33'})
	def showmenu11(self,cItem):
		self.addDir({'import':cItem['import'],'category' :'host2','title':'القراء','icon':cItem['icon'],'mode': '14'})		
		self.addDir({'import':cItem['import'],'category' :'host2','title':'المصاحف المسموعة','icon':cItem['icon'],'mode': '15'})		
		self.addDir({'import':cItem['import'],'category' :'host2','title':'الروايات','icon':cItem['icon'],'mode': '17'})				
	def showmenu12(self,cItem):
		self.addDir({'import':cItem['import'],'category' :'host2','title':'دعاة','icon':cItem['icon'],'mode': '21'})		
		self.addDir({'import':cItem['import'],'category' :'host2','title':'الدروس الاكثر مشاهدة','icon':cItem['icon'],'mode': '15'})		
		self.addDir({'import':cItem['import'],'category' :'host2','title':'جديد الدروس','icon':cItem['icon'],'mode': '17'})	
	def showmenu21(self,cItem):
		Url0=self.MAIN_URL+'/lesson'
		sts, data = self.getPage(Url0) 
		if sts:
			data_ = re.findall('<li class="activeFilter">(.*?)id="sort-container"', data, re.S)
			if data_:
				data_2 = re.findall('<li.*?href="(.*?)".*?">(.*?)<', '<li '+data_[0], re.S)
				for (url,name) in data_2:
					self.addDir({'import':cItem['import'],'category' :'host2','title':name,'url':self.MAIN_URL+url,'icon':cItem['icon'],'mode': '22'})
	def showmenu22(self,cItem):
		page=cItem.get('page',1)
		uRL=	cItem['url']
		Url0=uRL+'/page:'+str(page)
		sts, data = self.getPage(Url0) 
		if sts:
			data_ = re.findall('portfolio-image">.*?href="(.*?)".*?src="(.*?)".*?title="(.*?)"', data, re.S)
			i=0
			for (url,image,name) in data_:
				if name !='':
					self.addDir({'import':cItem['import'],'category' :'host2','title':name,'url':self.MAIN_URL+url,'icon':self.MAIN_URL+image,'mode': '30'})
					i=i+1
			if i>10:
				self.addDir({'import':cItem['import'],'category' : 'host2','title':'Next','url':uRL,'page':page+1,'mode':'20'})
	def showmenu14(self,cItem):
		Url0=self.MAIN_URL+'/quran'
		sts, data = self.getPage(Url0) 
		if sts:
			data_ = re.findall('<li class="activeFilter">(.*?)id="sort-container"', data, re.S)
			if data_:
				data_2 = re.findall('<li.*?href="(.*?)".*?">(.*?)<', '<li '+data_[0], re.S)
				for (url,name) in data_2:
					self.addDir({'import':cItem['import'],'category' :'host2','title':name,'url':self.MAIN_URL+url,'icon':cItem['icon'],'mode': '20'})
	def showmenu15(self,cItem):
		Url0=self.MAIN_URL+'/quran'
		sts, data = self.getPage(Url0) 
		if sts:
			data_ = re.findall('<div>المصاحف المسموعة</div>(.*?)<div>الروايات</div>', data, re.S)
			if data_:
				data_2 = re.findall('<li.*?href="(.*?)">(.*?)</a>', data_[0], re.S)
				for (url,name) in data_2:
					self.addDir({'import':cItem['import'],'category' :'host2','title':ph.clean_html(name),'url':self.MAIN_URL+url,'icon':cItem['icon'],'mode': '16'})
	def showmenu16(self,cItem):
		page=cItem.get('page',1)
		uRL=	cItem['url']
		Url0=uRL+'/page:'+str(page)
		sts, data = self.getPage(Url0) 
		if sts:
			i=0
			data_ = re.findall('name-surat">.*?href="(.*?)".*?data-recitation="(.*?)".*?data-name="(.*?)".*?reciters">(.*?)<.*?<span>(.*?)</span>', data, re.S)
			for (url,desc,name,desc2,riwaya) in data_:
				if name !='':
					i=i+1
					self.addDir({'import':cItem['import'],'category' :'host2','title':name+' - '+ph.clean_html(riwaya)+ ' - '+desc2,'desc':tscolor('\c00????00')+' تلاوة'+desc,'url':self.MAIN_URL+url,'icon':cItem['icon'],'mode': '22'})
			if i>14:
				self.addDir({'import':cItem['import'],'category' : 'host2','icon':cItem['icon'],'title':'Next','url':uRL,'page':page+1,'mode':'16'})
	def showmenu17(self,cItem):
		Url0=self.MAIN_URL+'/quran'
		sts, data = self.getPage(Url0) 
		if sts:
			data_ = re.findall('<div>الروايات</div>(.*?)"/quran/top">', data, re.S)
			if data_:
				data_2 = re.findall('<li.*?href="(.*?)">(.*?)</a>', data_[0], re.S)
				for (url,name) in data_2:
					self.addDir({'import':cItem['import'],'category' :'host2','title':ph.clean_html(name),'url':self.MAIN_URL+url,'icon':cItem['icon'],'mode': '16'})
	def showmenu19(self, cItem):
		url = cItem['url']
		sts, data = self.getPage(url)
		if sts:
			pattern = 'h2_sourat">.*?href="(.*?)".*?>(.*?)</a>.*?leftspan">(.*?)</div>.*?rightspan">(.*?)</div>'
			data_ = re.findall(pattern, data, re.S)
			for (url_sura, name_sura, left_info, right_info) in data_:
				name_sura = ph.clean_html(name_sura).strip()
				description = ph.clean_html(left_info) + " | " + ph.clean_html(right_info)
				description = description.replace('\n', '').replace('\t', '').replace('	 ', ' ').strip()
				self.addDir({'import': cItem['import'],'category': 'host2','title': name_sura,'url': self.MAIN_URL + url_sura,'icon': cItem['icon'],'desc': description,'mode': '40' })
	def showmenu20(self, cItem):
		url = cItem['url']
		sts, data = self.getPage(url)
		if not sts:
			return
		ajax_url = ph.search(data, r'<li[^>]+id="allriwaya".*?href="([^"]+)"')[0]
		if ajax_url:
			ajax_url = self.getFullUrl(ajax_url)
			sts, data = self.getPage(ajax_url)
			if not sts:
				return
		else:
			printDBG("AJAX URL NOT FOUND - fallback to original page")
		block = self.cm.ph.getDataBeetwenMarkers(data, '<div class="play-list', '</ul>', False)[1]
		items = self.cm.ph.getAllItemsBeetwenMarkers(block, '<li', '</li>')
		audios = []
		for item in items:
			track_id = ph.search(item, r'href="#(\d+)"')[0]
			if not track_id: continue
			pre = ph.search(item, r'data-pre\s*=\s*"([^"]+)"')[0]
			nom = ph.search(item, r'data-nom\s*=\s*"([^"]+)"')[0]
			person = (pre + ' ' + nom).strip()
			duration = self.cm.ph.getDataBeetwenMarkers(item, 'class="timer">', '</div>', False)[1]
			duration = ph.clean_html(duration).strip()
			kind_raw = self.cm.ph.getDataBeetwenMarkers(item, 'inff-arrow', '</span>', False)[1]
			kind = kind_raw.split('>')[-1] 
			kind = ph.clean_html(kind).strip()
			riwaya_raw = self.cm.ph.getDataBeetwenMarkers(item, 'inff-book', '</span>', False)[1]
			riwaya = riwaya_raw.split('>')[-1]
			riwaya = ph.clean_html(riwaya).strip()
			if person: title = tscolor('\c00FFFFFF') + riwaya + ' | ' + tscolor('\c00FFFF00') + person 
			else: title = tscolor('\c00FFFFFF') + riwaya + track_id + ' | ' + tscolor('\c00FFFF00') + "تلاوة " 
			desc = ''
			desc += tscolor('\c00FFFF00') + 'Duration : ' + tscolor('\c00FFFFFF') + duration + '\n'
			desc += tscolor('\c00FFFF00') + 'Kind : ' + tscolor('\c00FFFFFF') + kind + '\n'
			desc += tscolor('\c00FFFF00') + 'Riwaya : ' + tscolor('\c00FFFFFF') + riwaya
			audios.append({
				'import': cItem['import'],
				'category': 'host2',
				'title': title,
				'desc': desc,
				'url': '#' + track_id,
				'icon': cItem['icon'],
				'hst': 'tshost'
			})
		audios = sorted(audios, key=lambda x: x['title'])
		printDBG("showmenu20: total li items = " + str(len(items)))
		printDBG("showmenu20: audios count = " + str(len(audios)))
		for item in audios:
			self.addAudio(item)
	def showmenu30(self,cItem):
		uRL=	cItem['url']
		data_ = re.findall('(.*)/', uRL, re.S)
		if data_:
			URL=data_[0]+'/collection'
			sts, data = self.getPage(URL) 
			if sts:
				data_ = re.findall('name-surat">.*?href="(.*?)".*?data-recitation="(.*?)".*?data-name="(.*?)".*?data-riwaya="(.*?)"', data, re.S)
				for (url,desc,name,riwaya) in data_:
					if name !='':
						self.addDir({'import':cItem['import'],'category' :'host2','title':name+' - '+riwaya,'desc':tscolor('\c00????00')+' تلاوة'+desc,'url':self.MAIN_URL+url,'icon':cItem['icon'],'mode': '31'})
	def showmenu31(self,cItem):
		uRL=	cItem['url']
		sts, data = self.getPage(uRL) 
		if sts:
			data_ = re.findall('class="name">.*?link-media never".*?href="#(.*?)".*?">(.*?)</a.*?"timer">(.*?)<', data, re.S)
			for (url,name,desc) in data_:
				if name !='':
					self.addAudio({'import':cItem['import'],'category' :'host2','title':ph.clean_html(name),'desc':desc,'url':url,'icon':cItem['icon'],'hst': 'tshost'})
	def get_links(self, cItem):	
		urlTab = []
		URL = cItem['url']
		if URL.startswith('#'):
			URL = self.MAIN_URL + '/ajax/getrcita-link-' + URL.replace('#','')
			sts, data = self.getPage(URL, self.defaultParams)
			if sts and data:
				urlTab.append({'name': cItem['title'], 'url': data, 'need_resolve': 0})
		elif URL.startswith('@'):
			URL = self.MAIN_URL + '/ajax/getsnng-link-' + URL.replace('@','')
			sts, data = self.getPage(URL, self.defaultParams)
			if sts and data:
				urlTab.append({'name': cItem['title'], 'url': data, 'need_resolve': 0})
		elif URL.endswith('.htm'):
			sts, data = self.getPage(URL)
			if sts:
				link_ = re.findall('<source[^>]+src=["\'](.*?)["\']', data, re.I)
				if link_:
					urlTab.append({'name': cItem['title'], 'url': link_[0], 'need_resolve': 0})
				else:
					link_ = re.findall('file: "(.*?)"', data, re.S)
					if link_:
						urlTab.append({'name': cItem['title'], 'url': link_[0], 'need_resolve': 0})
		else:
			urlTab.append({'name': cItem['title'], 'url': URL, 'need_resolve': 0})
		return urlTab
	def start(self,cItem):
		mode=cItem.get('mode', None)
		if mode=='00':
			self.showmenu(cItem)
		if mode=='10':
			self.showmenu1(cItem)
		if mode=='11':
			self.showmenu2(cItem)
		if mode=='12':
			self.showmenu3(cItem)
		if mode=='20':
			self.showmenu4(cItem)
		if mode=='40':
			self.showmenu20(cItem)
		if mode=='21':
			self.showaudiomenu1(cItem)
		if mode=='22':
			self.showaudio1(cItem)
		if mode=='31':
			self.showserieaudiomenu1(cItem)
		if mode=='32':
			self.showserievidmenu1(cItem)
		if mode=='33':
			self.showvid1(cItem)
		if mode=='18':
			self.showmenudourous(cItem)
		if mode=='14':
			self.showmenu14(cItem)
		if mode=='15':
			self.showmenu15(cItem)
		if mode=='16':
			self.showmenu16(cItem)
		if mode=='17':
			self.showmenu17(cItem)
		if mode=='19':
			self.showmenu19(cItem)
		if mode=='30':
			self.showmenu30(cItem)
		return True