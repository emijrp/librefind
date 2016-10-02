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
        'Arabia Saudita': 'Q851',
        'Argelia': 'Q262',
        'Argentina': 'Q414',
        'Armenia': 'Q399',
        'Australia': 'Q408',
        'Austria': 'Q40',
        'Azerbaiyán': 'Q227',
        
        'España': 'Q29',
        
        'Francia': 'Q142',
        
        'Italia': 'Q38',
        
        'Noruega': 'Q20',
        
        'Portugal': 'Q45',
        
        'Rusia': 'Q159',
    }
    p27list = [[k, v] for k, v in p27.items()]
    p27list.sort()
    country2nationality = {
        'Afganistán': {'masculino': 'afgano', 'femenino': 'afgana' }, 
        'Albania': {'masculino': 'albanés', 'femenino': 'albanesa' }, 
        'Alemania': {'masculino': 'alemán', 'femenino': 'alemana' }, 
        'Andorra': {'masculino': 'andorrano', 'femenino': 'andorrana' }, 
        'Angola': {'masculino': 'angoleño', 'femenino': 'angoleña' }, 
        'Arabia Saudita': {'saudí': 'alemán', 'femenino': 'saudí' }, 
        'Argelia': {'masculino': 'argelino', 'femenino': 'argelina' }, 
        'Argentina': {'masculino': 'argentino', 'femenino': 'argentina' }, 
        'Armenia': {'masculino': 'armenio', 'femenino': 'armenia' }, 
        'Australia': {'masculino': 'australiano', 'femenino': 'australiana' }, 
        'Austria': {'masculino': 'austríaco', 'femenino': 'austríaca' }, 
        'Azerbaiyán': {'masculino': 'azerbaiyano', 'femenino': 'azerbaiyana' }, 
        
        'España': {'masculino': 'español', 'femenino': 'española' }, 
        
        'Francia': {'masculino': 'francés', 'femenino': 'francesa' }, 
        
        'Italia': {'masculino': 'italiano', 'femenino': 'italiana' }, 
        
        'Noruega': {'masculino': 'noruego', 'femenino': 'noruega' }, 
        
        'Portugal': {'masculino': 'portugués', 'femenino': 'portuguesa' }, 
        
        'Rusia': {'masculino': 'ruso', 'femenino': 'rusa' }, 
    }
    ocupfem = {
        '': '', 
        'abogado': 'abogada', 
        '': '', 
        'activista': 'activista', 
        '': '', 
        'actor': 'actriz', 
        '': '', 
        '': '', 
        'actor de teatro': 'actriz de teatro', 
        'actor de teatro musical': 'actriz de teatro musical', 
        'actor de televisión': 'actriz de televisión', 
        '': '', 
        'actor de voz': 'actriz de voz', 
        '': '', 
        'actor pornográfico': 'actriz pornográfica',
        '': '', 
        'agricultor': 'agricultora', 
        '': '', 
        'algorista': 'algorista', 
        '': '', 
        'arreglista': 'arreglista', 
        'artista': 'artista', 
        'artista digital': 'artista digital', 
        '': '', 
        'asistente social': 'asistenta social', 
        '': '', 
        'atleta': 'atleta', 
        '': '', 
        'autor': 'autora', 
        '': '', 
        'badmintonista': 'badmintonista', 
        '': '', 
        'bailarín': 'bailarina', 
        'bailarín de ballet': 'bailarina de ballet', 
        '': '', 
        'baterista': 'baterista', 
        '': '', 
        'bhikkhuni': 'bhikkhuni', 
        '': '', 
        'biógrafo': 'biógrafa', 
        '': '', 
        'cabaretista': 'cabaretista', 
        '': '', 
        'cantante': 'cantante', 
        'cantante de ópera': 'cantante de ópera', 
        '': '', 
        'cantautor': 'cantautora', 
        '': '', 
        'cartelista': 'cartelista', 
        '': '', 
        'catedrático': 'catedrática', 
        '': '', 
        'científico de la literatura': 'científica de la literatura', 
        '': '', 
        'ciclista': 'ciclista', 
        '': '', 
        'clavecinista': 'clavecinista', 
        '': '', 
        'comediante en vivo': 'comediante en vivo', 
        '': '', 
        'compositor': 'compositora', 
        '': '', 
        'compositor de canciones': 'compositora de canciones', 
        '': '', 
        'conductor radiofónico': 'conductora radiofónica', 
        'conservador de arte': 'conservadora de arte', 
        'coreógrafo': 'coreógrafa', 
        '': '', 
        'crítico literario': 'crítica literaria', 
        '': '', 
        'deportista': 'deportista', 
        '': '', 
        'disc jockey': 'disc jockey', 
        '': '', 
        'director artístico': 'directora artística', 
        '': '', 
        'director de cine': 'directora de cine', 
        '': '', 
        'director de coro': 'directora de coro', 
        '': '', 
        'diseñador': 'diseñadora', 
        'diseñador de alta costura': 'diseñadora de alta costura', 
        'diseñador de joyas': 'diseñadora de joyas', 
        '': '', 
        'diseñador gráfico': 'diseñadora gráfica', 
        '': '', 
        'docente': 'docente', 
        '': '', 
        'dramaturgo': 'dramaturga', 
        '': '', 
        'economista': 'economista', 
        'empresario': 'empresaria', 
        '': '', 
        'escritor': 'escritora', 
        'escritor de ciencia ficción': 'escritora de ciencia ficción', 
        'escritor de género policiaco': 'escritora de género policiaco', 
        '': '', 
        'escritor de literatura infantil': 'escritora de literatura infantil', 
        '': '', 
        'escritor de no ficción': 'escritora de no ficción', 
        '': '', 
        'escultor': 'escultora', 
        '': '', 
        'esgrimista': 'esgrimista', 
        '': '', 
        'esquiador': 'esquiadora', 
        'esquiador acrobático': 'esquiadora acrobática', 
        'esquiador de fondo': 'esquiadora de fondo', 
        'esquiador de travesía': 'esquiadora de travesía', 
        '': '', 
        'filántropo': 'filántropa', 
        '': '', 
        'filósofo': 'filósofa', 
        '': '', 
        'folclorista': 'folclorista', 
        '': '', 
        '': '', 
        '': '', 
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
        '': '', 
        'guitarrista de jazz': 'guitarrista de jazz', 
        '': '', 
        'historiador': 'historiadora', 
        'historiador de la Edad Moderna': 'historiadora de la Edad Moderna', 
        '': '', 
        '': '', 
        'ilustrador': 'ilustradora', 
        '': '', 
        'ingeniero': 'ingeniera', 
        '': '', 
        'investigador': 'investigadora', 
        '': '', 
        'jugador de squash': 'jugadora de squash', 
        '': '', 
        'jugador de voleibol de playa': 'jugadora de voleibol de playa', 
        '': '', 
        'juez': 'jueza', 
        '': '', 
        'jugador de go': 'jugadora de go', 
        '': '', 
        'jurista': 'jurista', 
        '': '', 
        'karateka': 'karateka', 
        '': '', 
        'librero': 'librera', 
        '': '', 
        'lingüista': 'lingüista', 
        '': '', 
        'luchador profesional': 'luchadora profesional', 
        '': '', 
        'manager': 'manager', 
        '': '', 
        'médico': 'médico', 
        '': '', 
        'modelo': 'modelo', 
        'modelo artístico': 'modelo artística', 
        'modelo erótica': 'modelo erótica', 
        '': '', 
        'montañero': 'montañera', 
        '': '', 
        'músico': 'música', 
        'musicólogo': 'musicóloga', 
        '': '', 
        'músico de jazz': 'música de jazz', 
        '': '', 
        'nadador': 'nadadora', 
        '': '', 
        'novelista': 'novelista', 
        '': '', 
        'oftalmólogo': 'oftalmóloga', 
        '': '', 
        'orador motivacional': 'oradora motivacional', 
        '': '', 
        'organista': 'organista', 
        '': '', 
        'organizador sindical': 'organizadora sindical', 
        '': '', 
        'patinador artístico sobre hielo': 'patinadora artística sobre hielo', 
        '': '', 
        'patinador de velocidad': 'patinadora de velocidad', 
        '': '', 
        'participante de concurso de belleza': 'participante de concurso de belleza', 
        '': '', 
        'pedagogo': 'pedagoga', 
        '': '', 
        'percusionista': 'percusionista', 
        '': '', 
        'periodista': 'periodista', 
        'pianista': 'pianista', 
        '': '', 
        'piloto de carreras': 'piloto de carreras', 
        '': '', 
        'pintor': 'pintora', 
        '': '', 
        'poeta': 'poeta', 
        'político': 'política', 
        '': '', 
        '': '', 
        '': '', 
        'presentador': 'presentadora', 
        'presentador de televisión': 'presentadora de televisión', 
        'productor': 'productora', 
        'productor de cine': 'productora de cine', 
        'productor discográfico': 'productora discográfica', 
        '': '', 
        'profesor': 'profesora', 
        'profesor de educación superior': 'profesora de educación superior', 
        'profesor de música': 'profesora de música', 
        '': '', 
        'psicólogo': 'psicóloga', 
        '': '', 
        'psiquiatra': 'psiquiatra', 
        '': '', 
        'rapero': 'rapera', 
        '': '', 
        'realizador': 'realizadora', 
        '': '', 
        'remero': 'remera', 
        '': '', 
        'saltador de esquí': 'saltadora de esquí', 
        '': '', 
        'saxofonista': 'saxofonista', 
        '': '', 
        'socialité': 'socialité', 
        '': '', 
        'sociólogo': 'socióloga', 
        '': '', 
        'solista': 'solista', 
        '': '', 
        'tenista en silla de ruedas': 'tenista en silla de ruedas', 
        '': '', 
        'tipógrafo': 'tipógrafa', 
        '': '', 
        'titiritero': 'titiritera', 
        '': '', 
        'traductor': 'traductora', 
        '': '', 
        'velocista': 'velocista', 
        '': '', 
        'veterinario': 'veterinaria', 
        '': '', 
        '': '', 
        'violinista': 'violinista', 
        '': '', 
        'viticultor': 'viticultora', 
        '': '', 
        'voleibolista': 'voleibolista', 
        '': '', 
        'windsurfista': 'windsurfista', 
        '': '', 
        'yudoca': 'yudoca', 
        '': '', 
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
      7 tirador
      7 ultramaratonista
      8 banquero
      8 explorador
      8 matemático
      9 director de teatro
      9 diseñador
      9 filólogo
      9 productor de televisión
      9 sindicalista
     10 alumno
     10 empresario
     10 maestro de ballet
     10 publicista
     10 saltador de pértiga
     11 autobiógrafo
     11 editor
     11 escritor de no ficción
     11 narrador de audiolibros
     12 antropólogo
     12 artista plástico
     12 columnista
     12 director de orquesta
     12 historietista
     12 militar
     12 prosista
     12 seiyū
     13 Liedermacher
     13 maratonista
     14 activista por los derechos humanos
     14 contador
     14 diseñador de vestuario
     14 ensayista
     14 escenógrafo
     14 pentatleta
     14 Perito
     15 ciclista de ciclocrós
     15 humorista
     15 piloto de automovilismo
     15 triatleta
     16 educador
     16 ilustrador
     16 surfista
     17 crítico literario
     17 vocalista
     17 yodeler
     18 etnomusicólogo
     18 historiador de la música
     18 presentador de noticias
     18 snowboarder
     19 showgirl
     19 tenista
     20 actor de doblaje
     20 astrólogo
     20 bloguero
     20 emprendedor
     20 esquiador alpino
     20 masajista
     20 portavoz
     20 regatista
     21 ciclista de pista
     22 ajedrecista
     22 biatleta
     22 comediante
     22 mediador lingüístico
     24 humanitario
     24 químico
     24 voluntariado
     25 diplomático
     25 escalador en roca
     26 diseñador de moda
     26 modelo erótica
     27 editor de moda
    """
    
    site = pywikibot.Site('librefind', 'librefind')
    totalbios = 0
    for p27k, p27v in p27list:
        print('\n','#'*50,'\n',p27k,'\n','#'*50)
        #url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=SELECT%20DISTINCT%20%3Fitem%20%3FitemLabel%20%3FcountryLabel%20%3FsexLabel%20%3FbirthplaceLabel%20%3Fbirthdate%20%3FdeathplaceLabel%20%3Fdeathdate%20%3FoccupationLabel%20%3Fimage%20%3Fcommonscat%20%3Fwebsite%20%3Fsitelink%20WHERE%20%7B%0A%20%20%3Fitem%20wdt%3AP31%20wd%3AQ5.%0A%20%20%3Fitem%20wdt%3AP27%20wd%3A' + p27v + '.%0A%20%20%3Fitem%20wdt%3AP27%20%3Fcountry.%0A%20%20%3Fitem%20wdt%3AP21%20%3Fsex.%0A%20%20%3Fitem%20wdt%3AP19%20%3Fbirthplace.%0A%20%20%3Fitem%20wdt%3AP569%20%3Fbirthdate.%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP20%20%3Fdeathplace.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP570%20%3Fdeathdate.%20%7D%0A%20%20%3Fitem%20wdt%3AP106%20%3Foccupation.%0A%20%20%3Fitem%20wdt%3AP18%20%3Fimage.%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP373%20%3Fcommonscat.%20%7D%0A%20%20%3Fitem%20wdt%3AP856%20%3Fwebsite.%0A%20%20%3Fsitelink%20schema%3Aabout%20%3Fitem.%0A%20%20FILTER%20NOT%20EXISTS%20%7B%20%3Fwfr%20schema%3Aabout%20%3Fitem%20.%20%3Fwfr%20schema%3AinLanguage%20%22es%22%20%7D%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22es%2Cen%22%20%7D%0A%7D'
        url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=SELECT%20DISTINCT%20%3Fitem%20%3FitemLabel%20%3FcountryLabel%20%3FsexLabel%20%3FbirthplaceLabel%20%3Fbirthdate%20%3FdeathplaceLabel%20%3Fdeathdate%20%3FoccupationLabel%20%3Fimage%20%3Fcommonscat%20%3Fwebsite%20%3Fsitelink%20WHERE%20%7B%0A%20%20%3Fitem%20wdt%3AP31%20wd%3AQ5.%0A%20%20%3Fitem%20wdt%3AP27%20wd%3A' + p27v + '.%0A%20%20%3Fitem%20wdt%3AP27%20%3Fcountry.%0A%20%20%3Fitem%20wdt%3AP21%20%3Fsex.%0A%20%20%3Fitem%20wdt%3AP19%20%3Fbirthplace.%0A%20%20%3Fitem%20wdt%3AP569%20%3Fbirthdate.%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP20%20%3Fdeathplace.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP570%20%3Fdeathdate.%20%7D%0A%20%20%3Fitem%20wdt%3AP106%20%3Foccupation.%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP18%20%3Fimage.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP373%20%3Fcommonscat.%20%7D%0A%20%20%3Fitem%20wdt%3AP856%20%3Fwebsite.%0A%20%20%3Fsitelink%20schema%3Aabout%20%3Fitem.%0A%20%20FILTER%20NOT%20EXISTS%20%7B%20%3Fwfr%20schema%3Aabout%20%3Fitem%20.%20%3Fwfr%20schema%3AinLanguage%20%22es%22%20%7D%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22es%2Cen%22%20%7D%0A%7D'
        print(url)
        url = '%s&format=json' % (url)
        
        req = urllib.request.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
        sparql = urllib.request.urlopen(req).read().strip().decode('utf-8')
        sparql = '%s ]\n  }\n}' % (', {\n      "item" : {'.join(sparql.split(', {\n      "item" : {')[:-1]))
        #print(sparql)
        json1 = json.loads(sparql)
        bios = {}
        for result in json1['results']['bindings']:
            q = 'item' in result and result['item']['value'].split('/entity/')[1] or ''
            nombre = 'itemLabel' in result and result['itemLabel']['value'] or ''
            country = 'countryLabel' in result and result['countryLabel']['value'] or ''
            sexo = 'sexLabel' in result and result['sexLabel']['value'] or ''
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
            sitelink = 'sitelink' in result and result['sitelink']['value'] or ''
            if '.wikipedia.' in sitelink:
                sitelink = '%s:%s' % (sitelink.split('://')[1].split('.')[0], urllib.parse.unquote(sitelink.split('/wiki/')[1]))
            else:
                sitelink = ''
            
            if sexo == 'femenino':
                #print(ocup)
                #continue
                pass
            
            if q in bios:
                for x, y in [[country, 'countries'], [image, 'images'], [ocup, 'ocups'], [website, 'websites'], [sitelink, 'sitelinks']]:
                    if x and x not in bios[q][y]:
                        bios[q][y].append(x)
                        bios[q][y].sort()
            else:
                bios[q] = {
                    'q': q, 'nombre': nombre, 'countries': [country], 'sexo': sexo, 'lnac': lnac, 'fnac': fnac, 'lfal': lfal, 'ffal': ffal, 'ocups': [ocup], 'images': [image], 'commonscat': commonscat, 'websites': [website], 'sitelinks': [sitelink], 
                }
        
        bios_list = [[props['nombre'], q, props] for q, props in bios.items()]
        bios_list.sort()
        print('Encontradas %s bios' % (len(bios_list)))
        totalbios += len(bios_list)
        #continue
        
        for nombre, q, props in bios_list:
            print(nombre, props['ocups'])
            
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
                    if ocupfem[ocups[-1]].lower().startswith('i'):
                        intro = '%s e %s' % (intro, ocupfem[ocups[-1]])
                    else:
                        intro = '%s y %s' % (intro, ocupfem[ocups[-1]])
                else:
                    intro = '%s%s' % (intro, ocupfem[ocups[-1]])
                intro = '%s %s' % (intro, country2nationality[props['countries'][0]][props['sexo']])
            else: #hombre
                continue
                
                intro = '%s un %s' % (intro, ', '.join(ocups[:-1]))
                if len(ocups) > 1:
                    if ocups[-1].lower().startswith('i'):
                        intro = '%s e %s' % (intro, ocups[-1])
                    else:
                        intro = '%s y %s' % (intro, ocups[-1])
                else:
                    intro = '%s%s' % (intro, ocups[-1])
                intro = '%s %s' % (intro, country2nationality[props['countries'][0]][props['sexo']])
            
            websites = ''.join(["{{Website\n|title=Web oficial\n|url=%s\n|level=0\n}}" % (x) for x in props['websites']])
            gallery = ''.join(["{{Gallery file\n|filename=%s\n}}" % (x) for x in images])
            birthdeath = '[[%s]], %s' % (props['lnac'], convertirfecha(props['fnac']))
            if props['lfal'] and props['ffal']:
                birthdeath = '%s - %s, %s' % (birthdeath, props['lfal'] == props['lnac'] and 'íbidem' or '[[%s]]' % (props['lfal']), convertirfecha(props['ffal']))
            if '' in props['sitelinks']:
                props['sitelinks'].remove('')
            sitelinks = '; '.join(props['sitelinks'])
            output = """{{Infobox Result2
|search=%s
|introduction=[[{{FULLPAGENAME}}|%s]] (%s) %s.
|wikipedia=%s
|commons=%s
|wikidata=%s
|websites=%s
|gallery=%s
}}""" % (props['nombre'], props['nombre'], birthdeath, intro, sitelinks, props['commonscat'], props['q'], websites, gallery)
            print('\n', '#'*10, props['nombre'], '#'*10, '\n')
            print(output)
            try:
                time.sleep(1)
                #page = pywikibot.Page(site, '%s (%s)' % (props['nombre'], props['q']))
                page = pywikibot.Page(site, props['nombre'])
                page.text = output
                page.save('BOT - Creando página de resultados')
            except:
                time.sleep(10)
                pass
    
    print('Total bios %s' % (totalbios))

if __name__ == '__main__':
    main()
