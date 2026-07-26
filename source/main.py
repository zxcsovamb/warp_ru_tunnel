import subprocess
import sys
import os
import requests
import tkinter as tk
from tkinter import messagebox
import time


#анимации 
from animation import ConsoleAnimation
download_anim = ConsoleAnimation(style="download", delay=0.05, clear_line=True, bar_length=30)
connect_check = ConsoleAnimation(style="2", delay=0.2, clear_line=True)
def logo_animated(text, delay=0.005):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def add_host(domain):
    subprocess.run(["warp-cli", "tunnel", "host", "add", domain], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    

def main():
    
    logo = """██    ██▒  ██▒       ██████▒   ████████▒  ██    ██▒
██    ██▒  ██▒      ██    ██▒        ██▒  ██    ██▒
██    ██▒  ██▒      ██    ██▒      ██▒    ██    ██▒
 ██  ██▒   ██▒      ██    ██▒    ██▒      ██    ██▒
  ████▒    ████████▒ ██████▒   ████████▒   ██████▒"""

    logo_animated(logo, delay=0.002)
    time.sleep(0.5)
    os.system('cls' if os.name == 'nt' else 'clear')
    try:
        connect_check("Проверка доступа к гитхабу", requests.get, "https://raw.githubusercontent.com/", timeout=1)
        print("Подключение есть")
        lines = requests.get("https://raw.githubusercontent.com/zxcsovamb/warp_ru_tunnel/refs/heads/main/domains.txt").text.splitlines()
    except:
        error = messagebox.showerror("Ошибка", "Подключение отсутствует. Пожалуйста, проверьте подключение к интернету.")
        sys.exit(1)

    try:
        output = subprocess.check_output("warp-cli.exe tunnel host list", shell=True, text=True)
        line_count = len(output.splitlines())
        if line_count != 1:
            delite = messagebox.askyesno("Вопрос","У вас установленны кастомные домены из-за которых установка может быть не удачной. Удаляем?")
            if delite:
                reset = subprocess.run(["warp-cli.exe","tunnel" ,"host", "reset"], shell=True, text=True)
                os.system('cls' if os.name == 'nt' else 'clear')
                output = subprocess.check_output("warp-cli.exe tunnel host list", shell=True, text=True)
                line_count = len(output.splitlines())
                if line_count == 1:
                    messagebox.showinfo("Успешно!","Успешно удалено")
                    
                else:
                    messagebox.showerror("Ошибка","Не удалось удалить домены")
            else:
                None
    except:
        None
    hosts = set()
    for line in lines:
        d = line.strip().lower()
        if d:
            hosts.add(d)
            hosts.add(f"www.{d}")

    hosts = sorted(list(hosts))
    try:
        download_anim.process_iterable("Добавление в WARP:", hosts, add_host)
    except Exception as e:
        print(f"Ошибка при добавлении доменов: {e}")
    messagebox.showinfo("Успешно!","Домены установились успешно")
if __name__ == "__main__":
    main()
