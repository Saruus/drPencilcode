speed 2
pen red
for [1..25]
  fd 100
  rt 88
keydown 'x', ->
  t = new Turtle red
write 'Hello.'
forever 10, ->
  turnto lastmouse
  fd 2
