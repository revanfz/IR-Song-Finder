# Import Library

import pandas as pd
import numpy as np
import nltk
# nltk.download('stopwords')

from tkinter import *
from tkinter import messagebox
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords


# Import Dataset

df = pd.read_csv(
    "https://raw.githubusercontent.com/revanfz/revanfz/main/dataset_lirik.csv", encoding="utf-8")
''' 
Preprocessing text
    Casefolding : merubah semua huruf menjadi lowecase (huruf kecil)
'''
df["lirik"] = df["lirik"].replace(r'\n', ' ', regex=True).str.casefold()
df

# Menghilangkan stopwords
id_stop_factory = stopwords.words('indonesian')
en_stop_factory = stopwords.words('english')

# Hilangkan stopwords langs == id
def remove_stop_word_id(text):
    clean_words = []
    text = text.split()
    for word in text:
        if word not in id_stop_factory:
            clean_words.append(word)
    return ' '.join(clean_words)

# Hilangkan stopwords langs == en
def remove_stop_word_en(text):
    clean_words = []
    text = text.split()
    for word in text:
        if word not in en_stop_factory:
            clean_words.append(word)
    return ' '.join(clean_words)

df["lirik"].apply(remove_stop_word_id)
df["lirik"].apply(remove_stop_word_en)

# Vektorisasi lirik
tfidf_v = TfidfVectorizer()
vektor_lirik = tfidf_v.fit_transform(df["lirik"].tolist())

# MEncari lagu
def cari_lagu(input_text, window):
    query = input_text.get().lower().split(' ')
    # Error jika kueri kosong
    if '' in query:
        messagebox.showerror("Error", "Lirik yang dimasukkan kosong!")
    else:
        clean_query = ""
        for i in query:
            if i not in id_stop_factory and i not in en_stop_factory:
                clean_query += i + " "
            else:
                pass

        clean_query = clean_query.strip()
            
        query_vektor = tfidf_v.transform([clean_query])
        cos_sim = cosine_similarity(query_vektor, vektor_lirik)
        sorted_index = np.argsort(cos_sim)[0][::-1]
        
        global index_relevan
        index_relevan = []
        for i in sorted_index:
        # Memfilter hasil dokumen yang memiliki nilai cosine similarity > 0
            if cos_sim[0][i] > 0:
                index_relevan.append([i, cos_sim[0][i]])
                
        for i in index_relevan:
            print("Dokumen {} memiliki cosine similarity sebesar {:.2f}".format(i[0], i[1]))
            
        print(f"Dokumen relevan yang dihasilkan sistem yakni : {len(index_relevan)} ")

        global lagu
        lagu = []
        for i in index_relevan:
            x = df.iloc[i[0]]['judul']
            y = df.iloc[i[0]]['artis']
            z = df.iloc[i[0]]['lirik']
            lagu.append([x, y, z])

        if len(lagu) > 0:
            target = lagu[0][0]
            hasil = Frame(window, bg="teal")
            hasil.grid(row=0, column=0, sticky="nsew")
            hasil.grid_rowconfigure(0, weight=1)
            hasil.grid_columnconfigure(0, weight=1)
            Label(hasil, fg="gold", bg="teal", text="Lagu yang anda cari adalah: ", font=("Times",20,"bold")).pack(pady=(40, 50))
            
            count = 1
            for i in lagu:
                if count == 2:
                    Label(hasil, bg="teal", text="atau mungkin: ").pack(pady=20, padx=70, anchor="center")
                Label(hasil, bg="teal", text=f"{count}. {i[0]}, oleh {i[1]}", font=("Helvetica", 10, "bold")).pack(padx=(150,20), anchor='w')
                count += 1

            Button(hasil, text="Search again", bg="lime", fg="#1d2021", font=("Times", 12, "bold"), command=lambda:hasil.destroy()).pack(pady=(40, 10), anchor="center")
            Button(hasil, text="Close", bg="red", font=("Times", 12), command=lambda:window.destroy()).pack(anchor="center")
        else:
            # Message box jika lagu tidak ditemukan
            messagebox.showinfo("Song Finder", "Lagu tidak ditemukan")

# Membuat GUI
window = Tk()
window.configure(bg="blue")
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

input_text = StringVar()
window.geometry("640x480")
window.title("Song Finder")

homepage = Frame(window, bg="teal")
homepage.grid(row=0, column=0, sticky='news')
Label(homepage, text="Song Finder", font=("Helvetica", 32, "bold"), bg="teal", fg="white").pack(pady=100)
input_field = Entry(homepage, text="Masukkan penggalan lirik", textvariable=input_text, font=("Helvetice",17), width=28)
input_field.pack()
Button(homepage, text="Cari", command=lambda:cari_lagu(input_text, window), width=15).pack(pady=20)

def click(*args):
    input_field.delete(0, 'end')

input_field.insert(0, 'Masukkan penggalan lirik')
input_field.pack(pady=10)
input_field.bind("<Button-1>", click)

homepage.tkraise()
window.mainloop()

# Evaluasi sistem terhadap query
dokumen_relevan_sebenarnya = {
    'kau tetap': [1, 7, 9], 
    'all the time': [0],
    'lost within the darkness': [4],
    "we're strolling down the boulevard": [6],
    'kau adalah hidupku' : [8]
}

avg_precision_list = {}

dokumen_relevan_sebenarnya_yang_dihasilkan = 0
dokumen_ke = 0
precision = 0
avg_precision = 0
sum_precision = 0

for i in index_relevan:
    dokumen_ke += 1
    if i[0] in dokumen_relevan_sebenarnya[input_text.get()]:
        dokumen_relevan_sebenarnya_yang_dihasilkan += 1
        sum_precision += dokumen_relevan_sebenarnya_yang_dihasilkan/dokumen_ke

if len(dokumen_relevan_sebenarnya[input_text.get()]) > 0:
    recall = dokumen_relevan_sebenarnya_yang_dihasilkan/len(dokumen_relevan_sebenarnya[input_text.get()])
    precision = dokumen_relevan_sebenarnya_yang_dihasilkan/len(index_relevan)
else:
    recall = 1
    precision = 1

avg_precision = sum_precision/len(dokumen_relevan_sebenarnya[input_text.get()])
avg_precision_list[input_text.get()] =  avg_precision

print(f"Kueri \"{input_text.get()}\" memiliki nilai:")
print(f"Recall: {int(recall*100)} %")
print(f"Precision: {int(precision*100)} %")
print(f"dan Average Precision: {int(avg_precision*100)} %")

mAP = sum(avg_precision_list.values())/len(avg_precision_list)
print(f"Nilai dari Mean Avrage Precision sistem adalah : {mAP}")

