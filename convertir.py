#!/usr/bin/env python3

import pandas as pd    
import os
import xml.etree.ElementTree as ET
from datetime import date
import re
import shutil
# import xlwt
import subprocess
import sys
import datetime
import csv
import arrow

# def valid_date(datestring):
#     """
#     valida un string con el formato dd/mm/aa
#     devuelve un datetime.date valido
#     en caso de no ser valido devuelve None
#     """
#     try:
#         mat=re.match('(\d{2})[/.-](\d{2})[/.-](\d{2})$', datestring)
#         if mat is not None:
#             fecha = re.split('[/.-]', datestring)
#             return date(int(fecha[2])+2000, int(fecha[1]), int(fecha[0]))
#         return None
#     except ValueError:
#         return None

# def valid_monto(montostring):
#     """
#     valida un string con el formato ###.###,##
#     devuelve un float valido
#     en caso de no ser valido devuelve None
#     """
#     try:
#         montostring = montostring.replace('.','')
#         montostring = montostring.replace(',','.')
#         return float(montostring)
#     except ValueError:
#         return None


# def parsear_xml(nombre_xml):
#     tree = ET.parse(nombre_xml)
#     root = tree.getroot()

#     primero = False
#     data = []

#     #Recorre el xml en paginas y en texto
#     for page in root:
#         for text in page:
#             #Si es un texto valido (distinto de None)
#             if text.text is not None:
#                 #Crea el renglon con datos validos
#                 renglon = (text.text).split()
#                 print text.text
#                 print renglon
#                 print len(renglon)>0
#                 if len(renglon)<=0:
#                     break
#                 #Si el primer elemento del renglon es una fecha valida 
#                 #entonces es un renglon del resumen
#                 #el indice 0 es la fecha
#                 #el indice -1 es el saldo
#                 #el indice -2 es el monto
#                 #el resto es la descripcion
#                 if valid_date(renglon[0]) is not None:
#                     primero = True
#                     fecha = valid_date(renglon[0])
#                     monto = valid_monto(renglon[-2])
#                     saldo = valid_monto(renglon[-1])
#                     descripcion = ' '.join(renglon[1:-2])
#                     data.append([fecha, descripcion, monto, monto, saldo, ''])
#                 else:
#                     #Si aun no encuentra el primer renglon del resumen
#                     #Toma el valor renglon[-1] que corresponde al saldo inicial
#                     if not primero:
#                         renglon = (text.text).split()
#                         print renglon
#                         saldo_inicial = valid_monto(renglon[-1])
    
#     #Recorre la lista y le agrega el tipo de movimiento
#     #'+' si es credito
#     #'-' si es debito
#     for e in data:
# #        print e[1][:5],e[2],saldo_inicial,round(e[2],2),round(saldo_inicial,2),(round(saldo_inicial+e[2],4)==round(e[4],4))
# #,int(saldo_inicial*100) + int(e[2]*100),int(e[4]*100),(int(saldo_inicial*100) + int(e[2]*100)) == int(e[4]*100)
#         if (round(saldo_inicial + e[2],4) == round(e[4],4)):
#             e[5] = '+'
#             e[3] = 0
#         else:
#             e[5] = '-'
#             e[2] = 0
#         saldo_inicial = e[4]


#     return data


# try:
#     shutil.rmtree('./xml')
# except OSError:
# 	pass
# os.mkdir('./xml')

# ficheros = os.listdir('./pdfs')
# ficheros.sort()

# for f in ficheros:
#     nombre_pdf = f.replace(' ', r'\ ')
#     nombre_xml = ''.join(f.split('.')[:-1])
#     nombre_xml = nombre_xml.replace(' ','_') + '.xml'
#     comando = 'pdftohtml -c -xml ./pdfs/%s ./xml/%s' % (nombre_pdf, nombre_xml)
#     x = os.system(comando)

#     if x != 0:
#         print "Instale pdftohtml he intente nuevamente"
#         exit()

# ficheros = os.listdir('./xml')
# ficheros.sort()

# for f in ficheros:
#     if ''.join(f.split('.')[-1]) == 'xml':
#         data = data + parsear_xml('./xml/'+f)

# book = xlwt.Workbook(encoding="utf-8")

