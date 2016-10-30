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

from librefindglobals import *

""" TODO
* Que cuando un elemento en wikidata cambie de alias (por ej. si alguien corrige el nombre o lo traduce), el bot renombre la pagina de librefind. Hay algunos "X of Y" de nombres aristocraticos y reyes sin traducir todavia por ejemplo.

Nuevas propiedades:
* youtube accounts, place of burial, https://www.wikidata.org/wiki/Q2831
* mass (pound) https://www.wikidata.org/wiki/Q20821793
* Height, mass (kg), participant of https://www.wikidata.org/wiki/Q1950
* En cuanto a familia la estructura de frase podría ser: Es/Fue hijo/a de X e Y. Se casó/Contrajo matrimonio con Z. Fue padre/madre de H hijos O Su hijo/a es/fue H. ¿O mejor lo mostramos solo en la infobox/un arbol genealogico? Y como almacenar los nombres? Con el QID o el nombre en plano? Lo segundo tiene el problema de que puede haber colisiones, lo primero que la pagina no la hayamos creado en librefind y no podamos recuperar el label...
* P1038 otros parientes https://www.wikidata.org/wiki/Q335022
* P737 influido por https://www.wikidata.org/wiki/Q335022
* P1066 fue alumno de https://www.wikidata.org/wiki/Q335022 / P802 Estudiante (estudiantes de una persona)
* Estudiante de https://www.wikidata.org/wiki/Property:P1066
* P135 movimiento https://www.wikidata.org/wiki/Q859
* P109 firma
* dbpedia

* Poner miniatura en la infobox de las personas si existen en librefind, ej: Elek Erkel tiene padre y 3 hermanos notables con imagen
* Páginas para días desde el año 1000 al 2016? Solo para las q tengan algun evento (nacimiento, fallecimiento, etc)
* Integrar comentarios (talkpage) en la parte baja de la pagina de resultados?
* Cada bio podria tener un mapa con las localizaciones importantes para la persona (lugar de nacimiento, fallecimiento y quizas otras cosas). Haria falta tener las coordenadas en un articulo para cada localizacion. Serían muchas páginass quizas...
"""

labels = { 'educatedat': {}, 'positions': {}, 'occupations': {}, 'awards': {}, }

