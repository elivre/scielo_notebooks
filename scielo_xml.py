
# coding: utf-8


from lxml import etree

class parse_xml(object):

    def __init__(self, url_xml):
        self.tree = etree.parse(url_xml)
        self.scielo_id = self.tree.xpath('/article/front/article-meta/article-id')[0].text

    def get_title(self):
        t=self.tree.xpath('/article/front/article-meta/title-group/article-title')
        titulo = {}
        titulo['scielo_id'] = self.scielo_id
        if t == []:
            n= ''
        else:
            n= t[0].text
        titulo['title'] = n
        return titulo

    def get_abstract(self):
        a=self.tree.xpath('/article/front/article-meta/abstract[@xml:lang="en"]')
        abstract={}
        abstract['scielo_id'] = self.scielo_id
        if a == []:
            r = ''
        else:
            r =(a[0][0].text)
        abstract['abstract'] = r
        return abstract
    
    def get_resumo(self):
        a=self.tree.xpath('/article/front/article-meta/abstract[@xml:lang="pt"]')
        resumo={}
        resumo['scielo_id'] = self.scielo_id
        if a == []:
            r = ''
        else:
            r =(a[0][0].text)
        resumo['resumo'] = r
        return resumo

    
    def get_keywords(self):
        ks=self.tree.xpath('/article/front/article-meta/kwd-group/kwd[@lng="en"]') 
        keywords = {}
        keywords['scielo_id'] = self.scielo_id
        kwlista = []
        for k in ks:
            kwlista.append(k.text)
        keywords['keywords'] = kwlista
        return keywords
 

    def get_palavras_chave(self):
        ks=self.tree.xpath('/article/front/article-meta/kwd-group/kwd[@lng="pt"]') 
        palavras_chave = {}
        palavras_chave['scielo_id'] = self.scielo_id
        plista = []
        for k in ks:
            plista.append(k.text)
        palavras_chave['palavras_chave'] = plista
        return palavras_chave

    
    def get_autores(self):
        autors=self.tree.xpath('/article/front/article-meta/contrib-group/contrib[@contrib-type="author"]')
        autores = {}
        autores['scielo_id'] = self.scielo_id
        alista = []
        for a in autors:
            autor = {}
            autor['surname'] = a[0][0].text
            autor['given_names'] = a[0][1].text
            alista.append(autor)
        autores['autores'] = alista
        return autores
    
    def get_instituicoes(self):
        ins=self.tree.xpath('/article/front/article-meta/aff')
        insts=[]
        sq = 1
        for i in ins:
            inst = {}
            inst['scielo_id'] = self.scielo_id
            inst['seq'] = str(sq)
            inst['instituicao'] = i[0].text
            inst['localidade'] = i[1].text
            inst['pais'] = i[2].text
            insts.append(inst)
            sq=sq+1
        return insts
    
    def get_referencias(self):     
        refs=self.tree.xpath('/article/back/ref-list/ref')
        referencias = []
        for r in refs:
            referencia={}
            referencia['scielo_id']=self.scielo_id
            referencia['ref_id'] = r.attrib['id']
            citation_type = r[0].attrib['citation-type']
            referencia['citation_type'] = citation_type
            if citation_type == 'journal':
                #citation_type = i.attrib['citation-type']
                referencia['article_title'] = r[0][1].text
                at = (r[0][1].attrib).values()
                referencia['article_lang'] = ''.join(at)
                referencia['source'] = r[0][2].text
                referencia['year'] = r[0][3].text
                referencia['volume'] = r[0][4].text
                referencia['page_range'] = r[0][5].text
                referencias.append(referencia)
                print(referencia)
            elif citation_type == 'book':
                print(len(r[0]))
                referencia['source'] = r[0][1].text
                referencia['year'] = r[0][2].text
                referencia['publisher_loc'] = r[0][3].text
                #referencia['publisher_name'] = r[0][4].text
                referencias.append(referencia)
        return referencias
    
    def get_autores_ref(self):
        autores=self.tree.xpath('/article/back/ref-list/ref/nlm-citation/person-group[@person-group-type="author"]/*')
        ref_autores = []        
        seq = 1
        for autor in autores:
            ref_autor = {}
            ref_autor['scielo_id']=self.scielo_id
            ref_autor['surname'] = autor[0].text
            ref_autor['given_names'] = autor[1].text
            ref_autores.append(ref_autor)
            seq=seq+1
        return ref_autores        

    def get_referencia_autores(self):  
        refs=self.tree.xpath('/article/back/ref-list/ref')
        ref_autor = {}
        ref_autores = []
        for ref in refs:
            scielo_id=self.scielo_id
            ref_id=ref.attrib['id']
            citation_type = ref[0].attrib['citation-type']

            #print(ref)
            source = ref[0][1].text
            if ref[0][0] != []:
                person_group = ref[0][0].attrib['person-group-type']

                autores = ref[0][0]
                
                #print(autores)
                seq = 1
                if autores != {}:
                    for autor in autores:
                        ref_autor['scielo_id'] = scielo_id
                        ref_autor['ref_id'] = ref_id
                        ref_autor['citation_type'] = citation_type
                        ref_autor['person_group'] = person_group
                        ref_autor['seq'] = str(seq)
                        ref_autor['surname'] = autor[0].text
                        ref_autor['given_names'] = autor[1].text
                        ref_autor['source']=source
                        ref_autores.append(ref_autor)
                        seq=seq+1
                        ref_autor={}
        return ref_autores

    def get_texto(self): 
        r=self.tree.xpath('/article/body')
        texto=[]
        seq=1
        for b in r:
            paragrafo={}
            paragrafo['scielo_id'] = scielo_id
            if b.text != None:
                paragrafo['seq']=str(seq)
                paragrafo['texto']=b.text
                texto.append(paragrafo)
                seq=seq+1
        return texto
    
    def get_referencias_journal(tree):     
        print('========== ref ==================')
        r=tree.xpath('/article/back/ref-list/ref/nlm-citation[@citation-type="journal"]/*')
        nomes = []
        for i in r:
            print(i.text)
            #nome = [i[0].text]+[i[1].text]
            #nomes.append(nome)
        return nomes
    
    def get_referencias_nomes(tree):     
        print('========== ref ==================')
        r=tree.xpath('/article/back/ref-list/ref/nlm-citation/person-group/name')
        nomes = []
        for i in r:
            nome = [i[0].text]+[i[1].text]
            nomes.append(nome)
        return nomes

    def get_referencias_source(tree):     
        print('========== ref ==================')
        r=tree.xpath('/article/back/ref-list/ref/nlm-citation/source')
        fontes = []
        for i in r:
            fontes.append(i.text)
        return fontes

    def get_book_autores(tree):
        n=tree.xpath('/article/back/ref-list/ref/nlm-citation[@citation-type="book"]/person-group[@person-group-type="author"]/name')
        nomes = []
        for i in n:
            nome = [i[0].text]+[i[1].text]
            nomes.append(nome)
        return nomes

