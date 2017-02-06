import sys
import re
import string
import math
train_text = sys.argv[1]
train_label = sys.argv[2]

with open(train_text, 'r') as fin:
    text = fin.read()

with open(train_label, 'r') as fin:
    label_text = fin.read()   


reviews=text.strip().split('\n')

label_rows = label_text.split('\n')

review_dict={} #Dict with key = unique identifier and Value = array of words of rest of review
label_isPositive_dict={} #key = unique identifier and Value = if that review is +ve or not
label_isGenuine_dict={} #key = unique identifier and Value = if that review is genuine or not
words_dict={} #key = each word and Value = array of +ve and -ve count
unique_list=[] #list of all unique identifiers

stop_words={'hotel','stay','i','it','chicago','day','ourselves', 'hers', 'between', 'yourself', 'but', 'the','again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than','1','2','3','4','5','6','7','8','9','0'}

positiveCount=0.0
negativeCount=0.0
positiveTokens = 0.0
negativeTokens=0.0
truthfulTokens = 0.0
deceptiveTokens = 0.0
prior_positive=0.0
prior_negative=0.0
truthfulCount=0.0
deceptiveCount=0.0
prior_truthful=0.0
prior_deceptive=0.0

no_of_words = 0

for indi_review in reviews:
	for ch in ['&','#','(',')','!','-','\t',';','.','?',',',';','"','\'','*','\\',r'/',':',"/"]:
     	 if ch in indi_review:
         	indi_review=indi_review.replace(ch," ")
	review_words = indi_review.split()
	review_dict.setdefault(review_words[0], [])
	unique_list.append(review_words[0])
	for each_word in review_words[1:]:
		if each_word not in stop_words:
			review_dict[review_words[0]].append(each_word.lower())

for indi_label_row in label_rows:
	label_row_split = indi_label_row.split();
	if label_row_split:
		label_isPositive_dict[label_row_split[0]] = label_row_split[2].strip()
		label_isGenuine_dict[label_row_split[0]]=label_row_split[1].strip()


for each in unique_list:
	if label_isPositive_dict[each] == "positive":
		isPositive = True
		positiveCount+=1
	else: 
		isPositive = False
		negativeCount+=1
		
	if label_isGenuine_dict[each] == "truthful":
		isGenuine = True
		truthfulCount+=1
	else:
		isGenuine = False
		deceptiveCount+=1
		
	for indi_words in review_dict[each]:
		if not (indi_words in words_dict):
			words_dict[indi_words] = [0,0,0,0]
			no_of_words+=1
	for indi_words in review_dict[each]:
		if isPositive:
			words_dict[indi_words][0]+=1 
			positiveTokens+=1
		else:
			words_dict[indi_words][1]+=1
			negativeTokens+=1
		if isGenuine:
			words_dict[indi_words][2]+=1
			truthfulTokens+=1
		else:
			words_dict[indi_words][3]+=1
			deceptiveTokens+=1

totalCount=positiveCount+negativeCount
totalGenuineCount = truthfulCount+deceptiveCount
prior_positive = positiveCount/totalCount
prior_negative = negativeCount/totalCount
prior_truthful = truthfulCount/totalGenuineCount
prior_deceptive = deceptiveCount/totalGenuineCount

target = open("nbmodel.txt", 'w')
target.write( "** Note: This file contains the Feature count, the probabilities before smoothing and the probabilities after smoothing. **") 

printVariable = "\nPrior Positive = " + str(prior_positive)
target.write( printVariable) 
printVariable = "\nPrior Negative = " + str(prior_negative)
target.write( printVariable) 
printVariable = "\nPrior Truthful = " + str(prior_truthful)
target.write( printVariable) 
printVariable = "\nPrior Deceptive = " + str(prior_deceptive)
target.write( printVariable) 


target.write("\n\nFeature Count\n")
target.write("Feature".ljust(30, ' ') + "Positive".ljust(30, ' ') + "Negative".ljust(30, ' ')+ "Truthful".ljust(30, ' ')+ "Deceptive\n")
for k, v in words_dict.items():
	    printVariable= k.ljust(30, ' ')+ str(v[0]).ljust(30, ' ')+str(v[1]).ljust(30, ' ')+str(v[2]).ljust(30, ' ')+str(v[3])+"\n"
	    target.write(printVariable)

target.write("\n\n\n")

target.write("Before Smoothing\n")
target.write("Feature".ljust(30, ' ') + "Positive".ljust(30, ' ') + "Negative".ljust(30, ' ')+ "Truthful".ljust(30, ' ')+ "Deceptive\n")

for k, v in words_dict.items():
	    printVariable = k.ljust(30, ' ') + str(v[0]/positiveTokens).ljust(30, ' ')+str(v[1]/negativeTokens).ljust(30, ' ')+str(v[2]/truthfulTokens).ljust(30, ' ')+str(v[3]/deceptiveTokens)+"\n"
	    target.write(printVariable)

target.write("\n\n\n")
target.write("After Smoothing (Values in logs) \n")
target.write("Feature".ljust(30, ' ') + "Positive".ljust(30, ' ') + "Negative".ljust(30, ' ')+ "Truthful".ljust(30, ' ')+ "Deceptive\n")
for k, v in words_dict.items():
	   printVariable=k.ljust(30, ' ')+ str(math.log((v[0]+1)/(positiveTokens+no_of_words))).ljust(30, ' ')+str(math.log((v[1]+1)/(negativeTokens+no_of_words))).ljust(30, ' ')+str(math.log((v[2]+1)/(truthfulTokens+no_of_words))).ljust(30, ' ')+str(math.log((v[3]+1)/(deceptiveTokens+no_of_words)))+"\n"
	   target.write(printVariable)



    
