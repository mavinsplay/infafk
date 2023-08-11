import customtkinter
import keyboard
import pyautogui
import time
from infafk import *

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.xy1, self.xy2 = (0, 0), (1920, 1080)        
        self.title('infinity afk        |        by o2o                                                                                             Alfa 0.1')
        self.geometry('660x420')
        
        self.button = customtkinter.CTkButton(self, text='Start script', command=self.start_but, width=640, height=40) # кнопка старт-стоп
        self.button.place(x=10, y=10)
        
        self.label2 = customtkinter.CTkLabel(self, text='cycles: 0', fg_color='transparent') # лейбл циклов 
        self.label2.place(x=300, y=60)
        
        self.entry = customtkinter.CTkEntry(self, width=50, height=10, placeholder_text='60') # ввод переодичности
        self.entry.place(x=110, y=100)
        
        self.label3 = customtkinter.CTkLabel(self, text='frequency of verification', fg_color='transparent')  # |>
        self.label3.place(x=70, y=130)
        
        self.entry2 = customtkinter.CTkEntry(self, width=200, height=20, placeholder_text='back') # ввод слова для проверки
        self.entry2.place(x=40, y=180)
        
        self.label4 = customtkinter.CTkLabel(self, text='a word to check') # |>
        self.label4.place(x=100, y=220)
        
        self.button2 = customtkinter.CTkButton(self, text='determine coordinates', command=self.coord_but, width=300, height=40, fg_color='#5f00d7') # тест координат
        self.button2.place(x=10, y=370)

        self.entry3 = customtkinter.CTkEntry(self, width=30, height=10, placeholder_text='q') # лейбл кнопки остановки опр. координат
        self.entry3.place(x=220, y=310)
        
        self.label5 = customtkinter.CTkLabel(self, text=f'to stop the\ncoordinates function, press:') # |>
        self.label5.place(x=60, y=300)
        
        self.button3 = customtkinter.CTkButton(self, text='xy 1', command=lambda: self.xy_but(1), width=100, fg_color='#5f00d7') # xy1
        self.button3.place(x=400, y=100)
        
        self.label6 = customtkinter.CTkLabel(self, text=f'x={self.xy1[0]} y={self.xy1[1]}') # |>
        self.label6.place(x=420, y=130)
        
        self.button4 = customtkinter.CTkButton(self, text='xy 2', command=lambda: self.xy_but(2), width=100, fg_color='#5f00d7') # xy2
        self.button4.place(x=540, y=100)
        
        self.label7 = customtkinter.CTkLabel(self, text=f'x={self.xy2[0]} y={self.xy2[1]}') # |>
        self.label7.place(x=550, y=130)
     
        self.checkbox = customtkinter.CTkCheckBox(self, text='show screenshot')
        self.checkbox.place(x=400, y=190)   
        
        self.optionmenu = customtkinter.CTkOptionMenu(self, values=['eng', 'rus'])
        self.optionmenu.place(x=400, y=260)
        
        self.label8 = customtkinter.CTkLabel(self, text='language check')
        self.label8.place(x=555, y=260)
    
    def start_script_thread(self):
        asyncio.run(start_script(sleep=int(self.period), prsl=self.prsl, xy1=self.xy1, xy2=self.xy2, showwindow=self.checkbox.get(), lang=self.optionmenu.get()))
    
    def start_updating_label(self, repetition=0): # не может обновляться в отдельном потоке !!баг
        pass
        #while not stop_thread_flag.is_set():
            #self.label2.configure(text=f'цкилов: {repetition}')

    def start_but(self):
        text = self.button.cget('text')

        self.prsl = 'back' if not self.entry2.get() else self.entry2.get()
        self.period = 60 if not self.entry.get() else self.entry.get()

        if text == 'Start script':  
            
            self.thread = threading.Thread(target=self.start_script_thread) # запуск в отдельном треде
            #self.thread2 = threading.Thread(target=self.start_updating_label) # запуск в отдельном треде !!баг
            self.thread.setDaemon(True)
            #self.thread2.setDaemon(True)
            self.thread.start()
            #self.thread2.start()
            self.button.configure(text='Stop script')
            self.entry.configure(state='disabled')
            print(f'the script is run periodically {self.period}\nThe test word: {self.prsl}')
            
        else:
            stop_thread_flag.set()
            self.thread.join()
            self.button.configure(text='Start script')
            self.entry.configure(state='normal')
            print('the script is stopped')
            stop_thread_flag.clear()
    
    def coord_but(self):
        button_to_stop = 'q' if not self.entry3.get() else self.entry3.get()
        self.coord(button_to_stop)
    
    def xy_but(self, button):
        if button == 1:
            self.xy1 = self.coord(key='q' if not self.entry3.get() else self.entry3.get())
            self.label6.configure(text=f'x={self.xy1[0]} y={self.xy1[1]}')
            
        elif button == 2:
            self.xy2 = self.coord(key='q' if not self.entry3.get() else self.entry3.get())
            self.label7.configure(text=f'x={self.xy2[0]} y={self.xy2[1]}')
            
    def coord(self, key='q'):
        while True:
            time.sleep(0.1)
            if keyboard.is_pressed(key):
                xy = pyautogui.position()
                print(f"The function is stopped by pressing a key {key}")
                print(xy)
                return xy


if __name__ == '__main__':
    app = App()
    app.mainloop()