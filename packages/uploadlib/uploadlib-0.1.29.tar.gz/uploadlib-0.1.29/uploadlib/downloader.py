from requests import get
def download(url,path):
  myfile=get(url)
  w=open(path,"wb+")
  w.write(myfile.content)
  w.close()
  return open(path,'r').read()