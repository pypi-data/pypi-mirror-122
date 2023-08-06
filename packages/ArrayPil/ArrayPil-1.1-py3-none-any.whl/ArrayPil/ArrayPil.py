from PIL import Image
import numpy as np


class ArrayPil(object):
	def ConvImgArray(self, imgdir, conv='RGB'):
		self.im1 = np.asarray(Image.open(imgdir).convert(conv))
		return self.im1
	def ImgSave(self, imgarray, dirsave, conv='RGB'):
	   	self.im2 = Image.fromarray(imgarray, conv)
	   	self.im2.save(dirsave)
	def ConvPilArray(self, imgpil, conv='RGB'):
		self.im3 = np.asarray(imgpil.convert(conv))
		return self.im3
	def ConvImgPil(self, imgarray, conv='RGB'):
		self.im4 = Image.fromarray(imgarray, conv)
		return self.im4


		
		
#testing
#obj = ArrayPil()
#a1 = obj.ConvImgArray('image1.jpg')
#print(a1)
#obj.ImgSave(a1, 'res.jpg')
#a2 = obj.ConvImgPil(a1)
#print(a2)
#a3 = obj.ConvPilArray(a2)
#print(a3)
