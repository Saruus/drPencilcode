speed Infinity

# draw the platforms:
moveto -325, -100
rt 90
pen red, 10
fd 200
lt 90
pen blue, 10
fd 50
pen red, 10
rt 90
fd 100
rt 90
pen blue, 10
fd 50
pen red, 10
lt 90
fd 300

# move into position:
lt 90
pen up
moveto -250, 100

velocity = [0, 0]
pen green # comment out to stop leaving debug traces
gravity = -0.5

numJumps = 0

keydown 'w', ->
  if numJumps < 2
    velocity[1] +=10
    numJumps += 1

forever ->
  move velocity
  velocity[1] += gravity
  if turtle.touches red
    while turtle.touches red
      fd 1
    velocity[1] = -velocity[1] * 0.1
    numJumps = 0
  if pressed 'a' 
    move -5, 0
    if turtle.touches blue
      move 5, 0
  if pressed 'd'
    move 5, 0
    if turtle.touches blue
      move -5, 0
