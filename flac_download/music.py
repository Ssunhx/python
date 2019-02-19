# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 21:44:49 2018

@author: ssun
"""

from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from urllib import request
from download import *
from tkinter import messagebox
import queue
import time

class MainGUI(Tk):
    def __init__(self):
        super().__init__()
        self.title('无损音乐下载 --Ssun')
        self.geometry('800x600')
        self.resizable(0, 0)
        self.main_image = PhotoImage(file = './image/image.png')
        self.Label_image = Label(self, image=self.main_image)
        self.Label_image.pack()
        self.queue = queue.Queue()
        
        self.song_n = StringVar()
        self.search_box = Entry(self, width=50, textvariable=self.song_n)
        #print(help(Entry))
        def submit(song_n):
            x = self.Tree.get_children()
            for item in x:
                self.Tree.delete(item)
            self.song_name = self.song_n.get()
            # print(self.song_name)
            self.music = Get_source(self.song_name)
            self.music_list = self.music.search_detail()
            self.show_list(self.music_list)
        self.search_box.bind('<Key-Return>',submit)
        self.search_box.place(x=200,y=100)
        self.treeview()
        # self.startdown()

    def startdown(self):
        #侦测队列，完成下载
        while 1:
            if not self.queue.empty():
                par = self.queue.get()
                if type(par) != bool:                   
                    self.music.StartDownload(*par)
       
    def show_list(self,music_list):
        for i in range(10):
            music_one = music_list[i]
            song_name = music_one['song_name']
            singer_name = music_one['singer_name']
            album_name = music_one['album_name']
            song_id = music_one['id']
            song_format = music_one['format']
            song_type = None
#            print(song_name,singer_name, album_name, song_format)
            if music_one['format']['size_flac'] > 0:
                song_type = '无损音质(flac)'
            elif music_one['format']['size_ape'] > 0:
                song_type = 'ape格式'
            elif music_one['format']['size_128'] > 0:
                song_type = 'mp3格式'
            self.Tree.insert('',i,values=('%d'%(i+1), song_name, singer_name, album_name, song_type))
            
    def download(self,event):
        item = self.Tree.selection()
        item_text = self.Tree.item(item,"values")
        #print(item_text)
        index = int(item_text[0]) - 1
        if 'flac' not in item_text[4]:
        	messagebox.showinfo(title='Warning！',message='非flac格式不能下载')
        else:
            flag = self.music.get_source(self.music_list[index])
            self.queue.put(flag)
            # print(flag)
            try:
            	if len(flag) == 1:
                	messagebox.showinfo(title='Warning！',message='该资源不能下载')
            	elif flag == False:
            		messagebox.showinfo(title='Warning！',message='该资源没有版权不能下载')
            except:
            	messagebox.showinfo(title='Warning！',message='该资源不能下载')
            
        
        
    def treeview(self):
        self.Pane_right = Panedwindow(
            width=650, height=230, style='right.TPanedwindow')
        self.Pane_right.place(x=75, y=155)
        self.Tree = Treeview(self.Pane_right, columns = ('id','song','singer','album','format'),show='headings',height=230)
        self.Tree.place(x=0,y=0)
        self.Tree.column('id',width=50,anchor='center')
        self.Tree.column('song',width=150,anchor='center')
        self.Tree.column('singer',width=150,anchor='center')
        self.Tree.column('album',width=150,anchor='center')
        self.Tree.column('format',width=150,anchor='center')
        self.Tree.heading('id',text='')
        self.Tree.heading('song',text='歌曲')
        self.Tree.heading('singer',text='歌手')
        self.Tree.heading('album',text='专辑')
        self.Tree.heading('format',text='格式')
        self.Tree.bind('<Double-1>', self.download)#绑定单击离开事件===========

if __name__ == '__main__':
    import os
    if 'music' not in os.listdir():
        os.makedirs('music')
    GUI = MainGUI()
    from threading import Thread
    t = Thread(target=GUI.startdown)
    t.start()
    GUI.mainloop()