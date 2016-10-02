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
        'Alemania': {'masculino': 'alemán', 'femenino': 'alemana' }, 
        'España': {'masculino': 'español', 'femenino': 'española' }, 
        'Francia': {'masculino': 'francés', 'femenino': 'francesa' }, 
        'Italia': {'masculino': 'italiano', 'femenino': 'italiana' }, 
        'Noruega': {'masculino': 'noruego', 'femenino': 'noruega' }, 
        'Portugal': {'masculino': 'portugués', 'femenino': 'portuguesa' }, 
        'Rusia': {'masculino': 'ruso', 'femenino': 'rusa' }, 
    }
    
    site = pywikibot.Site('librefind', 'librefind')
    
    for p27k, p27v in p27list:
        print('\n','#'*50,'\n',p27k,'\n','#'*50)
        #url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=SELECT%20DISTINCT%20%3Fitem%20%3FitemLabel%20%3FcountryLabel%20%3FsexLabel%20%3FbirthplaceLabel%20%3Fbirthdate%20%3FdeathplaceLabel%20%3Fdeathdate%20%3FoccupationLabel%20%3Fimage%20%3Fcommonscat%20%3Fwebsite%20%3Fsitelink%20WHERE%20%7B%0A%20%20%3Fitem%20wdt%3AP31%20wd%3AQ5.%0A%20%20%3Fitem%20wdt%3AP27%20wd%3A' + p27v + '.%0A%20%20%3Fitem%20wdt%3AP27%20%3Fcountry.%0A%20%20%3Fitem%20wdt%3AP21%20%3Fsex.%0A%20%20%3Fitem%20wdt%3AP19%20%3Fbirthplace.%0A%20%20%3Fitem%20wdt%3AP569%20%3Fbirthdate.%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP20%20%3Fdeathplace.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP570%20%3Fdeathdate.%20%7D%0A%20%20%3Fitem%20wdt%3AP106%20%3Foccupation.%0A%20%20%3Fitem%20wdt%3AP18%20%3Fimage.%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP373%20%3Fcommonscat.%20%7D%0A%20%20%3Fitem%20wdt%3AP856%20%3Fwebsite.%0A%20%20%3Fsitelink%20schema%3Aabout%20%3Fitem.%0A%20%20FILTER%20NOT%20EXISTS%20%7B%20%3Fwfr%20schema%3Aabout%20%3Fitem%20.%20%3Fwfr%20schema%3AinLanguage%20%22es%22%20%7D%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22es%2Cen%22%20%7D%0A%7D'
        url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=SELECT%20DISTINCT%20%3Fitem%20%3FitemLabel%20%3FcountryLabel%20%3FsexLabel%20%3FbirthplaceLabel%20%3Fbirthdate%20%3FdeathplaceLabel%20%3Fdeathdate%20%3FoccupationLabel%20%3Fimage%20%3Fcommonscat%20%3Fwebsite%20%3Fsitelink%20WHERE%20%7B%0A%20%20%3Fitem%20wdt%3AP31%20wd%3AQ5.%0A%20%20%3Fitem%20wdt%3AP27%20wd%3A' + p27v + '.%0A%20%20%3Fitem%20wdt%3AP27%20%3Fcountry.%0A%20%20%3Fitem%20wdt%3AP21%20%3Fsex.%0A%20%20%3Fitem%20wdt%3AP19%20%3Fbirthplace.%0A%20%20%3Fitem%20wdt%3AP569%20%3Fbirthdate.%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP20%20%3Fdeathplace.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP570%20%3Fdeathdate.%20%7D%0A%20%20%3Fitem%20wdt%3AP106%20%3Foccupation.%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP18%20%3Fimage.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP373%20%3Fcommonscat.%20%7D%0A%20%20%3Fitem%20wdt%3AP856%20%3Fwebsite.%0A%20%20%3Fsitelink%20schema%3Aabout%20%3Fitem.%0A%20%20FILTER%20NOT%20EXISTS%20%7B%20%3Fwfr%20schema%3Aabout%20%3Fitem%20.%20%3Fwfr%20schema%3AinLanguage%20%22es%22%20%7D%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22es%2Cen%22%20%7D%0A%7D'
        url = '%s&format=json' % (url)
        
        req = urllib.request.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
        sparql = urllib.request.urlopen(req).read().strip().decode('utf-8')
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
            
            if q in bios:
                for x, y in [[image, 'images'], [ocup, 'ocups'], [website, 'websites'], [sitelink, 'sitelinks']]:
                    if x and x not in bios[q][y]:
                        bios[q][y].append(x)
                        bios[q][y].sort()
            else:
                bios[q] = {
                    'q': q, 'nombre': nombre, 'country': country, 'sexo': sexo, 'lnac': lnac, 'fnac': fnac, 'lfal': lfal, 'ffal': ffal, 'ocups': [ocup], 'images': [image], 'commonscat': commonscat, 'websites': [website], 'sitelinks': [sitelink], 
                }
        
        bios_list = [[props['nombre'], q, props] for q, props in bios.items()]
        bios_list.sort()
        print('Encontradas %s bios' % (len(bios_list)))
        continue
        
        for nombre, q, props in bios_list:
            print(nombre, props['ocups'])
            if not props['ocups']:
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
                continue
            else: #hombre
                intro = '%s un %s' % (intro, ', '.join(ocups[:-1]))
                if len(ocups) > 1:
                    if ocups[-1].lower().startswith('i'):
                        intro = '%s e %s' % (intro, ocups[-1])
                    else:
                        intro = '%s y %s' % (intro, ocups[-1])
                else:
                    intro = '%s%s' % (intro, ocups[-1])
                intro = '%s %s' % (intro, country2nationality[props['country']][props['sexo']])
            
            websites = ''.join(["{{Website\n|title=Web oficial\n|url=%s\n|level=0\n}}" % (x) for x in props['websites']])
            gallery = ''.join(["{{Gallery file\n|filename=%s\n}}" % (x) for x in props['images']])
            birthdeath = '[[%s]], %s' % (props['lnac'], convertirfecha(props['fnac']))
            if props['lfal'] and props['ffal']:
                birthdeath = '%s - %s, %s' % (birthdeath, props['lfal'] == props['lnac'] and 'íbidem' or '[[%s]]' % (props['lfal']), convertirfecha(props['ffal']))
            if '' in props['sitelinks']:
                props['sitelinks'].remove('')
            sitelinks = ', '.join(props['sitelinks'])
            output = """{{Infobox Result2
|search=%s
|introduction='''%s''' (%s) %s.
|wikipedia=%s
|commons=%s
|wikidata=%s
|websites=%s
|gallery=%s
}}""" % (props['nombre'], props['nombre'], birthdeath, intro, sitelinks, props['commonscat'], props['q'], websites, gallery)
            print(output)
            #page = pywikibot.Page(site, '%s (%s)' % (props['nombre'], props['q']))
            page = pywikibot.Page(site, props['nombre'])
            page.text = output
            page.save('BOT - Creando página de resultados')

if __name__ == '__main__':
    main()