def convertirfecha(fecha):
    num2month = {1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril', 5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto', 9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'}
    fecha = fecha.split('T')[0]
    fecha = '%s de %s de %s' % (int(fecha.split('-')[2]), num2month[int(fecha.split('-')[1])], int(fecha.split('-')[0]))
    return fecha

def getLabel(q='', lang='es'):
    time.sleep(0.2)
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

def group_unconcat(concat='', labelclass=''):
    global labels
    
    unconcat = []
    if concat and labelclass:
        for qurl in concat.split('; '): # si hay traduccion al español guardamos, sino obviamos
            q = qurl.split('/entity/')[1]
            if q in labels[labelclass]:
                if labels[labelclass][q]: # evitar si es vacia, las almacenamos vacias para no hacer getLabel cada vez
                    unconcat.append(labels[labelclass][q])
            else:
                print('No hay LABEL para', q, '. Intentando bajar el label')
                templabel = getLabel(q=q)
                labels[labelclass][q] = templabel # aunque sea vacia la almacenamos, para evitar hacer getLabel otra vez
                print('Encontrado label:', labels[labelclass][q])
                print('Ahora hay %s labels de %s en memoria' % (len(labels[labelclass]), labelclass))
                if labels[labelclass][q]:
                    unconcat.append(labels[labelclass][q])
    unconcat = list(set(unconcat))
    unconcat.sort()
    return unconcat

def main():
    global labels
    global paises2qid_list
    global nacionalidades
    global ocupaciones
    
    labels['occupations'] = getOccupationLabels()
    labels['occupations'] = labels['occupations'].copy()
    print('Loaded %s occupations' % (len(labels['occupations'].items())))
    site = pywikibot.Site('librefind', 'librefind')
    totalbios = 0
    skipuntilcountry = ''
    skipuntilbio = ''
    skipbios = []
    for pk, pv in paises2qid_list:
        subtotalbios = 0
        print('\n','#'*50,'\n',pk,pv,'\n','#'*50)
        if skipuntilcountry:
            if skipuntilcountry == pk:
                skipuntilcountry = ''
            else:
                print('Skiping until... %s' % (skipuntilcountry))
                continue
        
        yearranges = [[1, 1000], [1000, 1200], [1200, 1300], [1300, 1400], [1400, 1500], [1500, 1550], [1550, 1600]]
        for yearstart, yearend, yearstep in [[1600, 1700, 10], [1700, 1800, 5], [1800, 1900, 2], [1900, 1990, 1]]:
            for yearx in range(yearstart, yearend):
                if yearx % yearstep == 0:
                    yearranges.append([yearx, yearx+yearstep])
        
        for minyear, maxyear in yearranges:
            print('\nFrom %s to %s' % (minyear, maxyear))
            url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=SELECT%20DISTINCT%20%3Fitem%20%3FitemLabel%20%3FcountryLabel%20%3FsexLabel%0A%3FbirthplaceLabel%20%3Fbirthdate%20%3FdeathplaceLabel%20%3Fdeathdate%20%0A(GROUP_CONCAT(DISTINCT%20%3Feducated%3B%20separator%20%3D%20%22%3B%20%22)%20AS%20%3Feducatedat)%0A(GROUP_CONCAT(DISTINCT%20%3Fposition%3B%20separator%20%3D%20%22%3B%20%22)%20AS%20%3Fpositions)%0A(GROUP_CONCAT(DISTINCT%20%3Foccupation%3B%20separator%20%3D%20%22%3B%20%22)%20AS%20%3Foccupations)%0A(GROUP_CONCAT(DISTINCT%20%3Faward%3B%20separator%20%3D%20%22%3B%20%22)%20AS%20%3Fawards)%0A%3FworksLabel%20%3Fimage%20%3Fcommonscat%20%3Fwebsite%20%3Ffacebook%20%3Fgoogleplus%20%3Finstagram%20%3Ftwitter%0A%3FfatherLabel%20%3FmotherLabel%20%3FbrotherLabel%20%3FsisterLabel%20%3FspouseLabel%20%3FchildLabel%0AWHERE%20%7B%0A%20%20%3Fitem%20wdt%3AP31%20wd%3AQ5.%0A%20%20%3Fitem%20wdt%3AP27%20wd%3A'+pv+'.%0A%20%20%3Fitem%20wdt%3AP27%20%3Fcountry.%0A%20%20%3Fitem%20wdt%3AP21%20%3Fsex.%0A%20%20%3Fitem%20wdt%3AP19%20%3Fbirthplace.%0A%20%20%3Fitem%20wdt%3AP569%20%3Fbirthdate.%0A%20%20FILTER%20(year(%3Fbirthdate)%20%3E%3D%20'+str(minyear)+')%20.%0A%20%20FILTER%20(year(%3Fbirthdate)%20%3C%20'+str(maxyear)+')%20.%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP20%20%3Fdeathplace.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP570%20%3Fdeathdate.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP69%20%3Feducated.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP39%20%3Fposition.%20%7D%0A%20%20%3Fitem%20wdt%3AP106%20%3Foccupation.%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP166%20%3Faward.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP800%20%3Fworks.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP18%20%3Fimage.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP373%20%3Fcommonscat.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP856%20%3Fwebsite.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP2013%20%3Ffacebook.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP2847%20%3Fgoogleplus.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP2003%20%3Finstagram.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP2002%20%3Ftwitter.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP22%20%3Ffather.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP25%20%3Fmother.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP7%20%3Fbrother.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP9%20%3Fsister.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP26%20%3Fspouse.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP40%20%3Fchild.%20%7D%0A%20%20FILTER%20NOT%20EXISTS%20%7B%20%3Fwfr%20schema%3Aabout%20%3Fitem%20.%20%3Fwfr%20schema%3AinLanguage%20%22es%22%20%7D%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22es%2Cen%2Cca%2Cgl%2Cpt%2Cit%2Cfr%2Cde%2Ceu%2Ccz%2Chu%2Cnl%2Csv%2Cno%2Cfi%2Cro%2Ceo%2Cda%2Csk%2Ctr%22%20%7D%0A%7D%0AGROUP%20BY%20%3Fitem%20%3FitemLabel%20%3FcountryLabel%20%3FsexLabel%0A%3FbirthplaceLabel%20%3Fbirthdate%20%3FdeathplaceLabel%20%3Fdeathdate%20%0A%3FworksLabel%20%3Fimage%20%3Fcommonscat%20%3Fwebsite%20%3Ffacebook%20%3Fgoogleplus%20%3Finstagram%20%3Ftwitter%20%0A%3FfatherLabel%20%3FmotherLabel%20%3FbrotherLabel%20%3FsisterLabel%20%3FspouseLabel%20%3FchildLabel'
            """
SELECT DISTINCT ?item ?itemLabel ?countryLabel ?sexLabel
?birthplaceLabel ?birthdate ?deathplaceLabel ?deathdate 
(GROUP_CONCAT(DISTINCT ?educated; separator = "; ") AS ?educatedat)
(GROUP_CONCAT(DISTINCT ?position; separator = "; ") AS ?positions)
(GROUP_CONCAT(DISTINCT ?occupation; separator = "; ") AS ?occupations)
(GROUP_CONCAT(DISTINCT ?award; separator = "; ") AS ?awards)
?worksLabel ?image ?commonscat ?website ?facebook ?googleplus ?instagram ?twitter
?fatherLabel ?motherLabel ?brotherLabel ?sisterLabel ?spouseLabel ?childLabel
WHERE {
  ?item wdt:P31 wd:Q5.
  ?item wdt:P27 wd:Q183.
  ?item wdt:P27 ?country.
  ?item wdt:P21 ?sex.
  ?item wdt:P19 ?birthplace.
  ?item wdt:P569 ?birthdate.
  FILTER (year(?birthdate) >= 1980) .
  FILTER (year(?birthdate) < 1981) .
  OPTIONAL { ?item wdt:P20 ?deathplace. }
  OPTIONAL { ?item wdt:P570 ?deathdate. }
  OPTIONAL { ?item wdt:P69 ?educated. }
  OPTIONAL { ?item wdt:P39 ?position. }
  ?item wdt:P106 ?occupation.
  OPTIONAL { ?item wdt:P166 ?award. }
  OPTIONAL { ?item wdt:P800 ?works. }
  OPTIONAL { ?item wdt:P18 ?image. }
  OPTIONAL { ?item wdt:P373 ?commonscat. }
  OPTIONAL { ?item wdt:P856 ?website. }
  OPTIONAL { ?item wdt:P2013 ?facebook. }
  OPTIONAL { ?item wdt:P2847 ?googleplus. }
  OPTIONAL { ?item wdt:P2003 ?instagram. }
  OPTIONAL { ?item wdt:P2002 ?twitter. }
  OPTIONAL { ?item wdt:P22 ?father. }
  OPTIONAL { ?item wdt:P25 ?mother. }
  OPTIONAL { ?item wdt:P7 ?brother. }
  OPTIONAL { ?item wdt:P9 ?sister. }
  OPTIONAL { ?item wdt:P26 ?spouse. }
  OPTIONAL { ?item wdt:P40 ?child. }
  FILTER NOT EXISTS { ?wfr schema:about ?item . ?wfr schema:inLanguage "es" }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "es,en,ca,gl,pt,it,fr,de,eu,cz,hu,nl,sv,no,fi,ro,eo,da,sk,tr" }
}
GROUP BY ?item ?itemLabel ?countryLabel ?sexLabel
?birthplaceLabel ?birthdate ?deathplaceLabel ?deathdate 
?worksLabel ?image ?commonscat ?website ?facebook ?googleplus ?instagram ?twitter 
?fatherLabel ?motherLabel ?brotherLabel ?sisterLabel ?spouseLabel ?childLabel
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
            
            # captura de datos de biografias
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
                    if re.search(r't\d+', result[propname]['value']):
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
                
                works = 'worksLabel' in result and result['worksLabel']['value'] or ''
                image = 'image' in result and urllib.parse.unquote(result['image']['value']).split('/Special:FilePath/')[1] or ''
                commonscat = 'commonscat' in result and result['commonscat']['value'] or ''
                if commonscat:
                    commonscat = 'Category:%s' % (commonscat)
                website = 'website' in result and result['website']['value'] or ''
                
                # no usamos concat en familiares pq son pocos los elementos que lo tienen y no merece la pena el esfuerzo de pedir los labels a la API uno a uno (que raramente se reutilizaran en otros elementos, al contrario que con las ocupaciones, etc)
                father = 'fatherLabel' in result and result['fatherLabel']['value'] or ''
                mother = 'motherLabel' in result and result['motherLabel']['value'] or ''
                brother = 'brotherLabel' in result and result['brotherLabel']['value'] or ''
                sister = 'sisterLabel' in result and result['sisterLabel']['value'] or ''
                child = 'childLabel' in result and result['childLabel']['value'] or ''
                
                if q in bios:
                    for x, y in [[country, 'countries'], [sexo, 'sexo'], [lnac, 'lnac'], [fnac, 'fnac'], [lfal, 'lfal'], [ffal, 'ffal'], [works, 'works'], [image, 'images'], [commonscat, 'commonscat'], [website, 'websites'], [father, 'father'], [mother, 'mother'], [brother, 'brother'], [sister, 'sister'], [child, 'child']]: #parametros sencillos
                        if x and not re.search(r'Q\d+', x) and x not in bios[q][y]:
                            bios[q][y].append(x)
                            bios[q][y].sort()
                    for x, y in [[educatedat, 'educatedat'], [positions, 'positions'], [occupations, 'occupations'], [awards, 'awards']]: #parametros group_concat
                        for xx in x:
                            if xx and not re.search(r'Q\d+', xx) and xx not in bios[q][y]:
                                bios[q][y].append(xx)
                                bios[q][y].sort()
                else:
                    bios[q] = {
                        'q': q, 'nombre': nombre, 'countries': [country], 'sexo': [sexo], 'lnac': [lnac], 'fnac': [fnac], 'lfal': [lfal], 'ffal': [ffal], 'educatedat': educatedat, 'positions': positions, 'occupations': occupations, 'awards': awards, 'works': [works], 'images': [image], 'commonscat': [commonscat], 'websites': [website], 'father': [father], 'mother': [mother], 'brother': [brother], 'sister': [sister], 'child': [child], 
                    }
            #fin captura de datos
            
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
                
                countries = props['countries']
                if '' in countries:
                    countries.remove('')
                if 'Rusia' in countries and 'Unión Soviética' in countries: #redundant
                    countries.remove('Unión Soviética')
                if 'Rusia' in countries and 'Imperio ruso' in countries: #redundant
                    countries.remove('Imperio ruso')
                
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
                works = props['works']
                if '' in works:
                    works.remove('')
                
                if not occupations:
                    print('Error, sin ocupacion, saltamos')
                    continue
                if len(countries) > 1:
                    pass
                    #print('Mas de una nacionalidad, saltamos')
                    #continue
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
                
                #resolucion de fechas
                if props['fnac'][0].endswith('-01-01') and props['ffal'][0].endswith('-01-01'): # si nace y muere en 1 enero
                    props['fnac'][0] = props['fnac'][0].split('-')[0]
                    props['ffal'][0] = props['ffal'][0].split('-')[0]
                elif props['fnac'] and props['fnac'][0] and int(props['fnac'][0].split('-')[0]) < 1900 and props['fnac'][0].endswith('-01-01'):
                    props['fnac'][0] = props['fnac'][0].split('-')[0]
                elif props['ffal'] and props['ffal'][0] and int(props['ffal'][0].split('-')[0]) < 1900 and props['ffal'][0].endswith('-01-01'):
                    props['ffal'][0] = props['ffal'][0].split('-')[0]
                #fin resolucion fechas
                
                images = props['images']
                if '' in images:
                    images.remove('')
                commonscat = props['commonscat']
                if '' in commonscat:
                    commonscat.remove('')
                if not images and not props['commonscat']:
                    print('No hay imagen, saltamos')
                    continue
                    #pass
                websites = props['websites']
                if '' in websites:
                    websites.remove('')
                if not websites:
                    pass
                    #print('No hay website, saltamos')
                    #continue
                
                #relatives
                father = props['father']
                if '' in father:
                    father.remove('')
                if len(father) > 1:
                    print('Mas de un padre, saltamos')
                    continue
                mother = props['mother']
                if '' in mother:
                    mother.remove('')
                if len(mother) > 1:
                    print('Mas de una madre, saltamos')
                    continue
                brother = props['brother']
                if '' in brother:
                    brother.remove('')
                sister = props['sister']
                if '' in sister:
                    sister.remove('')
                child = props['child']
                if '' in child:
                    child.remove('')
                #end relatives
                
                #start occupations
                #remove unuseful occupations
                occupations2 = []
                for occupation in occupations:
                    # excluir las de tipo "compositor"->"compositor de canciones" y "humorista"->"humorista gráfico"
                    if not '%s ' % (occupation) in ', '.join(occupations):
                        occupations2.append(occupation)
                occupations = occupations2.copy()
                occupations.sort()
                
                # femenine translation
                skipbio = False
                if 'sexo' in props and props['sexo'][0] == 'femenino':
                    for occupation in occupations:
                        if occupation not in ocupaciones:
                            skipbio = True #skip this bio, we have not female translation for this ocupation
                            print('Falta traduccion femenina para:', occupation)
                            with open('missing-female-ocups.txt', 'a') as logfile:
                                logfile.write('%s\n' % (occupation))
                    if skipbio:
                        continue
                    occupations = [ocupaciones[x]['fs'] for x in occupations]
                #end occupations
                
                skipbio = False
                for country in countries:
                    if not country in nacionalidades:
                        skipbio = True
                        print('Falta nacionalidad para:', country)
                        with open('missing-nationalities.txt', 'a') as logfile:
                            logfile.write('%s\n' % (country))
                if skipbio:
                    continue
                
                sexo = '%ss' % (props['sexo'][0][0]) # ms or fs, masculino singular, femenino singular
                properties_list = [
                    ['Clase', 'persona'], 
                    ['Nombre', props['nombre']], 
                    ['Sexo', '; '.join(props['sexo'])], 
                    ['Imagen', images and 'File:%s' % (images[0]) or ''], #only 1 image
                    ['Fecha de nacimiento', '; '.join(props['fnac'])], 
                    ['Lugar de nacimiento', '; '.join(props['lnac'])], 
                    ['Fecha de fallecimiento', '; '.join(props['ffal'])], 
                    ['Lugar de fallecimiento', '; '.join(props['lfal'])], 
                    ['Nacionalidad', '; '.join([nacionalidades[x][sexo] for x in countries])], 
                    ['Estudiado en', '; '.join(educatedat)], 
                    ['Cargo', '; '.join(positions)], 
                    ['Ocupación', '; '.join(occupations)], 
                    ['Premio', '; '.join(awards)], 
                    ['Obra destacada', '; '.join(works)], 
                    ['Padre', '; '.join(father)], 
                    ['Madre', '; '.join(mother)], 
                    ['Hermano', '; '.join(brother)], 
                    ['Hermana', '; '.join(sister)], 
                    ['Descendiente', '; '.join(child)], 
                ]
                
                gallery = ''.join(["{{Gallery file\n|filename=%s\n}}" % (x) for x in images])
                websites = ''.join(["{{Website\n|title=Web oficial\n|url=%s\n|level=0\n}}" % (x) for x in websites])
                properties = ''
                for pname, pvalue in properties_list:
                    if pvalue:
                        properties += "{{Property\n|property=%s\n|value=%s\n}}" % (pname, pvalue)

                output = """{{Búsqueda Persona
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
