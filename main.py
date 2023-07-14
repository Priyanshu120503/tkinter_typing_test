import tkinter as tk
import util
import random
from tkinter import messagebox


FONT = ('Lucida Sans Unicode', 20, 'normal')
ENTRY_FONT = ('Lucida Sans Unicode', 15, 'normal')


def countdown(time_left):
    if time_left == 0:
        time_up()
    timer.set(time_left)
    window.after(1000, countdown, time_left-1)


def time_up():
    text_entry.config(state=tk.DISABLED)
    messagebox.showinfo(title="Result", message=f"Correctly typed words: {correct}\nTotal words typed: {words_entered}")
    if messagebox.askyesno(title="Retry?", message="Wanna retry?"):
        timer.set(60)
        text_entry.config(state=tk.NORMAL)
    else:
        window.destroy()


def handle_type(e):
    global correct, words_entered
    if timer.get() == 60:
        countdown(60)
    text_box.config(state=tk.NORMAL)

    if e.char == ' ':
        if words_in_label.get(text.get()[:-1]):
            correct += 1
            text_box.tag_config(text.get()[:-1], foreground='#4872fa', background="white")
        else:
            text_box.tag_config(words[words_entered], foreground='#fa4848', background="white")

        text.set("")
        words_entered += 1
        text_box.yview(words_in_label[words[words_entered]][1])

    word_detail = words_in_label[words[words_entered]]
    text_box.tag_config(word_detail[0], background='#48fa7e')
    text_box.config(state=tk.DISABLED)


def init_words():
    random.shuffle(list_of_thousand_words)

    char_count = 0
    for word in list_of_thousand_words[:500]:
        words.append(word.lower())
        words_in_label[word.lower()] = [word.lower(), f"1.{char_count}", f"1.{char_count + len(word)}"]
        char_count += len(word) + 2


def init_textbox():
    text_box.config(state=tk.NORMAL)
    text_box.insert(tk.END, "  ".join(words))

    for word in list(words_in_label.values()):
        text_box.tag_add(word[0], word[1], word[2])

    text_box.tag_config(words[0], background="#48fa7e")
    text_box.config(state=tk.DISABLED)


# -------------------------------------------
correct = 0
words_entered = 0
words_in_label = {}
words = []

list_of_thousand_words = util.words

init_words()

# -------------------------------------------
window = tk.Tk()

window.geometry("600x300")
window.wm_title("Typing Speed Test")

frame = tk.Frame(window, width=600, height=600)

timer = tk.IntVar()
timer.set(60)
timer_label = tk.Label(frame, text='Time Remaining: ', font=('Arial', 14, 'normal'))
time_label = tk.Label(frame, textvariable=timer, font=('Arial', 14, 'normal'))


text_box = tk.Text(frame, width=21, height=3.3, bg="white", font=FONT, borderwidth=2, relief='solid',
                     padx=16, pady=10, state=tk.DISABLED, wrap=tk.WORD)
init_textbox()

text = tk.StringVar()
text.set("")
text_entry = tk.Entry(frame, textvariable=text, font=ENTRY_FONT, width=30, justify='center')
text_entry.bind('<KeyRelease>', handle_type)


timer_label.place(x=100, y=10)
time_label.place(x=250, y=10)
text_box.place(x=100, y=60)
text_entry.place(x=100, y=200)
frame.pack()

window.mainloop()
