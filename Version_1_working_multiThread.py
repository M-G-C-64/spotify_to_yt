# %%
import spotipy
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from youtubesearchpython import VideosSearch
# from icecream import ic
from spotipy.oauth2 import SpotifyClientCredentials
import threading

skip_video = threading.Event()

# birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="", client_secret=""))

# results = spotify.artist_albums(birdy_uri, album_type='album')
# albums = results['items']
# while results['next']:
#     results = spotify.next(results)
#     albums.extend(results['items'])

# for album in albums:
#     print(album['name'])

# %%
def get_song_details(TNS, lang):
    The_Native_Suite = spotify.playlist(TNS)
    # The_Native_Suite['tracks']
    TNS_track =  The_Native_Suite['tracks']
    # ic(TNS_track['items'][5]['track']['album']['artists'][0]['name'])
    # ic(TNS_track['items'][5]['track']['album']['name'])


    TNS_dic = {}
    while TNS_track:

        # i = 0
        for i in range(len(TNS_track['items'])):

            t_name = TNS_track['items'][i]['track']['name']
            t_artists = TNS_track['items'][i]['track']['album']['artists']
            t_album = TNS_track['items'][i]['track']['album']['name']
            t_added_at = TNS_track['items'][i]['added_at']

            if t_name and t_artists:
                TNS_dic[t_name] =  {'artist': t_artists[0]['name'],
                                    'album': t_album,
                                    'added_at': t_added_at}

            # debug
            # print('mgc_id_000', TNS_dic)
            # return
        
        TNS_track = spotify.next(TNS_track)

    # print(TNS_dic)
    return(TNS_dic)


# %%
def play_songs(url, lang, brow, shuffle):   

    global skip_video

    TNS_dic = get_song_details(url, lang)

    keys = list(TNS_dic.keys())
    print(keys)
    t_sleep = 20
    
    #debug
    # return

    if brow.lower() == "chrome":
        browser = webdriver.Chrome()
    elif brow.lower() == "edge":
        browser = webdriver.Edge()
    elif brow.lower() == "safari":
        browser = webdriver.Safari()
    elif brow.lower() == "firefox":
        browser = webdriver.Firefox()
    else:
        print("No Browser found")
        return 0

    while keys:
        skip_video.clear()
        # browser.fullscreen_window()

        if not shuffle:
            print('playing the latest added songs')
            key = keys.pop()
        else:
            print ('playing random songs')
            key = random.choice(keys)

        try:
            videos = VideosSearch(key+" "+TNS_dic[key].get('artist')+" "+"video 4k"+" "+TNS_dic[key].get('album')+" "+lang, limit=3)

            if videos.result()['result']:

                yt_duration = videos.result()['result'][0]['duration']
                yt_link = videos.result()['result'][0]['link']

                for i in videos.result()['result']:

                    temp_title = i.get('title')
                    # print(temp_title)
                    if (("Video" in temp_title) or ("video" in temp_title)) and ((("lyric" not in temp_title) or (("Lyric" not in temp_title)))):
                        print("video:",temp_title)

                        yt_duration = i.get('duration')
                        yt_link = i.get('link')

                        break
            time_sec = yt_duration.split(':')

            if len(time_sec) > 1:
                kk = int(time_sec[0])*60 + int(time_sec[1])
            else:
                kk = int(time_sec[0])

            if kk > 500:
                continue
            
            print(TNS_dic[key])

            browser.get(yt_link)

            time.sleep(t_sleep)

            body = browser.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.SPACE)

            time.sleep(3)

            body.send_keys("F")

            for remaining_time in range(kk, 0, -1):
                if skip_video.is_set():
                    print('skipped to next')
                    break
                time.sleep(1)

            # time.sleep(kk)

        except:
            print("some error occurred")

        if shuffle:
            keys.remove(key)

        t_sleep = 5
        
    browser.quit()

def handle_input():
    global skip_video
    while True:
        user_input = input()
        if user_input.lower() == 'n':
            skip_video.set()

# %%
# play_songs("https://open.spotify.com/playlist/7AqXmRc7mk5dhendjlxkpe?si=0e9fcafa6f7549a7", 
        #    "english", "Chrome")

def main():
    input_thread = threading.Thread(target=handle_input, daemon=True)
    input_thread.start()

    play_songs("https://open.spotify.com/playlist/6XhHeU2bF2bsLKfmjwuUlD?si=67ed3192131f4192", 
            "telugu", "FireFox", shuffle=False)


if __name__ == '__main__':
    main()
