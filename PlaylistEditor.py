#This script is meant to populate the playlist table with a user's playlist from google play music.
from gmusicapi import Mobileclient
import sqlite3
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

api = Mobileclient()
#Now using the newer oauth login!

api.oauth_login(device_id=Mobileclient.FROM_MAC_ADDRESS, oauth_credentials="oauth.txt")


if Mobileclient.is_authenticated(api) == True:
    print("Logged into GPM successfully")
else:
    print("Please log into Google Play Music")
    api.perform_oauth(storage_filepath="oauth.txt")
    api.oauth_login(device_id=Mobileclient.FROM_MAC_ADDRESS, oauth_credentials="oauth.txt")








def fillPlaylist():
    print("These playlists were detected on your Google Play Music account:")
    print(">>-------------------------------------<<")
    dplaylists = api.get_all_user_playlist_contents()
    index = 1
    for item in dplaylists:
        print((str(index) + ". " + item['name']))
        index += 1
    index -= 1
    print(">>-------------------------------------<<")
    selection = eval(input("Please type the number of the playlist you wish to import into the bot's backup playlist, then press ENTER. \n"))
    while (selection < 1) or (selection > index):
        selection = eval(input("The number you have entered is invalid. Please enter a number between 1 and " + str(index) + ". \n"))
    selection -= 1
    playlist = dplaylists[selection]

    print("Using the songs from playlist: " + playlist['name'])

    db = sqlite3.connect('songqueue.db')
    cursor = db.cursor()
    index = 0
    errors = 0
    for item in playlist['tracks']:
        if item['trackId'][0][0] == "T":
            try:
                songtitle = (item['track']['artist'] + " - " + item['track']['title'])
                key = item['track']['storeId']

                sqlcommand = '''
                            INSERT INTO playlist(song, key)
                            VALUES("{song_name}", "{key}");'''.format(song_name=songtitle, key=key)

                cursor.execute(sqlcommand)


                print(str(index) + " - Added: " + songtitle)
            except KeyError:
                pass
            except Exception as e:
                print(">>>>>>>>>>>>>>>Something went wrong with adding the last song. Error below.<<<<<<<<<<<<<<<<<<<<<<<<<<")
                errors += 1
                print(e)
        else:
            print(str(index) + " - >>>>>>>>User Uploaded File - Cannot add to the playlist. Try !plsr with Youtube or an online link.")
            errors += 1
        index += 1
    print(">>>Finished! Out of " + str(index) + " songs, " + str(index - errors) + " were added successfully. There were " + str(errors) + " songs that couldn't be added, probably because they were user uploaded files.")


#
    db.commit()
    db.close()



def shuffleplaylist():
    from random import shuffle
    db = sqlite3.connect('songqueue.db')
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM playlist ORDER BY RANDOM()''')
    listSongs = cursor.fetchall()
    shuffle(listSongs)
    clearplaylist()
    for item in listSongs:
        print("Added: " + item[1])
        sqlcommand = '''
                        INSERT INTO playlist(song, key)
                        VALUES("{song_name}", "{key}");'''.format(song_name=item[1], key=item[2])
        cursor.execute(sqlcommand)
    db.commit()
    db.close()











def clearplaylist():
    db = sqlite3.connect('songqueue.db')
    cursor = db.cursor()
    sqlcommand = '''DELETE FROM playlist'''
    cursor.execute(sqlcommand)
    db.commit()
    db.close()


print(">>-------------------------------------<<")
print("Welcome to the RXBot Backup Playlist Control Application. What would you like to do? \n1. Fill Playlist \n2. Shuffle Playlist \n3. Clear Playlist")
print(">>-------------------------------------<<")
inp = eval(input("Type the number of the option you would like here then press ENTER: \n"))
if inp == 1:
    fillPlaylist()
if inp == 2:
    shuffleplaylist()
    print("Shuffled the playlist!")
if inp == 3:
    clearplaylist()
    print("Cleared the whole backup playlist. Run this script again to fill it back up.")













