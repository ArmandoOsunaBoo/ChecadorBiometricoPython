import pymysql
from openpyxl import Workbook

class BaseDeDatos():

    def __init__(self,host, user, password,db,port):
        self.host=host
        self.user=user
        self.password=password
        self.db=db
        self.port=port
        print(self.password)
    
    def obtenerChecadas(self,fecha_inicio,fecha_final ):
        wb = Workbook()

        # grab the active worksheet
        ws = wb.active
        self.conexion = pymysql.connect(host=self.host,
                                 user=self.user,
                                 password=self.password,
                                 port=self.port,
                                 db=self.db)
        try:
            try:
                with self.conexion.cursor() as cursor:
                    # En este caso no necesitamos limpiar ningún dato
                    cursor.execute("SELECT * FROM checadas WHERE fecha>= \"" +fecha_inicio+"\" AND fecha <= \""+fecha_final+"\";")
                    # Con fetchall traemos todas las filas
                    checadas = cursor.fetchall()
                    ws.append(["Tiempo","Apellido","Estado","Nombre de Dispositivo"])
                    
                    # Recorrer e imprimir
                    for checada in checadas:
                        print(checada[0])
                        ws.append([checada[1],checada[2],checada[3],checada[4]])
                    wb.save("DataResult.xlsx")

                    return 0, ""
            finally:
                self.conexion.close()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
            return -1,e


    def insertRegistro(self,fecha,numempleado,evento,checador,fechac,h): 
        self.conexion = pymysql.connect(host=self.host,
                                 user=self.user,
                                 password=self.password,
                                 port=self.port,
                                 db=self.db)
        
        cursor=self.conexion.cursor()
        try:
            sql = "INSERT INTO `checadas` ( `fechacompleta`, `numempleado`, `evento`, `checador`,`fecha`,`hora`) VALUES (%s, %s, %s, %s,%s, %s)"

            # Execute the query
            cursor.execute(sql, (fecha,numempleado,evento,checador,fechac,h))

            # the connection is not autocommited by default. So we must commit to save our changes.
            self.conexion.commit()
        
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
        finally:
            self.conexion.close()

    