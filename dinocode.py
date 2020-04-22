import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import requests,time
import pswrd
urlBase = "http://192.168.0.9/"
filebase = 'image_'
     
key = pswrd.Key2

def Get_Image(filename):
     try:
          #value = requests.get(urlBase + 'start') #start saving images
          #time.sleep(.1)
          #value = requests.get(urlBase + 'stop')  #stop - you can get rid of this if you want a continuous stream
          #time.sleep(.1)
          value = requests.get(urlBase + 'download')
          time.sleep(.25)
          f = open('/Users/Morgan.Strong/Desktop/IMGS/' + filename,'wb')
          f.write(value.content)
          f.close()
          result = True
     except Exception as e:
          print(e)
          result = False
     return result

def findDino(filename):
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)
    # Load the model
    model = tensorflow.keras.models.load_model('keras_model.h5')

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open('/Users/Morgan.Strong/Desktop/IMGS/' + filename)

    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    #turn the image into a numpy array
    image_array = np.asarray(image)

    # display the resized image
    #image.show()

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    print(prediction)
    return prediction
## TAKEN FROM LEGO SORTER 2
def SL_setup():
     urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/"
     headers = {"Accept":"application/json","x-ni-api-key":key}
     return urlBase, headers
     
def Put_SL(Tag, Type, Value):
     urlBase, headers = SL_setup()
     urlValue = urlBase + Tag + "/values/current"
     propValue = {"value":{"type":Type,"value":Value}}
     try:
          reply = requests.put(urlValue,headers=headers,json=propValue).text
     except Exception as e:
          print(e)         
          reply = 'failed'
     return reply

def Get_SL(Tag):
     urlBase, headers = SL_setup()
     urlValue = urlBase + Tag + "/values/current"
     try:
          value = requests.get(urlValue,headers=headers).text
          data = json.loads(value)
          #print(data)
          result = data.get("value").get("value")
     except Exception as e:
          print(e)
          result = 'failed'
     return result
     
def Create_SL(Tag, Type):
     urlBase, headers = SL_setup()
     urlTag = urlBase + Tag
     propName={"type":Type,"path":Tag}
     try:
          requests.put(urlTag,headers=headers,json=propName).text
     except Exception as e:
          print(e) 




counter = 0
while True:
    filename = filebase + str(counter) + '.jpg'
    Get_Image(filename)
    counter += 1
    try:
         predic = findDino(filename)
         predic = predic.tolist()
         val = 0
         for i in range(4):
             if predic[0][i] > val:
                 dinoflag = i
                 val = predic[0][i]
         if dinoflag == 0:
              Put_SL('dino1', 'STRING', '1')
              print("DINO 1")
         if dinoflag == 1:
              Put_SL('dino2', 'STRING', '1')
              print("DINO 2")
         if dinoflag == 2:
              Put_SL('dino3', 'STRING', '1')
              print("DINO 3")
         if dinoflag == 3:
              Put_SL('dino4', 'STRING', '1')
              print("Dino 4")
    except:
         print("FAIL")
          




