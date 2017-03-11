speed 100
rt 90
ht()
for color in [red, gold, green, blue]
  jump -40, -160
  for sides in [3...6]
    pen path
    for x in [1..sides]
      fd 100 / sides
      lt 360 / sides
    fill aqua
    fd 40
st()
pu()
