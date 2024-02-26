import random
import math

def is_point_in_scope(pos,lim):
		if pos< min(lim):
			return False
		elif pos > max(lim):
			return False
		return True
		
def calculate_coefficients(p1, p2):
	if p1.x == p2.x:
		# Vertical branch, slope is infinite
		m = float('inf')
		b = None  # No y-intercept for vertical branch
	else:
		m = (p2.y - p1.y) / (p2.x - p1.x)
		b = p1.y - m * p1.x
	return m, b

def branch_intersect(branch1, branch2):
	m1, b1 = calculate_coefficients(branch1.p1, branch1.p2)
	m2, b2 = calculate_coefficients(branch2.p1, branch2.p2)

	if len(set(map(tuple,(branch1.p1.pos, branch1.p2.pos,branch2.p1.pos, branch2.p2.pos)))) != 4:
		return False


	# Check if branchs are parallel
	if m1 == m2:
		# Check if both branchs are vertical and have the same x-coordinate
		if m1 == float('inf') and branch1.p1.x == branch2.p1.x:
			return True  # branchs overlap as they are coincident vertical branchs
		return False  # branchs are parallel and do not intersect

	# Calculate the intersection point
	if m1 == float('inf'):
		x_intersection = branch1.p1.x
		y_intersection = m2 * x_intersection + b2
	elif m2 == float('inf'):
		x_intersection = branch2.p1.x
		y_intersection = m1 * x_intersection + b1
	else:
		x_intersection = (b2 - b1) / (m1 - m2)
		y_intersection = m1 * x_intersection + b1

	# branchs intersect if the intersection point is on both branchs
	if (
		min(branch1.p1.x, branch1.p2.x) <= x_intersection <= max(branch1.p1.x, branch1.p2.x)
		and min(branch2.p1.x, branch2.p2.x) <= x_intersection <= max(branch2.p1.x, branch2.p2.x)
	):
		return True  # branchs intersect

	return False  # branchs do not intersect

def generate_color(color,variation):
	n_color = list()
	for k in color:
		x = (k+random.randint(-1,1)*variation)%256
		n_color.append(x)
	return n_color
#input x , lim lim tuple of 2 float, output : x if x in lim right border else:
#exemple = -1 , (0,10) -> 0
# 1 , (0,10) -> 1
