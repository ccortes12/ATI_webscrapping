import web_scrapping
import connection

def welcome():

    print('Pronostico oleaje Webscrapper \n'
          'desarrollado por Carlos Cortes - ccortes@gmail.com \n\n')

if __name__ == '__main__':

    welcome()

    #Metodo para obtener los datos
    data = web_scrapping.collectData()

    #Metodo para guardar
    connection.saveData(data)



