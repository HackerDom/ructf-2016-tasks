from PIL import Image, ImageDraw
import sys
import binascii
import hashlib

#pictures on kotwizkiy.ru/ructf/ructf.zip

string = sys.argv[1]
hash_object = hashlib.md5(string.encode('utf-8'))
string = '0' + \
    bin(int(binascii.hexlify(
        bytes('RUCTF_' + hash_object.hexdigest()[:7], 'utf-8')), 16))[2:]

string.rjust(105,'0')

for i in range(1, 105):
    img = Image.open('image-' + str(i) + '.png')
    draw = ImageDraw.Draw(img)
    draw.point((13, 37),
               (int(string[i])*255, int(string[i])*255, int(string[i])*255))
    img.save('image-' + str(i) + '.png', 'PNG')
