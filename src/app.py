from flask import Flask, request, render_template, url_for, redirect
import speech_recognition as sr
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import requests
import os



app = Flask(__name__)
app.config["AUDIO_UPLOADS"] = "/Users/pranav/Downloads/"

#FUNCS

#LISTS --> STRING
def ListsintoStrings(l):
    string = " "
    string = string.join(l)
    return string

@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == "POST":
        
        if request.files:
           
            #SAVING FILE TO DIRECTORY

            wav_audio = request.files["wav_audio"]
            wav_audio_name = wav_audio.filename
            wav_audio.save(os.path.join(app.config["AUDIO_UPLOADS"], wav_audio_name))

            #RECOGNIZING WAV FILE WITH GOOGLE MODULE

            r = sr.Recognizer()
            
            with sr.AudioFile(f"/Users/pranav/Downloads/{wav_audio_name}") as source:
                audio = r.listen(source)
                translate_text = r.recognize_google(audio)

            #DELETING WAV FILE FROM WAV FOLDER

            filelist = [f for f in os.listdir(app.config["AUDIO_UPLOADS"]) if f.endswith('.wav')]
            for f in filelist:
                os.remove(os.path.join(app.config["AUDIO_UPLOADS"], f))

            #GETTING SERACH QUERY URL
            
            base_url = f"https://www.google.com/search?q={translate_text} genius.com"
            base_url = base_url.replace(' ', "%20")

            #INTIATING HTMLSESSION OBJECT AND GETTING SEARCH RESULTS
            
            session = HTMLSession()

            #GETTING SEARCH PAGE AND INITATING BS4 SOUP OBJECT

            search_page = session.get(base_url)
            soup = BeautifulSoup(search_page.content, "html.parser")

            #FINDING QUERY RESULT WITH FIND METHOD
            
            query_result = soup.find('h3', class_='LC20lb DKV0Md')
            query_result = query_result.span.contents[0]

            #USING LIST AND STRING FORMATTING TO GET ARTIST AND SONG NAME

            results_list = query_result.split()
            
            seperator = results_list.index('–')
            lyrics_keyword = results_list.index('Lyrics')

            artist_name = results_list[0:seperator]
            song_name = results_list[seperator+1:lyrics_keyword]
            
            #LIST CONTENTS --> STRING

            artist_name = ListsintoStrings(artist_name)
            song_name = ListsintoStrings(song_name)
            
            #GETTING ALBUM IMAGE

            album_image_url = f"https://genius.com/{artist_name}-{song_name}-lyrics".replace(" ", "-")
            album_image_page = session.get(album_image_url)
            album_image_soup = BeautifulSoup(album_image_page.content, "html.parser")

            album_image = album_image_soup.find('img', {"class": "cover_art-image"})
            album_image = album_image["src"]

            #RENDERING BACK TEMPLATES WITH VARIABLE

            return render_template("results.html", song_name=song_name, artist_name=artist_name, album_image=album_image)
       
    return render_template('index.html')

app.run(debug=True)
