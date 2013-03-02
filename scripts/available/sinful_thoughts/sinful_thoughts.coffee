sins = 1 # the original sin
the_seven_dirty_words = ['shit', 'piss', 'fuck', 'cunt', 'cocksucker', 'motherfucker', 'tits']

checkSins = (e) ->
  for sinful_word in the_seven_dirty_words
    console.log $(this).val().match(sinful_word)
    if $(this).val().match(sinful_word)?
      console.log "found #{sinful_word}"
      sins++
      if sins > 7
        $('body').append('<div id=TERRIBLE_SINNER></div>')
          .css('background-color','red')
          .css('position','fixed')
          .css('width','90%')
          .css('height','90%')
          .append('<h1>You are going to HELL</h1>')
      else
        alert 'I am sure you didnt mean that.'
        $(this).val($(this).val().replace(sinful_word,''))

$ ->
  $('input').on 'keypress', checkSins