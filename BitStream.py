'''

BitStream, author Michele Abruzzese, 22/08/2019
	
	This class provides a way to create a stream of pure boolean
	digits to be exported in files without the limitation of 8-bit
	chunks that standard python methods for file writing require.
	It's not optimized for performance but for ease of use by now.

	USAGE:
	
	{ bs = BitStream() } initializes an empty stream
	
	{ bs2 = BitStream(bs1) } makes a copy of another stream
	
	{ bs.put(symbol) } puts the exact representation of the symbol
	into the stream, any positive integer will be put with its
	minimal binary form (eg. bs.put(16) will put '10000'), lesser or
	bigger than 8 bit. You can use an integer or a list of binary
	(eg. [0, 1, 1, 1, 0, 1]) or a string of binary (eg. '011101') or
	a list of char (eg. ['0', '1', '1']) this method will ignore any
	char or digit different from 0 or 1. It works with direct binary
	or hexadecimal form of numbers.

	{ bs.putchar(char) } puts the 8 bit representation of the char
	into the stream. If char is a number puts the 8-bit (16, 24, 32...) 
	representation of it (eg. bs.putchar(3) puts '00000011', and 
	bs.putchar(256) puts '0000000100000000'). If char is a single char
	string it puts the ASCII representation of it and if the string is
	of multiple chars it puts each of them as ASCII binary. It works
	also with lists of char or int, and with binary or hexadecimal forms.

	{ bs.export() } renders the whole stream as a string, trailing zeroes
	if not aligned with 8-bit chunks. It can be used directly to write on
	files. Trailing zeroes will be added for each export, but the stream
	will continue without them, so be aware when exporting in different
	moments. It's best to export only once at the very end.

	{ bs.clear() } clears the stream deleting everything.

	{ print(bs), str(bs) } will render the stream in string of 0 and 1.
	You can use it to monitor the current state of the stream or to save
	a copy to reuse (eg. a = str(bs); bs.clear(); bs.putchar(a)). Contrary
	to export() it does not append trailing zeroes.

	{ bs.tostr() } is a commodity method that explicitly calls __str__ 

	{ bs3 = bs1 + bs2 } concatenates 2 or more streams into a new one

	{ bs2 = bs1 * 3 } repeats the stream N times
	
	{ bs1.concat(bs2) } append a stream at the end of another one


'''

class BitStream:
	def __init__(self, other=None):
		if other is not None:
			self.stream = list(other.stream)
			self.current = other.current
			self.position = other.position
		else:
			self.stream = []
			self.current = 0b00000000
			self.position = 7

	def put(self, symbol):
		if isinstance(symbol, str) or isinstance(symbol, list):
			for c in symbol:
				self.put(int(c))
			return
		if symbol in [0, 1]:
			self.current |= symbol << self.position
			self.position -= 1
			if (self.position < 0):
				self.position = 7
				self.stream.append(self.current)
				self.current = 0b00000000
		else:
			symbol = bin(symbol)[2:]
			for c in symbol:
				self.put(int(c))

	def putchar(self, char):
		if isinstance(char, str) or isinstance(char, list):
			if len(char) > 1:
				for c in char:
					self.putchar(c)
				return
			else:
				char = char[0]
		string = bin(char if isinstance(char, int) else ord(char))
		string = string[2:]
		while len(string) % 8 != 0:
			string = '0' + string
		for c in string:
			self.put(int(c))
			
	def export(self):
		string = ""
		for c in self.stream:
			string += chr(c)
		if self.position < 7:
			string += chr(self.current)
		return string

	def clear(self):
		self.position = 7
		self.current = 0b00000000
		self.stream = []

	def append(self, other):
		self.put(other.tostr())

	def tostr(self):
		return self.__str__()

	def __str__(self):
		string = ""
		for c in self.stream:
			binary = bin(c)[2:]
			while len(binary) < 8:
				binary = "0" + binary
			string += binary
		if self.position < 7:
			binary = bin(self.current)[2:]
			while len(binary) < 8:
				binary = "0" + binary
			string += binary if self.position == 0 else binary[:-(self.position+1)]
		return string

	def __add__(self, other):
		bs = BitStream()
		bs.put(self.tostr() + other.tostr())
		return bs

	def __mul__(self, num):
		bs = BitStream()
		string = self.tostr()
		for _ in range(num):
			bs.put(string)
		return bs
