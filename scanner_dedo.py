import tempfile
from pyfingerprint.pyfingerprint import PyFingerprint
from cv2 import cv2
from os import path
import os

class ScanerHuella():

    def __init__(self):
        print("inicializacion de scanner")
    
    def compararHuella(self,numempleado):
        ## Intentamos inicializar la huella
        try:
            f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

            if ( f.verifyPassword() == False ):
                raise ValueError('The given fingerprint sensor password is wrong!')

        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))
            exit(1)

        ## Gets some sensor information
        print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

        ## Tries to read image and download it
        try:
            print('Waiting for finger...')

            ## Wait that finger is read
            while ( f.readImage() == False ):
                pass

            print('Downloading image (this take a while)...')

            imageDestination =  os.getcwd()+'/'+'example.bmp'
            f.downloadImage(imageDestination)

            print('The image was saved to "' + imageDestination + '".')

        except Exception as e:
            print('Operation failed!')
            print('Exception message: ' + str(e))
            exit(1)
        
        ##Aqui empieza la comparación de la huella
        test_original = os.getcwd()+'/'+'example.bmp'
        for x in range(0, 3):
            fingerprint_database_image = cv2.imread("./dataset_huella/"+x+'_'+numempleado)
            
            sift = cv2.xfeatures2d.SIFT_create()
            
            keypoints_1, descriptors_1 = sift.detectAndCompute(test_original, None)
            keypoints_2, descriptors_2 = sift.detectAndCompute(fingerprint_database_image, None)
        ##
        matches = cv2.FlannBasedMatcher(dict(algorithm=1, trees=10), 
             dict()).knnMatch(descriptors_1, descriptors_2, k=2)
        match_points = []
   
        for p, q in matches:
            if p.distance < 0.1*q.distance:
                match_points.append(p)
            keypoints = 0
            if len(keypoints_1) <= len(keypoints_2):
                keypoints = len(keypoints_1)            
            else:
                keypoints = len(keypoints_2)
            if (len(match_points) / keypoints)>0.95:
                print("% match: ", len(match_points) / keypoints * 100)
                print("Figerprint ID: " + str(file)) 
                result = cv2.drawMatches(test_original, keypoints_1, fingerprint_database_image, keypoints_2, match_points, None) 
                result = cv2.resize(result, None, fx=2.5, fy=2.5)
                cv2.imshow("result", result)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                break;
        
    def obtenerHuella(self,contador,numempleado):
        ## Intentamos inicializar la huella
        try:
            f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

            if ( f.verifyPassword() == False ):
                raise ValueError('The given fingerprint sensor password is wrong!')

        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))
            #exit(1)

        ## Gets some sensor information
        #print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

        ## Tries to read image and download it
        try:
            print('Waiting for finger...')

            ## Wait that finger is read
            while ( f.readImage() == False ):
                pass

            print('Downloading image (this take a while)...')

            imageDestination =  os.getcwd()+ '/dataset_huella/'+str(contador)+'_'+str(numempleado)+'.bmp'
            f.downloadImage(imageDestination)

            print('The image was saved to "' + imageDestination + '".')

        except Exception as e:
            print('Operation failed!')
            print('Exception message: ' + str(e))
            #exit(1)
