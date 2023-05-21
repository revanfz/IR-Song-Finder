# Import Library

import pandas as pd
import numpy as np

from tkinter import *
from sklearn.metrics.pairwise import cosine_similarity

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

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_v = TfidfVectorizer()
vektor_lirik = tfidf_v.fit_transform(kumpulan_lirik)

target = StringVar()

# Fungsi mencari lagu
def searchSong(query):
   query = target.strip.lower()
   query_vector = tfidf_v.transform[query]
   cos_sim = cosine_similarity(query_vector, vektor_lirik)
   sorted_index = np.ragsort(cos_sim)[0][::1]
   hasil = sorted_index[0]
   hasil = df[hasil]
   return hasil

def search():
   choosen = searchSong()


# Penerimaan Inputan Kueri dari User

query = input("Masukkan lirik lagu yang akan dicari : ")

# Preprocessing Kueri

query = query.strip().lower()

# Menghitung nilai Cosine Similarity

def search_song(query, vektor):
  # Vektorisasi kueri
  query_vector = tfidf_v.transform([query])
  # Mengembalikan nilai cosine similarity
  return cosine_similarity(query_vector, vektor)

cos_sim = search_song(query, vektor_lirik)

sorted_index = np.argsort(cos_sim)[0][::-1]
index_relevan = []

for i in sorted_index:
    # Memfilter hasil dokumen yang memiliki nilai cosine similarity > 0
    if cos_sim[0][i] > 0:
      index_relevan.append([i, cos_sim[0][i]])

# Menampilkan urutan nilai Cosine Similarity Dokumen Relevan (Descending) 
for i in index_relevan:
    print("Dokumen {} memiliki cosine similarity sebesar {:.2f}".format(i[0], i[1]))

# Jumlah Dokumen relevan yang dihasilkan Sistem
print(f"Dokumen relevan yang dihasilkan sistem yakni : {len(index_relevan)} ")

# Inisialisasi Variabel untuk menampung dokumen relevan

hasil = []

# Menyimpan hasil dokumen relevan pada variabel

for i in index_relevan:
    x = df.iloc[i[0]]['judul']
    y = df.iloc[i[0]]['artis']
    z = df.iloc[i[0]]['lirik']
    hasil.append([x, y, z])

hasil = pd.DataFrame(hasil)
hasil.columns = ["Judul", "Artis", "Lirik"]

hasil

# Penghitungan Mean Reciprocal Rank (MRR) sebagai evaluasi sistem

# def compute_mrr(rankings, query):
#     reciprocal_ranks = []
#     count = 0
#     for idx in rankings.index:
#       reciprocal_ranks.append(1/(count+1))
#       if query in rankings["Lirik"][idx]:
#           break
#       count += 1
#     print(reciprocal_ranks)
#     print(f"Dokumen yang cocok dengan pencarian anda berada pada dokumen: {count}")
#     return sum(reciprocal_ranks)/len(reciprocal_ranks)

# hasil_mrr =  compute_mrr(hasil, query);

# print(f"Hasil MRR sistem terhadap kueri {query} adalah : {hasil_mrr}")