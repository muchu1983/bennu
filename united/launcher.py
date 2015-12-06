"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import time
from united.world import World
from united.client import Client
from united.gameboard import GameBoard
from tkinter import Tk,Frame,Grid
"""
啟動主程式
"""
def main():
    #server start
    world = World()
    world.startWorld()
    time.sleep(2)
    #client start
    client = Client()
    root = Tk()
    frame = Frame(root)
    board = GameBoard(frame)
    board.setClient(client)
    frame.grid(row=0, column=0, sticky="news")
    root.wm_state("zoom") #最大化
    root.resizable(0,0) #關閉調整大小
    Grid.grid_rowconfigure(root, 0, weight=1)
    Grid.grid_columnconfigure(root, 0, weight=1)
    root.mainloop()
    #client stop
    client.closeConnection()
    #server stop
    world.stopWorld()
    world.saveWorldToDb()
    
if __name__ == "__main__":
    main()