# Exemplo de utilização:
# 
# url_xml = 'file:///home/neilor/SCIELO_DADOS/dados/artigos_xml/S1415-47571998000100002.xml'
# 
# 
# xml = Scielo_XML(url_xml)
# print(xml.get_texto())
# 
# 
#     

# url_xml = 'file:///home/neilor/SCIELO_DADOS/dados/artigos_xml/S0034-73292013000200005.xml'
# 
# xml = Scielo_XML(url_xml)
# refs = (xml.get_referencia_autores())
# print("============================")
# for ref in refs:
#     print(ref)
#     print('-----------------------------------------')



import re


def normaliza_nome(nome):
    nome1 = nome.upper()
    nome2 = nome1.replace('Y','I')
    nome3 = nome2.replace('LL','L')

    rh = re.compile('^H')
    eh = re.compile('H$')
    
    n0 = nome3
    n1=re.sub('[Á|á|À|à|Â|â|Ã|ã|Ä|ä]','A',n0)
    n2=re.sub('[É|é|È|è|Ê|ê|Ẽ|ẽ|Ë|ë]','E',n1)
    n3=re.sub('[Í|í|Ì|ì|Î|î|Ĩ|ĩ|Ï|ï]','I',n2)
    n4=re.sub('[Ó|ó|Ò|ò|Ô|ô|Õ|õ|Ö|ö]','O',n3)
    n5=re.sub('[Ú|ú|Ù|ù|Û|û|Ũ|ũ|Ü|ü]','U',n4)
    n6=re.sub('[Ý|ý|Ỳ|ỳ|Ŷ|ŷ|Ỹ|ỹ|Ÿ|ÿ]','I',n5)
    n7=re.sub('[Ç|ç]','C',n6)
    n8=n7.upper()
    n9=n8.replace('LL','L')
    n10=n9.replace('NN','N')
    n11=n10.replace('EE','E')
    n12=n11.replace('TT','T')
    n13=n12.replace('SS','S')
    n14=n13.replace('PH','F')
    n15=rh.sub('',n14)
    n16=eh.sub('',n15)
    n17=n16.replace('TH','T')
    n18=n17.replace('RR','R')
    n19=n18.replace('MM','M')
    n20=n19.replace('CC','C')
    n21=n20.replace('AA','A')
    n22=n21.replace('W','V')
    n23=n22.replace('BB','B')
    n24=n23.replace('DD','D')
    n25=n24.replace('HH','H')
    
    
    return re.sub('[\s+]', '', n25)


