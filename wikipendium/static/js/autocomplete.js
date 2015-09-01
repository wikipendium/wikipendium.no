(function($) {
  $.fn.autocomplete = function(articles) {
    return this.each(function() {

      var sb = $(this).focus();
      var ul = $('#suggestions');
      var ullength = articles.length;
      var oldword = "";
      var index = 0;

      ul.on('mouseover', 'li', function(e) {
        $(ul.children()[index]).removeClass("active");
        index = $(this).attr('data-idx') | 0;
        $(this).addClass("active");
      }).on('mouseout', 'li', function(e) {
        if(!sb.val()) {
          $(this).removeClass('active');
        }
      });

      function heuristic(element, word) {
        var words = element.label.toLowerCase().split(' ');
        return words.map(
            function (substring, index) {
              var pos = substring.indexOf(word);
              if (pos == -1) {
                return 0;
              } else if (pos == 0) {
                return 1e10-1e7*(index+1);
              } else {
                return 1000 - 100*pos*(index+1);
              }
            }
            ).reduce(function(a, b) {
          return a + b;
        }, 0);
      }

      function search(articles, word){
        if (word.length == 0) return [];

        word = word.toLowerCase();
        var ret = [];
        for (var i=0;i<articles.length;i++) {
          if (articles[i].label.toLowerCase().indexOf(word) !== -1) {
            ret.push(articles[i]);
          }
        }

        ret.sort(function(a, b) {
          return heuristic(b, word) - heuristic(a, word);
        });

        return ret;
      }

      function render(articles, highlight) {
        ul.empty();
        for (var i=0;i<articles.length;i++) {
          var li = document.createElement("li");
          li.setAttribute('data-idx', i);

          var a = document.createElement("a");
          a.setAttribute('href', articles[i].url);
          a.innerHTML = articles[i].label.replace(
              new RegExp(highlight, 'gi'), '<span class=highlight>$&</span>');

          var date = document.createElement("p");
          date.textContent = "Last updated: " +
              moment(articles[i].updated).fromNow() + ".";
          date.setAttribute('class', 'date');

          a.appendChild(date);
          li.appendChild(a);
          ul.append(li); 
        }

        if (sb.val()) {
          $(ul.children()[index]).addClass("active");
        }

        if (ul.children().length == 0) {
          ullength = 0;
        }
      }


      $("body").on("keydown", function(e) {
        if (!sb.val()) return;
        if (e.keyCode == 13) { //enter
          e.preventDefault();
          var url = $(ul.children()[index]).children('a').attr('href') || escape(sb.val());
          window.location = url;
        }
        if (e.keyCode == 38) { //up
          e.preventDefault();
          index = (index-1)%ullength;
        } else if (e.keyCode == 40) { //down
          e.preventDefault();
          index = (index+1)%ullength;
        } else {
          return;
        }
        ul.children().removeClass('active');
        $(ul.children()[index]).addClass("active");
      });

      render(articles);

      var refresh = function(e) {
        if (oldword === sb.val()) return;
        oldword = sb.val();
        index = 0;
        var words = search(articles, oldword);
        if (sb.val()) {
          ullength = words.length;
          render(words, sb.val());
        } else {
          ullength = articles.length;
          render(articles);
        }
      }

      setInterval(refresh,100);
    });
  };
})(jQuery);
