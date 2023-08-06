# PyAppBuilder

Developed by Roop Majumder from Technical Earth (c) 2020

## Examples of How To Use

List all songs

```python
from DurgaMusicAPI import list_songs

print(list_songs())
```

output

```cmd
{'Name: Jatajutta Samayuktam, id: jatajutta', 'Name: Bajlo Tomar Alor Benu, id: bajlo-tomar', 'Name: Yaa Chandi, id: yaa-chandi', 'Name: Dhak Baja, id: dhak-baja', 'Name: Aigiri Nandini, id: aigiri', 'Name: Aaji Bangladesher Hridoy Hote, id: bangladesher-hridoy', 'Name: Dugga Elo, id: dugga-elo'}
```


Choose a song with playing

```cmd
pip install playsound
```

```python
from DurgaMusicAPI import song
from playsound import playsound

# song(songid)
# you don't need to install playsound it will be installed automatically.

playsound(song("song you interested in."))
```
	
##### There are more to explore stay around.

##### more things coming soon.