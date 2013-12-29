+function($) {
  $.fn.allsearchfilter = function(trie) {
    return this.each(function() {
      var $allList = $('#all-list');

      function search(word) {
        word = word.toLowerCase();

        for (var i=0; i<trie.length; i++) {
          if(trie[i].label.toLowerCase().indexOf(word) !== -1) {
            trie[i].elem.slideDown();
          } else {
            trie[i].elem.slideUp();
          }
        }
      }

      function generateAllList() {
        for(var i=0; i < trie.length; i++) {
          var $li = $('<li></li>', {
            "data-url": trie[i].url,
            "data-idx": i,
          }).append($('<a></a>', {
            text: trie[i].label,
            "href": trie[i].url,
          }));
          $allList.append($li);
          trie[i].elem = $li;
        }
      }

      var $sb = $(this);
      $sb.focus();

      generateAllList();

      var oldWord = "";
      var refresh = function(e) {
        if(oldWord == $sb.val()) return;
        oldWord = $sb.val();

        search(oldWord);
      }

      setInterval(refresh, 100);

      
      

    });
  };
}(jQuery);
