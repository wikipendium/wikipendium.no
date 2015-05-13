$(function(){

    var editor_has_been_updated = false;

    $('code').addClass('prettyprint');
    prettyPrint();

    CodeMirror.defineMode("markdown-math", function() {
        var markdown_mode = CodeMirror.getMode({}, "markdown");
        var latex_mode = CodeMirror.getMode({}, "mathjax");

        var block_latex = {
          open: "$$",
          close: "$$",
          mode: latex_mode,
          delimStyle: "mathjax-delimit",
          innerStyle: "mathjax-block",
          escapeDelimiters: true
        };

        var inner_latex = {
          open: "$",
          close: "$",
          mode: latex_mode,
          delimStyle: "mathjax-delimit",
          innerStyle: "mathjax-inline",
          escapeDelimiters: true
        };

        return CodeMirror.multiplexingMode(
          markdown_mode,
          block_latex,
          inner_latex
          );
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
            mode: CodeMirror.getMode({}, "markdown-math"),
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

    window.onbeforeunload = function(e) {
        if (editor_has_been_updated) {
            return "You have unsaved changes!";
        }
    };


    $('#help-tabs a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
        $('.tab-container .tab').removeClass('active');
        var tabId = $(this).attr('href');
        $(tabId).addClass('active');
    });

    $(window).on('hashchange', function(e) {
        // Impressively, this ensures scrolling doesn't break (as much) in Safari
        $('.toc').toggleClass('safari-reload-scroll-hack');
    });

    $('.section1 h1').click(function(e) {
        $(this).parent('.section1').toggleClass('open');
    });

    $('#toggle-toc').on('click', function(e) {
        $('body').toggleClass('toc-hidden');
    });

    $('[data-source-line-number]').each(function(i, el){
        var a = $('<a class="edit-section-button button">Edit</a>');
        var url = (window.location.pathname + '/edit/#').replace('//', '/');
        a.attr('href', url + $(el).attr('data-source-line-number'));
        $(el).prepend(a);

        var semaphor = 0;
        function show(){ semaphor++, a.css('opacity', 1); }
        function hide(){ setTimeout(function(){--semaphor || a.css('opacity', 0);}, 300); }
        $(a).hover(show, hide);
        $(el).hover(show, hide);
    });

    (function() {
        this.html("<em>Last updated:</em> " + moment(this.text()).fromNow() + ".")
    }).apply($('.last-updated'));
});

// Stay in web-app on iOS
(function(a,b,c){if(c in b&&b[c]){var d,e=a.location,f=/^(a|html)$/i;a.addEventListener("click",function(a){d=a.target;while(!f.test(d.nodeName))d=d.parentNode;"href"in d&&(d.href.indexOf("http")||~d.href.indexOf(e.host))&&(a.preventDefault(),e.href=d.href)},!1)}})(document,window.navigator,"standalone");

