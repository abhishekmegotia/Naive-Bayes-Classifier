import sys
import re
import string
import math

prior_positive=0
prior_negative=0
prior_truthful=0
prior_deceptive=0

testing_data = sys.argv[1]

with open(testing_data, 'r') as fin:
    text = fin.read()

reviews=text.strip().split('\n')

review_dict={} #Dict with key = unique identifier and Value = array of words of rest of review
words_dict={} #key = each word and Value = array of +ve and -ve count
unique_list=[] #list of all unique identifiers
stop_words={'hotel','stay','i','it','chicago','day','ourselves', 'hers', 'between', 'yourself', 'but','the', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than','1','2','3','4','5','6','7','8','9','0'}


for indi_review in reviews:
	for ch in ['&','#','(',')','!','-','\t',';','.','?',',',';','"','\'','*','\\','\/',':',"/"]:
     	 if ch in indi_review:
         	indi_review=indi_review.replace(ch," ")
	review_words = indi_review.split()
	review_dict.setdefault(review_words[0], [])
	unique_list.append(review_words[0])
	for each_word in review_words[1:]:
		if each_word not in stop_words:
			review_dict[review_words[0]].append(each_word.lower())


model = ""
with open("nbmodel.txt", 'r') as fin:
    for line in fin:
        if 'Prior Positive' in line:                
                prior_positive = line.split("=")[1].split("\n")[0]
        if 'Prior Negative' in line:                
                prior_negative = line.split("=")[1].split("\n")[0]
        if 'Prior Truthful' in line:                
                prior_truthful = line.split("=")[1].split("\n")[0]
        if 'Prior Deceptive' in line:                
                prior_deceptive = line.split("=")[1]

with open("nbmodel.txt", 'r') as fin:
    model = fin.read()
        	
model = model.split("After Smoothing")[1]
model = model.split("Deceptive")[1].strip().split("\n")
for each_line in model:
	    words = each_line.split()
	    words_dict[words[0]] = [words[1],words[2],words[3],words[4]]

target = open("nboutput.txt", 'w')

for each_item in unique_list:
	positive_probability=math.log(float(prior_positive))
	negative_probability=math.log(float(prior_negative))
	truthful_probability=math.log(float(prior_truthful))
	deceptive_probability=math.log(float(prior_deceptive))

	for each_word in review_dict[each_item]:
		if not (each_word in words_dict):
			continue
		positive_probability+= float(words_dict[each_word][0])
		negative_probability+=  float(words_dict[each_word][1])
		truthful_probability+=  float(words_dict[each_word][2])
		deceptive_probability+=  float(words_dict[each_word][3])

	if truthful_probability>deceptive_probability:
		print_variable = each_item + " truthful"
		target.write(print_variable)
	else:
		print_variable = each_item + " deceptive"
		target.write(print_variable)

	if positive_probability>negative_probability:
		print_variable = " positive\n"
		target.write(print_variable)
	else:
		print_variable =" negative\n"
		target.write(print_variable)

	
			



        