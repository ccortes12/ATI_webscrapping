#Conexion a bd
import pyodbc
import datetime
from decouple import config

server = config('SERVER')
db = config('DATABASE')
user = config('USER')
password = config('PASSWORD')

def checkConnection():
    try:
        conection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL server}; ' +
                                   'SERVER='+ server + ';' +
                                   'DATABASE=' + db + ';' +
                                   'UID=' + user + ';' +
                                    'PWD=' + password)
        return True, conection.cursor()

    except Exception as e:
        print('ERROR:', e.__str__())
        return False


def insert(cursor, utc_3, viento_dir, viento_mag, viento_fuerza, oleaje_dir, oleaje_tp, oleaje_hm):

    fecha,hora = utc_3.split(' ')
    fecha = fecha.split('-')
    hora = hora.split(':')
    fecha_registro = datetime.datetime(int('20'+ fecha[2]), int(fecha[1]), int(fecha[0]),int(hora[0]),int(hora[1]))

    try:
        # Do the insert
        cursor.execute("insert into dbo.tb_awac_Pronostico(utc_3, fecha_registro, viento_dir, viento_mag, viento_fuerza, oleaje_dir, oleaje_tp, oleaje_hm) " +
                       "values (?,?,?,?,?,?,?,?)",utc_3, fecha_registro, viento_dir, viento_mag, viento_fuerza, oleaje_dir, oleaje_tp, oleaje_hm)
        # commit the transaction
        cursor.commit()
    except Exception as e:
        print('ERROR:', e.__str__())

def delete(cursor,utc_3):

    try:
        cursor.execute("delete from dbo.tb_awac_Pronostico where utc_3 = ?",utc_3)
        # commit the transaction
        cursor.commit()
    except Exception as e:
        print('ERROR:', e.__str__())

def update(cursor, utc_3, viento_dir, viento_mag, viento_fuerza, oleaje_dir, oleaje_tp, oleaje_hm):

    fecha, hora = utc_3.split(' ')
    fecha = fecha.split('-')
    hora = hora.split(':')
    fecha_registro = datetime.datetime(int('20' + fecha[2]), int(fecha[1]), int(fecha[0]), int(hora[0]), int(hora[1]))

    try:
        cursor.execute("update dbo.tb_awac_Pronostico set fecha_registro=?, viento_dir=?, viento_mag=?, viento_fuerza=?, oleaje_dir=?, "
                       "oleaje_tp=?, oleaje_hm=? where utc_3=?", fecha_registro, viento_dir, viento_mag, viento_fuerza, oleaje_dir, oleaje_tp, oleaje_hm,utc_3)
        # commit the transaction
        cursor.commit()
    except Exception as e:
        print('ERROR:', e.__str__())

def exists(cursor,utc_3):
    #Retorna el numero de ocurrencias
    try:
        resultado = cursor.execute("select count(utc_3) from dbo.tb_awac_Pronostico where utc_3=?", utc_3)
        return resultado.fetchone()[0]
    except Exception as e:
        print('ERROR:', e.__str__())

def saveData(data):

    print('Conectando con la base de datos...')

    # Chequear conexion y obtener cursor
    if (checkConnection()):

        resultado, cursor = checkConnection()

        print('Conexion establecida con exito...')

        for utc_3, viento_dir, viento_mag, viento_fuerza, oleaje_dir, oleaje_tp, oleaje_hm in data:
            # En caso de que exista el registro se actualiza, caso contrario se inserta
            if (exists(cursor, utc_3) == 0):
                insert(cursor, utc_3, viento_dir, viento_mag, viento_fuerza, oleaje_dir, oleaje_tp,
                                  oleaje_hm)
                continue
            update(cursor, utc_3, viento_dir, viento_mag, viento_fuerza, oleaje_dir, oleaje_tp, oleaje_hm)

        cursor.close()
        print('----- Fin registro de datos ----- \n')

    else:
        print('ERROR: no fue posible establecer conexion con la base de datos')
