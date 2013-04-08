# -*- coding: utf-8 -*-

import numpy as np
import random
import math
from PIL import Image

#
# самоорганизующаяся карта Кохонена:
# подаем на вход набор цветов - на выходе получаем сгруппированную по этим цветам картинку
#

class Node:
  """
	Нейрон сети - он же узел на карте и пиксель на картинке
	"""
	def __init__(self, R=None, G=None, B=None):
		
		if R is not None:
			self.R = R
		else:
			self.R = random.randint(1,255)
		if G is not None:
			self.G = G
		else:
			self.G = random.randint(1,255)
		if B is not None:
			self.B = B
		else:
			self.B = random.randint(1,255)
	
	def __add__(self, r):
		
		return Node( self.R + r.R, self.G + r.G, self.B + r.B )
	
	def __sub__(self, r):
		
		return Node( self.R - r.R, self.G - r.G, self.B - r.B )
		
	def __mul__(self, r):
		
		return Node( self.R*r, self.G*r, self.B*r )
		
	def __str__(self):
		"""
		Перегружаем print
		"""
		return "(R: %.2f, G: %.2f, B: %.2f)" % (self.R, self.G, self.B)
			
	def distTo(self, node2):
		"""
		Расстояние на карте от одного узла до другого
		"""
		return (self.R - node2.R)**2 + (self.G - node2.G)**2 + (self.B - node2.B)**2

class Grid:
	
	def __init__(self):
		
		self.m = 50 # размер карты по х
		self.n = 50 # размер карты по y

		self.grid = []
		
		self.funAlpha = lambda t: 0.7 # должна монотонно не убывать
		self.funSigma = lambda t: 0.7 # должна монотонно не убывать
		
		for y in range(self.n):
			grid_row = []
			for x in range(self.m):
				grid_row.append( Node() ) # заполняем случайными узлами
				#grid_row.append( random.choice(input) )
			self.grid.append(grid_row)

#		self.grid = [ [ Node(254.0, 83.0, 207.0), Node( 51.0, 68.0, 17.0 ) ], [ Node( 219.0, 160.0, 120.0 ), Node( 69.0, 59.0, 42.0 ) ] ]
		#print self
	
	def __str__(self):
		str = "[\n"
		for row in self.grid:
			str += "\t[\n"
			for grid_elem in row:
				str += "\t%s" % (grid_elem.__str__())
			str += "\t]\n"
		str += "]\n"
		return str

	def Gauss(self, closestNode, x, y, t):
		"""
		Гауссова функция оценки "соседства" двух узлов
		"""
		return self.funAlpha(t)*math.exp(-( (closestNode["x"]-x)**2 + (closestNode["y"]-y)**2 )/(100*self.funSigma(t)) )

	def piecewise(self, closestNode, x, y, t):
		"""
		Тупая функция соседства: входит в квадрат - значит, 1, нет - значит, 0
		"""
		if abs(closestNode["x"]-x)/self.n < 2.0/10.0 and abs(closestNode["y"]-y)/self.m < 2.0/10.0:
			h = 1
		else: h = 0
		return self.funAlpha(t)*h

	def organize( self, elem, t):
		
		minDist = elem.distTo(self.grid[0][0])
		closestNode = { "x" : 0, "y" : 0 }
		
		# найдем наиболее близкую
		for row in self.grid:
			for grid_elem in row:
				if elem.distTo(grid_elem) < minDist:
					minDist = elem.distTo(grid_elem)
					closestNode = { "x" : self.grid.index(row), "y" : row.index(grid_elem) }
		
		# обновим состояние узлов
		for x, row in enumerate(self.grid):
			for y, col in enumerate(row):
				h = self.Gauss( closestNode, x, y, t )
				#h = self.piecewise( closestNode, x, y, t )
				delta = elem - self.grid[x][y]
				self.grid[x][y] = self.grid[x][y] + ( elem - self.grid[x][y] )*h

	def output( self, im, name ):
		"""
		Генерация картинки
		"""
		#im = Image.open(file)
		for x, row in enumerate(self.grid):
			for y, grid_elem in enumerate(row):
				im.putpixel( [y, x], (grid_elem.R, grid_elem.G, grid_elem.B) )
		im.save( name )
		
if __name__ == "__main__":
	
	iterations = 100
	g = Grid()
	input = [ Node(255,0,0), Node(0,255,0), Node(0,0,255), Node(255,255,0), Node(0,255,255), Node(255,0,255), Node(153,0,204), Node(51,0,0)  ]
	try:
			im = Image.open( "colors.jpg" )
	except:
			im = Image.new( "RGBA", (g.m, g.n) )
	g.output( im, "colors.jpg" )
	for t in range(1,iterations):
		filename = "colors" + str(t) + ".jpg"
		try:
			im = Image.open( filename )
		except:
			im = Image.new( "RGBA", (g.m, g.n) )
		randelem = random.choice(input) # случ из инпута
		g.organize(randelem, t)
		print g
		g.output( im, filename )
	filename = "colors_final.jpg"
	try:
			im = Image.open( filename )
	except:
			im = Image.new( "RGBA", (g.m, g.n) )
	g.output( im, filename ) # итоговая картинка
