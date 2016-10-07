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
import sys
import time
import urllib
import urllib.request
import urllib.parse

import pywikibot

""" TODO

* Que cuando un elemento en wikidata cambie de alias (por ej. si alguien corrige el nombre o lo traduce), el bot renombre la pagina de librefind. Hay algunos "X of Y" de nombres aristocraticos y reyes sin traducir todavia por ejemplo.
* Que hacer con las fechas incompletas que devuelven 1 de enero?

"""

labels = { 'educatedat': {}, 'positions': {}, 'occupations': {}, 'awards': {}, }
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
    'abad': 'abad', 
    'abogado': 'abogada', 
    'abogado defensor': 'abogada defensora', 
    'académico': 'académica', 
    'acordeonista': 'acordeonista', 
    'activista': 'activista', 
    'actor': 'actriz', 
    'actor de cine': 'actriz de cine', 
    'actor de doblaje': 'actriz de doblaje', 
    'actor de teatro': 'actriz de teatro', 
    'actor de teatro musical': 'actriz de teatro musical', 
    'actor de televisión': 'actriz de televisión', 
    'actor de voz': 'actriz de voz', 
    'actor pornográfico': 'actriz pornográfica',
    'aeronauta': 'aeronauta', 
    'agente de bolsa': 'agente de bolsa', 
    'agente de talentos': 'agente de talentos', 
    'agente doble': 'agente doble', 
    'agente penitenciario': 'agente penitenciaria', 
    'agricultor': 'agricultora', 
    'ajedrecista': 'ajedrecista', 
    'algorista': 'algorista', 
    'ama de llaves': 'ama de llaves', 
    'anatomista': 'anatomista', 
    'antropólogo': 'antropóloga', 
    'apneísta': 'apneísta', 
    'árbitro': 'árbitro', 
    'archivero': 'archivera', 
    'arqueólogo': 'arqueóloga', 
    'arqueólogo clásico': 'arqueóloga clásica', 
    'arquitecto': 'arquitecta', 
    'arreglista': 'arreglista', 
    'artesano': 'artesana', 
    'artista': 'artista', 
    'artista callejero': 'artista callejero', 
    'artista contemporáneo': 'artista contemporánea', 
    'artista de circo': 'artista de circo', 
    'artista de performance': 'artista de performance', 
    'artista digital': 'artista digital', 
    'artista musical': 'artista musical', 
    'artista plástico': 'artista plástica', 
    'asesino en serie': 'asesina en serie', 
    'asesor': 'asesora', 
    'asesor fiscal': 'asesora fiscal', 
    'asistente social': 'asistenta social', 
    'astrofísico': 'astrofísica', 
    'astrónomo': 'astrónoma', 
    'atleta': 'atleta', 
    'autobiógrafo': 'autobiógrafa', 
    'autor': 'autora', 
    'aventurero': 'aventurera', 
    'aviador': 'aviadora', 
    'bacteriólogo': 'bacterióloga', 
    'badmintonista': 'badmintonista', 
    'bailarín': 'bailarina', 
    'bailarín de ballet': 'bailarina de ballet', 
    'baloncestista': 'baloncestista', 
    'balonmanista': 'balonmanista', 
    'banjista': 'banjista', 
    'banquero': 'banquera', 
    'baterista': 'baterista', 
    'bhikkhuni': 'bhikkhuni', 
    'biatleta': 'biatleta', 
    'bibliotecario': 'bibliotecaria', 
    'biógrafo': 'biógrafa', 
    'biólogo': 'bióloga', 
    'bloguero': 'bloguera', 
    'botánico': 'botánica', 
    'boxeador': 'boxeadora', 
    'cabaretista': 'cabaretista', 
    'camarógrafo': 'camarógrafa', 
    'cantante': 'cantante', 
    'cantante de ópera': 'cantante de ópera', 
    'cantautor': 'cantautora', 
    'caricaturista': 'caricaturista', 
    'cartelista': 'cartelista', 
    'catedrático': 'catedrática', 
    'ceramista': 'ceramista', 
    'chef': 'chef', 
    'científico de la literatura': 'científica de la literatura', 
    'ciclista': 'ciclista', 
    'ciclista de ciclocrós': 'ciclista de ciclocrós', 
    'ciclista de pista': 'ciclista de pista', 
    'cirujano': 'cirujana', 
    'clarinetista': 'clarinetista', 
    'clavecinista': 'clavecinista', 
    'cocinero': 'cocinera', 
    'coleccionista de arte': 'coleccionista de arte', 
    'columnista': 'columnista', 
    'comediante': 'comediante', 
    'comediante en vivo': 'comediante en vivo', 
    'comentarista': 'comentarista', 
    'comentarista deportivo': 'comentarista deportiva', 
    'compositor': 'compositora', 
    'compositor de canciones': 'compositora de canciones', 
    'conductor radiofónico': 'conductora radiofónica', 
    'conservador de arte': 'conservadora de arte', 
    'consultor': 'consultora', 
    'contorsionista': 'contorsionista', 
    'coreógrafo': 'coreógrafa', 
    'corista': 'corista', 
    'corresponsal de guerra': 'corresponsal de guerra', 
    'crítico': 'crítica', 
    'crítico de arte': 'crítica de arte', 
    'crítico literario': 'crítica literaria', 
    'cuentista': 'cuentista', 
    'dama de compañía': 'dama de compañía', 
    'delineante': 'delineante', 
    'dentista': 'dentista', 
    'deportista': 'deportista', 
    'desarrollador de videojuegos': 'desarrolladora de videojuegos', 
    'diaconisa': 'diaconisa', 
    'diarista': 'diarista', 
    'diplomático': 'diplomática', 
    'dibujante': 'dibujante', 
    'dibujante de historieta': 'dibujante de historieta', 
    'dibujante de prensa': 'dibujante de prensa', 
    'director artístico': 'directora artística', 
    'director de cine': 'directora de cine', 
    'director de coro': 'directora de coro', 
    'director de finanzas': 'directora de finanzas', 
    'director de fotografía': 'directora de fotografía', 
    'director de teatro': 'directora de teatro', 
    'director de televisión': 'directora de televisión', 
    'director de orquesta': 'directora de orquesta', 
    'director de videos musicales': 'directora de videos musicales', 
    'director musical': 'directora musical', 
    'disc jockey': 'disc jockey', 
    'diseñador': 'diseñadora', 
    'diseñador de alta costura': 'diseñadora de alta costura', 
    'diseñador de estampillas': 'diseñadora de estampillas', 
    'diseñador de joyas': 'diseñadora de joyas', 
    'diseñador de moda': 'diseñadora de moda', 
    'diseñador de vestuario': 'diseñadora de vestuario', 
    'diseñador gráfico': 'diseñadora gráfica', 
    'docente': 'docente', 
    'dramaturgo': 'dramaturga', 
    'economista': 'economista', 
    'editor': 'editora', 
    'editor colaborador': 'editora colaboradora', 
    'editor de moda': 'editora de moda', 
    'educador': 'educadora', 
    'educador especializado': 'educadora especializada', 
    'educador sexual': 'educadora sexual', 
    'egiptólogo': 'egiptóloga', 
    'empleado': 'empleada', 
    'emprendedor': 'emprendedora', 
    'empresario': 'empresaria', 
    'enfermero': 'enfermera', 
    'ensayista': 'ensayista', 
    'entomólogo': 'entomóloga', 
    'entrenador de baloncesto': 'entrenadora de baloncesto', 
    'entrenador de fútbol': 'entrenadora de fútbol', 
    'entrenador personal': 'entrenadora personal', 
    'escalador en roca': 'escaladora en roca', 
    'escenógrafo': 'escenógrafa', 
    'escritor': 'escritora', 
    'escritora': 'escritora', 
    'escritor de ciencia ficción': 'escritora de ciencia ficción', 
    'escritor de género policiaco': 'escritora de género policiaco', 
    'escritor de literatura infantil': 'escritora de literatura infantil', 
    'escritor de no ficción': 'escritora de no ficción', 
    'escritor sobre medicina': 'escritora sobre medicina', 
    'escultor': 'escultora', 
    'esgrimista': 'esgrimista', 
    'eslavista': 'eslavista', 
    'especialista de cine': 'especialista de cine', 
    'esquiador': 'esquiadora', 
    'esquiador acrobático': 'esquiadora acrobática', 
    'esquiador alpino': 'esquiadora alpino', 
    'esquiador de fondo': 'esquiadora de fondo', 
    'esquiador de travesía': 'esquiadora de travesía', 
    'esquiador orientador': 'esquiadora orientadora', 
    'etnógrafo': 'etnógrafa', 
    'etnólogo': 'etnóloga', 
    'etnomusicólogo': 'etnomusicóloga', 
    'explorador': 'exploradora', 
    'fabricante de pianos': 'fabricante de pianos', 
    'feminista': 'feminista', 
    'filántropo': 'filántropa', 
    'filólogo': 'filóloga', 
    'filósofo': 'filósofa', 
    'filólogo clásico': 'filósofa clásica', 
    'físico': 'física', 
    'folclorista': 'folclorista', 
    'fondista': 'fondista', 
    'fotógrafo': 'fotógrafa', 
    'fotomodelo': 'fotomodelo', 
    'fotoperiodista': 'fotoperiodista', 
    'futbolista': 'futbolista', 
    'ganadero': 'ganadera', 
    'genetista': 'genetista', 
    'germanista': 'germanista', 
    'gimnasta': 'gimnasta', 
    'gimnasta artístico': 'gimnasta artística', 
    'gimnasta rítmico': 'gimnasta rítmica', 
    'ginecólogo': 'ginecóloga', 
    'glaciólogo': 'glacióloga', 
    'golfista': 'golfista', 
    'grabador': 'grabadora', 
    'grabador de cobre': 'grabadora de cobre', 
    'guardabosques': 'guardabosques', 
    'guionista': 'guionista', 
    'guitarrista': 'guitarrista', 
    'guitarrista clásico': 'guitarrista clásico', 
    'guitarrista de jazz': 'guitarrista de jazz', 
    'historiador': 'historiadora', 
    'historiador de la Edad Moderna': 'historiadora de la Edad Moderna', 
    'historiador de la literatura': 'historiadora de la literatura', 
    'historiador de la matemática': 'historiadora de la matemática', 
    'historiador de la música': 'historiadora de la música', 
    'historiador del arte': 'historiadora del arte', 
    'historiador del derecho': 'historiadora del derecho', 
    'historiador local': 'historiadora local', 
    'historiador social': 'historiadora social', 
    'historietista': 'historietista', 
    'humorista': 'humorista', 
    'humorista gráfico': 'humorista gráfico', 
    'ilustrador': 'ilustradora', 
    'industrial': 'industrial', 
    'informático teórico': 'informática teórica', 
    'ingeniero': 'ingeniera', 
    'ingeniero de software': 'ingeniera de software', 
    'ingeniero de sonido': 'ingeniera de sonido', 
    'internista': 'internista', 
    'investigador': 'investigadora', 
    'jefe de empresa': 'jefa de empresa', 
    'jugador de hockey sobre hielo': 'jugadora de hockey sobre hielo', 
    'jugador de póquer': 'jugadora de póquer', 
    'jugador de rugby union': 'jugadora de rugby union', 
    'jugador de sóftbol': 'jugadora de sóftbol', 
    'jugador de squash': 'jugadora de squash', 
    'jugador de voleibol de playa': 'jugadora de voleibol de playa', 
    'juez': 'jueza', 
    'jugador de go': 'jugadora de go', 
    'jurista': 'jurista', 
    'karateka': 'karateka', 
    'lanzador de disco': 'lanzadora de disco', 
    'lanzador de jabalina': 'lanzadora de jabalina', 
    'letrista': 'letrista', 
    'librero': 'librera', 
    'libretista': 'libretista', 
    'lingüista': 'lingüista', 
    'litógrafo': 'litógrafa', 
    'lobista': 'lobista', 
    'luchador de artes marciales mixtas': 'luchadora de artes marciales mixtas', 
    'luchador profesional': 'luchadora profesional', 
    'luger': 'luger', 
    'maestro de ballet': 'maestra de ballet', 
    'maestro de ceremonias': 'maestra de ceremonias', 
    'mago': 'maga', 
    'manager': 'manager', 
    'mandolinista': 'mandolinista', 
    'mangaka': 'mangaka', 
    'maquillador': 'maquilladora', 
    'maratonista': 'maratonista', 
    'matemático': 'matemática', 
    'matrona': 'matrona', 
    'medallista': 'medallista', 
    'médico': 'médico', 
    'médico especialista': 'médico especialista', 
    'mediofondista': 'mediofondista', 
    'militante de la resistencia': 'militante de la resistencia', 
    'militar': 'militar', 
    'místico': 'mística', 
    'modelo': 'modelo', 
    'modelo artístico': 'modelo artística', 
    'modelo erótico': 'modelo erótica', 
    'modelo erótica': 'modelo erótica', 
    'monja': 'monja', 
    'montador': 'montadora', 
    'montañero': 'montañera', 
    'multiinstrumentista': 'multiinstrumentista', 
    'musher': 'musher', 
    'músico': 'música', 
    'musicólogo': 'musicóloga', 
    'músico de jazz': 'música de jazz', 
    'nadador': 'nadadora', 
    'naturalista': 'naturalista', 
    'neurocientífico': 'neurocientífica', 
    'neurólogo': 'neuróloga', 
    'novelista': 'novelista', 
    'nutricionista': 'nutricionista', 
    'obstetra': 'obstetra', 
    'oficial': 'oficial', 
    'oftalmólogo': 'oftalmóloga', 
    'orador motivacional': 'oradora motivacional', 
    'organista': 'organista', 
    'organizador sindical': 'organizadora sindical', 
    'ornitólogo': 'ornitóloga', 
    'pacifista': 'pacifista', 
    'paleontólogo': 'paleontóloga', 
    'pastor': 'pastora', 
    'patinador artístico sobre hielo': 'patinadora artística sobre hielo', 
    'patinador de velocidad': 'patinadora de velocidad', 
    'participante de concurso de belleza': 'participante de concurso de belleza', 
    'pedagogo': 'pedagoga', 
    'pediatra': 'pediatra', 
    'peluquero': 'peluquera', 
    'pentatleta': 'pentatleta', 
    'percusionista': 'percusionista', 
    'periodista': 'periodista', 
    'pianista': 'pianista', 
    'piloto de automovilismo': 'piloto de automovilismo', 
    'piloto de carreras': 'piloto de carreras', 
    'piloto de helicóptero': 'piloto de helicóptero', 
    'pintor': 'pintora', 
    'pintor retratista': 'pintora retratista', 
    'playmate': 'playmate', 
    'podcaster': 'podcaster', 
    'poeta': 'poeta', 
    'político': 'política', 
    'politólogo': 'politóloga', 
    'portavoz': 'portavoz', 
    'prehistoriador': 'prehistoriadora', 
    'presentador': 'presentadora', 
    'presentador de noticias': 'presentadora de noticias', 
    'presentador de televisión': 'presentadora de televisión', 
    'princesa': 'princesa', 
    'productor': 'productora', 
    'productor de cine': 'productora de cine', 
    'productor de televisión': 'productora de televisión', 
    'productor discográfico': 'productora discográfica', 
    'productor ejecutivo': 'productora ejecutiva', 
    'profesor': 'profesora', 
    'profesor de educación superior': 'profesora de educación superior', 
    'profesor de música': 'profesora de música', 
    'programador': 'programadora', 
    'prosista': 'prosista', 
    'prostituta': 'prostituta', 
    'psicólogo': 'psicóloga', 
    'psicoterapeuta': 'psicoterapeuta', 
    'psiquiatra': 'psiquiatra', 
    'publicista': 'publicista', 
    'químico': 'química', 
    'rapero': 'rapera', 
    'realizador': 'realizadora', 
    'redactor en jefe': 'redactora en jefe', 
    'regatista': 'regatista', 
    'religioso': 'religiosa', 
    'remero': 'remera', 
    'reportero': 'reportera', 
    'restaurador': 'restauradora', 
    'revolucionario': 'revolucionaria', 
    'sacerdote': 'sacerdote', 
    'salonnière': 'salonnière', 
    'saltador': 'saltadora', 
    'saltador de esquí': 'saltadora de esquí', 
    'saltador de longitud': 'saltadora de longitud', 
    'saltador de pértiga': 'saltadora de pértiga', 
    'sastre': 'sastre', 
    'saxofonista': 'saxofonista', 
    'secretario': 'secretaria', 
    'seiyū': 'seiyū', 
    'sindicalista': 'sindicalista', 
    'snowboarder': 'snowboarder', 
    'socialité': 'socialité', 
    'sociólogo': 'socióloga', 
    'soldado': 'soldado', 
    'solista': 'solista', 
    'surfista': 'surfista', 
    'talud': 'talud', 
    'tatuador': 'tatuadora', 
    'tarento': 'tarento', 
    'técnico en emergencias médicas': 'técnica en emergencias médicas', 
    'tejedor': 'tejedora', 
    'tendero': 'tendera', 
    'tenista': 'tenista', 
    'tenista en silla de ruedas': 'tenista en silla de ruedas', 
    'teólogo': 'teóloga', 
    'teórico racial': 'teórica racial', 
    'teclista': 'teclista', 
    'tipógrafo': 'tipógrafa', 
    'tirador': 'tiradora', 
    'titiritero': 'titiritera', 
    'torturador': 'torturadora', 
    'traductor': 'traductora', 
    'triatleta': 'triatleta', 
    'trompetista': 'trompetista', 
    'trompista': 'trompista', 
    'ultramaratonista': 'ultramaratonista', 
    'velocista': 'velocista', 
    'verdugo': 'verdugo', 
    'veterinario': 'veterinaria', 
    'videoartista': 'videoartista', 
    'videógrafo': 'videógrafa', 
    'violinista': 'violinista', 
    'violonchelista': 'violonchelista', 
    'viticultor': 'viticultora', 
    'vocalista': 'vocalista', 
    'volatinero': 'volatinero', 
    'voleibolista': 'voleibolista', 
    'windsurfista': 'windsurfista', 
    'yudoca': 'yudoca', 
    'youtuber': 'youtuber', 
    'zoólogo': 'zoóloga', 
}

