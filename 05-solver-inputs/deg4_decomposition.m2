-- Level-3 certification target (Macaulay2 cross-check)
R = QQ[a0,a1,a2,a3,b0,b1,b2,c0,c1]
I = ideal(
  -4*a3*b2*c1,
  4*a2*b2*c1,
  -a1*b2*c1 - 8*a3*b1*c1 - 2*a3*b2*c0,
  -a2*b1*c1 + 5*a2*b2*c0,
  2*a0*b2*c1 - 5*a1*b1*c1 + a1*b2*c0 + 6*a2*b0*c1 - 6*a3*b1*c0,
  2*a1*b0*c1 - 2*a3*b2 - 4*a3*c1 - 3*b2*c1,
  -2*a0*b1*c1 + 4*a0*b2*c0 - 3*a1*b1*c0 + 5*a2*b0*c0 + 3*a2*b2 + a2*c1,
  4*a0*b0*c1 + 2*a1*b0*c0 - 2*a1*c1 - 4*a3*b1 - 4*a3*c0 - 6*b1*c1,
  4*a0*b0*c0 + 2*a0*b2 - 2*a1*b1 - 2*a1*c0 + 3*a2*b0 - 3*b1*c0,
  a1*b0 - 2*a3 + b0*c0 - b2 - 3*c1,
  2*a0*b0 - a1 - 2*b1 - 2*c0)
D = decompose I
print("minimal primes: " | toString(#D));
print(D)
