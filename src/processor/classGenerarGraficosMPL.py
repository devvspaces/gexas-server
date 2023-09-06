from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
import numpy as np
import pandas as pd
from django.conf import settings

mplstyle.use('fast')


class generarGraficosMPL:

    def __init__(self, GRAFNOTAS, RESPxPREG, DISCRIMINACION, FACILIDAD, MARCAJESPREG, RESPCORR, ESTNOTAS, GRAPH_ID):
        """
        Genera gráfocas con Mathplotlib

        :param GRAFNOTAS: lista de notas
        :type GRAFNOTAS: list
        :param HISTOGRAMA:Lista histograma
        :type HISTOGRAMA: list
        :param RESPxPREG: Lista respuestas por pregunta
        :type RESPxPREG: list
        :param DISCRIMINACION: Lista discriminacion
        :type DISCRIMINACION: list
        :param FACILIDAD: Lista facilidad
        :type FACILIDAD: list
        """
        self.GRAPH_ID = GRAPH_ID  # Identificador de gráfica
        self.media_dir: Path = settings.BASE_DIR / f"media/{self.GRAPH_ID}/"
        self.media_dir.mkdir(parents=True)

        self.graficaNotas(GRAFNOTAS)
        self.respxPreg(RESPxPREG)
        self.discriminacion(DISCRIMINACION)
        self.facilidad(FACILIDAD)

        self.MARCAJESPREG = MARCAJESPREG
        self.RESPCORR = RESPCORR
        self.ESTNOTAS = ESTNOTAS
        self.DISCRIMINACION = DISCRIMINACION
        self.FACILIDAD = FACILIDAD
        self.DISCRIMINACION = DISCRIMINACION
        self.FACILIDAD = FACILIDAD

    def graficaNotas(self, GRAFNOTAS):
        """
        Genera la gráfica de notas del examen y el histograma de notas

        :param GRAFNOTAS: Lista con vlores de las notas
        :type GRAFNOTAS: list
        """
        plt.figure(figsize=(18, 6))         # Curva de notas
        plt.title("GRÁFICA DE NOTAS", fontsize=18,
                  fontweight='bold', color='#00a0df')
        plt.grid(True, axis='y')
        plt.ylabel('Nota')
        plt.ylim(0, 10.5)
        values = np.arange(0, 11, 1)
        value_increment = 1
        plt.yticks(values * value_increment, ['%d' % val for val in values])
        plt.plot(GRAFNOTAS)
        print("==================")
        print(self.media_dir)
        img_dir = self.media_dir / "graf1.png"
        plt.savefig(str(img_dir), bbox_inches='tight')

        if GRAFNOTAS[0] <= 10:        # Histograma de notas
            bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        else:
            bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110]
        plt.figure(figsize=(6, 6))
        plt.title("HISTOGRAMA DE NOTAS", fontsize=18,
                  fontweight='bold', color='#00a0df')
        n_bins = 12
        values, bins, bars = plt.hist(GRAFNOTAS, bins, width=.5, color='y')
        plt.bar_label(bars, fontsize=10, color='navy')
        indx = np.arange(len(bins))  # the x locations for the groups
        plt.xticks(indx, indx, fontsize=10)
        img_dir = self.media_dir / "graf2.png"
        plt.savefig(str(img_dir), bbox_inches='tight')

    def respxPreg(self, RESPxPREG):
        """
        Gráfica de respuestas bien, mal, en blanco por pregunta

        :param RESPxPREG: Lista de bien, mal, en blanco por pregunta
        :type RESPxPREG: list
        """
        numpreg, bien, mal, enbl = [], [], [], []
        for index, value in enumerate(RESPxPREG):
            numpreg.append(index+1)
            bien.append(value[0])
            mal.append(value[1])
            enbl.append(value[2])

        data = [bien, mal, enbl]

        columns = tuple(numpreg)
        rows = ['Bien', 'Mal', 'En blanco']

        fig, ax = plt.subplots(figsize=(30, 6))

        # Get some pastel shades for the colors
        colors = ['g', 'r', '#CCC']
        n_rows = len(data)

        index = np.arange(len(columns)) + 0.3
        bar_width = 0.8

        # Initializar el desplazamiento vertical de las barras apiladas
        y_offset = np.zeros(len(columns))

        cell_text = []      # Dibujar barras y crear etiquetas para la tabla

        plt.subplots(figsize=(30, 6))
        for row in range(n_rows):
            plt.bar(index, data[row], bar_width,
                    bottom=y_offset, color=colors[row])
            y_offset = y_offset + data[row]

        values = np.arange(0, 1, 0.1)
        value_increment = 0.1

        plt.ylabel('')
        plt.yticks(values * value_increment, ['%d' % val for val in values])
        plt.xticks([])
        indx = np.arange(len(numpreg))  # Posición x de los grupos
        plt.xticks(indx, numpreg, rotation=90)

        cell_text.reverse()     # Invertir colores y texto para mostrar el último valor arriba

        bien, mal, enbl, column_labels, data = [], [], [
        ], [], []       # Montar tabla con valores

        for x in range(len(RESPxPREG)):
            bien.append(RESPxPREG[x][0])
            mal.append(RESPxPREG[x][1])
            enbl.append(RESPxPREG[x][2])
            column_labels.append(str(x+1))

        data = [bien, mal, enbl]

        # Crear un dataframe bidimensional de la tabla
        df = pd.DataFrame(data, columns=column_labels)

        ax.axis('tight')  # turns off the axis lines and labels
        ax.axis('off')  # changes x and y axis limits such that all data is shown

        table = plt.table(cellText=df.values,
                          colLabels=df.columns,
                          rowLabels=["Bien", "Mal", "EnBl"],
                          rowColours=["g", "r", "#CCC"],
                          loc="top")
        table.set_fontsize(10)

        # Ajustar gráfica debajo de la tabla
        plt.subplots_adjust(left=0.2, bottom=0.2)

        plt.title('RESPUESTAS x PREGUNTA', fontsize=18,
                  fontweight='bold', color='#00a0df', pad=55)

        img_dir = self.media_dir / "graf3.png"
        plt.savefig(str(img_dir), bbox_inches='tight')

    def discriminacion(self, DISCRIMINACION):
        """
        Genera gráfica de barras de discriminación de las preguntas del examen

        :param DISCRIMINACION: Lista (ordenada) de valores de discriminación y pregunta asociada
        :type DISCRIMINACION: List
        """
        numpreg, disc, barcolor, textcolor = [], [], [], [
        ]  # Separa la lista de entrada en dos tablas para generar gráfica y asigna color
        for index, value in enumerate(DISCRIMINACION):
            numpreg.append(value[0])
            disc.append(value[1])
            color = self.colorDiscr(value[1])
            barcolor.append(color)
            textcolor.append(color)

        x_values = np.arange(len(numpreg))
        fig, ax = plt.subplots(figsize=(30, 6))

        ax.bar(x_values, disc, width=.8, color=barcolor)

        vmax, vmin = 0, 0       # Para establecer rango

        for x, y in zip(x_values, disc):
            if y > vmax:
                vmax = y      # Calcular máximo y mínimo
            if y < vmin:
                vmin = y
            ax.annotate(
                str(y),        # label is our y-value as a string
                xy=(x, y),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center',
                va='bottom',
                rotation=90,
                color=textcolor[x],
                fontsize=8
            )

        ax.set_xticks(x_values)
        ax.set_xticklabels(numpreg, rotation=90, fontsize=8)
        ax.set_xlabel('Nº pregunta')
        ax.set_ylim(vmin, vmax+0.1)
        ax.set_title("DISCRIMINACIÓN DE PREGUNTAS", fontsize=18,
                     fontweight='bold', color='#00a0df')
        buf = '>= 0,35 y <= 1: Excelente'
        buf += '\n>= 0.25 y <= 0,35: Bueno'
        buf += '\n>= 0.15 y <= 0,25: Límite'
        buf += '\n < 0.15: Reexaminar'

        # Info a pie gráfica
        text = fig.text(0.51, -0.1, buf,
                        horizontalalignment='center', wrap=True)

        img_dir = self.media_dir / "graf4.png"
        plt.savefig(str(img_dir), bbox_inches='tight')

    def facilidad(self, FACILIDAD):
        """
        Genera gráfica de barras de facilidad de las preguntas del examen

        :param FACILIDAD: Lista (ordenada) de valores de discriminación y pregunta asociada
        :type FACILIDAD: List
        """
        numpreg, facil, barcolor, textcolor = [], [], [], [
        ]  # Separa la lista de entrada en dos tablas para generar gráfica y asigna color
        for index, value in enumerate(FACILIDAD):
            numpreg.append(value[0])
            facil.append(value[1])

            color = self.colorFacil(value[1])
            barcolor.append(color)
            textcolor.append(color)

        x_values = np.arange(len(numpreg))
        fig, ax = plt.subplots(figsize=(30, 6))

        ax.bar(x_values, facil, width=.8, color=barcolor)

        vmax, vmin = 0, 0       # Para establecer rango

        for x, y in zip(x_values, facil):
            if y > vmax:
                vmax = y      # Calcular máximo y mínimo
            if y < vmin:
                vmin = y
            ax.annotate(
                str(y),        # label is our y-value as a string
                xy=(x, y),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center',
                va='bottom',
                rotation=90,
                color=textcolor[x],
                fontsize=8
            )

        ax.set_xticks(x_values)
        ax.set_xticklabels(numpreg, rotation=90, fontsize=8)
        ax.set_xlabel('Nº pregunta')
        ax.set_ylim(0, 120)
        ax.set_title("FACILIDAD DE PREGUNTAS", fontsize=18,
                     fontweight='bold', color='#00a0df')
        buf = '>= 70 y <= 100: Fácil'
        buf += '\n>= 50 y <= 70'
        buf += '\n>= 35 y <= 50'
        buf += '\n < 35:\: Difícil'

        text = fig.text(0.51, -0.1, buf,
                        horizontalalignment='center', wrap=True)

        img_dir = self.media_dir / "graf5.png"
        plt.savefig(str(img_dir), bbox_inches='tight')

    def generarPDF(self):
        """
        Genera un informe en formato PDF con todos los datos del examen. Genera HTML y PDF
        :param MARCAJESPREG: Lista de marcajes x pregunta
        :type MARCAJESPREG: list
        :param RESPCORR: Lista de respuestas correctas
        :type RESPCORR: list
        :param ESTNOTAS: Lista de datos globales del examen
        :type ESTNOTAS: list
        """
        DISCRIMINACION = sorted(
            self.DISCRIMINACION, key=lambda x: x[0])   # Clasifica POR PREGUNTA ASCENDENTE
        # Clasifica POR PREGUNTA ASCENDENTE
        FACILIDAD = sorted(self.FACILIDAD, key=lambda x: x[0])

        tablanotas = self.montarTablaNotas(self.ESTNOTAS)
        tablaaudit = self.montarTablaAudit(
            self.MARCAJESPREG, self.RESPCORR, self.ESTNOTAS,
            DISCRIMINACION, FACILIDAD
        )

        return {
            'tablanotas': tablanotas,
            'tablaaudit': tablaaudit,
        }

    def montarTablaNotas(self, est):
        """
        Montar html con las líneas utilizadas en notas

        :param ESTNOTAS: Información general del examen
        :type ESTNOTAS: list
        """
        tablaNotas = ''

        tablaNotas += '<tr><td class="t1c1">Nota mínima: </td><td class="t1c2">' + \
            str(round(est[7], 2)).replace('.', ',') + '</td>'
        tablaNotas += '<td class="t1c3">Nº alumnos: </td><td class="t1c4">' + \
            str(est[0]) + '</td></tr>'

        tablaNotas += '<tr><td class="t1c1">1er. cuartil:: </td><td class="t1c2">' + \
            str(round(est[3], 2)).replace('.', ',') + '</td>'
        tablaNotas += '<td class="t1c3">Nº preguntas: </td><td class="t1c4">' + \
            str(est[1]) + '</td></tr>'

        tablaNotas += '<tr><td class="t1c1">Nota mediana: </td><td class="t1c2">' + \
            str(round(est[6], 2)).replace('.', ',') + '</td>'
        tablaNotas += '<td class="t1c3">Máx. nº respuestas: </td><td class="t1c4">' + \
            str(est[2]) + '</td></tr>'

        tablaNotas += '<tr><td class="t1c1">3er. cuartil: </td><td class="t1c2">' + \
            str(round(est[4], 2)).replace('.', ',') + '</td>'
        tablaNotas += '<td class="t1c3"></td><td class="t1c4"></td></tr>'

        tablaNotas += '<tr><td class="t1c1">Nota máxima: </td><td class="t1c2">' + \
            str(round(est[8], 2)).replace('.', ',') + '</td>'
        tablaNotas += '<td class="t1c3"></td><td class="t1c4"></td></tr>'

        tablaNotas += '<tr><td class="t1c1">Nota media: </td><td class="t1c2">' + \
            str(round(est[5], 2)).replace('.', ',') + '</td>'
        tablaNotas += '<td class="t1c3"></td><td class="t1c4"></td></tr>'

        return tablaNotas

    def montarTablaAudit(self, MARCAJESPREG, RESPCORR, ESTNOTAS, DISCRIMINACION, FACILIDAD):
        """
        Montar html con las líneas utilizadas en auditoría de notas

        :param MARCAJESPREG: Lista de marcajes de preguntas
        :type MARCAJESPREG: list
        :param RESPCORR: Lista de respuestas correctas
        :type RESPCORR: list
        :param ESTNOTAS: Lista con datos generales del examen
        :type ESTNOTAS: list
        """
        tablaAudit = ''
        tablaAudit += self.montarTableHeaderAudit(MARCAJESPREG[0])

        for i in range(len(RESPCORR)):
            tablaAudit += self.montarLineaTablaAudit(
                i+1, MARCAJESPREG[i], RESPCORR[i], ESTNOTAS[0], DISCRIMINACION[i], FACILIDAD[i])

        return tablaAudit

    def montarTableHeaderAudit(self, marcajes):
        """
        Monta cabecera del informe de auditoría. Lo genera dinámicamente en función de las respuestas

        :param marcajes: Marcajes de cada pregunta
        :type marcajes: list
        :return: html de tabla montado
        :rtype: str
        """
        buf = '<tr><th class="tabla2">Preg</th>'
        for nr in range(len(marcajes)):
            if nr == 0:
                buf += '<th class="tabla2">Bl</th>'
            else:
                buf += '<th class="tabla2">R' + str(nr) + '</th>'
        buf += '<th class="tabla2">% Respuesta<br/>Correcta</th>'
        buf += '<th class="tabla2">% Respuesta<br>+ contestada</th>'
        buf += '<th class="tabla2">Discrimin.</th>'
        buf += '<th class="tabla2">Facilidad</th></tr>'

        return buf

    def montarLineaTablaAudit(self, np, marcajes, respcorr, numpreg, discr, facil):
        """
        Montar html con las líneas utilizadas en auditoría de preguntas

        :param np: _description_
        :type np: _type_
        :param marcajes: _description_
        :type marcajes: _type_
        :param respcorr: _description_
        :type respcorr: _type_
        :param numpreg: _description_
        :type numpreg: _type_
        :param discr: _description_
        :type discr: _type_
        :param facil: _description_
        :type facil: _type_
        :return: _description_
        :rtype: _type_
        """
        buf = '<tr>'
        buf += '<td class = "numpreg">' + str(np) + '</td>'
        imax, max = self.mayor(marcajes)
        porcRC = marcajes[respcorr]/numpreg
        porcRMC = marcajes[imax]/numpreg

        for index, resp in enumerate(marcajes):
            if index == respcorr:
                buf += '<td class = "respcorr">' + \
                    str(resp).replace('.', ',') + '</td>'
            else:
                buf += '<td>' + str(resp) + '</td>'

        buf += '<td>' + str(round(porcRC*100, 2)) + '%' + '</td>'
        if porcRMC > porcRC:
            buf += '<td bgcolor= "#ff0">' + \
                str(round(porcRMC*100, 2)).replace('.', ',') + '%' + '</td>'
        else:
            buf += '<td>' + str(round(porcRMC*100, 2)
                                ).replace('.', ',') + '%' + '</td>'

        buf += '<td class = "discfac" bgcolor=' + \
            self.colorDiscr(discr[1]) + '>' + \
            str(discr[1]).replace('.', ',') + '</td>'

        buf += '<td class = "discfac" bgcolor=' + \
            self.colorFacil(facil[1]) + '>' + \
            str(facil[1]).replace('.', ',') + '</td>'

        buf += '</tr><tr></tr>'

        return buf

    def mayor(self, lista):
        """
        Calcula el valor máximo y posición de una lista

        :param lista: lista a evaluar
        :type lista: list
        :return: posición y valor máximo
        :rtype: int
        """
        max = lista[0]
        imax = 0
        for x in range(len(lista)):
            if lista[x] > max:
                max = lista[x]
                imax = x
        return imax, max

    def colorDiscr(self, discr):
        """
        Calcula colores asociados a discriminación

        :param discr: Lista con valores discriminación
        :type discr: list
        :return: Color asociado
        :rtype: str
        """
        color = ''
        if discr >= 0.35:
            color = '#00ff00'
        elif discr >= 0.25 and discr < 0.35:
            color = '#008000'
        elif discr >= 0.15 and discr < 0.24:
            color = '#FF8000'
        else:
            color = '#F00'

        return color

    def colorFacil(self, facil):
        """
        Calcula colores asociados a facilidad

        :param discr: Lista con valores facilidad
        :type discr: list
        :return: Color asociado
        :rtype: str
        """
        color = ''
        if facil >= 70:
            color = '#F00'
        elif facil >= 50 and facil < 70:
            color = '#FF8000'
        elif facil >= 35 and facil < 50:
            color = '#008000'
        else:
            color = '#00ff00'

        return color
