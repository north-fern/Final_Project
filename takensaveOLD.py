import requests, time
urlBase = "http://192.168.0.14/"
filebase = 'image_'
     
def Get_Image(filename):
     try:
          value = requests.get(urlBase + 'start') #start saving images
          time.sleep(.1)
          value = requests.get(urlBase + 'stop')  #stop - you can get rid of this if you want a continuous stream
          time.sleep(.1)
          value = requests.get(urlBase + 'download')
          f = open('/Users/Morgan.Strong/Desktop/IMGS/' + filename,'wb')
          f.write(value.content)
          f.close()
          result = True
     except Exception as e:
          print(e)
          result = False
     return result

counter = 0;

while True:
    filename = filebase + str(counter) + '.jpg'
    Get_Image(filename)
    counter += 1
    
