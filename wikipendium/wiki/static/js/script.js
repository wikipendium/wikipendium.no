$(function(){

    var editor_has_been_updated = false;

    prettyPrint();

    CodeMirror.defineMode("markdown-math", function(config, parserConfig) {
        var markdownMath = {
            token: function(stream, state) {
                var ch;
                if (stream.match("$$")) {
                    while ((ch = stream.next()) != null)
                    if (ch == "$" && stream.next() == "$") break;
                    stream.eat("$");
                    return "mathjax-block";
                }
                if (stream.match("$")) {
                    while ((ch = stream.next()) != null)
                    if (ch == "$" && stream.current().substr(-2) != "\\$") break;
                    return "mathjax-inline";
                }
                while (stream.next() != null && !stream.match("$", false)) {}
                return null;
            }
        };
        return CodeMirror.overlayMode(CodeMirror.getMode(config, parserConfig.backdrop || "markdown"), markdownMath);
    });

    var textarea;
    if (textarea = document.getElementById("id_content")) {
        var codeMirror = CodeMirror.fromTextArea(textarea, {
            mode: "markdown-math",
            theme: "wikipendium",
            lineWrapping: true
        }).on("change", function(){
            editor_has_been_updated = true;
        });

        $('form').submit(function(){
            // Allow form to submit without being bugged about unsaved changes
            editor_has_been_updated = false;
        });
    }

    $(".select_chosen").chosen({
        width:'100%',
        no_results_text: "Language already in use, or doesn't exist."
    });

    function create_article() {
        var redirect_url = $('#create-article-slug').val() + "/edit/";
        window.location.href = redirect_url;
        return false;
    }
    $('#create-button').click( create_article );
    $('#create-article-slug').on('keypress', function(e) {
        if(e.keyCode==13){
            create_article();
        }
    });

    window.addEventListener('beforeunload', function(){
        if (editor_has_been_updated) {
            return "You have unsaved changes!";
        }
    });

    
    $('#help-tabs a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
        $('.tab-container .tab').removeClass('active');
        var tabId = $(this).attr('href');
        $(tabId).addClass('active');
    });
});

// Stay in web-app on iOS
(function(a,b,c){if(c in b&&b[c]){var d,e=a.location,f=/^(a|html)$/i;a.addEventListener("click",function(a){d=a.target;while(!f.test(d.nodeName))d=d.parentNode;"href"in d&&(d.href.indexOf("http")||~d.href.indexOf(e.host))&&(a.preventDefault(),e.href=d.href)},!1)}})(document,window.navigator,"standalone");

