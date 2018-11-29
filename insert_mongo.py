import psycopg2 as driver
from pymongo import MongoClient
import datetime


host = "127.0.0.1"
banco_de_dados = "spotify_final"
usuario = "bd_t2"
password = "senha"

con = driver.connect(host=host, database=banco_de_dados, user=usuario, password=password)
cur = con.cursor()

cliente = MongoClient('localhost', 27017)

#Track---------------------------------------------------
#Track_playlist
track_playlist = []
sql = 'select * from spotify_db.track_playlist'
cur.execute(sql)
track_playlist = cur.fetchall()

#Track_popularity
track_popularity = []
sql = 'select * from spotify_db.track_popularity'
cur.execute(sql)
track_popularity = cur.fetchall()


track = []
sql = 'select * from spotify_db.track'
cur.execute(sql)
track = cur.fetchall()

collection = cliente['spotify_db'].track
for i in track:
    popularity = []
    playlist = []
    for x in track_popularity:
        if(x[0] == i[0]):
            popularity.append({"data_popularidade": x[1],"track_popularity":x[2]})
    for x in track_playlist:
        if(x[0] == i[0]):
            sql = "select * from spotify_db.playlist where playlist_id ='" + x[1] +"'"
            cur.execute(sql)
            j = cur.fetchall()
            playlist.append({"playlist_name":j[0][1],"playlist_colaborative": j[0][2],"playlist_category": j[0][3]})

    doc = {
        "_id" : i[0],
        "track_name":i[1],
        "track_liveness": i[2],
        "track_speechness": i[3],
        "track_explicit" : i[4],
        "track_tempo" : i[5],
        "track_valence" : i[6],
        "track_number" : i[7],
        "track_energy" : i[8],
        "track_acousticness" : i[9],
        "track_instrumentalness" : i[10],
        "track_dancebility" : i[11],
        "track_duration" : i[12],
        "track_popularity" : popularity,
        "track_playlist" : playlist
    }
    collection.insert_one(doc)

#Album----------------------------------------------------
#Track_album
track_album = []
sql = 'select * from spotify_db.track_album'
cur.execute(sql)
track_album = cur.fetchall()
collection = cliente['spotify_db'].track_album

album = []
sql = 'select * from spotify_db.album'
cur.execute(sql)
album = cur.fetchall()

collection = cliente['spotify_db'].album
track_presentes = []

for i in album:
    for j in track_album:
        if(j[1] == i[0]):
            track_presentes.append(j[0]);
    doc = {
        "_id" : i[0],
        "album_name":i[1],
        "album_release_date": i[2],
        "album_popularity":i[3],
        "track_album" : track_presentes
    }
    collection.insert_one(doc).inserted_id

#Track_artist---------------------------------
track_artist = []
sql = 'select * from spotify_db.track_artist'
cur.execute(sql)
track_artist = cur.fetchall()

#Artist Popularity---------------------------------
artist_popularity = []
sql = 'select * from spotify_db.artist_popularity'
cur.execute(sql)
artist_popularity = cur.fetchall()

#Artist---------------------------------
artist = []
sql = 'select * from spotify_db.artist'
cur.execute(sql)
artist = cur.fetchall()
collection = cliente['spotify_db'].artist

for i in artist:
    popularity = []
    tracks_presentes = []
    for x in artist_popularity:
        if(x[0] == i[0]):
            popularity.append({"data_popularidade": x[1],"artist_popularity":x[2]})
    for x in track_artist:
        if(x[1] == i[0]):
            tracks_presentes.append(x[0])
    doc = {
        "_id" : i[0],
        "artist_name":i[1],
        "artist_genre": i[2],
        "artist_followers":i[3],
        "artist_popularity" : popularity,
        "track_artist" : track_presentes
    }
    collection.insert_one(doc).inserted_id



cur.close()
con.close()