# hoja1 = book.add_sheet("Python hoja 1")

# for i, e in enumerate(data):
#     for j, dato in enumerate(e):
#         hoja1.write(i,j, dato)

# book.save("./xls/python_spreadsheet_conerror.xls")

# print len(data)
######################################################################

def parsear_xml(nombre_xml):
    tree = ET.parse(nombre_xml)
    root = tree.getroot()

    primero = False
    data = []
    contador = 0
    #Recorre el xml en paginas y en texto
    print(nombre_xml)
    for page in root:
        for text in page:
            if text.tag == "text":
                if list(text):
                    if "$" in text[0].text and "," in text[0].text:
                        data.append([nombre_xml, text[0].text])
                else:
                    if "$" in text.text and "," in text.text:
                        data.append([nombre_xml, text.text])

    return data


def extraer_xml(directorio):
    data = []

    #Borra el contenido del directorio xml
    comando = "rm ./xml/*"
    os.system(comando)

    ficheros = os.listdir('./' + directorio)
    ficheros.sort()

    #INICIA - Por cada 
    #          pdf en el directorio "directorio" crea un xml con pdftohtml en el directorio xml
    for f in ficheros:
        #el pdf debe contener la palabra "pago" en su nombre
        if "pago" in f:
            nombre_pdf = f.replace(' ', r'\ ')
            nombre_pdf = nombre_pdf.replace('(', r'\(')
            nombre_pdf = nombre_pdf.replace(')', r'\)')

            nombre_xml = ''.join(f.split('.')[:-1])
            nombre_xml = nombre_xml.replace(' ','_') + '.xml'
            nombre_xml = nombre_xml.replace("(","_")
            nombre_xml = nombre_xml.replace(")","_")
            
            comando = '/usr/bin/pdftohtml -c -xml ./{}/{} ./xml/{} >/dev/null'.format(directorio, nombre_pdf, nombre_xml)
            #TODO: Seria mejor hacerlo con subprocess en lugar de os.system.
            # try:
            #     print(comando)
            #     p = subprocess.call(comando.split(), capture_output=True)
            #     # print(p)
            #     salida_comando = p.stdout.decode().split("\n")
            #
            #     if p.returncode !=0:
            #         print(p.stderr.decode())
            #         sys.exit(1)
            # except:
            #     print("pasaporaca????")
            #     sys.exit(1)

            x = os.system(comando)
            if x != 0:
                print ("Instale pdftohtml he intente nuevamente")
                exit()
    #TERMINA - Por cada 
    #          pdf en el directorio "directorio" crea un xml con pdftohtml en el directorio xml


    #INICIA elimina
    #           todos los archivos creados por pdftohtml que no sean xml
    ficheros = os.listdir('./xml')
    ficheros.sort()
    extensiones = set()
    for f in ficheros:
        extension = f.split(".")[-1]
        extensiones.add(extension)

    for extension in extensiones:
        if extension != "xml":
            comando = "rm ./xml/*." + extension
            os.system(comando)
    #TERMINA elimina
    #           todos los archivos creados por pdftohtml que no sean xml



    #INICIA Parseo del xml
    ficheros = os.listdir('./xml')
    ficheros.sort()

    for f in ficheros:
        if not f.startswith("."):
            data = data + parsear_xml('./xml/'+f)
    #TERMINA Parseo del xml

    #INICIA volcado a xls
    # print("*-"*15)
    # print(data)
    df = pd.DataFrame(data)
    csv_data = df.to_csv(index=False)
    df.to_csv(directorio + "_" + str(arrow.get().timestamp) + '.csv', index=False)
    # print("*-"*15)
    # print(datetime.datetime.now().timestamp())

    # book = xlwt.Workbook(encoding="utf-8")

    # hoja1 = book.add_sheet("Python hoja 1")

    # for i, e in enumerate(data):
    #     for j, dato in enumerate(e):
    #         hoja1.write(i,j, dato)

    # book.save("./xls/python_spreadsheet_conerror.xls")
    #TERMINA volcado a xls
    return None

if __name__ == "__main__":
    extraer_xml("Agua")
    extraer_xml("DGR")
    extraer_xml("Municipalidad")

