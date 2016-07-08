[width, height] = [9,9]
grid = table(width, height).home()

sides = [
  {dx: 0, dy: -1, ob: 'borderTop', ib: 'borderBottom'}
  {dx: 1, dy: 0, ob: 'borderRight', ib: 'borderLeft'}
  {dx: 0, dy: 1, ob: 'borderBottom', ib: 'borderTop'}
  {dx: -1, dy: 0, ob: 'borderLeft', ib: 'borderRight'}
]

isopen = (x, y, side) ->
  return /none/.test(
    grid.cell(y,x).css side.ob)
    
isbox = (x, y) ->
  return false unless (
    0 <= x < width and
    0 <= y < height)
  for s in sides
    if isopen x, y, s
      return false
  return true
  
makemaze = (x, y) ->
  loop
    adj = (s for s in sides when isbox x + s.dx, y + s.dy)
    if adj.length is 0 then return
    choice = random adj
    [nx, ny] = [x + choice.dx, y + choice.dy]
    grid.cell(x, y).css choice.ob, 'none'
    grid.cell(ny, nx).css choice.ib, 'none'
    makemaze nx, ny

wander = (x, y, lastdir) ->
  moveto grid.cell y, x
  for d in [lastdir + 3 .. lastdir + 7]
    dir = d % 4
    s = sides[dir]
    if isopen x, y, s then break
  turnto grid.cell y + s.dy, x + s.dx unless dir is lastdir
  plan -> wander x + s.dx, y + s.dy, dir
  
makemaze 0, 0, 0
speed 5
wander 4, 4, 0
