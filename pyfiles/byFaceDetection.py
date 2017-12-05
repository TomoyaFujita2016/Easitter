try:
    import cv2 
except:
    pass
def detectFace(image):
    cascadePath = "/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml"
    FACE_SHAPE = 0.45
    result = image.copy()
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(cascadePath)
    faceRect = cascade.detectMultiScale(imageGray, scaleFactor=1.1, minNeighbors=1, minSize=(1,1))
    
    if len(faceRect) <= 0:
        return False
    else:
        # confirm face
        imageSize = image.shape[0] * image.shape[1]
        #print("d1")
        filteredFaceRects = []
        for faceR in faceRect:
            faceSize = faceR[2]*faceR[3]
            if FACE_SHAPE > min(faceR[2], faceR[3])/max(faceR[2], faceR[3]):
                break
            filteredFaceRects.append(faceR)
        
        if len(filteredFaceRects) > 0:
            return True
        else:
            return False
