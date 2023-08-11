import asyncio
import numpy as np
import pyscreenshot as ImageGrab
import cv2
import os
import pytesseract
import pyautogui as pg
import time
import threading

stop_thread_flag = threading.Event()
repetitions = 0
pg.FAILSAFE = False

async def start_script(sleep=60, prsl='none', lang='rus', filepath='perem.png', 
                       xy1=(0, 0), xy2=(1920, 1080), clicks=[(0, 0)], clickcd=False, showwindow=False):
    global repetitions
    last_time = time.time()

    while not stop_thread_flag.is_set():
        repetitions += 1
        print(f'cycle: {repetitions}')
        
        x1, y1 = xy1 #754, 534
        x2, y2 = xy2 #1158, 577
        
        screen = np.array(ImageGrab.grab(bbox=(x1, y1, x2, y2)))
        print(f'loop: {time.time() - last_time}')
        last_time = time.time()
        cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
        cv2.imwrite(filepath, screen)
 
        if not showwindow:
            cv2.destroyAllWindows()
        
        img = cv2.imread(filepath)
        txt = pytesseract.image_to_string(img, lang)
        print(f'\n-------------\n{txt}\n-------------\n')
        
        if prsl in txt:
            for x, y in clicks:
                if clickcd:
                    await asyncio.sleep(clickcd)
                pg.click(x, y) #950, 560  #482, 785
        if stop_thread_flag.is_set():
            break
        await asyncio.sleep(sleep)


if __name__ == '__main__':
    asyncio.run(start_script(sleep=1, prsl='да', xy1=(754, 534), xy2=(1158, 577), clicks=[(950, 560), (482, 785)], clickcd=1, showwindow=True))
