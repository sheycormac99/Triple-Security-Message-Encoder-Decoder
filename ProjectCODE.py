import onetimepad
import string
import math
from PIL import Image
all_letters = string.ascii_letters

def Subencrypt(plain_txt,key):
    dict1 = {}
    for i in range(len(all_letters)):
        dict1[all_letters[i]] = all_letters[(i + key) % len(all_letters)]

    cipher_txt = []
    # loop to generate ciphertext
    for char in plain_txt:
        if char in all_letters:
            temp = dict1[char]
            cipher_txt.append(temp)
        else:
            temp = char
            cipher_txt.append(temp)

    cipher_txt = "".join(cipher_txt)
    return cipher_txt

def Subdecrypt(cipher_txt,key):
    dict2 = {}
    for i in range(len(all_letters)):
        dict2[all_letters[i]] = all_letters[(i - key) % (len(all_letters))]

    # loop to recover plain text
    decrypt_txt = []
    for char in cipher_txt:
        if char in all_letters:
            temp = dict2[char]
            decrypt_txt.append(temp)
        else:
            temp = char
            decrypt_txt.append(temp)

    decrypt_txt = "".join(decrypt_txt)
    return decrypt_txt

def transEncrypt(text,key):
    cipher = ""
    # track key indices
    k_indx = 0

    text_len = float(len(text))
    text_lst = list(text)
    key_lst = sorted(list(key))
    # calculate column of the matrix
    col = len(key)

    # calculate maximum row of the matrix
    row = int(math.ceil(text_len / col))
    # add the padding character '_' in empty
    # the empty cell of the matix
    fill_null = int((row * col) - text_len)
    text_lst.extend('_' * fill_null)

    # create Matrix and insert message and
    # padding characters row-wise
    matrix = [text_lst[i: i + col]
              for i in range(0, len(text_lst), col)]

    # read matrix column-wise using key
    for _ in range(col):
        curr_idx = key.index(key_lst[k_indx])
        cipher += ''.join([row[curr_idx]
                           for row in matrix])
        k_indx += 1
    return cipher

def transDecrypt(cipher,key):
    txt = ""
    # track key indices
    k_indx = 0

    # track text txt indices
    txt_indx = 0
    txt_len = float(len(cipher))
    txt_lst = list(cipher)

    # calculate column of the matrix
    col = len(key)

    # calculate maximum row of the matrix
    row = int(math.ceil(txt_len / col))

    # convert key into list and sort
    # alphabetically so we can access
    # each character by its alphabetical position.
    key_lst = sorted(list(key))

    # create an empty matrix to
    # store deciphered message
    dec_cipher = []
    for _ in range(row):
        dec_cipher += [[None] * col]

    # Arrange the matrix column wise according
    # to permutation order by adding into new matrix
    for _ in range(col):
        curr_idx = key.index(key_lst[k_indx])

        for j in range(row):
            dec_cipher[j][curr_idx] = txt_lst[txt_indx]
            txt_indx += 1
        k_indx += 1
    # convert decrypted msg matrix into a string
    try:
        txt = ''.join(sum(dec_cipher, []))
    except TypeError:
        raise TypeError("This program cannot",
                        "handle repeating words.")

    null_count = txt.count('_')
    if null_count > 0:
        return txt[: -null_count]

    return txt


def encrpyt(text,k1,k2,k3):
    cipher1= Subencrypt(text,k1)
    cipher2= transEncrypt(cipher1,k2)
    cipher3= onetimepad.encrypt(cipher2,k3)
    return cipher3

def decrypt(text,k1,k2,k3):
    cipher3 = onetimepad.decrypt(text,k3)
    cipher2 = transDecrypt(cipher3,k2)
    cipher1= Subdecrypt(cipher2,k1)
    return cipher1

def genData(data):
    # list of binary codes
    # of given data
    newd = []

    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd


# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):

        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]

        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1

            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if (pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
                # pix[j] -= 1

        # Eighth pixel of every set tells
        # whether to stop ot read further.
        # 0 means keep reading; 1 means thec
        # message is over.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if (pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1

        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):

        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1


# Encode data into image
def encodeImg(data):
    img = input("Enter image name(with extension) : ")
    image = Image.open(img)

    newimg = image.copy()
    encode_enc(newimg, data)
    new_img_name = input("Enter the name of new image(with extension) : ")
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

# Decode the data in the image
def decodeImg():
    img = input("Enter image name(with extension) : ")
    image = Image.open(img, 'r')

    data = ''
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                  imgdata.__next__()[:3] +
                  imgdata.__next__()[:3]]

        # string of binary data
        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data

print("Welcome To TriPLe SeCuriTy IMAGE EnCODER-DeCODER.")
choice='Y'
while (choice=='Y' or choice == 'y'):
    a = int(input(":: Welcome to Steganography :: \nChoose:\n"
                  "1. Encode\n2. Decode\n"))
    if (a == 1):
        plain_txt = input("Enter text to Encrypt :")
        print("Enter Three Keys for Encryption as followed:")
        key1 = int(input("Enter Key for Substitution Cipher(Input Shift Value):"))
        key2 = input("Enter Key for Transposition Cipher(Input String Value):")
        key3 = input("Enter Key for OneTimePad Cipher(Input String Value):")
        code = encrpyt(plain_txt, key1, key2, key3)
        print("The Encoded Message :" + code)
        ch = input("Do You Want to DeCode the message to Check? Press Y or N:")
        if (ch == 'Y' or ch == 'y'):
            decode = decrypt(code, key1, key2, key3)
            print("The Decoded Message :" + decode)
        encodeImg(code)
        print("Code has been Encrypted in the Provided Image.")
        choice=input("DO YOU WISH TO CONTINUE?")
    elif (a == 2):
        stegoImage = decodeImg()
        print("Enter Three Keys for Decryption as followed:")
        key1 = int(input("Enter Key for Substitution Cipher(Input Shift Value):"))
        key2 = input("Enter Key for Transposition Cipher(Input String Value):")
        key3 = input("Enter Key for OneTimePad Cipher(Input String Value):")
        decode = decrypt(stegoImage, key1, key2, key3)
        print("The Decoded Message :"+decode)
        choice = input("DO YOU WISH TO CONTINUE?\n")
    else:
        raise Exception("Enter Correct Input")

print("THANK YOU FOR USING TriPLe-SeCuriTy EnCODER-DeCODER.")
