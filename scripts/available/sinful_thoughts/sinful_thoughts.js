// Generated by CoffeeScript 1.4.0
(function() {
  var checkSins, sins, the_seven_dirty_words;

  sins = 1;

  the_seven_dirty_words = ['shit', 'piss', 'fuck', 'cunt', 'cocksucker', 'motherfucker', 'tits'];

  checkSins = function(e) {
    var sinful_word, _i, _len, _results;
    _results = [];
    for (_i = 0, _len = the_seven_dirty_words.length; _i < _len; _i++) {
      sinful_word = the_seven_dirty_words[_i];
      console.log($(this).val().match(sinful_word));
      if ($(this).val().match(sinful_word) != null) {
        console.log("found " + sinful_word);
        sins++;
        if (sins > 7) {
          _results.push($('body').append('<div id=TERRIBLE_SINNER></div>').css('background-color', 'red').css('position', 'fixed').css('width', '90%').css('height', '90%').append('<h1>You are going to HELL</h1>'));
        } else {
          alert('I am sure you didnt mean that.');
          _results.push($(this).val($(this).val().replace(/[ ]sinful_word[ ]/, '')));
        }
      } else {
        _results.push(void 0);
      }
    }
    return _results;
  };

  $(function() {
    return $('input').on('keypress', checkSins);
  });

}).call(this);