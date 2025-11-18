import csv
import time
import math

# Grace Cochran
# COS 226 Hw 5
# Creating, Analyzing, and Improving Hash Tables 

class DataItem:	# Takes a given movie's statistics and stores it in its own list to be used.
    def __init__(self, line):
        self.movie_name = line[0]
        self.genre = line[1]
        self.release_date = line[2]
        self.director = line[3]
        self.box_office_revenue = float(line[4][1:])
        self.rating = float(line[5])
        self.duration_minutes = int(line[6])
        self.production_company = line[7]
        self.quote = line[8]

class Node: # To be used for the linked list insertion method
	def __init__(self, data):
		self.data = data
		self.next = None

def hashFunct(stringData):
    # does some mathematics to make a hash key, supposedly with the use of prime numbers
	hashPrime = 5381
	for i in stringData:
		hashPrime = ((hashPrime << 5) + hashPrime) + ord(i)
	key = hashPrime
	return key

def linearInsert(table, index, data): # inserts data into a hash table through linear probing, returning the amount of collisions and empty spots filled once a place has been found for the data to be stored in the table. 
	placeFound = False
	collisions = 0
	emptySpots = 0

	while placeFound == False:
		if table[index] != None:
			collisions += 1
			if index + 1 >= len(table):
				index = 0
			else:
				index += 1
		else:
			table[index] = data
			placeFound = True
			emptySpots += 1

	return collisions, emptySpots

def linkInsert(table, index, node): # inserts data into a hash table through linked list insertion, adding to an index's linked list when a collision occurs, returning the amount of collisions afterwards.
	collisions = 0

	if table[index] != None:
		collisions += 1
		currNode = table[index]
		while currNode.next != None:
			collisions += 1
			currNode = currNode.next
		currNode.next = node
	else:
		table[index] = node

	return collisions

def linkWasteCheck(table):
	emptySpaces = 0
	for i in table:
		if i == None:
			emptySpaces += 1
	return emptySpaces

def nextPrime(num): # finds the next prime number greater than a given number
	primeFound = False
	nextNum = num

	while(primeFound == False):
		primeFound = True
		nextNum += 1
		for i in range(2, int(math.sqrt(nextNum)) + 1):
			if nextNum % i == 0:
				primeFound = False
				break
				
	return nextNum


def main():

	file = "MOCK_DATA.csv"
	counter = 0

	size = 0 # initializing the hash tables and setting parameters 
	loadFactor = 0.75
	titleColTotal = 0
	quoteColTotal = 0

	start = time.time()
	with open(file, "r", newline = "", encoding = "utf8") as csvfile:
		data = csv.reader(csvfile) # initializing and reading the csv file's data 

		for row in data: # determining an optimal size for the hash tables.
			size += 1
		size -= 1 
		size = size / loadFactor
		size = nextPrime(math.ceil(size))
	
	with open(file, "r", newline = "", encoding = "utf8") as csvfile:
		data = csv.reader(csvfile)

		hashTitleTable = [None] * size
		hashQuoteTable = [None] * size
		titleWasteTotal = size
		quoteWasteTotal = size

		for row in data:
			# print(row)
			if counter == 0:
				counter += 1
				continue
			movie = DataItem(row)

			titleKey = hashFunct(movie.movie_name) # getting the keys of the appropriate fields
			quoteKey = hashFunct(movie.quote)
			titleIndex = titleKey % len(hashTitleTable) # getting the indexes of the row's data
			quoteIndex = quoteKey % len(hashQuoteTable)

			# inserting the DataItems into the hash tables
			# titleCollisions, titleFilled = linearInsert(hashTitleTable, titleIndex, movie) 
			# quoteCollisions, quoteFilled = linearInsert(hashQuoteTable, quoteIndex, movie)
			titleCollisions = linkInsert(hashTitleTable, titleIndex, Node(movie)) 
			quoteCollisions = linkInsert(hashQuoteTable, quoteIndex, Node(movie))
	
			titleColTotal += titleCollisions # updating the total collisions and empty indexes
			quoteColTotal += quoteCollisions
			# titleWasteTotal -= titleFilled
			# quoteWasteTotal -= quoteFilled
			counter += 1
		titleWasteTotal = linkWasteCheck(hashTitleTable)
		quoteWasteTotal = linkWasteCheck(hashQuoteTable)
	
	end = time.time()
	print("Commit Four(4). Added a method to find an optimal size for the hash tables.\n")
	print(f"Hash table creation sucessful, went through loop {counter} times.")
	print(f"Construction of the hash tables took {end-start:0.2f} seconds.")
	print(f"The title-oriented hash table encountered {titleColTotal} collisions, while the quote-oriented hash table encountered {quoteColTotal} collisions.")
	print(f"The amount of wasted space from the title-oriented hash table was {titleWasteTotal} indexes, while the quote-oriented hash table wasted {quoteWasteTotal} indexes.")


if __name__ == "__main__":
    main()