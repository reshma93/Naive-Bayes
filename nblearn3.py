import re
import json
import sys
import operator

path =sys.argv[1]
tagged_data_file = open(path)
tagged_data = tagged_data_file.read().splitlines()
model = dict()
prior_probs=dict()
total=0
each_class = dict()
word_freq = dict()
for x,val in enumerate(tagged_data):
	total=total+1
	line = val.split()
	
	class_1 = line[1]
	class_2 = line[2]
	if class_1 in prior_probs:
		prior_probs[class_1]=prior_probs[class_1]+1
	else:
		prior_probs[class_1]=1
		
	if class_2 in prior_probs:
		prior_probs[class_2]=prior_probs[class_2]+1
	else:
		prior_probs[class_2]=1
		
	new_list = line[3:]
	new_list = re.findall(r"[\w']+|[.,!?;():]", " ".join(new_list))
	
	length = len(new_list)
	if class_1 in each_class:
		each_class[class_1]=each_class[class_1]+length
	else:
		each_class[class_1]=length
	
	if class_2 in each_class:
		each_class[class_2]=each_class[class_2]+length
	else:
		each_class[class_2]=length
	
	for y, word in enumerate(new_list):	
		word = word.lower()
		if word in model:
			if class_1 in model[word]:
				model[word][class_1]=model[word][class_1]+1
			else:
				model[word][class_1]= 1
				
			if class_2 in model[word]:
				model[word][class_2]=model[word][class_2]+1
			else:
				model[word][class_2]= 1				
		else:
			model[word]= dict()
			model[word][class_1]=1
			model[word][class_2]=1
		
		if word in word_freq:
			word_freq[word]=word_freq[word]+1
		else:
			word_freq[word]=1

sorted_x = sorted(word_freq.items(), key=operator.itemgetter(1))
sorted_x.reverse()
sorted_x = sorted_x[:15]
#print(sorted_x)			
			
for class_type in prior_probs:
		prior_probs[class_type]=prior_probs[class_type]/total

for word in model:
	for class_name in prior_probs:
		if class_name in model[word]:
			model[word][class_name]=model[word][class_name]+1
		else:
			model[word][class_name]=1
		each_class[class_name]=each_class[class_name]+1

for word in model:
	for class_name in model[word]:
		model[word][class_name]=model[word][class_name]/each_class[class_name]
		
together= dict()
together['model']= model
together['prior_probs']= prior_probs			
together['high_freq']=sorted_x

with open('nbmodel.txt','w') as fp:
	json.dump(together,fp)
tagged_data_file.close()
fp.close()