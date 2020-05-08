import os
from bs4 import BeautifulSoup,Tag

TMP_FOLDER = './pages/'

class WebPages:
     def __init__(self,path_pr:dict,sv_addr='127.0.0.1'):
          text = []
          prev = 0
          for path in path_pr:
               if path_pr[path] < 0:
                    continue
               if path_pr[path] == 0:
                    continue
               if path_pr[path] < prev:
                    text.append(path)
               else:
                    prev = path_pr[path]
                    text = [path] + text
               print(path,path_pr[path])

          self.list_of_pages = text
          self.links = f'<body>'
          for t in self.list_of_pages:
               tag = 'link'
               description = ""
               x = t
               with open(x) as f:
                    soup = BeautifulSoup(f.read(),'html.parser')
                    try:
                         tag = soup.find('title').text
                         
                    except AttributeError as e:
                         print('Erro:',e)
                         print(soup.text)
                         tag = t.replace(TMP_FOLDER,'')

                    try:
                         description = soup.find('body').text
                         description = description.split(' ')
                         d = ''
                         if len(description) >= 50:
                              for i in range(50):
                                   d += description[i]+' '
                              d = d[:-1]+"..."
                         else:
                              for i in range(len(description)):
                                   d += description[i]+' '
                         
                         description = d

                    except AttributeError as e:
                         print('Erro:',e)
                    
               self.links += f'<div class = "link"><a href = "//{sv_addr}/{x}">{tag}</a>{description}</div>'
          self.links = self.links.replace('\n','')
          self.links = self.links.replace('\t','')
          self.links += '</body>'








def LookFor(query:str,folder:str):
     html_files = dict()

     for pwd,sub_folders,files in os.walk(f'{folder}'):
          print(pwd,sub_folders,files)
          for file in files:
               if not file.endswith('.html'):
                    continue
               if pwd.endswith('/'):
                    with open(pwd+file) as f:
                         soup = BeautifulSoup(f.read(),'html.parser')
                         html_files[pwd+file] = soup.find('body').text.lower().count(query)
                         html_files[pwd+file] += soup.find('title').text.lower().count(query) * 2
                         if soup.find('body').text == '':
                              html_files[pwd+file] = -100
               else:
                    with open(pwd+'/'+file) as f:
                         soup = BeautifulSoup(f.read(),'html.parser')
                         html_files[pwd+'/'+file] = soup.find('body').text.lower().count(query)
                         html_files[pwd+'/'+file] += soup.find('title').text.lower().count(query) * 2
                         if soup.find('body').text == '':
                              html_files[pwd+'/'+file] = -100

     link_text = []
     server_addr = '127.0.0.1'
     wbp = WebPages(html_files,server_addr)
     return wbp.links

     with open('index.html','w') as f:
          f.write(wbp.links)
          return wbp.links