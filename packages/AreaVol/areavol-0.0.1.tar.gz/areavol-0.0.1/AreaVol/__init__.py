#code for area perimeter
import math
    
def triangle(height,base):
    area = (height*base)/2
    return area
        
def circle(radius):
    area = radius*radius*math.pi
    return area
    
def square(side):
    area = side**2
    return area
    
def rectangle(lenght,base):
    area = lenght*base
    return area

def shpere(radius):
    volume = math.pi*(radius**3)*4/3
    return volume
        
def prism(height,base,lenght):
    volume = height*base*lenght*0.5
    return volume
        
def cube(side):
    volume = side**3
    return volume
        
def cuboid(height,base,lenght):
    volume = height*base*lenght
    return volume