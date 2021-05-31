import numpy as np

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SYMMETRIC CIPHERS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def caesar(text, step=3, encrypt=True) :
    """
    Performs caesar cipher
    
    Parameters :
    text : String ==> text to be ciphered or deciphered
    step : integer (default=3) ==> step to be taken e.g. 3, 4, 5 etc
    encrypt : Bool (default=True) ==> True to encrypt, False to decrypt
    """
    assert step > 0 , "Step must be a natural number"
    
    lst = [chr(ord(x)+step) for x in text] if encrypt else [chr(ord(x)-step) for x in text]
    return "".join(lst)


def vernam(text, key, encrypt=True) :
    """
    Performs vernam cipher
    
    Parameters :
    text : String ==> text to be ciphered or deciphered
    key : String ==> key to be used ()
    encrypt : Bool (default=True) ==> True to encrypt, False to decrypt
    """
    assert len(text) > len(key), "Length of key cannot be greater than length of text"
    
    mod_key = key * (len(text)//len(key)) + key[:(len(text)%len(key))]
    if encrypt :
        return "".join([chr(ord(x)+ord(y)) for x, y in zip(text, mod_key)])
    else :
        return "".join([chr(ord(x)-ord(y)) for x, y in zip(text, mod_key)])



def transposition(text, key=None, encrypt=True) :
    """
    Performs Transposition cipher
    
    Parameters :
    text : String ==> text to be ciphered or deciphered
    key: String (default=None) ==> key for the column transposition cipher method. Format - each column number separated by colon, ':'. If key is provided, column cipher is performed, else keyless cipher is performed
    encrypt : Bool (default=True) ==> True to encrypt, False to decrypt
    """
    
    length = len(text)

    if key is not None:
        key = [int(i)-1 for i in key.split(":")]
        
    if encrypt :
        if key :
            col = len(key)
            assert col < length, "Length of key must be less than length of text"
            
            text += " "*(col - length%col)  # adding blank spaces after the text to complete the text matrix
            return "".join([text[i::col] for i in key])
        else :
            return text[1::2] + text[::2]
    
    else :
        if key :
            cols = len(key)
            assert cols < length, "Length of key must be less than length of text"
            rows = length//cols + (length%cols != 0)
            
            string = ""
            for r in range(rows) :
                # since we have blank spaces in the end, so the matrix is complete and each row has same number of characters in it
                string += ''.join([text[key.index(i)*rows + r] for i in range(cols)])
            return string.strip()  #stripping the blank spaces

        else :
            p1, p2 = text[:length//2], text[length//2:]
            string = ""
            for idx, val in enumerate(p1) :
                string += p2[idx] + val
                
            if length%2 != 0:
                string += p2[-1]
            
            return string


def hill_cipher(text, key=None, decrypt=False) :
    '''
    Performs hill cipher algorithm using a 2x2 key matrix or a 4 letter key
    INPUT --> text : text to be encrypted or decrypted
                key : key for performing encryption or decryption. If left None, a random key of 4 letters is generated
                    MANDATORY TO PROVIDE KEY FOR DECRYPTION
                decrypt : True when performing encryption
    OUTPUT --> a dictionary of format {'cipher' : ciphered_text, 'key' : key_used} when performing encryption
                a string of deciphered text when performing decryption
    '''
    if decrypt :
        key = list(key)
    
    else :
        if key is None :
            key = [chr(np.random.randint(0+97, 25+97)) for _ in range(4)] #making a 2x2 matrix with random characters
        else :
            key = list(key)
        
    key_matrix = np.array([ord(i)-97 for i in key]).reshape((2,2))

    if decrypt :
        det = np.rint(np.linalg.det(key_matrix) % 26)
        i = 1
        #finding Multiplicative inverse of det(key_matrix)  finding x for which det(key)*x = 26*y + 1
        while True :
            if (det * i)%26 == 1 :
                det = i
                break
            i += 1

        adj = np.array([ [key_matrix[1,1], -key_matrix[0,1]] , [-key_matrix[1,0], key_matrix[0,0]] ]) % 26

        key_matrix = (det * adj)%26

    flag = 0
    l = len(text)

    if l%2 != 0 :
        text = text + 'x'      #adding an arbitarary character, here 'x', at the end if length of string is odd
        flag = 1
    
    ascii = np.array([ord(i)-97 for i in text.lower()]).reshape((len(text), 1))  #getting ASCII characters - 97 

    cipher = ''
    for i in range(len(text)//2) :
        ch = np.dot(key_matrix, ascii[i*2 : i*2 + 2]) % 26
        cipher += chr(int(ch[0][0])+97) + chr(int(ch[1][0])+97)

    cipher = cipher[:-1] if flag == 1 else cipher

    return cipher if decrypt else {'key': ''.join(key), 'cipher' : cipher} 

