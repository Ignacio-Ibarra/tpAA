import pandas as pd
import re
import string
import unicodedata
from collections import Counter
from collections import defaultdict



class CleaningData: 

	def __init__(self, data=None, path=None):

		if isinstance(data, pd.DataFrame): 
			self.data = data
		else: 
			print(f"Loading Properati Data from path...\n")
			self.data = pd.read_csv('./data/cabaventa.csv')
			print("Done!\n")


	def drop_columns(self, columns=None): 
		print("Cleaning columns with no valuable information...\n")
		self.data = self.data.drop(columns=columns)
		return self.data

	""" AUX FUNCTIONS"""

	def lowering(self, text): 
		return text.lower()


	def strip_accents(self, text):
		return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn') 


	def del_punct_wsp(self, text):
		text = text.replace(".","").replace('('," ").replace(")"," ")
		text = re.sub(r'[!"\#\$%\'\(\)\*\+,\-\./:;<=>\?@\[\\\]\^_`\{\|\}\~]',' ',text) #borra punct y agrega espacio
		#text = re.sub(r'\b\d+\b',' ', text) #removía digitos también
		return text

	def remove_digits(self, text):
		splitted = re.compile('\w+').findall(text)
		cleanned = []
		for word in splitted:
			evaluation = [1 if i.isdigit() else 0 for i in word]
			suma = reduce(lambda x,y: x+y, evaluation,0)
			if suma==0:
				cleanned.append(word)
			elif suma<2:
				cleanned.append(word)
			else: 
				word = ''.join([i for i in word if not i.isdigit()])
				cleanned.append(word)
		return " ".join(cleanned)    


	def strip_spaces(self,text): 
		return text.lstrip().rstrip()

	def remove_within_wsp(self,text):
		return " ".join(re.findall(r'\b\S+\b', text))

	def text_cleaning(self, text,
		lowering = True,
		punctuation=True,
		strip_accents=True,
		within_spaces=True,
		digits=True,
		strip_spaces=True):
		if isinstance(text, str): 
			if lowering:
				text = self.lowering(text)
		
			if punctuation:
				text = self.del_punct_wsp(text)
		
			if strip_accents:
				text = self.strip_accents(text)

			if within_spaces:
				text = self.remove_within_wsp(text)
			
			if digits:
				text = self.remove_digits(text)
		
			if strip_spaces:
				text = self.strip_spaces(text)

			if within_spaces:
				text = self.remove_within_wsp(text)  

			return text
		else: 
			return None


	def text_col_cleaning(self,
		text_column=None,
		params = {'lowering':True,
		'punctuation':True,
		'accents': True,
		'strip_spaces':True,
		'digits':False,'within_spaces':True}):

		self.data[text_column+"_cleaned"] = self.data[text_column].apply(lambda text: self.text_cleaning(text, 
																						lowering=params['lowering'],
																						punctuation=params['punctuation'],
																						strip_accents=params['accents'],
																						within_spaces=params['within_spaces'],
																						digits=params['digits'],
																						strip_spaces=params['strip_spaces']))
		return self.data


	def remove_sw_from_text(self, text, stopwords_list=None): 

		if isinstance(stopwords_list, list):
			wordlist = re.compile('\w+').findall(text)
			return " ".join([w for w in wordlist if w not in stopwords_list])
		else:
			return None 


	def remove_sw_from_col(self, text_column= None, stopwords={'list':None, 'threshold':None}):

		if stopwords['list']:
			stopwords_list = stopwords['list']  
			

		else:  
			"""Select stopwords from document collection"""
			all_text = " ".join(self.data[text_column])
			wordlist = re.compile('\w+').findall(all_text)
			counter = defaultdict(int)
			for word in wordlist:
			    counter[word] += 1

			if stopwords['threshold']: 
				threshold = stopwords['threshold']
			else:
				threshold = 100
			stopwords_list = [k for k,v in counter.items() if v>=threshold]

		if len(stopwords_list)>20: 
			print(len(stopwords_list),"\n",",".join(stopwords_list[:20]))
		else:
			print(stopwords_list)

		new_col = self.data[text_column].apply(lambda text: self.remove_sw_from_text(text, stopwords_list=stopwords_list))

		if isinstance(new_col, pd.Series): 
			self.data[text_column+"_no_sw"] = new_col
		
		return self.data
