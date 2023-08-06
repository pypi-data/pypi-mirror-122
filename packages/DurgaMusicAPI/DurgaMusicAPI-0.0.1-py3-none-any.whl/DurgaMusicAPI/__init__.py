from playsound import playsound

def list_songs():
    songs = {
        "Name: Dugga Elo, id: dugga-elo",
        "Name: Dhak Baja, id: dhak-baja",
        "Name: Yaa Chandi, id: yaa-chandi",
        "Name: Jatajutta Samayuktam, id: jatajutta",
        "Name: Bajlo Tomar Alor Benu, id: bajlo-tomar",
        "Name: Aigiri Nandini, id: aigiri",
        "Name: Aaji Bangladesher Hridoy Hote, id: bangladesher-hridoy"
    }
    return songs

def song(songid):
    if songid=="dugga-elo":
        return "https://technicalearth.github.io/BollyWood-Binge/audio/dugga-elo.mp3"
    elif songid=="bangladesher-hridoy":
        return "https://technicalearth.github.io/BollyWood-Binge/audio/aaji-bangalidesher.mp3"
    elif songid=="dhak-baja":
        return "https://technicalearth.github.io/BollyWood-Binge/audio/dhak-baja.mp3"
    elif songid=="yaa-chandi":
        return "https://technicalearth.github.io/BollyWood-Binge/audio/yaa-chandi.mp3"
    elif songid=="jatajutta":
        return "https://technicalearth.github.io/BollyWood-Binge/audio/jatajutta-samayuktam.mp3"
    elif songid=="bajlo-tomar":
        return "https://technicalearth.github.io/BollyWood-Binge/audio/bajlo-tomar.mp3"
    elif songid=="aigiri":
        return "https://technicalearth.github.io/BollyWood-Binge/audio/aigiri.mp3"