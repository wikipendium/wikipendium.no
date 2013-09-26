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

    /* from https://github.com/marijnh/CodeMirror/issues/988#issuecomment-14921785 */
    function betterTab(cm) {
      if (cm.somethingSelected()) {
        cm.indentSelection("add");
      } else {
        cm.replaceSelection(cm.getOption("indentWithTabs")? "\t":
          Array(cm.getOption("indentUnit") + 1).join(" "), "end", "+input");
      }
    }

    var textarea;
    if (textarea = document.getElementById("id_content")) {
        var codeMirror = CodeMirror.fromTextArea(textarea, {
            mode: "markdown-math",
            theme: "wikipendium",
            indentUnit: 4,
            extraKeys: {
                Tab: betterTab
            },
            lineWrapping: true
        })

        codeMirror.on("change", function(){
            editor_has_been_updated = true;
        });

        !function(){
            var line_number = window.location.hash && +window.location.hash.substring(1);
            if(line_number){
                /* scroll to bottom first, so that the line we want will appear in the top of the window */
                codeMirror.doc.setCursor(1e1000);
                codeMirror.doc.setCursor(line_number - 1);
            }
        }();

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

    $('[data-source-line-number]').each(function(i, el){
        var a = $('<a class="edit-section-button button">Edit</a>');
        a.attr('href',window.location.pathname + '/edit#' + $(el).attr('data-source-line-number'));
        $(el).prepend(a);

        var semaphor = 0;
        function show(){ semaphor++, a.css('opacity', 1); }
        function hide(){ setTimeout(function(){--semaphor || a.css('opacity', 0);}, 300); }
        $(a).hover(show, hide);
        $(el).hover(show, hide);
    });
});

// Stay in web-app on iOS
(function(a,b,c){if(c in b&&b[c]){var d,e=a.location,f=/^(a|html)$/i;a.addEventListener("click",function(a){d=a.target;while(!f.test(d.nodeName))d=d.parentNode;"href"in d&&(d.href.indexOf("http")||~d.href.indexOf(e.host))&&(a.preventDefault(),e.href=d.href)},!1)}})(document,window.navigator,"standalone");

