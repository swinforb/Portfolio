##########################################
# Author: Ben Swinford
# Date: 5/26/21
# Program: Assn3
##########################################

import sys

vocab = []
features = []
features2 = []
lineRate = []
lineRate2 = []
whatWord = []
whatWord2 = []


# Open training file and create a list called vocab
# vocab list is sorted alphebitcally and has no duplicates
with open(sys.argv[1], 'r') as training_file:
	currWord = []
	fail = 0
	lineCount = 0
	for line in training_file:
		word = list(line)
		for x in range(len(word)):
			if word[x] == " ":
				chToStr = ''.join(currWord)
				for y in range(len(vocab)):
					if chToStr == vocab[y]:
						fail = 1
				if fail == 0:
					vocab.append(chToStr)
				currWord = []
				fail = 0
			elif ord('a') <= ord(word[x].lower()) <= ord('z'):
				currWord.append(word[x].lower())

	vocab.sort()
	del vocab[0]


# Open training file and create a list of features for each review
with open(sys.argv[1], 'r') as training_file:
	currWord = []
	for line in training_file:
		strF = ''
		currLine = []
		currFeatures = []
		currGlobalWord = []
		word = list(line)
		for a in range(len(word)):
			if word[a] == " ":
				chToStr = ''.join(currWord)
				currLine.append(chToStr)
				currWord = []
				fail = 0
			elif ord('a') <= ord(word[a].lower()) <= ord('z'):
				currWord.append(word[a].lower())
			elif word[a] == '1' and word[a+2] == "\r" and word[a+3] =="\n" or word[a] == '0' and word[a+2] == "\r" and word[a+3] =="\n":
				lineRate.append(int(word[a]))
		isIn = 0
		for b in range(len(vocab)):
			for c in range(len(currLine)):
				if currLine[c] == vocab[b]:
					isIn = 1
			currFeatures.append(isIn)
			currGlobalWord.append(b)
			isIn = 0
		features.append(currFeatures)
		whatWord.append(currGlobalWord)


# Open test file and create a list of features for each review
# Added number 2 to features for words not found in the vocab
with open(sys.argv[2], 'r') as training_file:
	currWord = []
	for line in training_file:
		currLine = []
		currFeatures = []
		currGlobalWord = []
		word = list(line)
		for a in range(len(word)):
			if word[a] == " ":
				chToStr = ''.join(currWord)
				currLine.append(chToStr)
				currWord = []
				fail = 0
			elif ord('a') <= ord(word[a].lower()) <= ord('z'):
				currWord.append(word[a].lower())
			elif word[a] == '1' and word[a+2] == "\r" and word[a+3] == "\n" or word[a] == '0' and word[a+2] == "\r" and word[a+3] == "\n":
				lineRate2.append(int(word[a]))
		isIn = 0
		for b in range(len(vocab)):
			weGood = 0
			for c in range(len(currLine)):
				if currLine[c] == vocab[b]:
					isIn = 1
				else:
					weGood = weGood + 1
			currFeatures.append(isIn)
			currGlobalWord.append(b)
			isIn = 0
		features2.append(currFeatures)
		whatWord2.append(currGlobalWord)
 


		
