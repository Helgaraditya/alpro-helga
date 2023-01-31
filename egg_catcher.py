#itertools untuk menggilir beberapa warna
from itertools import cycle 

#membuat telur muncul di tempat acak 
from random import randrange 

#menganimasikan game di layar
from tkinter import Canvas, Tk, messagebox, font 

#menyesuaikan ukuran Canvas Tk
canvas_width = 1366
canvas_height = 768

#menciptakan jendela Tk
root = Tk() 

#membuat judul Tk
root.title("Egg Catcher - TUBES ALPRO")

#membuat warna kanvas biru langit
c = Canvas(root, width=canvas_width, height=canvas_height, background="#B0D6F5")
c.create_rectangle(-5, canvas_height-150, canvas_width+5, \
    canvas_height+5, fill="#70FF66", width=0)
c.create_oval(-80, -80, 150, 150, fill='yellow', width=0)

#menggambar jendela utama dan semua isi
c.pack()

#menggunakan berbagai jenis warna telur 
color_cycle = cycle(["white", "red", "purple", "brown", "orange"])

#pergerakan telur dan warna penangkap telur(catcher)
egg_width = 45
egg_height = 55
egg_score = 10
egg_speed = 500
egg_interval = 4000
difficulty = 0.95
catcher_color = "blue"
catcher_width = 100
catcher_height = 100
catcher_startx = canvas_width / 2 - catcher_width / 2
catcher_starty = canvas_height - catcher_height - 20
catcher_startx2 = catcher_startx + catcher_width
catcher_starty2 = catcher_starty + catcher_height

#menggambar penangkap telur
catcher = c.create_arc(catcher_startx, catcher_starty, catcher_startx2, \
    catcher_starty2, start=200, extent=140, style="arc", outline=catcher_color, width=3)

#membuat gaya dan ukuran font
game_font = font.nametofont("TkFixedFont")
game_font.config(size=18)

#skor game
score = 0
score_text = c.create_text(10, 10, anchor="nw", font=game_font, \
    fill="darkblue", text="Score: "+ str(score))

#nyawa untuk bermain game 
lives_remaining = 3
lives_text = c.create_text(canvas_width-10, 10, anchor="ne", \
    font=game_font, fill="darkblue", text="Lives: "+ str(lives_remaining))

#daftar melacak telur 
eggs = []

#fungsi posisi acak untuk telur 
def create_egg():
    x = randrange(10, 740)
    y = 40
    new_egg = c.create_oval(x, y, x+egg_width, y+egg_height, \
        fill=next(color_cycle), width=0)
    eggs.append(new_egg)
    root.after(egg_interval, create_egg)

#fungsi untuk menggerakkan telur 
def move_eggs():
    for egg in eggs:
        (eggx, eggy, eggx2, eggy2) = c.coords(egg) #koordinat setiap telur
        c.move(egg, 0, 10) #telur jatuh kebawah
        if eggy2 > canvas_height:
            egg_dropped(egg)
    root.after(egg_speed, move_eggs)

#fungsi menghapus telur setelah jatuh
def egg_dropped(egg):
    eggs.remove(egg) #menghapus telur 
    c.delete(egg) #telur menghilang dari canvas
    lose_a_life()
    if lives_remaining == 0:
        messagebox.showinfo("Game Over!", "Final Score: "+ str(score))
        root.destroy() #permainan berakhir 

#melibatkan pengurangan nyawa dari variabel
def lose_a_life():
    global lives_remaining
    lives_remaining -= 1
    c.itemconfigure(lives_text, text="Lives: "+ str(lives_remaining))

#fungsi Telur ditangkap jika berada di dalam busur penangkap
def check_catch():
    (catcherx, catchery, catcherx2, catchery2) = c.coords(catcher) #koordinat penangkap
    for egg in eggs:
        (eggx, eggy, eggx2, eggy2) = c.coords(egg) #koordinat telur
        if catcherx < eggx and eggx2 < catcherx2 \
            and catchery2 - eggy2 < 40: #telur dalam horizontal / vertikal 
            eggs.remove(egg)
            c.delete(egg)
            increase_score(egg_score) #menambah score 
    root.after(100, check_catch)

#meningkatkan score 
def increase_score(points):
    global score, egg_speed, egg_interval
    score += points #tambahkan score player
    egg_speed = int(egg_speed * difficulty)
    egg_interval = int(egg_interval * difficulty)
    c.itemconfigure(score_text, text="Score: "+ str(score)) #memperbarui teks untuk score 

# fungsi mengatur kontrol untuk menangkap telur 
def move_left(event): #fungsi kontrol ke kiri
    (x1, y1, x2, y2) = c.coords(catcher)
    if x1 > 0:
        c.move(catcher, -20, 0)

def move_right(event): #fungsi kontrol kekanan
    (x1, y1, x2, y2) = c.coords(catcher)
    if x2 < canvas_width:
        c.move(catcher, 20, 0)

#memanggil fungsi saat tombol ditekan 
c.bind("<Left>", move_left)
c.bind("<Right>", move_right)
c.focus_set()

# 3 putaran permainan dimulai setelah jeda 1 detik
root.after(1000, create_egg)
root.after(1000, move_eggs)
root.after(1000, check_catch)

#memulai jendela utama setelah program dibuat
root.mainloop()

