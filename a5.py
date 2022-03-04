from tkinter import messagebox, filedialog, Button, Entry, Tk, Label, Frame
import re

r1 = []
r2 = []
r3 = []


def initialize_registers(session_key):
    global r1, r2, r3

    r1 = list(session_key[0:20])
    r1 = [int(x) for x in r1]

    r2 = list(session_key[20:42])
    r2 = [int(x) for x in r2]

    r3 = list(session_key[42:65])
    r3 = [int(x) for x in r3]


def get_gamma_stream(length):
    global r1, r2, r3
    gamma = []

    i = 0
    while i < length:

        f = F(r1[-9], r2[-11], r3[-11])
        gamma.insert(i, r1[0] ^ r2[0] ^ r3[0])

        if r1[-9] == f:
            r1 = iterate_r1(r1)
        if r2[-11] == f:
            r2 = iterate_r2(r2)
        if r3[-11] == f:
            r3 = iterate_r3(r3)

        i = i + 1

    return gamma


def F(x, y, z):
    return (x & y) | (x & z) | (y & z)


def iterate_r1(line):
    eighteenth = line[0]
    line = left_shift(line)
    line[-1] = ((eighteenth ^ line[0]) ^ line[1]) ^ line[4]

    return line


def iterate_r2(line):
    twenty_first = line[0]
    line = left_shift(line)
    line[-1] = twenty_first ^ line[0]

    return line


def iterate_r3(line):
    twenty_second = line[0]
    line = left_shift(line)
    line[-1] = ((twenty_second ^ line[0]) ^ line[1]) ^ line[-8]

    return line


def left_shift(line):
    for b in range(0, len(line) - 1):
        line[b] = line[b + 1]

    line[-1] = 0

    return line


def text_to_binary(text):
    s = ""
    for i in text:
        binary = str(' '.join(format(ord(x), 'b') for x in i))
        j = len(binary)

        while j < 8:
            binary = "0" + binary
            j = j + 1

        s = s + binary

    return s


def binary_to_text(binary):
    s = ""
    length = len(binary) - 8
    i = 0
    while i <= length:
        s = s + chr(int(binary[i:i + 8], 2))
        i = i + 8
    return str(s)


def encrypt(text, session_key):
    initialize_registers(session_key)

    s = ""
    binary = text_to_binary(text)
    binary_text = list([int(x) for x in binary])
    gamma = get_gamma_stream(len(binary_text))

    for text_bit, gamma_bit in zip(binary_text, gamma):
        s = s + str(text_bit ^ gamma_bit)

    return binary_to_text(s)


def decrypt(cipher, session_key):
    initialize_registers(session_key)

    s = ""
    binary_cipher = list([int(x) for x in cipher])
    gamma = get_gamma_stream(len(cipher))

    for cipher_bit, gamma_bit in zip(binary_cipher, gamma):
        s = s + str(cipher_bit ^ gamma_bit)

    return binary_to_text(str(s))


def open_encrypted_file():
    key = key_entry.get()
    if len(key) == 64 and re.match("^([01])+", key):
        file = filedialog.askopenfile()
        text = file.read()
        result = open("result.txt", "w")
        result.write(encrypt(text, key))
        messagebox.showinfo("Info", "File encrypted! Result in: result.txt")
    else:
        messagebox.showerror("Error", "Nice try, try again!")


def open_decrypted_file():
    key = key_entry.get()
    if len(key) == 64 and re.match("^([01])+", key):
        file = filedialog.askopenfile()
        text = file.read()
        result = open("result.txt", "w")
        result.write(decrypt(text_to_binary(text), key))
        messagebox.showinfo("Info", "File decrypted! Result in: result.txt")
    else:
        messagebox.showerror("Error", "Nice try, try again!")


# Ключ шифрования (64 bit key) ОБЯЗАТЕЛЬНО должен состоять только из нулей и единиц.
# Размер ключа должен быть обязательно равен 64 символам - ни больше, ни меньше.

# interface
root = Tk()
root.title("A5 cipher")
root.resizable("false", "false")

frame_labels = Frame(root, relief="ridge")
key_label = Label(frame_labels, text="64 bit key: ")
key_entry = Entry(frame_labels, width=65)
frame_labels.pack()
key_label.grid(row=0, column=0)
key_entry.grid(row=0, column=1)

frame_buttons = Frame(root, relief="ridge")
encrypt_button = Button(frame_buttons, text="Encrypt", command=open_encrypted_file)
decrypt_button = Button(frame_buttons, text="Decrypt", command=open_decrypted_file)
frame_buttons.pack()
encrypt_button.grid(row=0, column=0)
decrypt_button.grid(row=0, column=1)

root.mainloop()
