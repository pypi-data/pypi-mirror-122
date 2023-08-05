def binToDec(binary):
	decimal = 0
	power = 0
	while binary > 0:
		decimal += 2 ** power * (binary % 10) 
		binary //= 10	
		power += 1
	return decimal
	
def decToBin(decimal):
	binary = 0
	power = 0
	while decimal > 0:
		binary += 10 ** power * (decimal % 2)
		decimal //= 2
		power += 1
	return binary