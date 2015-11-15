numero = 20
if (numero == 5)
  write "El numero es 5!"
else
  write "El numero no es 5"
await read 'Escribe', defer x
write x
defer y
keyup 'x', ->
  write 'up'
keydown 'x', ->
  write 'down'
keypress 'c', ->
  write 'press'
z = 'hola'
write(typeof z)
see z
fd 100
