from tkinter import *
import random
 
# ширина экрана
w = 800
# высота экрана
h = 600
# Размер сегмента змейки
seg_sz = 20
# Переменная отвечающая за состояние игры
in_game = True



# ////////////////////////////////
def create_block():
    """ Создает блок в случайной позиции на карте """
    global BLOCK
    posx = seg_sz * (random.randint(1, (w-seg_sz) / seg_sz))
    posy = seg_sz * (random.randint(1, (h-seg_sz) / seg_sz))
     
    # блок это кружочек красного цвета
    BLOCK = c.create_oval(posx, posy,
                          posx + seg_sz,
                          posy + seg_sz,
                          fill="red")

def main():
    global in_game
     
    if in_game:
        # Двигаем змейку
        s.move()
        # Определяем координаты головы
        head_coords = c.coords(s.segments[-1].instance)
        x1, y1, x2, y2 = head_coords
        # Столкновение с границами экрана
        if x1 < 0 or x2 > w or y1 < 0 or y2 > h:
            in_game = False
    
        # Поедание яблок 
        elif head_coords == c.coords(BLOCK):
            s.add_segment()
            c.delete(BLOCK)
            create_block()

        # Самоедство
        else:
            # Проходим по всем сегментам змеи
            for index in range(len(s.segments)-1):
                if c.coords(s.segments[index].instance) == head_coords:
                    in_game = False
        root.after(100, main)
    # Если не в игре выводим сообщение о проигрыше
    else:
        c.create_text(w/2, h/2,
                            text="GAME OVER!",
                            font="TimesNewRoman 25",
                            fill="#ff0000")
        c.bind("<Return>", nwgame)
# ////////////////////////////

# /////////////////////////////////////////////
# Segment snake
class Segment(object):
    def __init__(self, x, y):
        self.instance = c.create_rectangle(x, y, x+seg_sz, y+seg_sz, fill="#173B0B")
# //////////////////////////////////////////////
# Snake (class)
class Snake(object):
    def __init__(self, segments):
        self.segments = segments
        # список доступных направлений движения змейки
        self.mapping = {"Down": (0, 1), "Up": (0, -1), "Left": (-1, 0), "Right": (1, 0) }
        # изначально змейка двигается вправо
        self.vector = self.mapping["Right"]
     
    def move(self):
         """ Двигает змейку в заданном направлении """
          
         # перебираем все сегменты кроме первого
         for index in range(len(self.segments)-1):
              segment = self.segments[index].instance
              x1, y1, x2, y2 = c.coords(self.segments[index+1].instance)
              # задаем каждому сегменту позицию сегмента стоящего после него
              c.coords(segment, x1, y1, x2, y2)
          
         # получаем координаты сегмента перед "головой"
         x1, y1, x2, y2 = c.coords(self.segments[-2].instance)
          
         # помещаем "голову" в направлении указанном в векторе движения
         c.coords(self.segments[-1].instance,
                       x1 + self.vector[0]*seg_sz,
                       y1 + self.vector[1]*seg_sz,
                       x2 + self.vector[0]*seg_sz,
                       y2 + self.vector[1]*seg_sz)
     
    def change_direction(self, event):
        """ Изменяет направление движения змейки """
        # event передаст нам символ нажатой клавиши
        # и если эта клавиша в доступных направлениях 
        # изменяем направление
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]

    def add_segment(self):
        """ Добавляет сегмент змейке """

        # определяем последний сегмент
        last_seg = c.coords(self.segments[0].instance)
        # определяем координаты куда поставить следующий сегмент
        x = last_seg[2] - seg_sz
        y = last_seg[3] - seg_sz

        # добавляем змейке еще один сегмент в заданных координатах
        self.segments.insert(0, Segment(x, y))
# ///////////////////////////////////////////////////////

# ////////////////////////////////
def nwgame(event):
    global in_game, s
    # game state
    in_game = True
    # //delete snake & apple(all)
    c.delete(ALL)
    c.delete(Text)
    # //paint new snake
    # создаем набор сегментов
    segments = [Segment(seg_sz, seg_sz),
                Segment(seg_sz*2, seg_sz),
                Segment(seg_sz*3, seg_sz)]
    # собственно змейка
    s = Snake(segments)
    c.bind("<KeyPress>", s.change_direction)
    create_block()
    main()
    # Запускаем окно
    root.mainloop()
# ////////////////////////////////

# Создаем окно
root = Tk()
# Устанавливаем название окна
root.title("Snake_v2.0(Nikitka_Edition)")

# создаем экземпляр класса Canvas (его мы еще будем использовать) и заливаем все зеленым цветом
c = Canvas(root, width=w, height=h, bg="#9FF781")
c.grid()
# Наводим фокус на Canvas, чтобы мы могли ловить нажатия клавиш
c.focus_set()

# создаем набор сегментов
segments = [Segment(seg_sz, seg_sz),
            Segment(seg_sz*2, seg_sz),
            Segment(seg_sz*3, seg_sz)]
 
# собственно змейка
s = Snake(segments)

# KeyPress(action)
c.bind("<KeyPress>", s.change_direction)

create_block()
main()
# Запускаем окно
root.mainloop()