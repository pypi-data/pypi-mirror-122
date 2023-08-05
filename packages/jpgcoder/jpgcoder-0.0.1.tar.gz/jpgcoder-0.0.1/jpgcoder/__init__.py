import os

# HIDE TEXT 
def encode(file, text):
    with open(file, 'ab') as f:
        f.write(bytes(text, 'utf-8'))


# READ TEXT
def decode(file):
    with open(file, 'rb') as f:
        content = f.read()
        offset = content.index(bytes.fromhex('FFD9'))
        f.seek(offset + 2)

        try:
            os.system('cls')
        except:
            os.system('clear')
            
        print(f.read())