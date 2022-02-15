
import glob
from bs4 import BeautifulSoup
import nltk
from nltk import stem
import re

def preprocessing():
	freq = {}
	all_words = 0
	for filename in glob.glob('./data/nytimes/*.html'):
		with open(filename, encoding='utf-8') as f:
			html = f.read()
			html = re.sub('[,.’“”-]', '', html) # 記号の置き換え
			#html = re.sub('\d', '', html) # 数字の処理したらタグが破壊される?ようなので一旦保留
			soup = BeautifulSoup(html, 'html.parser')
			texts = soup.find_all("p", class_="evys1bk0")
			for text in texts:
				words = nltk.word_tokenize(text.text)	
				for word in words:
					all_words += 1
					word_ = stemmer.stem(word) # 語幹化 (精度は完璧ではない)
					if word_ in freq:
						freq[word_] += 1
					else:
						freq[word_] = 1
	return freq, all_words


if __name__ == '__main__':

	# nltk 関連の機能ダウンロード
	nltk.download('punkt')
	stemmer = stem.PorterStemmer()

	# 辞書の作成
	freq, all_words = preprocessing()
	freq = sorted(freq.items(), key=lambda x:x[1], reverse=True)
	
	counter = 0
	for i, tup in enumerate(freq):
		word, num = tup
		counter += num

		# 100語ごと, もしくは最後の単語通過時にカバー率を print
		if i%100 == 0 or i == len(freq)-1:
			print(i, counter, f'{counter/all_words*100:.3f}%')

		# matplotlib でグラフにする
		# 日本語と英語のどちらの方が語彙が多いか?
		
