import os, sys, glob, random, threading, time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import winsound

def asset(*parts):
    root = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(root, "assets", *parts)

class RansomSim:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("RANSOM")
        self.root.configure(bg="black")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self.quit())
        self.w, self.h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.frames = sorted(glob.glob(asset("intro_frames", "*.jpg")))
        self.jump_frames = sorted(glob.glob(asset("jumpscare_frames", "*.jpg")))
        self.photos = []
        self.popup_windows = []
        self.running = True
        self.started = time.time()
        self.files = [f"C:\\Users\\Admin\\{folder}\\{name}" for folder in
                      ["Documents","Pictures","Downloads","Desktop","Videos"]
                      for name in ["notes.txt","photo_001.jpg","gameclip.mp4","homework.docx","setup.exe"]]
        self.root.after(100, self.play_intro)
        self.root.mainloop()

    def sound(self, name):
        path = asset("audio", name + ".wav")
        if os.path.isfile(path):
            threading.Thread(target=lambda: winsound.PlaySound(path, winsound.SND_FILENAME), daemon=True).start()

    def show_frame(self, path):
        try:
            im = Image.open(path).convert("RGB")
            im.thumbnail((self.w, self.h), Image.Resampling.LANCZOS)
            bg = Image.new("RGB", (self.w, self.h), "black")
            bg.paste(im, ((self.w-im.width)//2, (self.h-im.height)//2))
            photo = ImageTk.PhotoImage(bg)
            self.canvas.delete("all")
            self.canvas.create_image(0,0,image=photo,anchor="nw")
            self.canvas.image = photo
        except Exception:
            pass

    def play_intro(self):
        if not self.running: return
        if not hasattr(self, "intro_i"): self.intro_i = 0
        if self.intro_i < len(self.frames):
            if self.intro_i == 0: self.sound("intro")
            self.show_frame(self.frames[self.intro_i])
            self.intro_i += 1
            self.root.after(125, self.play_intro)
        else:
            self.show_game()

    def show_game(self):
        self.canvas.delete("all")
        self.canvas.configure(bg="#100000")
        self.canvas.create_text(self.w//2, 55, text="R A N S O M", fill="#ff2222",
                                font=("Consolas", 34, "bold"))
        self.status = self.canvas.create_text(self.w//2, 115, text="YOUR FILES ARE BEING LOCKED",
                                fill="white", font=("Consolas", 19, "bold"))
        self.progress = self.canvas.create_rectangle(self.w*.2, 155, self.w*.2, 178,
                                fill="#ff2020", outline="")
        self.counter = self.canvas.create_text(self.w//2, 215, text="TIME REMAINING: 01:30",
                                fill="#ff5555", font=("Consolas", 25, "bold"))
        self.list_text = self.canvas.create_text(self.w//2, self.h//2,
            text="", fill="#b8ffb8", font=("Consolas", 15), justify="left")
        self.canvas.create_text(self.w//2, self.h-65,
            text="DEMO SIMULATION  •  FILES SHOWN ARE FICTIONAL  •  ESC TO EXIT",
            fill="#888888", font=("Consolas", 11))
        self.remaining = 90
        self.file_i = 0
        self.tick()
        self.teleport_loop()
        self.root.after(15000, self.jumpscare)

    def tick(self):
        if not self.running: return
        mins, secs = divmod(max(0,self.remaining),60)
        self.canvas.itemconfigure(self.counter, text=f"TIME REMAINING: {mins:02d}:{secs:02d}")
        x = self.w*.2 + (self.w*.6)*(90-self.remaining)/90
        self.canvas.coords(self.progress, self.w*.2,155,x,178)
        shown = self.files[:self.file_i]
        lines = "\n".join(("LOCKED  " + f.replace("\\\\","/") + ".locked") for f in shown[-12:])
        self.canvas.itemconfigure(self.list_text, text=lines or "Preparing file list...")
        self.file_i = min(len(self.files), self.file_i+2)
        if self.remaining > 0:
            self.remaining -= 1
            self.root.after(1000, self.tick)
        else:
            self.jumpscare()

    def teleport_loop(self):
        if not self.running: return
        self.spawn_popup()
        self.root.after(random.randint(450,950), self.teleport_loop)

    def spawn_popup(self):
        win = tk.Toplevel(self.root)
        win.overrideredirect(True)
        win.attributes("-topmost", True)
        ww, hh = random.randint(210,330), random.randint(110,180)
        x = random.randint(0,max(0,self.w-ww)); y=random.randint(0,max(0,self.h-hh))
        win.geometry(f"{ww}x{hh}+{x}+{y}")
        colors = [("#ff1744","#090909"),("#a000ff","#080008"),("#00ff9c","#00120c"),("#ff006e","#16000b")]
        fg,bg=random.choice(colors)
        c=tk.Canvas(win,bg=bg,highlightthickness=2,highlightbackground=fg)
        c.pack(fill="both",expand=True)
        c.create_text(ww//2,25,text="RANSOM",fill=fg,font=("Consolas",19,"bold"))
        c.create_text(ww//2,65,text=random.choice(["YOUR FILES ARE LOCKED","PAY ATTENTION","NO ESCAPE","SYSTEM COMPROMISED"]),
                      fill="white",font=("Consolas",10,"bold"))
        c.create_text(ww//2,hh-22,text="!!!  " + random.choice(["0xA91F","0xFF02","ERROR 404","LOCKED"]) + "  !!!",
                      fill=fg,font=("Consolas",10))
        self.popup_windows.append(win)
        def move():
            if not self.running or not win.winfo_exists(): return
            nx=random.randint(0,max(0,self.w-ww)); ny=random.randint(0,max(0,self.h-hh))
            win.geometry(f"{ww}x{hh}+{nx}+{ny}")
            win.after(random.randint(350,850), move)
        win.after(250,move)
        win.after(random.randint(1800,3800),win.destroy)

    def jumpscare(self):
        if not self.running or getattr(self,"jumping",False): return
        self.jumping=True
        self.sound("jumpscare")
        for win in self.popup_windows:
            try: win.destroy()
            except: pass
        self.popup_windows=[]
        self.jump_i=0
        self.play_jump_frame()

    def play_jump_frame(self):
        if not self.running: return
        if self.jump_i < len(self.jump_frames):
            self.show_frame(self.jump_frames[self.jump_i])
            self.jump_i += 1
            self.root.after(125,self.play_jump_frame)
        else:
            self.canvas.delete("all")
            self.canvas.configure(bg="black")
            self.canvas.create_text(self.w//2,self.h//2,text="R A N S O M",fill="#ff1111",
                                    font=("Consolas",58,"bold"))
            self.canvas.create_text(self.w//2,self.h//2+90,text="SIMULATION COMPLETE  •  PRESS ESC TO EXIT",
                                    fill="white",font=("Consolas",16))
    def quit(self):
        self.running=False
        try: winsound.PlaySound(None,winsound.SND_PURGE)
        except: pass
        self.root.destroy()

if __name__ == "__main__":
    RansomSim()
