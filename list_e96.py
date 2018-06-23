import e96_Resistors

print("Y=10^-2;X=10^-1;A=10^0;B=10^1;C=10^2;D=10^3;E=10^4;F=10^5")
for i in range(0,96):
    print("{},{}".format(i+1,e96_Resistors.DecodeResistorE96(i,0)))
