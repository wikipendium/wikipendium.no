(function($) {
    $.fn.autocompletrie = function(trie) {
        return this.each(function() {

            var suggestions = $('<ul id=suggestions></ul>');
            $(this).after(suggestions);

            function search(trie, word){
                if(word.length == 0) return [];
                word = word.toLowerCase();
                var ret = [];
                for(var i=0;i<trie.length;i++){
                    if(trie[i].toLowerCase().indexOf(word) !== -1){
                        ret.push(trie[i]);        
                    }
                }
                return ret;
            }

            var sb = $(this);
            sb.focus();
            var ul = suggestions;
            var ullength = 0;
            var oldword = "";
            var index = 0;

            sb.on("keydown",function(e){
                if(e.keyCode == 13){ //enter
                    e.preventDefault();
                    window.location = '/'+$(ul.children()[index]).text().replace(/ /g,'_');
                }
                if(e.keyCode == 38){ //up
                    e.preventDefault();
                    index = (index-1)%ullength;
                }else if(e.keyCode === 40){ //down
                    e.preventDefault();
                    index = (index+1)%ullength;
                }
                for(var i=0;i<ullength;i++){
                    $(ul.children()[i]).removeClass("active");
                }
                $(ul.children()[index]).addClass("active");
            });

            var refresh = function(e){
                if(oldword === sb.val()) return;
                oldword = sb.val();
                index = 0;
                ul.empty();
                var words = search(trie,oldword);
                console.log(words);
                ullength = words.length;
                for(var i=0;i<words.length;i++){
                    var li = document.createElement("li");
                    li.textContent = words[i];
                    ul.append(li); 
                }
                $(ul.children()[index]).addClass("active");
            }
            setInterval(refresh,100);

        });
    };
})(jQuery);
