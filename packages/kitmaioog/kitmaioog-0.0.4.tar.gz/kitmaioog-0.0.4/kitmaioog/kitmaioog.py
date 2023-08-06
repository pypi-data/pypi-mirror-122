from kitmaioog.kitmaioog import cyphertext

use = cyphertext()

print("-" * 20, "Secret", "-" * 20)
print("1.Encode")
print("2.Decode")
print("-" * 48)
menu = input("Select Menu : ")

if menu == "1" :
    use.encode()
elif menu == "2" :
    use.decode()
