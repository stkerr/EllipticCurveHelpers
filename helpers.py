import fractions

class EllipticHelpers():
	def __init__(self, p=7, c=0, b=0, a=0):
		self.p = p
		self.a = a
		self.b = b
		self.c = c

	def calculate_points_on_curve(self):
		# Calculate points on curve		
		y2s_dict = dict()
		for y in range(self.p):
			y2 = pow(y,2)%self.p

			if y2 in y2s_dict.keys():
				y2s_dict[y2].append(y)
			else:
				y2s_dict[y2] = [y]
		
		points = list()
		for x in range(self.p):
			xs = (pow(x,3)+self.a*pow(x,2)+self.b*x+self.c) % self.p

			if xs in y2s_dict.keys():
				for y in y2s_dict[xs]:
					points.append((x,y))
		
		self.points = points   
		return points

	def add_points(self, point1, point2):
		if self.points != None:
			if point1 not in self.points:
				raise AttributeError(str(point1) + " not in curve!")
			if point2 not in self.points:
				raise AttributeError(str(point2) + " not in curve!")
				
		new_point = (0,0)
		
		m = None
		if point1 == point2:
			x = point1[0]
			y = point1[1]

			# This step is done with implicit differentiation
			m_numerator = 3*pow(x,2) + 2*self.a*x + self.b
			m_denominator = 2 * y
		else:
			m_numerator = (point2[1] - point1[1]) % self.p
			m_denominator = (point2[0] - point1[0]) % self.p

		if fractions.gcd(self.p, m_denominator) != 1:
			raise ArithmeticError("gcd(" + str(self.p) + "," + str(m_denominator % self.p) +") != 1")

		if m_numerator % m_denominator != 0: # We are going to get a float
			m_denominator_prime = pow(m_denominator, self.p-2, self.p) # y = x^(p-2) mod p, assuming p is prime
			# If m_denominator_prime * m_denominator % p != 1, then that indicates that p isn't prime!
			if (m_denominator_prime * m_denominator) % self.p != 1:
				raise ArithmeticError(str(self.p) + " isn't prime!")
			m = (m_numerator * m_denominator_prime) % self.p
		else:
			m = m_numerator / m_denominator
		
		x3 = (pow(m,2) - point1[0] - point2[0]) % self.p
		y3 = (m*(point1[0] - x3) - point1[1]) % self.p

		return (x3,y3)

#e = EllipticHelpers(p=35,b=5,c=8)
e = EllipticHelpers(p=35,c=26)
points = e.calculate_points_on_curve()
print points

try:
	print e.add_points((10,179),(10,9))
except ArithmeticError, e:
	print e
except AttributeError, ae:
	print ae
