#!/usr/bin/python
# -*- coding: utf-8 -*-

import twitter
import json
import io
import datetime
import urllib2
from urllib import unquote
from collections import Counter
from flask import Flask, render_template
from flask.ext.googlemaps import GoogleMaps
from flask.ext.googlemaps import Map
from pprint import pprint

app = Flask(__name__)
GoogleMaps(app)


#Credenciales de nuestra API
CONSUMER_KEY = 'Dm1Q0DPbBWJh3NGvIGwWtINFm'
CONSUMER_SECRET ='v29T668iPJYQXqjuQDskjNW8UF0bfjJ6uXOz3tm1baBMBWuLO3'
OAUTH_TOKEN = '3148519900-uJjC7HEFck2Vvm8Knpd8YfHyC9zt4gTqM4XEfyZ'
OAUTH_TOKEN_SECRET = 'xLlxPwwwIZUUHcTfdhxjqK1mnBP9eCS4GTuoqlqJhe5kZ'

# Se autentica con Twitter
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
CONSUMER_KEY, CONSUMER_SECRET)

# Crea una conexión a la API
twitter_api = twitter.Twitter(auth=auth)

# Crea una conexión a la API de Streamming
#twitter_stream = twitter.TwitterStream(auth=auth)

#Where On Earth ID de algunos lugares en los que nos interesa centrar la búsqueda
WORLD_WOE_ID = 1
US_WOE_ID = 23424977
CADIZ_WOE_ID = 755404
SANLUCAR_WOE_ID = 773544
JEREZ_WOE_ID = 762833
 
# usaremos la variable now como prefijo para nombrar diferentes archivos y no reescribirlos.
now = str(datetime.datetime.now())
 
# el usuario o palabra que queremos consultar
QUERY = 'jerez'
count = 1000
 
# El archivo al que grabaremos los resultados en JSON separados
# por línea y con la fecha en el nombre.
OUT_FILE = QUERY + now + ".json"

#Mensaje que se muestra para indicar que se a comenzado a filtrar
#la palabra que queremos consultar
print 'Buscando tweets en el timeline que contengan "{0}"'.format(QUERY)
 
# mire https://dev.twitter.com/docs/streaming-apis en los parametros de las keywords
#stream = twitter_stream.statuses.filter(track=QUERY)

search_results = twitter_api.search.tweets(q=QUERY, count=count)

statuses = search_results['statuses']
marcas=[]

# Escriba un tweet por linea en un documento JSON
with io.open(OUT_FILE, 'w', encoding='utf-8', buffering=1) as f:
  for tweet in statuses:
    f.write(unicode(u'{0}\n'.format(json.dumps(tweet, ensure_ascii=False))))
    if str(tweet['coordinates']) != "None":
        #print '_' + str(tweet['coordinates']) + '_'
        #print str(tweet['coordinates']).find('coordinates')
	#print str(tweet['coordinates'])[str(tweet['coordinates']).find('coordinates')+15:]
	print 'Latitud= ' + str(tweet['coordinates'])[str(tweet['coordinates']).find('coordinates')+15:][:str(tweet['coordinates'])[str(tweet['coordinates']).find('coordinates')+15:].find(',')]
	#print str(tweet['coordinates'])[str(tweet['coordinates']).find('coordinates')+15:].find(',')+2
	print 'Longitud= '+str(tweet['coordinates'])[str(tweet['coordinates']).find('coordinates')+15:][str(tweet['coordinates'])[str(tweet['coordinates']).find('coordinates')+15:].find(',')+2:-2]        
	marcas.append([str(tweet['coordinates'])[str(tweet['coordinates']).find('coordinates')+15:][str(tweet['coordinates'])[str(tweet['coordinates']).find('coordinates')+15:].find(',')+2:-2] ,str(tweet['coordinates'])[str(tweet['coordinates']).find('coordinates')+15:][:str(tweet['coordinates'])[str(tweet['coordinates']).find('coordinates')+15:].find(',')]])

pprint (marcas)

@app.route("/")
def mapview():
    mymap = Map(
        identifier="view-side",
        lat=40.3450396,
        lng=-3.6517684,
        zoom=6,
        markers=marcas,  
        style="height:800px;width:800px;margin:0;"
    ) 
    return render_template('template2.html', mymap=mymap)



if __name__ == "__main__":
    app.run(debug=True)


#borrar el archivo aqui

# Show one sample search result by slicing the list...
#statuses = json.loads(open(OUT_FILE).read())

#print json.dumps(statuses[0], indent=1)



