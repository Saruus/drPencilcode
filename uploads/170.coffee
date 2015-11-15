secret = random [1..100]
turns = 5
write "Guess my number."
write "You get #{turns} guesses."
while turns > 0
  await readnum defer pick
  if pick is secret
    write "You got it!"
    break
  if 1 <= pick < secret
    write "Too small! "
  else if secret < pick <= 100
    write "Too big! "
  else
    write "It's a number 1 to 100."
    continue
  turns = turns - 1
  if turns > 1
    write "#{turns} left."
  else if turns is 1
    write "Last guess!"
  else
    write "Game over."
    write "It was #{secret}."
