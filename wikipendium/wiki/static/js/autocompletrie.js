(function($) {

    $.fn.autocompletrie = function(trie) {
        return this.each(function() {

            var suggestions = $('#suggestions');

            function search(trie, word){
                if(word.length == 0) {
                    reset();
                    return [];
                }
                word = word.toLowerCase();
                var ret = [];
                for(var i=0;i<trie.length;i++){
                    if(trie[i].label.toLowerCase().indexOf(word) !== -1){
                        ret.push(trie[i]);
                    }
                }

                function heuristic(element){
                    return element.label.toLowerCase().split(' ').map(
                        function(substring){
                            return substring.indexOf(word);
                        }
                    ).reduce(function(a, b){
                        return a + b;
                    }, 0) + element.label.toLowerCase().indexOf(word);
                }

                ret.sort(function(a, b){
                    return heuristic(a) - heuristic(b);
                });

                return ret;
            }

            function bindElements() {
                ul.children().on('mouseover', function(e){
                    index = $(this).attr('data-idx') | 0;
                    ul.children().removeClass('active');
                    $(ul.children()[index]).addClass("active");
                }).on('click',function(e){
                    e.preventDefault();
                    var url = $(ul.children()[index]).attr('data-url') || sb.val();
                    window.location = url;
                    return false;
                }).on('mouseout', function(e) {
                    if(sb.val() === "") {
                        ul.children().removeClass('active');
                    }
                });
                if(sb.val() !== "")
                    $(ul.children()[index]).addClass("active");
            }

            function reset() {
                ul.empty();
                for(var i = 0; i < trie.length; i++) {
                    var li = document.createElement("li");
                    li.textContent = trie[i].label;
                    li.setAttribute('data-url', trie[i].url);
                    li.setAttribute('data-idx', i);
                    li.setAttribute('class', 'compendium-title');
                    var date = document.createElement("p");
                    date.textContent = "Last updated: " + trie[i].updated;
                    date.setAttribute('class', 'date');
                    $(li).append(date);
                    ul.append(li); 
                }
                bindElements();
            }

            var sb = $(this);
            sb.focus();
            var ul = suggestions;
            var ullength = trie.length;
            var oldword = "";
            var index = 0;

            $("body").on("keydown",function(e){
                if(sb.val() === "") return;
                if(e.keyCode == 13){ //enter
                    e.preventDefault();
                    var url = $(ul.children()[index]).attr('data-url') || escape(sb.val());
                    window.location = url;
                }
                if(e.keyCode == 38){ //up
                    e.preventDefault();
                    index = (index-1)%ullength;
                }else if(e.keyCode == 40){ //down
                    e.preventDefault();
                    index = (index+1)%ullength;
                }
                ul.children().removeClass('active');
                $(ul.children()[index]).addClass("active");
            });

            reset();

            var refresh = function(e){
                if(oldword === sb.val()) return;
                oldword = sb.val();
                index = 0;
                ul.empty();
                var words = search(trie,oldword);
                ullength = words.length || trie.length;
                for(var i=0;i<words.length;i++){
                    var li = document.createElement("li");
                    li.textContent = words[i].label;
                    li.setAttribute('data-url', words[i].url);
                    li.setAttribute('data-idx', i);
                    li.setAttribute('class', 'compendium-title');
                    var date = document.createElement("p");
                    date.textContent = "Last updated: " + trie[i].updated;
                    date.setAttribute('class', 'date');
                    $(li).append(date);
                    ul.append(li); 
                }
                bindElements();

                if(ul.children().length == 0) {
                    ullength = 0;
                    var li = document.createElement("li");
                    li.textContent = "Sorry no compendiums were found";
                    li.setAttribute('class', 'no-found');
                    ul.append(li);
                }
            }

            setInterval(refresh,100);

        });
    };
})(jQuery);
