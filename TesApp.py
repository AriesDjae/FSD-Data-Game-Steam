import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import numpy as np

# Membaca dataset
data = pd.read_csv('steam_cleaned.csv')

# Fungsi untuk mengkonversi USD ke IDR
def usd_to_idr(usd):
    if pd.isna(usd):
        return np.nan
    return usd * 16000  # Asumsi 1 USD = 16.000 IDR

# Mengkonversi harga ke IDR
data['Price_IDR'] = data['Price'].apply(usd_to_idr)

# 1. Distribusi harga game (dalam Rupiah)
plt.figure(figsize=(12, 6))
sns.histplot(data['Price_IDR'].dropna(), bins=30, kde=True)
plt.title('Distribusi Harga Game (dalam Rupiah)', fontsize=16)
plt.xlabel('Harga (IDR)', fontsize=12)
plt.ylabel('Jumlah', fontsize=12)
plt.ticklabel_format(style='plain', axis='x')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Hubungan antara harga dan jumlah ulasan (dalam Rupiah)
plt.figure(figsize=(12, 6))
plt.scatter(data['Price_IDR'], data['Review_no'])
plt.title('Hubungan antara Harga (IDR) dan Jumlah Ulasan', fontsize=16)
plt.xlabel('Harga (IDR)', fontsize=12)
plt.ylabel('Jumlah Ulasan', fontsize=12)
plt.ticklabel_format(style='plain', axis='x')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 3. Jenis ulasan berdasarkan persentase (diperbaiki)
review_counts = data['Review_type'].value_counts()
plt.figure(figsize=(12, 6))
sns.barplot(x=review_counts.index, y=review_counts.values, palette='viridis')
plt.title('Distribusi Jenis Ulasan', fontsize=16)
plt.xlabel('Jenis Ulasan', fontsize=12)
plt.ylabel('Jumlah', fontsize=12)
plt.xticks(rotation=45, ha='right')
for i, v in enumerate(review_counts.values):
    plt.text(i, v, str(v), ha='center', va='bottom')
plt.tight_layout()
plt.show()

# 4. Game paling populer berdasarkan jumlah ulasan
top_games = data.nlargest(10, 'Review_no')
plt.figure(figsize=(12, 6))
plt.bar(top_games['Name'], top_games['Review_no'])
plt.title('10 Game Terpopuler Berdasarkan Jumlah Ulasan', fontsize=16)
plt.xlabel('Nama Game', fontsize=12)
plt.ylabel('Jumlah Ulasan', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.ticklabel_format(style='plain', axis='y')
for i, v in enumerate(top_games['Review_no']):
    plt.text(i, v, f'{v:,}', ha='center', va='bottom', fontsize=10)
plt.tight_layout()
plt.show()

# 5. Distribusi tag game (diperbaiki)
all_tags = ' '.join(data['Tags'].dropna().astype(str))
tags = [tag.strip() for tag in all_tags.split(',')]
tag_counts = pd.Series(tags).value_counts().nlargest(20)

plt.figure(figsize=(12, 8))
bars = plt.barh(tag_counts.index, tag_counts.values, color=plt.cm.viridis(np.linspace(0, 1, 20)))
plt.title('20 Tag Game Terpopuler', fontsize=16)
plt.xlabel('Jumlah', fontsize=12)
plt.ylabel('Tag', fontsize=12)

# Menambahkan label jumlah pada setiap bar
for i, bar in enumerate(bars):
    width = bar.get_width()
    plt.text(width, bar.get_y() + bar.get_height()/2, f'{width:,}', 
             ha='left', va='center', fontweight='bold')

plt.gca().invert_yaxis()  # Membalik urutan tag agar yang terpopuler ada di atas
plt.tight_layout()
plt.show()

# Tambahan: Word Cloud yang lebih jelas
wordcloud = WordCloud(width=1200, height=800, background_color='white', 
                      min_font_size=10).generate(all_tags)
plt.figure(figsize=(12, 8), facecolor=None)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Distribusi Tag Game (Word Cloud)', fontsize=16)
plt.tight_layout(pad=0)
plt.show()
