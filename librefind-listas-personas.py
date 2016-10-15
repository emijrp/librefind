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

import re
import pywikibot
import urllib
import urllib.parse
from librefindglobals import *

def main():
    global nacionalidades_list
    global ocupaciones_list
    
    site = pywikibot.Site('librefind', 'librefind')
    skipuntilcountry = ''
    skipuntilocup = ''
    for pais, nacprops in nacionalidades_list:
        if skipuntilcountry:
            if skipuntilcountry == pais:
                skipuntilcountry = ''
            else:
                print('Skiping until... %s' % (skipuntilcountry))
                continue
        
        for ocupacion, ocuprops in ocupaciones_list:
            if skipuntilocup:
                if skipuntilocup == ocupacion:
                    skipuntilocup = ''
                else:
                    print('Skiping until... %s' % (skipuntilocup))
                    continue
            
            print(pais, ocupacion)
            query = '[[clase%3A%3Apersona]][[ocupaci%C3%B3n%3A%3A' + urllib.parse.quote(ocuprops['ms']) + '||' + urllib.parse.quote(ocuprops['fs']) + ']][[nacionalidad%3A%3A' + urllib.parse.quote(nacprops['ms']) +'||' + urllib.parse.quote(nacprops['fs']) +']]&p=format%3Dbroadtable%2Flink%3Dall%2Fheaders%3Dshow&eq=no'
            url = 'https://www.librefind.org/w/index.php?title=Especial:Ask&q=' + query
            raw = getURL(url).strip()
            #print(url)
            if 'No hay resultados' in raw:
                print('No hay resultados')
            else:
                print('Si hay resultados')
                title = '%s %s' % (ocuprops['mp'], nacprops['mp'])
                page = pywikibot.Page(site, title)
                output = """{{personas
|ocupación masculino=%s
|ocupación femenino=%s
|ocupación masculino plural=%s
|ocupación femenino plural=%s
|nacionalidad masculino=%s
|nacionalidad femenino=%s
|nacionalidad masculino plural=%s
|nacionalidad femenino plural=%s
}}""" % (ocuprops['ms'], ocuprops['fs'], ocuprops['mp'], ocuprops['fp'], nacprops['ms'], nacprops['fs'], nacprops['mp'], nacprops['fp'])
                page.text = output
                try:
                    page.save('BOT - Creando página de resultados')
                    redtitle = '%s %s' % (ocuprops['ms'], nacprops['ms'])
                    redpage = pywikibot.Page(site, redtitle)
                    redpage.text = '#REDIRECT [[%s]]' % (title)
                    redpage.save('BOT - Creando redirección')
                except:
                    print('Error guardando pagina')

if __name__ == '__main__':
    main()
