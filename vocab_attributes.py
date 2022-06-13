import requests
from bs4 import BeautifulSoup as soup
import random
import json
class Vocab():

    def __init__(self,word) -> None:
        self.word = word.lower()
        url_ox = f"https://www.oxfordlearnersdictionaries.com/definition/english/{self.word}_1?q={self.word}"
        url_trs = f"https://www.thesaurus.com/browse/{self.word}"
        url_voc = f"https://www.vocabulary.com/dictionary/{self.word}"
        self.user_agent = []
        self.pos = ''
        self.defi = ''
        self.sentence = []
        self.synonyms = []
        self.antonyms = []
        self.wordfamilies = []
# call method
        self.user()
        self.part_find(url_ox)
        self.defi_find(url_ox)
        self.example(url_ox)
        self.synonym_find(url_trs)
        self.antonyms_find(url_trs)
        self.wordfamily(url_voc)

    def user(self):
        f = open("user-agents.txt","r")
        for i in f.read().splitlines(): 
            self.user_agent.append(i)
        self.user_agent = self.user_agent[random.randint(0,len(self.user_agent))-1]


    def part_find(self,url_ox):
        req = requests.get(url_ox,headers={
            "user-agent" : self.user_agent
        })
        if req.status_code == 404:
            return False
        else :
            pofs = soup(req.text,'html.parser')
            posx = pofs.find('span',{"class" : "pos"})
            if type(posx) == type(None):
                self.pos ='-'
                return False
            self.pos = posx.get_text()
            return self.pos

    def defi_find(self,url_ox):
        req = requests.get(url_ox,headers={
            'user-agent' : self.user_agent
        })
        if req.status_code == 404:
            return False
        else :
            defi = soup(req.text,'html.parser')
            defix = defi.find('span',{"class" : "def"})
            self.defi = defix.get_text()
            return self.defi
    
    def example(self,url_ox):
        req = requests.get(url_ox,headers={
            "user-agent" : self.user_agent
        })
        if req.status_code == 404:
            self.sentence = '-'
            return False
        else :
            exam = soup(req.text,'html.parser') 
            if exam.find_all('span',{"class" : "x"}) == []:
                self.sentence = ''
                return False
            for ex in exam.find_all('span',{"class" : "x"}):
                self.sentence.append(ex.get_text())
            random.shuffle(self.sentence)
            self.sentence = random.choices(self.sentence, k = 1)
            return self.sentence
    
    def synonym_find(self,url_trs):
        req = requests.get(url_trs,headers={
            "user-agent" : self.user_agent
        })
        if req.status_code == 404:
            self.synonyms = '-'
            return False
        else :
            syn = soup(req.text,'html.parser')
            if  syn.find_all('a',{"class" : "css-1kg1yv8 eh475bn0"}) == []:
                self.synonyms = '-'
                return False
            for synx in syn.find_all('a',{"class" : "css-1kg1yv8 eh475bn0"}):
                self.synonyms.append(synx.get_text())
            random.shuffle(self.synonyms)
            self.synonyms = random.choices(self.synonyms ,k=3)
            return self.synonyms
    
    def antonyms_find(self,url_trs):
        req = requests.get(url_trs,headers={
            "user-agent" : self.user_agent
        })
        if req.status_code == 404:
            self.antonyms = '-'
            return False
        else :
            ant = soup(req.text,'html.parser')
            if ant.find_all('a',{"class" : "css-15bafsg eh475bn0"}) == []:
                self.antonyms = '-'
                return False
            for antx in ant.find_all('a',{"class" : "css-15bafsg eh475bn0"}):
                self.antonyms.append(antx.get_text())
            random.shuffle(self.antonyms)
            self.antonyms = random.choices(self.antonyms,k=3) 
            return self.antonyms

    def wordfamily(self,url_voc):
        req = requests.get(url_voc,headers={
            "user-agent" : self.user_agent
        })
        fam = soup(req.text,'html.parser')
        if type(fam.find('div',{"class" : "word-area"})) == type(None):
            self.wordfamilies = '-'
            return False
        else :
            famx = fam.find("vcom:wordfamily")
            famx_en = json.loads(famx['data'])
            for i in famx_en:
               self.wordfamilies.append(i['word'])
            random.shuffle(self.wordfamilies)
            self.wordfamilies = random.choices(self.wordfamilies,k=5)
            return self.wordfamilies


    
