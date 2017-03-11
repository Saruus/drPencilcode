
triangle = (x, y, size) ->
  c = random color
  t = new Turtle c 
  t.moveto x, y
  #sync t, turtle
  t.pen c
  t.fd size
  t.rt 90
  t.fd size
  t.fill c
  t.ht()
  
sierpinski = (x, y, size) ->
  if size > 5
    triangle x, y, size
    plan ->
      sierpinski (x-size/2), y, (size/2)
      sierpinski x+size/2, y+size, size/2
      sierpinski x+size/2, y, size/2

ht()  
sierpinski(0,0,100)