def convertirfecha(fecha):
    num2month = {1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril', 5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto', 9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'}
    fecha = fecha.split('T')[0]
    fecha = '%s de %s de %s' % (int(fecha.split('-')[2]), num2month[int(fecha.split('-')[1])], int(fecha.split('-')[0]))
    return fecha

def getLabel(q='', lang='es'):
    label = ''
    url = 'https://www.wikidata.org/w/api.php?action=wbgetentities&ids='+q+'&props=labels&languages=es&format=json'
    raw = getURL(url=url)
    j = json.loads(raw)
    if 'entities' in j and \
       'es' in j['entities'][q]['labels']:
        label = j['entities'][q]['labels']['es']['value']
    return label

def getOccupationLabels():
    #load occupations Q
    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=SELECT%20%3Fitem%20%3FitemLabel%20%0AWHERE%20%7B%0A%20%20%3Fitem%20wdt%3AP31%20wd%3AQ28640.%0A%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22es%22%20%7D%0A%7D&format=json'
    sparql = getURL(url=url)
    #sparql = '%s ]\n  }\n}' % (', {\n      "item" : {'.join(sparql.split(', {\n      "item" : {')[:-1]))
    #print(sparql)
    try:
        json1 = json.loads(sparql)
    except:
        print('Error downloading SPARQL? Skiping\n')
        sys.exit()
    occupations = {}
    for result in json1['results']['bindings']:
        q = 'item' in result and result['item']['value'].split('/entity/')[1] or ''
        occupationlabel = 'itemLabel' in result and result['itemLabel']['value'] or ''
        if q and not re.search(r'(?im)^Q\d', occupationlabel):
            occupations[q] = occupationlabel
    return occupations

def getURL(url=''):
    raw = ''
    req = urllib.request.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
    try:
        raw = urllib.request.urlopen(req).read().strip().decode('utf-8')
    except:
        sleep = 10 # seconds
        maxsleep = 100
        while sleep <= maxsleep:
            print('Error while retrieving: %s' % (url))
            print('Retry in %s seconds...' % (sleep))
            time.sleep(sleep)
            try:
                raw = urllib.request.urlopen(req).read().strip().decode('utf-8')
            except:
                pass
            sleep = sleep * 2
    return raw

def group_unconcat(concat='', labelclass=''):
    unconcat = []
    if concat and labelclass:
        for qurl in concat.split('; '): # si hay traduccion al español guardamos, sino obviamos
            q = qurl.split('/entity/')[1]
            if q in labels[labelclass]:
                unconcat.append(labels[labelclass][q])
            else:
                print('No hay LABEL para', q, '. Intentando bajar el label')
                templabel = getLabel(q=q)
                if templabel:
                    labels[labelclass][q] = templabel
                    unconcat.append(labels[labelclass][q])
                    print('Encontrado label:', labels[labelclass][q])
                    print('Ahora hay %s labels de %s en memoria' % (len(labels[labelclass]), labelclass))
    unconcat = list(set(unconcat))
    unconcat.sort()
    return unconcat

def main():
    labels['occupations'] = getOccupationLabels()
    labels['occupations'] = labels['occupations'].copy()
    print('Loaded %s occupations' % (len(labels['occupations'].items())))
    site = pywikibot.Site('librefind', 'librefind')
    totalbios = 0
    skipuntilcountry = 'Estonia'
    skipuntilbio = ''
    skipbios = []
    for p27k, p27v in p27list:
        subtotalbios = 0
        print('\n','#'*50,'\n',p27k,p27v,'\n','#'*50)
        if skipuntilcountry:
            if skipuntilcountry == p27k:
                skipuntilcountry = ''
            else:
                print('Skiping until... %s' % (skipuntilcountry))
                continue
        
        yearranges = [[1, 1000], [1000, 1200], [1200, 1300], [1300, 1400], [1400, 1500], [1500, 1550], [1550, 1600]]
        for yearx in range(1600, 1700):
            if yearx % 20 == 0:
                yearranges.append([yearx, yearx+20])
        for yearx in range(1700, 1800):
            if yearx % 10 == 0:
                yearranges.append([yearx, yearx+10])
        for yearx in range(1800, 1900):
            if yearx % 5 == 0:
                yearranges.append([yearx, yearx+5])
        for yearx in range(1900, 1990):
            yearranges.append([yearx, yearx+1])
        
        for minyear, maxyear in yearranges:
            print('\nFrom %s to %s' % (minyear, maxyear))
            url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=SELECT%20DISTINCT%20%3Fitem%20%3FitemLabel%20%3FcountryLabel%20%3FsexLabel%0A%3FbirthplaceLabel%20%3Fbirthdate%20%3FdeathplaceLabel%20%3Fdeathdate%20%0A(GROUP_CONCAT(%3Feducated%3B%20separator%20%3D%20%22%3B%20%22)%20AS%20%3Feducatedat)%0A(GROUP_CONCAT(%3Fposition%3B%20separator%20%3D%20%22%3B%20%22)%20AS%20%3Fpositions)%0A(GROUP_CONCAT(%3Foccupation%3B%20separator%20%3D%20%22%3B%20%22)%20AS%20%3Foccupations)%0A(GROUP_CONCAT(%3Faward%3B%20separator%20%3D%20%22%3B%20%22)%20AS%20%3Fawards)%0A%3Fimage%20%3Fcommonscat%20%3Fwebsite%20%0AWHERE%20%7B%0A%20%20%3Fitem%20wdt%3AP31%20wd%3AQ5.%0A%20%20%3Fitem%20wdt%3AP27%20wd%3A'+p27v+'.%0A%20%20%3Fitem%20wdt%3AP27%20%3Fcountry.%0A%20%20%3Fitem%20wdt%3AP21%20%3Fsex.%0A%20%20%3Fitem%20wdt%3AP19%20%3Fbirthplace.%0A%20%20%3Fitem%20wdt%3AP569%20%3Fbirthdate.%0A%20%20FILTER%20(year(%3Fbirthdate)%20%3E%3D%20'+str(minyear)+')%20.%0A%20%20FILTER%20(year(%3Fbirthdate)%20%3C%20'+str(maxyear)+')%20.%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP20%20%3Fdeathplace.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP570%20%3Fdeathdate.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP69%20%3Feducated.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP39%20%3Fposition.%20%7D%0A%20%20%3Fitem%20wdt%3AP106%20%3Foccupation.%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP166%20%3Faward.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP18%20%3Fimage.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP373%20%3Fcommonscat.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP856%20%3Fwebsite.%20%7D%0A%20%20FILTER%20NOT%20EXISTS%20%7B%20%3Fwfr%20schema%3Aabout%20%3Fitem%20.%20%3Fwfr%20schema%3AinLanguage%20%22es%22%20%7D%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22es%2Cen%2Cca%2Cpt%2Cit%2Cfr%2Cde%2Ccz%2Chu%22%20%7D%0A%7D%0AGROUP%20BY%20%3Fitem%20%3FitemLabel%20%3FcountryLabel%20%3FsexLabel%0A%3FbirthplaceLabel%20%3Fbirthdate%20%3FdeathplaceLabel%20%3Fdeathdate%20%0A%3Fimage%20%3Fcommonscat%20%3Fwebsite%20'
            
            """
SELECT DISTINCT ?item ?itemLabel ?countryLabel ?sexLabel
?birthplaceLabel ?birthdate ?deathplaceLabel ?deathdate 
(GROUP_CONCAT(?educated; separator = "; ") AS ?educatedat)
(GROUP_CONCAT(?position; separator = "; ") AS ?positions)
(GROUP_CONCAT(?occupation; separator = "; ") AS ?occupations)
(GROUP_CONCAT(?award; separator = "; ") AS ?awards)
?image ?commonscat ?website 
WHERE {
  ?item wdt:P31 wd:Q5.
  ?item wdt:P27 wd:Q183.
  ?item wdt:P27 ?country.
  ?item wdt:P21 ?sex.
  ?item wdt:P19 ?birthplace.
  ?item wdt:P569 ?birthdate.
  FILTER (year(?birthdate) >= 1877) .
  FILTER (year(?birthdate) < 1878) .
  OPTIONAL { ?item wdt:P20 ?deathplace. }
  OPTIONAL { ?item wdt:P570 ?deathdate. }
  OPTIONAL { ?item wdt:P69 ?educated. }
  OPTIONAL { ?item wdt:P39 ?position. }
  ?item wdt:P106 ?occupation.
  OPTIONAL { ?item wdt:P166 ?award. }
  OPTIONAL { ?item wdt:P18 ?image. }
  OPTIONAL { ?item wdt:P373 ?commonscat. }
  OPTIONAL { ?item wdt:P856 ?website. }
  FILTER NOT EXISTS { ?wfr schema:about ?item . ?wfr schema:inLanguage "es" }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "es,en,ca,pt,it,fr,de,cz,hu" }
}
GROUP BY ?item ?itemLabel ?countryLabel ?sexLabel
?birthplaceLabel ?birthdate ?deathplaceLabel ?deathdate 
?image ?commonscat ?website 
            """
            #print(url)
            url = '%s&format=json' % (url)
            time.sleep(1)
            sparql = getURL(url=url)
            #print(sparql)
            
            if sparql:
                #sparql = '%s ]\n  }\n}' % (', {\n      "item" : {'.join(sparql.split(', {\n      "item" : {')[:-1]))
                try:
                    json1 = json.loads(sparql)
                except:
                    print('Error downloading SPARQL? Malformatted JSON? Skiping\n')
                    continue
            else:
                print('Server return empty file')
                continue
            
            bios = {}
            for result in json1['results']['bindings']:
                q = 'item' in result and result['item']['value'].split('/entity/')[1] or ''
                
                if skipuntilbio:
                    if skipuntilbio == q:
                        skipuntilbio = ''
                    else:
                        print('Skiping until... %s' % (skipuntilbio))
                        continue
                
                #algunas veces puede devolver basura? en algun value (del tipo: t329308714), descartar esas bios
                for propname in result.keys():
                    if re.search(r'(?m)^t\d+$', result[propname]['value']) or \
                       (propname == 'educatedat' and re.search(r't\d+', result[propname]['value'])) or \
                       (propname == 'positions' and re.search(r't\d+', result[propname]['value'])) or \
                       (propname == 'occupations' and re.search(r't\d+', result[propname]['value'])) or \
                       (propname == 'awards' and re.search(r't\d+', result[propname]['value'])):
                        print('ERROR: la propiedad %s contiene %s. Saltando...' % (propname, result[propname]['value']))
                        skipbios.append(q)
                if q in skipbios:
                    continue
                
                nombre = 'itemLabel' in result and result['itemLabel']['value'] or ''
                country = 'countryLabel' in result and result['countryLabel']['value'] or ''
                sexo = 'sexLabel' in result and result['sexLabel']['value'] or ''
                if sexo:
                    if sexo == 'femenino' or sexo.startswith('mujer'): #mujer transgenero Q1052281
                        sexo = 'femenino'
                    else:
                        sexo = 'masculino'
                lnac = 'birthplaceLabel' in result and result['birthplaceLabel']['value'] or ''
                fnac = 'birthdate' in result and result['birthdate']['value'].split('T')[0] or ''
                lfal = 'deathplaceLabel' in result and result['deathplaceLabel']['value'] or ''
                ffal = 'deathdate' in result and result['deathdate']['value'].split('T')[0] or ''
                
                educatedat = group_unconcat('educatedat' in result and result['educatedat']['value'] or '', 'educatedat')
                positions = group_unconcat('positions' in result and result['positions']['value'] or '', 'positions')
                occupations = group_unconcat('occupations' in result and result['occupations']['value'] or '', 'occupations')
                awards = group_unconcat('awards' in result and result['awards']['value'] or '', 'awards')
                
                image = 'image' in result and urllib.parse.unquote(result['image']['value']).split('/Special:FilePath/')[1] or ''
                commonscat = 'commonscat' in result and result['commonscat']['value'] or ''
                if commonscat:
                    commonscat = 'Category:%s' % (commonscat)
                website = 'website' in result and result['website']['value'] or ''
                
                if q in bios:
                    for x, y in [[country, 'countries'], [sexo, 'sexo'], [lnac, 'lnac'], [fnac, 'fnac'], [lfal, 'lfal'], [ffal, 'ffal'], [image, 'images'], [commonscat, 'commonscat'], [website, 'websites']]: #parametros sencillos
                        if x and x not in bios[q][y]:
                            bios[q][y].append(x)
                            bios[q][y].sort()
                    for x, y in [[educatedat, 'educatedat'], [positions, 'positions'], [occupations, 'occupations'], [awards, 'awards']]: #parametros group_concat
                        for xx in x:
                            if xx and xx not in bios[q][y]:
                                bios[q][y].append(xx)
                                bios[q][y].sort()
                else:
                    bios[q] = {
                        'q': q, 'nombre': nombre, 'countries': [country], 'sexo': [sexo], 'lnac': [lnac], 'fnac': [fnac], 'lfal': [lfal], 'ffal': [ffal], 'educatedat': educatedat, 'positions': positions, 'occupations': occupations, 'awards': awards, 'images': [image], 'commonscat': [commonscat], 'websites': [website], 
                    }
            
            bios_list = [[props['nombre'], q, props] for q, props in bios.items()]
            bios_list.sort()
            print('Encontradas %s bios\n' % (len(bios_list)))
            totalbios += len(bios_list)
            subtotalbios += len(bios_list)
            #continue
            
            for nombre, q, props in bios_list:
                print('\n', '#'*10, props['nombre'], q, '#'*10, '\n')

                if re.search(r'(?im)^Q\d', nombre):
                    print('Error, nombre indefinido, saltamos')
                    continue
                if len(props['sexo']) > 1:
                    print('Mas de un sexo, saltamos')
                    continue
                
                educatedat = props['educatedat']
                if '' in educatedat:
                    educatedat.remove('')
                positions = props['positions']
                if '' in positions:
                    positions.remove('')
                occupations = props['occupations']
                if '' in occupations:
                    occupations.remove('')
                awards = props['awards']
                if '' in awards:
                    awards.remove('')
                
                if not props['occupations']:
                    print('Error, sin ocupacion, saltamos')
                    continue
                if len(props['countries']) > 1:
                    print('Mas de una nacionalidad, saltamos')
                    continue
                if len(props['fnac']) > 1:
                    print('Mas de una fecha de nacimiento, saltamos')
                    continue
                if len(props['ffal']) > 1:
                    print('Mas de una fecha de fallecimiento, saltamos')
                    continue
                #quizas mas adelante interese meter los 2 o los niveles q haya en wikidata?
                if len(props['lnac']) > 1:
                    print('Mas de un lugar de nacimiento, saltamos')
                    continue
                if len(props['lfal']) > 1:
                    print('Mas de un lugar de fallecimiento, saltamos')
                    continue
                #fin quizas
                images = props['images']
                if '' in images:
                    images.remove('')
                commonscat = props['commonscat']
                if '' in commonscat:
                    commonscat.remove('')
                if not images and not props['commonscat']:
                    print('No hay imagen, saltamos')
                    continue
                websites = props['websites']
                if '' in websites:
                    websites.remove('')
                if not websites:
                    pass
                    #print('No hay website, saltamos')
                    #continue
                
                #remove unuseful occupations
                occupations2 = []
                for occupation in occupations:
                    # excluir las de tipo "compositor"->"compositor de canciones" y "humorista"->"humorista gráfico"
                    if not '%s ' % (occupation) in ', '.join(occupations):
                        occupations2.append(occupation)
                occupations = occupations2.copy()
                occupations.sort()
                
                skipbio = False
                if 'sexo' in props and props['sexo'][0] == 'femenino':
                    missingfemaleocups = []
                    for occupation in occupations:
                        if occupation not in ocupfem:
                            missingfemaleocups.append(occupation)
                            skipbio = True #skip this bio, we have not female translation for this ocupation
                    if skipbio:
                        print('Falta traduccion femenina para:', ', '.join(missingfemaleocups))
                        with open('missing-female-ocups.txt', 'a') as logfile:
                            logfile.write('%s\n' % ('\n'.join(missingfemaleocups)))
                        continue
                    occupations = [ocupfem[x] for x in occupations]
                
                skipbio = False
                for x in props['countries']:
                    if not x in country2nationality:
                        print('ERROR: Falta nacionalidad para %s. Saltamos...' % (x))
                        skipbio = True
                if skipbio:
                    continue
                
                properties_list = [
                    ['Clase', 'persona'], 
                    ['Nombre', props['nombre']], 
                    ['Sexo', ', '.join(props['sexo'])], 
                    ['Fecha de nacimiento', ', '.join(props['fnac'])], 
                    ['Lugar de nacimiento', ', '.join(props['lnac'])], 
                    ['Fecha de fallecimiento', ', '.join(props['ffal'])], 
                    ['Lugar de fallecimiento', ', '.join(props['lfal'])], 
                    ['Nacionalidad', ', '.join([country2nationality[x][props['sexo'][0]] for x in props['countries']])], 
                    ['Estudiado en', ', '.join(educatedat)], 
                    ['Cargo', ', '.join(positions)], 
                    ['Ocupación', ', '.join(occupations)], 
                    ['Premio', ', '.join(awards)], 
                ]
                
                gallery = ''.join(["{{Gallery file\n|filename=%s\n}}" % (x) for x in images])
                websites = ''.join(["{{Website\n|title=Web oficial\n|url=%s\n|level=0\n}}" % (x) for x in websites])
                properties = ''
                for pname, pvalue in properties_list:
                    if pvalue:
                        properties += "{{Property\n|property=%s\n|value=%s\n}}" % (pname, pvalue)

                output = """{{Infobox Result2
|search=%s%s
|wikidata=%s%s%s%s
}}""" % (props['nombre'], props['commonscat'] and '\n|commons=%s' % (props['commonscat'][0]) or '', props['q'], websites and '\n|websites=%s' % (websites) or '', gallery and '\n|gallery=%s' % (gallery) or '', properties and '\n|properties=%s' % (properties) or '')
                
                pagename = ''
                try:
                    #time.sleep(1)
                    # Find page in LibreFind, and move if duplicate name
                    apiquery = 'https://www.librefind.org/w/index.php?title=Especial:Ask&q=[[wikidata%3A%3A'+props['q']+']]&p=format%3Djson'
                    result = getURL(url=apiquery)
                    if result:
                        try:
                            apijson = json.loads(result)
                        except:
                            print('Error API? Malformatted JSON? Skiping\n')
                            continue
                        #print(apijson)
                        if len(apijson['results'].keys()) == 1:
                            pagename = list(apijson['results'].keys())[0]
                            #print(pagename)
                        elif len(apijson['results'].keys()) > 1:
                            #pagina duplicada? loguear y gestionar mas adelante
                            with open('duplicate-q.txt', 'a') as duplicatelog:
                                duplicatelog.write('%s\n' % (props['q']))
                            continue #evitar hasta revisar el log y q este arreglado
                        else:
                            pagename = props['nombre']
                    else: #no existe pagina para este Q todavia, segun la API
                        #comprobar que el nombre no este ocupado por otra pagina
                        #en ese caso, mover para desambiguar
                        pagename = props['nombre']
                        page = pywikibot.Page(site, pagename)
                        if page.exists():
                            if re.search(r'(?im)\{\{\s*(dis|des)', page.text): #desambiguacion? dejamos como esta y generamos nombre con Q
                                pagename = '%s (%s)' % (props['nombre'], props['q'])
                            else: #no es desambiguacion, movemos a su Q y creamos desambiguacion
                                qamover = re.findall('(?im)wikidata\s*=\s*(Q\d+)', page.text)
                                if qamover:
                                    qamover = qamover[0]
                                else: #no tiene parametro wikidata? q tipo de pagina es? loguear y saltar
                                    with open('log-sin-q.txt', 'a') as logsinq:
                                        logsinq.write('%s\n' % (page.title()))
                                    continue
                                page.move('%s (%s)' % (page.title(), qamover), reason='BOT - Moviendo para desambiguar en [[%s]]' % (page.title()))
                                disambig = pywikibot.Page(site, props['nombre'])
                                disambig.text = '{{disambiguation}}'
                                disambig.save('BOT - Creando desambiguación')
                                pagename = '%s (%s)' % (props['nombre'], props['q'])
                                
                    #guardar la bio
                    page = pywikibot.Page(site, pagename)
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
