import math

max = 0
min = 0

for i in range(10000):
    value = i*math.pi/4
    s = math.sin(math.radians(math.degrees(value)))
    print(i, " - ", s)

    if s < min:
        min = s
    if s > max:
        max = s

print(min, max)
