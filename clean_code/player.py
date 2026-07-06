from mutagen.easyid3 import EasyID3
import pygame
from tkinter.filedialog import *
from tkinter import *
pygame.init()

class FrameApp(Frame):
    def __init__(self,master):
        super(FrameApp, self).__init__(master)
        self.grid()

        self.songs: list = []
        self.current_song: int = 0
        self.paused: bool = False
        self.song_end: int = pygame.USEREVENT + 1
        
        self.play_btn: Button = Button(self, text="PLAY SONG",command=self.play_song,bg='AntiqueWhite1',width=40)
        self.play_btn.grid(row=2,column=0)
        
        self.previous_btn: Button = Button(self, text="PREVIOUS SONG",command=self.previous_song,bg='AntiqueWhite1',width=40)
        self.previous_btn.grid(row=4,column=0)
        
        self.pause_btn: Button = Button(self, text="PAUSE/UNPAUSE",command=self.pause_song,bg='AntiqueWhite1',width=40)
        self.pause_btn.grid(row=3,column=0)
        
        self.next_btn: Button = Button(self, text="NEXT SONG",command=self.next_song,bg='AntiqueWhite1',width=40)
        self.next_btn.grid(row=5,column=0)
        
        self.add_btn: Button = Button(self, text="ADD TO LIST",command=self.add_songs,bg='AntiqueWhite1',width=40)
        self.add_btn.grid(row=1,column=0)
        
        self.currently_playing = Label(self, fg='Black',font=('Helvetica 12 bold italic',10),bg='ivory2')
        self.currently_playing.grid(row=6,column=0)
        
        self.playlist_songs = Text(self,wrap=WORD,width=60)
        self.playlist_songs.grid(row=8,column=0)
        
    #################################################################################
    def add_songs(self):
        try:
            directory = askopenfilenames()
            for song_dir in directory:
                print(song_dir)
                self.songs.append(song_dir)
            self.playlist_songs.delete("1.0", END)
            for key, item in enumerate(self.songs):
                song = EasyID3(item)
                song_data = (str(key + 1) + ' : ' + song['title'][0] + ' - ' +
                    song['artist'][0])
                self.playlist_songs.insert(END, song_data + '\n')
        except Exception as e:
            print(f"Error occurred: {e}")
    #################################################################################
    def song_data(self):
        try:
            song = EasyID3(self.songs[self.current_song])
            song_data = "Now playing: Nr:" + str(self.current_song + 1) + " " + \
                        str(song['title']) + " - " + str(song['artist'])
            return song_data
        except Exception as e:
            print(f"Error occurred: {e}")
    #################################################################################
    def play_song(self):
        try:
            directory = self.songs[self.current_song]
            pygame.mixer.music.load(directory)
            pygame.mixer.music.play(1, 0.0)
            pygame.mixer.music.set_endevent(self.song_end)
            self.paused = False
            self.currently_playing.config(text=self.song_data())
        except Exception as e:
            print(f"Error occurred: {e}")
    #################################################################################
    def check_music(self):
        try:
            for event in pygame.event.get():
                if event.type == self.song_end:
                    self.next_song()
        except Exception as e:
            print(f"Error occurred: {e}")
    #################################################################################
    def pause_song(self):
        try:
            if self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
            elif not self.paused:
                pygame.mixer.music.pause()
                self.paused = True
        except Exception as e:
            print(f"Error occurred: {e}")
    #################################################################################
    def get_next_song(self):
        try:
            if self.current_song + 2 <= len(self.songs):
                return self.current_song + 1
            else:
                return 0
        except Exception as e:
            print(f"Error occurred: {e}")
    #################################################################################
    def next_song(self):
        try:
            self.current_song = self.get_next_song()
            self.play_song()
        except Exception as e:
            print(f"Error occurred: {e}")
    #################################################################################
    def get_previous_song(self):
        try:
            if self.current_song - 1 >= 0:
                return self.current_song - 1
            else:
                return len(self.songs) - 1
        except Exception as e:
            print(f"Error occurred: {e}")
    #################################################################################
    def previous_song(self):
        try:
            self.current_song = self.get_previous_song()
            self.play_song()
        except Exception as e:
            print(f"Error occurred: {e}")
    #################################################################################
    def poll_music(self):
        try:
            self.check_music()
        except Exception as e:
            print(f"Error occurred: {e}")

        self.after(100, self.poll_music)
#################################################################################
window = Tk()
window.geometry("500x500")
window.title("MP3 Music Player")
#################################################################################
app = FrameApp(window)
#################################################################################
app.poll_music()
window.mainloop()