def testing_phase():
	review = []
	trReview = []
	lineTrue = 0
	lineFalse = 0
	wordGood = []
	wordBad = []

	# Initialize 2 lists to count the number of times a word is present in a pos or neg review
	for k in vocab:
		wordGood.append(0)
		wordBad.append(0)

	# Determine how many positive and negative reviews there are
	for x in range(len(lineRate)):
		if lineRate[x] == 1:
			lineTrue = lineTrue + 1
		else:
			lineFalse = lineFalse + 1

	# Cycle through each word of each review, setting the likelihood of a word being in a pos or neg review
	# This is done using the training file
	for z in range(len(lineRate)):
		for y in range(len(features[z])):
			# the amount of times the word is present in a positive sentence
			if features[z][y] == 1 and lineRate[z] == 1:
				for u in range(len(vocab)):
					if whatWord[z][y] == u:
						wordGood[u] = wordGood[u] + 1
			# the amount of times the word is present in a negative sentence
			elif features[z][y] == 1 and lineRate[z] == 0:
				for r in range(len(vocab)):
					if whatWord[z][y] == r:
						wordBad[r] = wordBad[r] + 1

	# Cycle through each word of each review, performing some computations to determine the likelihood that the review is pos or neg
	# This is done using the test file
	for i in range(len(lineRate2)):
		pos = float(lineTrue)
		neg = float(lineFalse)
		for j in range(len(features2[i])):
			# This is where the computation of likelihood happens
			if features2[i][j] == 1:
				# pos is the current total (starting at the amount of pos / neg reviews)
				# whatWord2[i][j] is the index that points to the location in vocab (vocab and wordGood/Bad correspond w/ each other) 
				# wordGood/Bad[whatWord2[i][j]] is the total amount of times the word is present in a pos / neg review
				# lineTrue/False is the constant total amount of pos/neg reviews
				pos = (float(pos) * float((float(wordGood[whatWord2[i][j]]) / float(lineTrue))))
				neg = (float(neg) * float((float(wordBad[whatWord2[i][j]]) / float(lineFalse))))
		if pos > neg:
			review.append(1)
		else:
			review.append(0)

	# Compares the computed answers to the correct answers for correctness
	correct = 0
	falsee = 0
	for count in range(len(review)):
		if review[count] == lineRate2[count]:
			correct = correct + 1
		else:
			falsee = falsee + 1
	percent = float((float(correct) / (float(correct) + float(falsee))))
	print("\nFor Test\n")
	print("correct, incorrect, percent")
	print(correct, falsee, percent)
	results = open(sys.argv[5], 'w')
	results.write("For Test Case: \ncorrect, incorrect, percent\n")
	ans = [correct, falsee, percent]
	ans = str(ans)
	results.write(ans)


	# Cycle through each word of each review, performing some computations to determine the likelihood that the review is pos or neg
	# This is done using the test file
	for i in range(len(lineRate)):
		pos = float(lineTrue)
		neg = float(lineFalse)
		for j in range(len(features[i])):
			# This is where the computation of likelihood happens
			if features[i][j] == 1:
				# pos is the current total (starting at the amount of pos / neg reviews)
				# whatWord2[i][j] is the index that points to the location in vocab (vocab and wordGood/Bad correspond w/ each other) 
				# wordGood/Bad[whatWord2[i][j]] is the total amount of times the word is present in a pos / neg review
				# lineTrue/False is the constant total amount of pos/neg reviews
				pos = (float(pos) * float((float(wordGood[whatWord[i][j]]) / float(lineTrue))))
				neg = (float(neg) * float((float(wordBad[whatWord[i][j]]) / float(lineFalse))))
		if pos > neg:
			trReview.append(1)
		else:
			trReview.append(0)

	# Compares the computed answers to the correct answers for correctness
	correct = 0
	falsee = 0
	for count in range(len(trReview)):
		if trReview[count] == lineRate[count]:
			correct = correct + 1
		else:
			falsee = falsee + 1
	percent = float((float(correct) / (float(correct) + float(falsee))))
	print("\n\nFor Training\n")
	print("correct, incorrect, percent")
	print(correct, falsee, percent)
	print(" ")

	results.write("\n\nFor Training Case: \ncorrect, incorrect, percent\n")
	ans = [correct, falsee, percent]
	ans = str(ans)
	results.write(ans)
	results.close()




def main():

	# Outputs for me to see
	for i in range(len(vocab)):
		if features[0][i] == 1:
			print("'" + vocab[i] + "'")
	print(lineRate)
	print(len(lineRate))
	for j in range(len(vocab)):
		if features2[0][j] == 1:
			print("'" + vocab[j] + "'")
	print(lineRate2)

	# Convert vocab into a str to send to file
	strVocab = ''
	for x in range(len(vocab)):
		strVocab = strVocab + str(vocab[x])
		strVocab = strVocab + ', '
	strVocab = strVocab + 'classlabel'
	output_file = open(sys.argv[3], 'w')

	# Send vocab and features to file (TRAINING)
	output_file.write(strVocab)
	for y in range(len(features)):
		strFeatures = ''
		for z in range(len(features[y])):
			strFeatures = strFeatures + str(features[y][z]) + ','
		output_file.write(strFeatures)
		output_file.write("\n")
	output_file.close()

	# Send vocab and features to file (TEST)
	output_file2 = open(sys.argv[4], 'w')
	output_file2.write(strVocab)
	for i in range(len(features2)):
		strFeatures2 = ''
		for j in range(len(features2[i])):
			strFeatures2 = strFeatures2 + str(features2[i][j]) + ','
		output_file2.write(strFeatures2)
		output_file2.write("\n")
	output_file2.close()

	testing_phase()


if __name__ == '__main__':
	main()

