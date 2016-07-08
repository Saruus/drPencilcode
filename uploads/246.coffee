# This function looks at the words in your
# answer and picks the troll's response.
replyto = (a) ->
  for word in a.toLowerCase().split /\W+/
    switch word
      when "secret"
        return "Right."
      when "money"
        return "I don't want your money!"
      when "advice"
        return "My advice: think again."
      when "who"
        return "I am the Bridge Troll!"
      when "troll"
        return "The troll laughs at you."
      when "know"
        return "I know the answer. Do you?"
  # If no words were recognized, a random
  # canned response is picked.
  return random [
    "That doesn't make sense."
    "Guess again!"
    "That is not right!"
  ]

riddle = ->
  write """
    A troll blocks the bridge and asks:
  """
  type """
      When you don't have me,
      you want me,
      but when you do have me,
      you want to give me away.
      What am I?
    """
  while s isnt "Right."
    # Wait for an answer and reply to it.
    await readstr defer a
    s = replyto a
    write s
  do proceed

proceed = ->
  write """
    The troll steps aside, and you cross.
    (what happens next?)
  """

# start the game
do riddle
