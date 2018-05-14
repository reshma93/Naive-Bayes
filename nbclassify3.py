import json
import re
import math
import sys

path =sys.argv[1]
with open('nbmodel.txt', 'r') as fp:
	complete_dict = json.load(fp)

f= open("nboutput.txt","w+",encoding='utf8')	
	
prior_probs = complete_dict['prior_probs']
model = complete_dict['model']
high_freq_list = complete_dict['high_freq']
#print(high_freq_list)
high_freq = [i[0] for i in high_freq_list]

data_file = open(path, encoding = "utf8")
raw_data = data_file.read().splitlines()
probs = dict()
for sentence in raw_data:	
	sent = re.findall(r"[\w']+|[.,!?;():]", sentence)
	new_sent= sent[1:]
	unique_code= sent[0]
	
	probs['Neg']=0
	probs['Pos']=0
	probs['True']=0
	probs['Fake']=0
	for word in new_sent:
		word = word.lower()
		if word in model:
			if word not in high_freq:
				for class_prob in model[word]:
					if class_prob in probs:
						probs[class_prob]=probs[class_prob]+math.log(model[word][class_prob])
					else:
						probs[class_prob]=math.log(model[word][class_prob])
		for class_prob in probs:
			probs[class_prob]=probs[class_prob]+math.log(prior_probs[class_prob])
	if probs["Fake"] > probs["True"]:
		class_1 = "Fake"
	else: 
		class_1 = "True"
	if probs["Neg"] > probs["Pos"]:
		class_2 = "Neg"
	else:	
		class_2 = "Pos"
		
	string_to_write = unique_code+" "+class_1+" "+class_2+"\n"	
	f.write(string_to_write)
f.close()	