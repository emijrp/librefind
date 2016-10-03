# -*- coding: utf-8 -*-

# Copyright (C) 2016 emijrp <emijrp@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime
import json
import re
import time
import urllib
import urllib.request
import urllib.parse

import pywikibot

def convertirfecha(fecha):
    num2month = {1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril', 5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto', 9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'}
    fecha = fecha.split('T')[0]
    fecha = '%s de %s de %s' % (int(fecha.split('-')[2]), num2month[int(fecha.split('-')[1])], int(fecha.split('-')[0]))
    return fecha

def main():
    p27 = {
        'Afganistán': 'Q889', 
        'Albania': 'Q222', 
        'Alemania': 'Q183', 
        'Andorra': 'Q228', 
        'Angola': 'Q916', 
        'Antigua y Barbuda': 'Q781', 
        'Arabia Saudita': 'Q851', 
        'Argelia': 'Q262', 
        'Argentina': 'Q414', 
        'Armenia': 'Q399', 
        'Australia': 'Q408', 
        'Austria': 'Q40', 
        'Azerbaiyán': 'Q227', 
        'Bahamas': 'Q778', 
        'Bangladés': 'Q902', 
        'Barbados': 'Q244', 
        'Baréin': 'Q398', 
        'Bélgica': 'Q31', 
        'Belice': 'Q242', 
        'Benín': 'Q962', 
        'Bielorrusia': 'Q184', 
        'Birmania': 'Q836', 
        'Bolivia': 'Q750', 
        'Bosnia y Herzegovina': 'Q225', 
        'Botsuana': 'Q963', 
        'Brasil': 'Q155', 
        'Brunéi': 'Q921', 
        'Bulgaria': 'Q219', 
        'Burkina Faso': 'Q965', 
        'Burundi': 'Q967', 
        'Bután': 'Q917', 
        'Cabo Verde': 'Q1011', 
        'Camboya': 'Q424', 
        'Camerún': 'Q1009', 
        'Canadá': 'Q16', 
        'Catar': 'Q846', 
        'Chad': 'Q657', 
        'Chile': 'Q298', 
        'Chipre': 'Q229', 
        'Ciudad del Vaticano': 'Q237', 
        'Colombia': 'Q739', 
        'Comoras': 'Q970', 
        'Corea del Norte': 'Q423', 
        'Corea del Sur': 'Q884', 
        'Costa de Marfil': 'Q1008', 
        'Costa Rica': 'Q800', 
        'Croacia': 'Q224', 
        'Cuba': 'Q241', 
        'Dinamarca': 'Q35', 
        'Dominica': 'Q784', 
        'Ecuador': 'Q736', 
        'Egipto': 'Q79', 
        'El Salvador': 'Q792', 
        'Emiratos Árabes Unidos': 'Q878', 
        'Eritrea': 'Q986', 
        'Eslovaquia': 'Q214', 
        'Eslovenia': 'Q215', 
        'España': 'Q29', 
        'Estados Unidos': 'Q30', 
        'Estonia': 'Q191', 
        'Etiopía': 'Q115', 
        'Filipinas': 'Q928', 
        'Finlandia': 'Q33', 
        'Fiyi': 'Q712', 
        'Francia': 'Q142', 
        'Gabón': 'Q1000', 
        'Gambia': 'Q1005', 
        'Georgia': 'Q230', 
        'Ghana': 'Q117', 
        'Granada': 'Q769', 
        'Grecia': 'Q41', 
        'Guatemala': 'Q774', 
        'Guinea': 'Q1006', 
        'Guinea Ecuatorial': 'Q983', 
        'Guinea-Bisáu': 'Q1007', 
        'Guyana': 'Q734', 
        'Haití': 'Q790', 
        'Honduras': 'Q783', 
        'Hungría': 'Q28', 
        'India': 'Q668', 
        'Indonesia': 'Q252', 
        'Irak': 'Q796', 
        'Irán': 'Q794', 
        'Irlanda': 'Q27', 
        'Islandia': 'Q189', 
        'Islas Marshall': 'Q709', 
        'Islas Salomón': 'Q685', 
        'Israel': 'Q801', 
        'Italia': 'Q38', 
        'Jamaica': 'Q766', 
        'Japón': 'Q17', 
        'Jordania': 'Q810', 
        'Kazajistán': 'Q232', 
        'Kenia': 'Q114', 
        'Kirguistán': 'Q813', 
        'Kiribati': 'Q710', 
        'Kosovo': 'Q1246', 
        'Kuwait': 'Q817', 
        'Laos': 'Q819', 
        'Lesoto': 'Q1013', 
        'Letonia': 'Q211', 
        'Líbano': 'Q822', 
        'Liberia': 'Q1014', 
        'Libia': 'Q1016', 
        'Liechtenstein': 'Q347', 
        'Lituania': 'Q37', 
        'Luxemburgo': 'Q32', 
        'Madagascar': 'Q1019', 
        'Malasia': 'Q833', 
        'Malaui': 'Q1020', 
        'Maldivas': 'Q826', 
        'Malí': 'Q912', 
        'Malta': 'Q233', 
        'Marruecos': 'Q1028', 
        'Mauricio': 'Q1027', 
        'Mauritania': 'Q1025', 
        'México': 'Q96', 
        #'Micronesia': 'Q702', 
        'Moldavia': 'Q217', 
        'Mónaco': 'Q235', 
        'Mongolia': 'Q711', 
        'Montenegro': 'Q236', 
        'Mozambique': 'Q1029', 
        'Namibia': 'Q1030', 
        'Nauru': 'Q697', 
        'Nepal': 'Q837', 
        'Nicaragua': 'Q811', 
        'Níger': 'Q1032', 
        'Nigeria': 'Q1033', 
        'Noruega': 'Q20', 
        'Nueva Zelanda': 'Q664', 
        'Omán': 'Q842', 
        'Países Bajos': 'Q55', 
        'Pakistán': 'Q843', 
        'Palaos': 'Q695', 
        'Panamá': 'Q804', 
        'Papúa Nueva Guinea': 'Q691', 
        'Paraguay': 'Q733', 
        'Perú': 'Q419', 
        'Polonia': 'Q36', 
        'Portugal': 'Q45', 
        'Reino Unido': 'Q145', 
        'República Árabe Saharaui Democrática': 'Q40362', 
        'República Centroafricana': 'Q929', 
        'República Checa': 'Q213', 
        'República de China': 'Q865', 
        'República de Macedonia': 'Q221', 
        'República del Congo': 'Q971', 
        'República Democrática del Congo': 'Q974', 
        'República Dominicana': 'Q786', 
        'República Popular China': 'Q148', 
        'Ruanda': 'Q1037', 
        'Rumania': 'Q218', 
        'Rusia': 'Q159', 
        'Samoa': 'Q683', 
        'San Cristóbal y Nieves': 'Q763', 
        'San Marino': 'Q238', 
        'San Vicente y las Granadinas': 'Q757', 
        'Santa Lucía': 'Q760', 
        'Santo Tomé y Príncipe': 'Q1039', 
        'Senegal': 'Q1041', 
        'Serbia': 'Q403', 
        'Seychelles': 'Q1042', 
        'Sierra Leona': 'Q1044', 
        'Singapur': 'Q334', 
        'Siria': 'Q858', 
        'Somalia': 'Q1045', 
        'Sri Lanka': 'Q854', 
        'Suazilandia': 'Q1050', 
        'Sudáfrica': 'Q258', 
        'Sudán': 'Q1049', 
        'Sudán del Sur': 'Q958', 
        'Suecia': 'Q34', 
        'Suiza': 'Q39', 
        'Surinam': 'Q730', 
        'Tailandia': 'Q869', 
        'Tanzania': 'Q924', 
        'Tayikistán': 'Q863', 
        'Timor Oriental': 'Q574', 
        'Togo': 'Q945', 
        'Tonga': 'Q678', 
        'Trinidad y Tobago': 'Q754', 
        'Túnez': 'Q948', 
        'Turkmenistán': 'Q874', 
        'Turquía': 'Q43', 
        'Tuvalu': 'Q672', 
        'Ucrania': 'Q212', 
        'Uganda': 'Q1036', 
        'Uruguay': 'Q77', 
        'Uzbekistán': 'Q265', 
        'Vanuatu': 'Q686', 
        'Venezuela': 'Q717', 
        'Vietnam': 'Q881', 
        'Yemen': 'Q805', 
        'Yibuti': 'Q977', 
        'Zambia': 'Q953', 
        'Zimbabue': 'Q954', 
    }
    p27list = [[k, v] for k, v in p27.items()]
    p27list.sort()
    
    #https://query.wikidata.org/#SELECT%20DISTINCT%20%3Fitem%20%3FitemLabel%0AWHERE%20{%0A%20%20%3Fitem%20wdt%3AP31%20wd%3AQ6256.%0A%20%20SERVICE%20wikibase%3Alabel%20{%20bd%3AserviceParam%20wikibase%3Alanguage%20%22es%2Cen%22%20}%0A}
    country2nationality = {
        'Afganistán': {'masculino': 'afgano', 'femenino': 'afgana' }, 
        'Albania': {'masculino': 'albanés', 'femenino': 'albanesa' }, 
        'Alemania': {'masculino': 'alemán', 'femenino': 'alemana' }, 
        'Andorra': {'masculino': 'andorrano', 'femenino': 'andorrana' }, 
        'Angola': {'masculino': 'angoleño', 'femenino': 'angoleña' }, 
        'Antigua y Barbuda': {'masculino': 'antiguano', 'femenino': 'antiguana' }, 
        'Arabia Saudita': {'masculino': 'saudí', 'femenino': 'saudí' }, 
        'Argelia': {'masculino': 'argelino', 'femenino': 'argelina' }, 
        'Argentina': {'masculino': 'argentino', 'femenino': 'argentina' }, 
        'Armenia': {'masculino': 'armenio', 'femenino': 'armenia' }, 
        'Australia': {'masculino': 'australiano', 'femenino': 'australiana' }, 
        'Austria': {'masculino': 'austríaco', 'femenino': 'austríaca' }, 
        'Azerbaiyán': {'masculino': 'azerbaiyano', 'femenino': 'azerbaiyana' }, 
        'Bahamas': {'masculino': 'bahameño', 'femenino': 'bahameña' }, 
        'Bangladés': {'masculino': 'bangladesí', 'femenino': 'bangladesí' }, 
        'Barbados': {'masculino': 'barbadense', 'femenino': 'barbadense' }, 
        'Baréin': {'masculino': 'bareiní', 'femenino': 'bareiní' }, 
        'Bélgica': {'masculino': 'belga', 'femenino': 'belga' }, 
        'Belice': {'masculino': 'beliceño', 'femenino': 'beliceña' }, 
        'Benín': {'masculino': 'beninés', 'femenino': 'beninesa' }, 
        'Bielorrusia': {'masculino': 'bielorruso', 'femenino': 'bielorrusa' }, 
        'Birmania': {'masculino': 'birmano', 'femenino': 'birmana' }, 
        'Bolivia': {'masculino': 'boliviano', 'femenino': 'boliviana' }, 
        'Bosnia y Herzegovina': {'masculino': 'bosnio', 'femenino': 'bosnia' }, 
        'Botsuana': {'masculino': 'botsuano', 'femenino': 'botsuana' }, 
        'Brasil': {'masculino': 'brasileño', 'femenino': 'brasileña' }, 
        'Brunéi': {'masculino': 'bruneano', 'femenino': 'bruneana' }, 
        'Bulgaria': {'masculino': 'búlgaro', 'femenino': 'búlgara' }, 
        'Burkina Faso': {'masculino': 'burkinés', 'femenino': 'burkinesa' }, 
        'Burundi': {'masculino': 'burundés', 'femenino': 'burundesa' }, 
        'Bután': {'masculino': 'butanés', 'femenino': 'butanesa' }, 
        'Cabo Verde': {'masculino': 'caboverdiano', 'femenino': 'caboverdiana' }, 
        'Camboya': {'masculino': 'camboyano', 'femenino': 'camboyana' }, 
        'Camerún': {'masculino': 'camerunés', 'femenino': 'camerunesa' }, 
        'Canadá': {'masculino': 'canadiense', 'femenino': 'canadiense' }, 
        'Catar': {'masculino': 'catarí', 'femenino': 'catarí' }, 
        'Chad': {'masculino': 'chadiano', 'femenino': 'chadiana' }, 
        'Chile': {'masculino': 'chileno', 'femenino': 'chilena' }, 
        'Chipre': {'masculino': 'chipriota', 'femenino': 'chipriota' }, 
        'Ciudad del Vaticano': {'masculino': 'vaticano', 'femenino': 'vaticana' }, 
        'Colombia': {'masculino': 'colombiano', 'femenino': 'colombiana' }, 
        'Comoras': {'masculino': 'comorense', 'femenino': 'comorense' }, 
        'Corea del Norte': {'masculino': 'norcoreano', 'femenino': 'norcoreana' }, 
        'Corea del Sur': {'masculino': 'surcoreano', 'femenino': 'surcoreana' }, 
        'Costa de Marfil': {'masculino': 'marfileño', 'femenino': 'marfileña' }, 
        'Costa Rica': {'masculino': 'costarricense', 'femenino': 'costarricense' }, 
        'Croacia': {'masculino': 'croata', 'femenino': 'croata' }, 
        'Cuba': {'masculino': 'cubano', 'femenino': 'cubana' }, 
        'Dinamarca': {'masculino': 'danés', 'femenino': 'danesa' }, 
        'Dominica': {'masculino': 'dominiqués', 'femenino': 'dominiquesa' }, 
        'Ecuador': {'masculino': 'ecuatoriano', 'femenino': 'ecuatoriana' }, 
        'Egipto': {'masculino': 'egipcio', 'femenino': 'egipcia' }, 
        'El Salvador': {'masculino': 'salvadoreño', 'femenino': 'salvadoreña' }, 
        'Emiratos Árabes Unidos': {'masculino': 'emiratí', 'femenino': 'emiratí' }, 
        'Eritrea': {'masculino': 'eritreo', 'femenino': 'eritrea' }, 
        'Eslovaquia': {'masculino': 'eslovaco', 'femenino': 'eslovaca' }, 
        'Eslovenia': {'masculino': 'esloveno', 'femenino': 'eslovena' }, 
        'España': {'masculino': 'español', 'femenino': 'española' }, 
        'Estados Unidos': {'masculino': 'estadounidense', 'femenino': 'estadounidense' }, 
        'Estonia': {'masculino': 'estonio', 'femenino': 'estonia' }, 
        'Etiopía': {'masculino': 'etíope', 'femenino': 'etíope' }, 
        'Filipinas': {'masculino': 'filipino', 'femenino': 'filipina' }, 
        'Finlandia': {'masculino': 'finlandés', 'femenino': 'finlandesa' }, 
        'Fiyi': {'masculino': 'fiyiano', 'femenino': 'fiyiana' }, 
        'Francia': {'masculino': 'francés', 'femenino': 'francesa' }, 
        'Gabón': {'masculino': 'gabonés', 'femenino': 'gabonesa' }, 
        'Gambia': {'masculino': 'gambiano', 'femenino': 'gambiana' }, 
        'Georgia': {'masculino': 'georgiano', 'femenino': 'georgiana' }, 
        'Ghana': {'masculino': 'ghanés', 'femenino': 'ghanesa' }, 
        'Granada': {'masculino': 'granadino', 'femenino': 'granadina' }, 
        'Grecia': {'masculino': 'griego', 'femenino': 'griega' }, 
        'Guatemala': {'masculino': 'guatemalteco', 'femenino': 'guatemalteca' }, 
        'Guinea': {'masculino': 'guineano', 'femenino': 'guineana' }, 
        'Guinea Ecuatorial': {'masculino': 'ecuatoguineano', 'femenino': 'ecuatoguineana' }, 
        'Guinea-Bisáu': {'masculino': 'guineano', 'femenino': 'guineana' }, 
        'Guyana': {'masculino': 'guyanés', 'femenino': 'guyanesa' }, 
        'Haití': {'masculino': 'haitiano', 'femenino': 'haitiana' }, 
        'Honduras': {'masculino': 'hondureño', 'femenino': 'hondureña' }, 
        'Hungría': {'masculino': 'húngaro', 'femenino': 'húngara' }, 
        'India': {'masculino': 'indio', 'femenino': 'india' }, 
        'Indonesia': {'masculino': 'indonesio', 'femenino': 'indonesia' }, 
        'Irak': {'masculino': 'iraquí', 'femenino': 'iraquí' }, 
        'Irán': {'masculino': 'iraní', 'femenino': 'iraní' }, 
        'Irlanda': {'masculino': 'irlandés', 'femenino': 'irlandesa' }, 
        'Islandia': {'masculino': 'islandés', 'femenino': 'islandesa' }, 
        'Islas Marshall': {'masculino': 'marshalés', 'femenino': 'marshalesa' }, 
        'Islas Salomón': {'masculino': 'salomonense', 'femenino': 'salomonense' }, 
        'Israel': {'masculino': 'israelí', 'femenino': 'israelí' }, 
        'Italia': {'masculino': 'italiano', 'femenino': 'italiana' }, 
        'Jamaica': {'masculino': 'jamaicano', 'femenino': 'jamaicana' }, 
        'Japón': {'masculino': 'japonés', 'femenino': 'japonesa' }, 
        'Jordania': {'masculino': 'jordano', 'femenino': 'jordana' }, 
        'Kazajistán': {'masculino': 'kazajo', 'femenino': 'kazaja' }, 
        'Kenia': {'masculino': 'keniano', 'femenino': 'keniana' }, 
        'Kirguistán': {'masculino': 'kirguís', 'femenino': 'kirguís' }, 
        'Kiribati': {'masculino': 'kiribatiano', 'femenino': 'kiribatiana' }, 
        'Kosovo': {'masculino': 'kosovar', 'femenino': 'kosovar' }, 
        'Kuwait': {'masculino': 'kuwaití', 'femenino': 'kuwaití' }, 
        'Laos': {'masculino': 'laosiano', 'femenino': 'laosiana' }, 
        'Lesoto': {'masculino': 'lesotense', 'femenino': 'lesotense' }, 
        'Letonia': {'masculino': 'letón', 'femenino': 'letona' }, 
        'Líbano': {'masculino': 'libanés', 'femenino': 'libanesa' }, 
        'Liberia': {'masculino': 'liberiano', 'femenino': 'liberiana' }, 
        'Libia': {'masculino': 'libio', 'femenino': 'libia' }, 
        'Liechtenstein': {'masculino': 'liechtensteiniano', 'femenino': 'liechtensteiniana' }, 
        'Lituania': {'masculino': 'lituano', 'femenino': 'lituana' }, 
        'Luxemburgo': {'masculino': 'luxemburgués', 'femenino': 'luxemburguesa' }, 
        'Madagascar': {'masculino': 'malgache', 'femenino': 'malgache' }, 
        'Malasia': {'masculino': 'malasio', 'femenino': 'malasia' }, 
        'Malaui': {'masculino': 'malauí', 'femenino': 'malauí' }, 
        'Maldivas': {'masculino': 'malivo', 'femenino': 'maldiva' }, 
        'Malí': {'masculino': 'maliense', 'femenino': 'maliense' }, 
        'Malta': {'masculino': 'maltés', 'femenino': 'maltesa' }, 
        'Marruecos': {'masculino': 'marroquí', 'femenino': 'marroquí' }, 
        'Mauricio': {'masculino': 'mauriciano', 'femenino': 'mauriciana' }, 
        'Mauritania': {'masculino': 'mauritano', 'femenino': 'mauritana' }, 
        'México': {'masculino': 'mexicano', 'femenino': 'mexicana' }, 
        #'Micronesia': {'masculino': '', 'femenino': '' }, 
        'Moldavia': {'masculino': 'moldavo', 'femenino': 'moldava' }, 
        'Mónaco': {'masculino': 'monegasco', 'femenino': 'monegasca' }, 
        'Mongolia': {'masculino': 'mongol', 'femenino': 'mongola' }, 
        'Montenegro': {'masculino': 'montenegrino', 'femenino': 'montenegrina' }, 
        'Mozambique': {'masculino': 'mozambiqueño', 'femenino': 'mozambiqueña' }, 
        'Namibia': {'masculino': 'namibio', 'femenino': 'namibia' }, 
        'Nauru': {'masculino': 'nauruano', 'femenino': 'nauruana' }, 
        'Nepal': {'masculino': 'nepalés', 'femenino': 'nepalesa' }, 
        'Nicaragua': {'masculino': 'nicaragüense', 'femenino': 'nicaragüense' }, 
        'Níger': {'masculino': 'nigerino', 'femenino': 'nigerina' }, 
        'Nigeria': {'masculino': 'nigeriano', 'femenino': 'nigeriana' }, 
        'Noruega': {'masculino': 'noruego', 'femenino': 'noruega' }, 
        'Nueva Zelanda': {'masculino': 'neozelandés', 'femenino': 'neozelandesa' }, 
        'Omán': {'masculino': 'omaní', 'femenino': 'omaní' }, 
        'Países Bajos': {'masculino': 'neerlandés', 'femenino': 'neerlandesa' }, 
        'Pakistán': {'masculino': 'pakistaní', 'femenino': 'pakistaní' }, 
        'Palaos': {'masculino': 'palauano', 'femenino': 'palauana' }, 
        'Panamá': {'masculino': 'panameño', 'femenino': 'panameña' }, 
        'Papúa Nueva Guinea': {'masculino': 'papú', 'femenino': 'papú' }, 
        'Paraguay': {'masculino': 'paraguayo', 'femenino': 'paraguaya' }, 
        'Perú': {'masculino': 'peruano', 'femenino': 'peruana' }, 
        'Polonia': {'masculino': 'polaco', 'femenino': 'polaca' }, 
        'Portugal': {'masculino': 'portugués', 'femenino': 'portugesa' }, 
        'Reino Unido': {'masculino': 'británico', 'femenino': 'británica' }, 
        'República Árabe Saharaui Democrática': {'masculino': 'saharaui', 'femenino': 'saharaui' }, 
        'República Centroafricana': {'masculino': 'centroafricano', 'femenino': 'centroafricana' }, 
        'República Checa': {'masculino': 'checo', 'femenino': 'checa' }, 
        'República de China': {'masculino': 'taiwanés', 'femenino': 'taiwanesa' }, 
        'República de Macedonia': {'masculino': 'macedonio', 'femenino': 'macedonia' }, 
        'República del Congo': {'masculino': 'congoleño', 'femenino': 'congoleña' }, 
        'República Democrática del Congo': {'masculino': 'congoleño', 'femenino': 'congoleña' }, 
        'República Dominicana': {'masculino': 'dominicano', 'femenino': 'dominicana' }, 
        'República Popular China': {'masculino': 'chino', 'femenino': 'china' }, 
        'Ruanda': {'masculino': 'ruandés', 'femenino': 'ruandesa' }, 
        'Rumania': {'masculino': 'rumano', 'femenino': 'rumana' }, 
        'Rusia': {'masculino': 'ruso', 'femenino': 'rusa' }, 
        'Samoa': {'masculino': 'samoano', 'femenino': 'samoana' }, 
        'San Cristóbal y Nieves': {'masculino': 'sancristobaleño', 'femenino': 'sancristobaleña' }, 
        'San Marino': {'masculino': 'sanmarinense', 'femenino': 'sanmarinense' }, 
        'San Vicente y las Granadinas': {'masculino': 'sanvicentino', 'femenino': 'sanvicentina' }, 
        'Santa Lucía': {'masculino': 'santalucense', 'femenino': 'santalucense' }, 
        'Santo Tomé y Príncipe': {'masculino': 'santotomense', 'femenino': 'santotomense' }, 
        'Senegal': {'masculino': 'senegalés', 'femenino': 'senegalesa' }, 
        'Serbia': {'masculino': 'serbio', 'femenino': 'serbia' }, 
        'Seychelles': {'masculino': 'seychellense', 'femenino': 'seychellense' }, 
        'Sierra Leona': {'masculino': 'sierraleonés', 'femenino': 'sierraleonesa' }, 
        'Singapur': {'masculino': 'singpurense', 'femenino': 'singpurense' }, 
        'Siria': {'masculino': 'sirio', 'femenino': 'siria' }, 
        'Somalia': {'masculino': 'somalí', 'femenino': 'somalí' }, 
        'Sri Lanka': {'masculino': 'ceilanés', 'femenino': 'ceilanesa' }, 
        'Suazilandia': {'masculino': 'suazi', 'femenino': 'suazi' }, 
        'Sudáfrica': {'masculino': 'sudafricano', 'femenino': 'sudafricana' }, 
        'Sudán': {'masculino': 'sudanés', 'femenino': 'sudanesa' }, 
        'Sudán del Sur': {'masculino': 'sursudanés', 'femenino': 'sursudanés' }, 
        'Suecia': {'masculino': 'sueco', 'femenino': 'sueca' }, 
        'Suiza': {'masculino': 'suizo', 'femenino': 'suiza' }, 
        'Surinam': {'masculino': 'surinamés', 'femenino': 'surinamesa' }, 
        'Tailandia': {'masculino': 'tailandés', 'femenino': 'tailandesa' }, 
        'Tanzania': {'masculino': 'tanzano', 'femenino': 'tanzana' }, 
        'Tayikistán': {'masculino': 'tayiko', 'femenino': 'tayika' }, 
        'Timor Oriental': {'masculino': 'timorense', 'femenino': 'timorense' }, 
        'Togo': {'masculino': 'togolés', 'femenino': 'togolesa' }, 
        'Tonga': {'masculino': 'tongano', 'femenino': 'tongana' }, 
        'Trinidad y Tobago': {'masculino': 'trinitense', 'femenino': 'trinitense' }, 
        'Túnez': {'masculino': 'tunecino', 'femenino': 'tunecina' }, 
        'Turkmenistán': {'masculino': 'turcomano', 'femenino': 'turcomana' }, 
        'Turquía': {'masculino': 'turco', 'femenino': 'turca' }, 
        'Tuvalu': {'masculino': 'tuvaluano', 'femenino': 'tuvaluana' }, 
        'Ucrania': {'masculino': 'ucraniano', 'femenino': 'ucraniana' }, 
        'Uganda': {'masculino': 'ugandés', 'femenino': 'ugandesa' }, 
        'Uruguay': {'masculino': 'uruguayo', 'femenino': 'uruguaya' }, 
        'Uzbekistán': {'masculino': 'uzbeko', 'femenino': 'uzbeka' }, 
        'Vanuatu': {'masculino': 'vanuatuense', 'femenino': 'vanuatuense' }, 
        'Venezuela': {'masculino': 'venezolano', 'femenino': 'venezolana' }, 
        'Vietnam': {'masculino': 'vietnamita', 'femenino': 'vietnamita' }, 
        'Yemen': {'masculino': 'yemení', 'femenino': 'yemení' }, 
        'Yibuti': {'masculino': 'yibutiano', 'femenino': 'yibutiana' }, 
        'Zambia': {'masculino': 'zambiano', 'femenino': 'zambiana' }, 
        'Zimbabue': {'masculino': 'zimbabuense', 'femenino': 'zimbabuense' }, 
    }
    ocupfem = {
        'abogado': 'abogada', 
        'activista': 'activista', 
        'actor': 'actriz', 
        'actor de doblaje': 'actriz de doblaje', 
        'actor de teatro': 'actriz de teatro', 
        'actor de teatro musical': 'actriz de teatro musical', 
        'actor de televisión': 'actriz de televisión', 
        'actor de voz': 'actriz de voz', 
        'actor pornográfico': 'actriz pornográfica',
        'agricultor': 'agricultora', 
        'ajedrecista': 'ajedrecista', 
        'algorista': 'algorista', 
        'antropólogo': 'antropóloga', 
        'arreglista': 'arreglista', 
        'artista': 'artista', 
        'artista digital': 'artista digital', 
        'artista plástico': 'artista plástica', 
        'asistente social': 'asistenta social', 
        'atleta': 'atleta', 
        'autobiógrafo': 'autobiógrafa', 
        'autor': 'autora', 
        'badmintonista': 'badmintonista', 
        'bailarín': 'bailarina', 
        'bailarín de ballet': 'bailarina de ballet', 
        'banquero': 'banquera', 
        'baterista': 'baterista', 
        'bhikkhuni': 'bhikkhuni', 
        'biatleta': 'biatleta', 
        'biógrafo': 'biógrafa', 
        'bloguero': 'bloguera', 
        'cabaretista': 'cabaretista', 
        'cantante': 'cantante', 
        'cantante de ópera': 'cantante de ópera', 
        'cantautor': 'cantautora', 
        'cartelista': 'cartelista', 
        'catedrático': 'catedrática', 
        'científico de la literatura': 'científica de la literatura', 
        'ciclista': 'ciclista', 
        'ciclista de ciclocrós': 'ciclista de ciclocrós', 
        'ciclista de pista': 'ciclista de pista', 
        'clavecinista': 'clavecinista', 
        'columnista': 'columnista', 
        'comediante': 'comediante', 
        'comediante en vivo': 'comediante en vivo', 
        'compositor': 'compositora', 
        'compositor de canciones': 'compositora de canciones', 
        'conductor radiofónico': 'conductora radiofónica', 
        'conservador de arte': 'conservadora de arte', 
        'coreógrafo': 'coreógrafa', 
        'crítico literario': 'crítica literaria', 
        'deportista': 'deportista', 
        'diplomático': 'diplomática', 
        'director artístico': 'directora artística', 
        'director de cine': 'directora de cine', 
        'director de coro': 'directora de coro', 
        'director de teatro': 'directora de teatro', 
        'director de orquesta': 'directora de orquesta', 
        'disc jockey': 'disc jockey', 
        'diseñador': 'diseñadora', 
        'diseñador de alta costura': 'diseñadora de alta costura', 
        'diseñador de joyas': 'diseñadora de joyas', 
        'diseñador de moda': 'diseñadora de moda', 
        'diseñador de vestuario': 'diseñadora de vestuario', 
        'diseñador gráfico': 'diseñadora gráfica', 
        'docente': 'docente', 
        'dramaturgo': 'dramaturga', 
        'economista': 'economista', 
        'editor': 'editora', 
        'editor de moda': 'editora de moda', 
        'educador': 'educadora', 
        'emprendedor': 'emprendedora', 
        'empresario': 'empresaria', 
        'ensayista': 'ensayista', 
        'escalador en roca': 'escaladora en roca', 
        'escenógrafo': 'escenógrafa', 
        'escritor': 'escritora', 
        'escritor de ciencia ficción': 'escritora de ciencia ficción', 
        'escritor de género policiaco': 'escritora de género policiaco', 
        'escritor de literatura infantil': 'escritora de literatura infantil', 
        'escritor de no ficción': 'escritora de no ficción', 
        'escultor': 'escultora', 
        'esgrimista': 'esgrimista', 
        'esquiador': 'esquiadora', 
        'esquiador acrobático': 'esquiadora acrobática', 
        'esquiador alpino': 'esquiadora alpino', 
        'esquiador de fondo': 'esquiadora de fondo', 
        'esquiador de travesía': 'esquiadora de travesía', 
        'etnomusicólogo': 'etnomusicóloga', 
        'explorador': 'exploradora', 
        'filántropo': 'filántropa', 
        'filólogo': 'filóloga', 
        'filósofo': 'filósofa', 
        'folclorista': 'folclorista', 
        'fondista': 'fondista', 
        'fotógrafo': 'fotógrafa', 
        'fotomodelo': 'fotomodelo', 
        'gimnasta': 'gimnasta', 
        'gimnasta artístico': 'gimnasta artística', 
        'gimnasta rítmico': 'gimnasta rítmica', 
        'golfista': 'golfista', 
        'guionista': 'guionista', 
        'guitarrista': 'guitarrista', 
        'guitarrista clásico': 'guitarrista clásico', 
        'guitarrista de jazz': 'guitarrista de jazz', 
        'historiador': 'historiadora', 
        'historiador de la Edad Moderna': 'historiadora de la Edad Moderna', 
        'historiador de la música': 'historiadora de la música', 
        'historietista': 'historietista', 
        'humorista': 'humorista', 
        'ilustrador': 'ilustradora', 
        'ingeniero': 'ingeniera', 
        'investigador': 'investigadora', 
        'jugador de squash': 'jugadora de squash', 
        'jugador de voleibol de playa': 'jugadora de voleibol de playa', 
        'juez': 'jueza', 
        'jugador de go': 'jugadora de go', 
        'jurista': 'jurista', 
        'karateka': 'karateka', 
        'librero': 'librera', 
        'lingüista': 'lingüista', 
        'luchador profesional': 'luchadora profesional', 
        'maestro de ballet': 'maestra de ballet', 
        'manager': 'manager', 
        'maratonista': 'maratonista', 
        'matemático': 'matemática', 
        'médico': 'médico', 
        'militar': 'militar', 
        'modelo': 'modelo', 
        'modelo artístico': 'modelo artística', 
        'modelo erótico': 'modelo erótica', 
        'modelo erótica': 'modelo erótica', 
        'montañero': 'montañera', 
        'músico': 'música', 
        'musicólogo': 'musicóloga', 
        'músico de jazz': 'música de jazz', 
        'nadador': 'nadadora', 
        'novelista': 'novelista', 
        'oftalmólogo': 'oftalmóloga', 
        'orador motivacional': 'oradora motivacional', 
        'organista': 'organista', 
        'organizador sindical': 'organizadora sindical', 
        'patinador artístico sobre hielo': 'patinadora artística sobre hielo', 
        'patinador de velocidad': 'patinadora de velocidad', 
        'participante de concurso de belleza': 'participante de concurso de belleza', 
        'pedagogo': 'pedagoga', 
        'pentatleta': 'pentatleta', 
        'percusionista': 'percusionista', 
        'periodista': 'periodista', 
        'pianista': 'pianista', 
        'piloto de automovilismo': 'piloto de automovilismo', 
        'piloto de carreras': 'piloto de carreras', 
        'pintor': 'pintora', 
        'poeta': 'poeta', 
        'político': 'política', 
        'portavoz': 'portavoz', 
        'presentador': 'presentadora', 
        'presentador de noticias': 'presentadora de noticias', 
        'presentador de televisión': 'presentadora de televisión', 
        'productor': 'productora', 
        'productor de cine': 'productora de cine', 
        'productor de televisión': 'productora de televisión', 
        'productor discográfico': 'productora discográfica', 
        'profesor': 'profesora', 
        'profesor de educación superior': 'profesora de educación superior', 
        'profesor de música': 'profesora de música', 
        'prosista': 'prosista', 
        'psicólogo': 'psicóloga', 
        'psiquiatra': 'psiquiatra', 
        'publicista': 'publicista', 
        'químico': 'química', 
        'rapero': 'rapera', 
        'realizador': 'realizadora', 
        'regatista': 'regatista', 
        'remero': 'remera', 
        'saltador de esquí': 'saltadora de esquí', 
        'saltador de pértiga': 'saltadora de pértiga', 
        'saxofonista': 'saxofonista', 
        'sindicalista': 'sindicalista', 
        'socialité': 'socialité', 
        'sociólogo': 'socióloga', 
        'solista': 'solista', 
        'surfista': 'surfista', 
        'tenista': 'tenista', 
        'tenista en silla de ruedas': 'tenista en silla de ruedas', 
        'tipógrafo': 'tipógrafa', 
        'tirador': 'tiradora', 
        'titiritero': 'titiritera', 
        'traductor': 'traductora', 
        'triatleta': 'triatleta', 
        'ultramaratonista': 'ultramaratonista', 
        'velocista': 'velocista', 
        'veterinario': 'veterinaria', 
        'violinista': 'violinista', 
        'viticultor': 'viticultora', 
        'vocalista': 'vocalista', 
        'voleibolista': 'voleibolista', 
        'windsurfista': 'windsurfista', 
        'yudoca': 'yudoca', 
        'youtuber': 'youtuber', 
    }

    """
    29 poeta abogado
      5 playmate
      5 powerlifter
      5 Q21500772
      6 nightclub owner
      6 romanista
      7 salonnière
     10 alumno
     11 escritor de no ficción
     11 narrador de audiolibros
     12 seiyū
     13 Liedermacher
     14 activista por los derechos humanos
     14 contador
     14 Perito
     17 yodeler
     18 snowboarder
     19 showgirl
     20 astrólogo
     20 masajista
     22 mediador lingüístico
     24 humanitario
     24 voluntariado
    """
    
    site = pywikibot.Site('librefind', 'librefind')
    totalbios = 0
    skipuntilcountry = ''
    for p27k, p27v in p27list:
        subtotalbios = 0
        print('\n','#'*50,'\n',p27k,p27v,'\n','#'*50)
        if skipuntilcountry:
            if skipuntilcountry == p27k:
                skipuntilcountry = ''
            else:
                print('Skiping...')
                continue
        
        for minyear, maxyear in [[1, 1700], [1700, 1800], [1800, 1850], [1850, 1900], [1900, 1920], [1920, 1940], [1940, 1950], [1950, 1960], [1960, 1970], [1970, 1980], [1980, 1990]]:
            print('From %s to %s' % (minyear, maxyear))
            #url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=SELECT%20DISTINCT%20%3Fitem%20%3FitemLabel%20%3FcountryLabel%20%3FsexLabel%20%3FbirthplaceLabel%20%3Fbirthdate%20%3FdeathplaceLabel%20%3Fdeathdate%20%3FoccupationLabel%20%3Fimage%20%3Fcommonscat%20%3Fwebsite%20%3Fsitelink%20WHERE%20%7B%0A%20%20%3Fitem%20wdt%3AP31%20wd%3AQ5.%0A%20%20%3Fitem%20wdt%3AP27%20wd%3A' + p27v + '.%0A%20%20%3Fitem%20wdt%3AP27%20%3Fcountry.%0A%20%20%3Fitem%20wdt%3AP21%20%3Fsex.%0A%20%20%3Fitem%20wdt%3AP19%20%3Fbirthplace.%0A%20%20%3Fitem%20wdt%3AP569%20%3Fbirthdate.%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP20%20%3Fdeathplace.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP570%20%3Fdeathdate.%20%7D%0A%20%20%3Fitem%20wdt%3AP106%20%3Foccupation.%0A%20%20%3Fitem%20wdt%3AP18%20%3Fimage.%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP373%20%3Fcommonscat.%20%7D%0A%20%20%3Fitem%20wdt%3AP856%20%3Fwebsite.%0A%20%20%3Fsitelink%20schema%3Aabout%20%3Fitem.%0A%20%20FILTER%20NOT%20EXISTS%20%7B%20%3Fwfr%20schema%3Aabout%20%3Fitem%20.%20%3Fwfr%20schema%3AinLanguage%20%22es%22%20%7D%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22es%2Cen%22%20%7D%0A%7D'
            #url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=SELECT%20DISTINCT%20%3Fitem%20%3FitemLabel%20%3FcountryLabel%20%3FsexLabel%20%3FbirthplaceLabel%20%3Fbirthdate%20%3FdeathplaceLabel%20%3Fdeathdate%20%3FoccupationLabel%20%3Fimage%20%3Fcommonscat%20%3Fwebsite%20%3Fsitelink%20WHERE%20%7B%0A%20%20%3Fitem%20wdt%3AP31%20wd%3AQ5.%0A%20%20%3Fitem%20wdt%3AP27%20wd%3A' + p27v + '.%0A%20%20%3Fitem%20wdt%3AP27%20%3Fcountry.%0A%20%20%3Fitem%20wdt%3AP21%20%3Fsex.%0A%20%20%3Fitem%20wdt%3AP19%20%3Fbirthplace.%0A%20%20%3Fitem%20wdt%3AP569%20%3Fbirthdate.%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP20%20%3Fdeathplace.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP570%20%3Fdeathdate.%20%7D%0A%20%20%3Fitem%20wdt%3AP106%20%3Foccupation.%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP18%20%3Fimage.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP373%20%3Fcommonscat.%20%7D%0A%20%20%3Fitem%20wdt%3AP856%20%3Fwebsite.%0A%20%20%3Fsitelink%20schema%3Aabout%20%3Fitem.%0A%20%20FILTER%20NOT%20EXISTS%20%7B%20%3Fwfr%20schema%3Aabout%20%3Fitem%20.%20%3Fwfr%20schema%3AinLanguage%20%22es%22%20%7D%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22es%2Cen%22%20%7D%0A%7D'
            url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=SELECT%20DISTINCT%20%3Fitem%20%3FitemLabel%20%3FcountryLabel%20%3FsexLabel%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3FbirthplaceLabel%20%3Fbirthdate%20%3FdeathplaceLabel%20%3Fdeathdate%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3FoccupationLabel%20%3Fimage%20%3Fcommonscat%20%3Fwebsite%20%0AWHERE%20%7B%0A%20%20%3Fitem%20wdt%3AP31%20wd%3AQ5.%0A%20%20%3Fitem%20wdt%3AP27%20wd%3A'+p27v+'.%0A%20%20%3Fitem%20wdt%3AP27%20%3Fcountry.%0A%20%20%3Fitem%20wdt%3AP21%20%3Fsex.%0A%20%20%3Fitem%20wdt%3AP19%20%3Fbirthplace.%0A%20%20%3Fitem%20wdt%3AP569%20%3Fbirthdate.%0A%20%20FILTER%20(year(%3Fbirthdate)%20%3E%3D%20'+str(minyear)+')%20.%0A%20%20FILTER%20(year(%3Fbirthdate)%20%3C%20'+str(maxyear)+')%20.%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP20%20%3Fdeathplace.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP570%20%3Fdeathdate.%20%7D%0A%20%20%3Fitem%20wdt%3AP106%20%3Foccupation.%0A%20%20%3Fitem%20wdt%3AP18%20%3Fimage.%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP373%20%3Fcommonscat.%20%7D%0A%20%20%23OPTIONAL%20%7B%20%3Fitem%20wdt%3AP856%20%3Fwebsite.%20%7D%0A%20%20FILTER%20NOT%20EXISTS%20%7B%20%3Fwfr%20schema%3Aabout%20%3Fitem%20.%20%3Fwfr%20schema%3AinLanguage%20%22es%22%20%7D%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22es%2Cen%2Cfr%2Cpt%2Cit%2Cde%2Cca%22%20%7D%0A%7D' # %23 delante de OPTIONAL website para q no descarte las q no tienen web
            """
            SELECT DISTINCT ?item ?itemLabel ?countryLabel ?sexLabel
                ?birthplaceLabel ?birthdate ?deathplaceLabel ?deathdate 
                ?occupationLabel ?image ?commonscat ?website 
            WHERE {
              ?item wdt:P31 wd:Q5.
              ?item wdt:P27 wd:Q38.
              ?item wdt:P27 ?country.
              ?item wdt:P21 ?sex.
              ?item wdt:P19 ?birthplace.
              ?item wdt:P569 ?birthdate.
              FILTER (year(?birthdate) >= 1900) .
              FILTER (year(?birthdate) < 1920) .
              OPTIONAL { ?item wdt:P20 ?deathplace. }
              OPTIONAL { ?item wdt:P570 ?deathdate. }
              ?item wdt:P106 ?occupation.
              ?item wdt:P18 ?image.
              OPTIONAL { ?item wdt:P373 ?commonscat. }
              OPTIONAL { ?item wdt:P856 ?website. }
              FILTER NOT EXISTS { ?wfr schema:about ?item . ?wfr schema:inLanguage "es" }
              SERVICE wikibase:label { bd:serviceParam wikibase:language "es,en,fr,pt,it,de,ca" }
            }
            """
            #print(url)
            url = '%s&format=json' % (url)
            
            time.sleep(1)
            req = urllib.request.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
            sparql = urllib.request.urlopen(req).read().strip().decode('utf-8')
            sparql = '%s ]\n  }\n}' % (', {\n      "item" : {'.join(sparql.split(', {\n      "item" : {')[:-1]))
            #print(sparql)
            try:
                json1 = json.loads(sparql)
            except:
                print('Error downloading SPARQL? Skiping\n')
                continue
            bios = {}
            for result in json1['results']['bindings']:
                q = 'item' in result and result['item']['value'].split('/entity/')[1] or ''
                nombre = 'itemLabel' in result and result['itemLabel']['value'] or ''
                country = 'countryLabel' in result and result['countryLabel']['value'] or ''
                sexo = 'sexLabel' in result and result['sexLabel']['value'] or ''
                if sexo:
                    if sexo == 'femenino' or sexo.startswith('mujer'): #mujer transgenero Q1052281
                        sexo = 'femenino'
                    else:
                        sexo = 'masculino'
                lnac = 'birthplaceLabel' in result and result['birthplaceLabel']['value'] or ''
                fnac = 'birthdate' in result and result['birthdate']['value'] or ''
                lfal = 'deathplaceLabel' in result and result['deathplaceLabel']['value'] or ''
                ffal = 'deathdate' in result and result['deathdate']['value'] or ''
                ocup = 'occupationLabel' in result and result['occupationLabel']['value'] or ''
                image = 'image' in result and urllib.parse.unquote(result['image']['value']).split('/Special:FilePath/')[1] or ''
                commonscat = 'commonscat' in result and result['commonscat']['value'] or ''
                if commonscat:
                    commonscat = 'Category:%s' % (commonscat)
                website = 'website' in result and result['website']['value'] or ''
                
                """
                if sexo == 'femenino': # para ver ocupaciones femeninas y traducirlas en el dict
                    print(ocup)
                    continue
                """
                
                if q in bios:
                    for x, y in [[country, 'countries'], [image, 'images'], [ocup, 'ocups'], [website, 'websites']]:
                        if x and x not in bios[q][y]:
                            bios[q][y].append(x)
                            bios[q][y].sort()
                else:
                    bios[q] = {
                        'q': q, 'nombre': nombre, 'countries': [country], 'sexo': sexo, 'lnac': lnac, 'fnac': fnac, 'lfal': lfal, 'ffal': ffal, 'ocups': [ocup], 'images': [image], 'commonscat': commonscat, 'websites': [website], 
                    }
            
            bios_list = [[props['nombre'], q, props] for q, props in bios.items()]
            bios_list.sort()
            print('Encontradas %s bios\n' % (len(bios_list)))
            totalbios += len(bios_list)
            subtotalbios += len(bios_list)
            #continue
            
            for nombre, q, props in bios_list:
                print('\n', '#'*10, props['nombre'], '#'*10, '\n')
                if re.search(r'(?im)^Q\d', nombre):
                    print('Error, nombre indefinido, saltamos')
                    continue
                if not props['ocups']:
                    print('Error, sin ocupacion, saltamos')
                    continue
                if len(props['countries']) > 1:
                    print('Mas de una nacionalidad, saltamos')
                    continue
                images = props['images']
                if '' in images:
                    images.remove('')
                if not images:
                    print('No hay imagen, saltamos')
                    continue
                websites = props['websites']
                if '' in websites:
                    websites.remove('')
                if not websites:
                    print('No hay website, saltamos')
                    #continue
                
                #remove unuseful ocups
                ocups = []
                for ocup in props['ocups']:
                    ocup2 = '%s de' % (ocup)
                    if not ocup2 in ', '.join(props['ocups']):
                        ocups.append(ocup)
                
                #intro
                if props['ffal']: #fallecido ya
                    intro = 'fue'
                else: #vivo
                    intro = 'es'
                
                if 'sexo' in props and props['sexo'] == 'femenino': #mujer
                    skipbio = False
                    for ocup in ocups:
                        if ocup not in ocupfem:
                            skipbio = True #skip this bio, we have not female translation for this ocupation
                    if skipbio:
                        continue
                    
                    intro = '%s una %s' % (intro, ', '.join([ocupfem[x] for x in ocups[:-1]]))
                    if len(ocups) > 1:
                        if ocupfem[ocups[-1]].lower().startswith('i') or ocupfem[ocups[-1]].lower().startswith('hi'):
                            intro = '%s e %s' % (intro, ocupfem[ocups[-1]])
                        else:
                            intro = '%s y %s' % (intro, ocupfem[ocups[-1]])
                    else:
                        intro = '%s%s' % (intro, ocupfem[ocups[-1]])
                    intro = '%s %s' % (intro, country2nationality[props['countries'][0]][props['sexo']])
                else: #hombre
                    intro = '%s un %s' % (intro, ', '.join(ocups[:-1]))
                    if len(ocups) > 1:
                        if ocups[-1].lower().startswith('i') or ocups[-1].lower().startswith('hi'):
                            intro = '%s e %s' % (intro, ocups[-1])
                        else:
                            intro = '%s y %s' % (intro, ocups[-1])
                    else:
                        intro = '%s%s' % (intro, ocups[-1])
                    intro = '%s %s' % (intro, country2nationality[props['countries'][0]][props['sexo']])
                
                websites = ''.join(["{{Website\n|title=Web oficial\n|url=%s\n|level=0\n}}" % (x) for x in websites])
                gallery = ''.join(["{{Gallery file\n|filename=%s\n}}" % (x) for x in images])
                birthdeath = '[[%s]], %s' % (props['lnac'], convertirfecha(props['fnac']))
                if props['lfal'] and props['ffal']:
                    birthdeath = '%s - %s, %s' % (birthdeath, props['lfal'] == props['lnac'] and 'íbidem' or '[[%s]]' % (props['lfal']), convertirfecha(props['ffal']))

                output = """{{Infobox Result2
|search=%s
|introduction={{selflink|%s}} (%s) %s.%s
|wikidata=%s%s%s
}}""" % (props['nombre'], props['nombre'], birthdeath, intro, props['commonscat'] and '\n|commons=%s' % (props['commonscat']) or '', props['q'], websites and '\n|websites=%s' % (websites) or '', gallery and '\n|gallery=%s' % (gallery) or '')
                
                try:
                    time.sleep(1)
                    #page = pywikibot.Page(site, '%s (%s)' % (props['nombre'], props['q']))
                    page = pywikibot.Page(site, props['nombre'])
                    if page.exists():
                        if page.text != output:
                            pywikibot.showDiff(page.text, output)
                            page.text = output
                            page.save('BOT - Actualizando página de resultados')
                        else:
                            print('No changes needed')
                    else:
                        pywikibot.showDiff('', output)
                        page.text = output
                        page.save('BOT - Creando página de resultados')
                except:
                    print('Error while saving, waiting some seconds and skiping')
                    time.sleep(10)
        
        print('Subtotal bios %s\n' % (subtotalbios))
    print('\nTotal bios %s' % (totalbios))

if __name__ == '__main__':
    main()
