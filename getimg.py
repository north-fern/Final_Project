import requests,time

urlBase = "http://192.168.0.14/"
     
def Get_Image():
     try:
          value = requests.get(urlBase + 'start') #start saving images
          time.sleep(.1)
          value = requests.get(urlBase + 'stop')  #stop - you can get rid of this if you want a continuous stream
          time.sleep(.1)
          value = requests.get(urlBase + 'download')
          f = open('/Users/Morgan.Strong/Desktop/file1.jpg','wb')
          f.write(value.content)
          f.close()
          result = True
     except Exception as e:
          print(e)
          result = False
     return result

Get_Image()
