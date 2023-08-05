#coding:gbk
import os
try:
    import keyboard
except:
    os.system("pip install keyboard")
import ME

def key_user_message():
    ME.user_message()

def key_Poli():
    ME.run_Poli()

def key_dow():
    ME.dow()

def key_quit():
    return exit()

def key_new_user():
    ME.new_user()

def key_open_files():
    ME.open_files()
def main():
    message = "快捷键窗口>"
    print(message)
    keyboard.add_hotkey('ctrl+u', key_user_message)
    keyboard.add_hotkey('ctrl+p', key_Poli)
    keyboard.add_hotkey('ctrl+d', key_dow)
    keyboard.add_hotkey('ctrl+n', key_new_user)
    keyboard.add_hotkey('ctrl+q', key_quit)
    keyboard.add_hotkey('ctrl+f', key_open_files)
    keyboard.wait()
    return message
if __name__ == '__main__':
    main()
