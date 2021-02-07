import math

radius = 950
centerx = 1250
centery = 1250

f = open("circle.txt", "w")

for angle in range(0, 360, 1):
    x = (math.cos(math.radians(angle)) * radius) + centerx
    y = (math.sin(math.radians(angle)) * radius) + centery
    f.write("[%.2fmil %.2fmil]\n" %( x, y ))
f.close()
