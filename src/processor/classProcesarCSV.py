import math, statistics
from logger import err_logger

class procesarCSV:
    
    def __init__ (self, fichero):
        """
        Carga el csv con las interpretaciones y devuelve las tablas (listas), para generar las gráficas
        
        :param fichero: Ruta a fichero CSV
        :type fichero: str
        """           

        self.NOTAS = []             # Cargar notas
        self.GRAFNOTAS = []         # Gráfica de notas
        self.ESTNOTAS = []          # Valores significativos de notas
        self.RESPxPREG = []         # Respuestas por pregunta
        self.DISCRIMINACION = []    # Discriminación
        self.FACILIDAD = []         # Facilidad
        self.AUDITxPREG = []        # Auditoria por pregunta
        self.MARCAJESPREG = []      # Marcajes de cada pregunta
        self.RESPCORR = []          # Respuesta correcta
        self.ERROR = ''             # Por si hay errores
        
        self.generarListaPreguntas(fichero)                    # Generalista preguntas a partir fichero CSV
        if self.ERROR != '':
            return
        self.calcularEstNotas(self.NOTAS)                      # Devuelve estadística de notas
        self.calcularEstPreguntas(self.NOTAS)                  # Calcula respuestas a nivel pregunta
        self.calcularDiscriminacionFacilidad(self.NOTAS)       # Calcular discriminación y facilidad
        self.calcularAuditoriaPreg(self.NOTAS)                 # Calcular informe auditoria

    def generarListaPreguntas(self, fichero: str):
        """
        Genera self.NOTAS (lista preguntas) a partir fichero CSV

        :param fichero: Ruta a fichero csv
        :type fichero: str
        """
        try:
            lineas = fichero.split('\n')
            try:
                np = 0    
                for index1, linea in enumerate(lineas):
                    if index1 > 1 and len(linea) > 0:
                        linea = linea.split(';')
                        
                        resp = []
                        
                        for index2 in range(5, len(linea)):
                            resp.append(linea[index2].replace('"', ''))
                        
                        self.NOTAS.append([np, float(linea[4].replace(',', '.')), resp, linea[0]])        # Nota
                        np += 1         
            
            except Exception as err:
                err_logger.error(err)
                self.ERROR = str(err) 
                
        except Exception as err:
            err_logger.error(err)
            self.ERROR = str(err)    
   
    def calcularEstNotas(self, notas):
        """
        Ordena las notas y calcula histograma

        :param notas: Lista de listas con: nº preg, nota, marcajes e id
        :type notas: list
        """ 
        notas = sorted(notas, key=lambda x: x[1], reverse=True)   # Clasifica por nota descendente
        
        for linea in notas:                     # Genera lista notas
            self.GRAFNOTAS.append(linea[1])
            
        '''
        Calcular resto valores útiles
        '''
        numal = len(self.NOTAS)
        numpreg = len(self.NOTAS[0][2])
        numresp = self.calcularResp(self.NOTAS)    
        percentil_25 = sorted(self.GRAFNOTAS)[int(math.ceil((len(self.GRAFNOTAS) * 25) / 100)) - 1] 
        percentil_75 = sorted(self.GRAFNOTAS)[int(math.ceil((len(self.GRAFNOTAS) * 75) / 100)) - 1]           
        media = statistics.mean(self.GRAFNOTAS)
        mediana = statistics.median(self.GRAFNOTAS)
        notamin = self.GRAFNOTAS[len(self.GRAFNOTAS)-1]
        notamax = self.GRAFNOTAS[0]
        
        self.ESTNOTAS = [numal, numpreg, numresp, percentil_25, percentil_75, media, mediana, notamin, notamax]            
            
    def calcularEstPreguntas(self, notas):
        """
        Calcula respuestas bien, mal en blanco a nivel de pregunta

        :param notas: Lista de notas del examen
        :type notas: list
        """        
        for linea in range(len(notas[0][2])):  # No funciona self.RESPxPREG = [[0, 0, 0]]*len(notas[0][2]) (suma en todas las listas)
            self.RESPxPREG.append([0, 0, 0])
            
        for index1 in range (0, len(notas)):    # Obtiene alumno a alumno preguntas acertadas grupo débil
            marcajes = notas[index1][2]
            for index2 in range(0, len(marcajes)):
                if int(marcajes[index2]) > 0:       # Si la respuesta es correcta, suma 1
                    self.RESPxPREG[index2][0] += 1
                elif int(marcajes[index2]) < 0:       # Si la respuesta es incorrecta, suma 1
                    self.RESPxPREG[index2][1] += 1
                else:
                    self.RESPxPREG[index2][2] += 1    # Sumar 1 si en blanco
        
    def calcularDiscriminacionFacilidad(self, notas):
        """
        Calcula la discriminación y facilidad de cada pregunta

        :param notas: Lista de listas con: nº preg, nota, marcajes e id
        :type notas: list
        """        
        numAlGrupo = int(len(notas)*0.27)         #Calcular el número de alumnos de grupos fuerte / débil
        notas = sorted(notas, key=lambda x: x[1])   # Clasifica por nota
        
        grupoFuerte = [0]*len(notas[0][2])   # Lista de n preguntas para ver aciertos de grupo fuerte
        grupoDebil =  [0]*len(notas[0][2])   # Lista de n preguntas para ver aciertos de grupo débil
        
        for index1 in range (0, numAlGrupo):    # Obtiene alumno a alumno preguntas acertadas grupo débil
            marcajes = notas[index1][2]
            for index2 in range(0, len(marcajes)):
                if int(marcajes[index2]) > 0:       # Si la respuesta es correcta, suma 1
                    grupoDebil[index2] += 1
                     
        for index1 in range (len(notas)-numAlGrupo, len(notas)):    # Obtiene alumno a alumno preguntas acertadas grupo fuerte
            marcajes = notas[index1][2]
            for index2 in range(0, len(marcajes)):
                if int(marcajes[index2]) > 0:       # Si la respuesta es correcta, suma 1
                    grupoFuerte[index2] += 1
                      
        for index1 in range(len(grupoFuerte)):  # Calcula coeficientes
            disc = round((grupoFuerte[index1] - grupoDebil[index1])/numAlGrupo, 2)
            facil = round((grupoFuerte[index1] + grupoDebil[index1])*100/(numAlGrupo*2),2)
            self.DISCRIMINACION.append([index1, disc])
            self.FACILIDAD.append([index1, facil])
            
        self.DISCRIMINACION = sorted(self.DISCRIMINACION, key=lambda x: x[1], reverse=True)   # Clasifica descendente
        self.FACILIDAD = sorted(self.FACILIDAD, key=lambda x: x[1], reverse=True)   # Clasifica descendente
        
    def calcularAuditoriaPreg(self, notas):
        """
        Calcula el informe de auditoría

        :param notas: Lista con notas y marcajes
        :type notas: list
        :return: Valor mas alto
        :rtype: int
        """ 
        self.MARCAJESPREG , self.RESPCORR = self.generarMatricesMarcajes(notas)
        
        for index1 in range(len(notas)):
            for index2 in range(len(notas[index1][2])):
                resp = notas[index1][2][index2]
                if len(resp) <= 2:
                    self.MARCAJESPREG[index2][abs(int(resp))] += 1     # Sumar 1 a la respuesta
                    resp = int(resp)
                    if resp > 0:
                        self.RESPCORR[index2] = resp
                        
    def calcularResp(self, notas):
        """
        Calcula el valor máximo de una matriz

        :param notas: Lista con notas y marcajes
        :type notas: list
        :return: Valor mas alto
        :rtype: int
        """        
        nr = 0
        for index1 in range(len(notas)):
            for index2 in range(len(notas[index1][2])):
                valor = notas[index1][2][index2]
                if abs(int(valor)) >=  nr:
                    nr = abs(int(valor))
                    
        return nr
    
    def generarMatricesMarcajes(self, notas):
        """
        Devuelve matriz con elementos a 0

        :param notas: Matriz generada a partir CSV
        :return: matriz de preguntas y matriz de respuestas correctas
        :rtype: list
        """        
        
        nr = self.calcularResp(notas)   # Calcular nº respuestas examen

        mp = [[0]*(nr+1) for _ in range(len(notas[0][2]))]
        rc = [0] * len(notas[0][2])
                    
        return mp, rc
    