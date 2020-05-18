# coding=utf-8

try:
    import Image
except ImportError:
    from PIL import Image
import urllib
import pytesseract


con = urllib.urlopen("http://pmo.ultrapower.com.cn/ucas/user/auth/generator.htm")
jpg = open("code.jpg", "wb")
jpg.write(con.read())
jpg.close()
con.close()

print(pytesseract.image_to_string(Image.open(r"code.jpg")))