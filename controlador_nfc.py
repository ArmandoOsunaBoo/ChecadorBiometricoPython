import board
## 
###
import os 
import busio
from digitalio import DigitalInOut
from adafruit_pn532.i2c import PN532_I2C
import board
import busio
from cv2 import cv2
from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_B
from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_A
from adafruit_pn532.i2c import PN532_I2C

class Controlador_NFC():

    def __init__(self):
        print("Iniciando Conexión con PN532")
    
    def escribir_tarjeta(self,numero_empleado,frame):
        error=0
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            pn532 = PN532_I2C(i2c, debug=False)
            ic, ver, rev, support = pn532.firmware_version
            print("Encontrado dispositivo PN532 con la version: {0}.{1}".format(ver, rev)) 
            pn532.SAM_configuration() 
            print("Version Clasicc MIFARE V1!")

            key = b"\xFF\xFF\xFF\xFF\xFF\xFF" 
            while True:
                # Check if a card is available to read
                uid = pn532.read_passive_target(timeout=0.5) 
                # Try again if no card is available.
                if uid is not None:
                    break
    
            print("\n") 
            print("bandera 0")

            authenticated = pn532.mifare_classic_authenticate_block(uid, 4, MIFARE_CMD_AUTH_B, key)
            if not authenticated:
                print("AUtenticación fallida!")

            # Set 16 bytes of block to 0xFEEDBEEF
            data = bytearray(4)
            val="-----------"+str(numero_empleado)
            print(val)
            val = val.encode('UTF-8')
            data[0:4] = bytearray(val)
            print("bandera 1")
            #Antes de asignar el numero de empleado a la tarjeta primero realizamos la comprobacion de si hay una foto de empleado para borrarla
            a = pn532.mifare_classic_read_block(4)
            a = a.decode('utf-8')
            
            numempleado=a
            numempleado= numempleado[11:17]
            print("### "+numempleado)
            filename = os.getcwd()+"/fotos_empleados/"+str(numempleado)+".png"
            if os.path.exists(filename):
                os.remove(filename)
                print("imagen borrada de "+numempleado)
            else:
                print("No se ha podido remover %s." % filename)

            print("bandera 2")
            # Write 16 byte block.
            pn532.mifare_classic_write_block(4, data)
            print(pn532.mifare_classic_read_block(4))
            cv2.imwrite( os.getcwd()+"/fotos_empleados/"+str(numero_empleado)+".png", frame[0:250, 95:300])
            # Read block #6
            print("-------------------------") 
        except Exception as e:
            try:
                i2c = busio.I2C(board.SCL, board.SDA)
                pn532 = PN532_I2C(i2c, debug=False)
                ic, ver, rev, support = pn532.firmware_version
                print("Dispositivo PN532 encontrado con la version: {0}.{1}".format(ver, rev))
                # Configure PN532 to communicate with MiFare cards
                pn532.SAM_configuration()

                print("Version TAG203 A-3") 
                while True:
                    # Check if a card is available to read
                    uid = pn532.read_passive_target(timeout=0.5)
                    print(".", end="")
                    # Try again if no card is available.
                    if uid is not None:
                        break

                #foto
                a = pn532.ntag2xx_read_block(6)
                a = a.decode('utf-8')
                
                b = pn532.ntag2xx_read_block(7)
                b = b.decode('utf-8') 
                numempleado= str(a[3:4])+str(b)

                filename = os.getcwd()+"/fotos_empleados/"+str(numempleado)+".png"
                if os.path.exists(filename):
                    os.remove(filename)
                    print("imagen borrada de "+numempleado)
                else:
                    print("No se ha podido remover %s." % filename)
                
                
                
                data2 = bytearray(4) 
                
                val=str(numero_empleado[1:])
                val = val.encode('UTF-8')
                data = bytearray(4)
                val2=str("000")+numero_empleado[:1]
                val2 = val2.encode('UTF-8')
                data[0:4] =bytearray(val2)



                data2[0:4] = bytearray(val)
                # Write 4 byte block.
                pn532.ntag2xx_write_block(6, data)
                pn532.ntag2xx_write_block(7, data2)
                cv2.imwrite( os.getcwd()+"/fotos_empleados/"+str(numero_empleado)+".png", frame[0:250, 95:300])
                # Read block #6
                print("-------------------------")
                print(pn532.ntag2xx_read_block(6))
                print(pn532.ntag2xx_read_block(7))
                print("-------------------------")
                
            except Exception as ex:
                print("Error: "+str(ex))
                error=1



        return error

    
    def leer_tarjeta(self):
        error=0
        numempleado=""
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            pn532 = PN532_I2C(i2c, debug=False)
            ic, ver, rev, support = pn532.firmware_version
            print("Encontrado dispositivo PN532 con la version: {0}.{1}".format(ver, rev)) 
            pn532.SAM_configuration() 
            print("Esperando dispoditivo NFC! version MIFARE CLASIC V1")

            key = b"\xFF\xFF\xFF\xFF\xFF\xFF" 
            while True:
                # Check if a card is available to read
                uid = pn532.read_passive_target(timeout=0.5) 
                # Try again if no card is available.
                if uid is not None:
                    break
    
            print("\n") 
            print("bandera 1")
            authenticated = pn532.mifare_classic_authenticate_block(uid, 4, MIFARE_CMD_AUTH_B, key)
            if not authenticated:
                print("AUtenticación fallida!")
            print("bandera 2")
            print(pn532.mifare_classic_read_block(4))
            numempleado=pn532.mifare_classic_read_block(4) 
            numempleado = numempleado.decode('utf-8') 
            print("bandera 3")
            numempleado= numempleado[11:17]
            print("### "+numempleado)
            print("bandera 4")
        except Exception as e:
            try:
                i2c = busio.I2C(board.SCL, board.SDA)
                pn532 = PN532_I2C(i2c, debug=False)
                ic, ver, rev, support = pn532.firmware_version
                print("Dispositivo PN532 encontrado con la version: {0}.{1}".format(ver, rev))
                # Configure PN532 to communicate with MiFare cards
                pn532.SAM_configuration()

                print("Esperando por tarjeta FID/NFC!")
                while True:
                    # Check if a card is available to read
                    uid = pn532.read_passive_target(timeout=0.5)
                    print(".", end="")
                    # Try again if no card is available.
                    if uid is not None:
                        break
                
                # Read block #6
                print("-------------------------")
                print(pn532.ntag2xx_read_block(6))
                print(pn532.ntag2xx_read_block(7))
                print("-------------------------")
                a = pn532.ntag2xx_read_block(6)
                a = a.decode('utf-8')
                
                b = pn532.ntag2xx_read_block(7)
                b = b.decode('utf-8') 
                numempleado= str(a[3:4])+str(b)
                print(a[3:4])
                print(a[1:])



                print("### "+numempleado)
            except Exception as ex:
                print("Error: "+str(ex))
                numempleado=-1



        
        return numempleado
        


    