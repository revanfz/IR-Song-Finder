# Import Library

import pandas as pd
import numpy as np
from tkinter import messagebox
from tkinter import *
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Import Dataset

df = pd.read_csv("https://raw.githubusercontent.com/revanfz/revanfz/main/dataset_lirik.csv", encoding="utf-8")
''' 
Preprocessing text
    Casefolding : merubah semua huruf menjadi lowecase (huruf kecil)
'''
df["lirik"] = df["lirik"].replace(r'\n', ' ', regex=True).str.casefold()
df

kumpulan_lirik = df["lirik"].tolist()

# Vektorisasi dataset menggunakan TF-IDF

tfidf_v = TfidfVectorizer()
vektor_lirik = tfidf_v.fit_transform(kumpulan_lirik)

window = Tk()
input_text = StringVar()
window.geometry("480x480")
window.title("Song Finder")

homepage = Frame(window)

homepage.grid(row=0, column=0, sticky='news')

# Fungsi mencari lagu

def cari_lagu():
    global input_text
    query = input_text.get().lower()
    if query == "":
        messagebox.showerror("Error", "Input some lyrics!")
    else:
        query_vektor = tfidf_v.transform([query])
        cos_sim = cosine_similarity(query_vektor, vektor_lirik)
        sorted_index = np.argsort(cos_sim)[0][::-1]
        index_relevan = []
        for i in sorted_index:
        # Memfilter hasil dokumen yang memiliki nilai cosine similarity > 0
            if cos_sim[0][i] > 0:
                index_relevan.append([i, cos_sim[0][i]])
                
        for i in index_relevan:
            print("Dokumen {} memiliki cosine similarity sebesar {:.2f}".format(i[0], i[1]))
        print(f"Dokumen relevan yang dihasilkan sistem yakni : {len(index_relevan)} \n")

        lagu = []
        for i in index_relevan:
            x = df.iloc[i[0]]['judul']
            y = df.iloc[i[0]]['artis']
            z = df.iloc[i[0]]['lirik']
            lagu.append([x, y, z])

        # Jika lagu tidak ada pada dataset
        if len(lagu) == 0:
            messagebox.showinfo("Info", "It doens't exist!")
        else:
            hasil = Frame(window)
            hasil.grid(row=0, column=0, sticky='news')
            hasil.tkraise()
            Label(hasil, text="Lagu yang anda cari adalah: ",  font=("Times",20,"bold")).pack()
            Label(hasil, text=lagu[0][0]).pack()
            Button(hasil, text="search again", command=lambda:hasil.destroy()).pack()
            Button(hasil, text="close", command=lambda:window.destroy()).pack()

Label(homepage, text="Song Finder", bg="teal", fg="white", font=("Times",20,"bold")).pack(padx=100, pady=5)
Entry(homepage, text="Masukkan penggalan lirik",font=("Times",20,"bold"),  textvariable=input_text).pack(padx=100, pady=5)
Button(homepage, text="Cari", font=("Times",14,"bold"), command=lambda:cari_lagu()).pack(padx=100, pady=5)

homepage.tkraise()
window.mainloop()