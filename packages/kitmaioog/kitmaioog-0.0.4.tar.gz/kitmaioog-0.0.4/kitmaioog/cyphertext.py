list = []
class cyphertext :
    def __innit__(self) :
        pass
    def encode(self) :
        list = []
        text = input("Enter your text : ")
        for encode in text :
            list.append(ord(encode))
        for e in list :
            data = str(chr(e+1))
            print(data, end="")
    def decode(self) :
        list = []
        text = input("Enter your cyphertext : ")
        for decode in text :
            list.append(ord(decode))
        for n in list :
            data = str(chr(n-1))
            print(data, end="")