from numpy import cos,sin,pi


teta1 = 60*pi/180
teta2 = 0*pi/180
teta3 = 20*pi/180
px = 17.2*cos(teta1)+13.7*cos(teta3)*cos(teta1)-13.7*sin(teta3)*sin(teta2)*sin(teta1)-8*sin(teta1)*cos(teta2)
py = 17.2*sin(teta1)+13.7*sin(teta1)*cos(teta3)+8*cos(teta2)*cos(teta1)+13.7*sin(teta3)*sin(teta2)*cos(teta1)
pz = 8*sin(teta2)-13.7*sin(teta3)*cos(teta2)+4

print(px)
print(py)
print(pz)