arcs = new Turtle red
arcs.pen purple, 10
square1 = new Turtle orange
square1.pen orange
square2 = new Turtle yellow
square2.pen orange
square1.ht()
square1.speed 3
square2.ht()
square2.speed 5
fib1 = 1
fib2 = 1
for [1..10]
  dist = fib1*10
  
  square1.fd dist
  square1.rt 90
  square1.fd dist
  
  square2.rt 90
  square2.fd dist
  square2.lt 90
  square2.fd dist
  square2.rt 90
  
  arcs.rt 90, dist
  sum = fib1+fib2
  fib1 = fib2
  fib2 = sum
  sync arcs, square1, square2
