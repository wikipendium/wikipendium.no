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

            $.throttle(100, parseHeadlines)();
        });

        function parseHeadlines() {
            var headlines = [];
            var regex = RegExp("^#+");
            codeMirror.eachLine(function(lineHandle) {
                if (lineHandle.text.substr(0, 1) == "#") {
                    var headerIndent = regex.exec(lineHandle.text);
                    var text = lineHandle.text.replace(regex, '').trim();
                    headlines.push({
                        text: text,
                        lineNumber: codeMirror.getLineNumber(lineHandle),
                        level: headerIndent[0].length,
                        children: []
                    });
                    headlines[headlines.length-1].children.text = text;
                }
            });

            var toc = [];
            var currentLevel = 0;
            var currentStack = [toc];
            for (var i=0; i < headlines.length; i++) {
                var headline = headlines[i];
                var currentParent;
                while (headline.level <= currentLevel) {
                    currentParent = currentStack.pop();
                    currentLevel = currentStack.length - 1;
                }
                currentParent = currentStack[currentStack.length - 1];

                currentParent.push(headline);
                currentLevel = headline.level;
                currentStack.push(headline.children);
            }

            var tocContainer = document.querySelector('.toc > ol');
            tocContainer.innerHTML = '';
            createTocList(toc, tocContainer);
        }

        function createTocList(tree, parentNode) {
            for (var i=0; i < tree.length; i++) {
                var node = tree[i];
                var li = document.createElement('li');
                var a = document.createElement('a');
                a.setAttribute('href', '#' + node.lineNumber);
                a.textContent = node.text;
                li.appendChild(a);

                if (node.children.length > 0) {
                    var ol = document.createElement('ol');
                    createTocList(node.children, ol);
                    li.appendChild(ol);
                }
                parentNode.appendChild(li);
            }
        }

        function goToLine() {
            var line_number = window.location.hash && +window.location.hash.substring(1);
            if (line_number !== "") {
                /* scroll to bottom first, so that the line we want will appear in the top of the window */
                codeMirror.doc.setCursor(1e1000);
                codeMirror.doc.setCursor(line_number - 1);
            }
        }

        goToLine();
        parseHeadlines();
        $(window).on('hashchange', goToLine);

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

    $('#tab-close-button, #overlay').click(function(e) {
        $('#help-container').hide();
        $('#overlay').hide();
    });
    $('#display-help-button').click(function(e) {
        $('#help-container').show();
        $('#overlay').show();
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

    function scrollContainerToShowDomElement(container, element) {
      var containerHeight = $(container).outerHeight();
      var containerScrollTop = $(container).scrollTop();
      var elementOffset = $(element).position().top;
      var elementHeight = $(element).outerHeight();
      var padding = 10;

      if(elementOffset - padding < 0) {
        $(container).scrollTop(containerScrollTop + elementOffset - padding);
      } else if(elementOffset  + elementHeight + padding > containerHeight) {
        $(container).scrollTop(containerScrollTop + elementOffset - containerHeight + elementHeight + padding);
      }
    }

    var scrollDirty = false;
    var sections = $('#article section');
    function highlightScrollPositionInTOC() {
      scrollDirty = false;
      var scrollTop = $(window).scrollTop();
      var bestOffset = -1e99;
      var currentSection = sections.eq(0);
      for(var i = 0; i < sections.length; i++) {
        var section = sections.eq(i);
        // Using floor to avoid half pixel problems
        // scrollTop() returns an integer while offset().top can return a decimal
        var offset = Math.floor($(section).offset().top - scrollTop);
        if(offset <= 0 && offset > bestOffset) {
          bestOffset = offset;
          currentSection = section;
        }
      }

      var elementToHilight = $('.toc a[href=#' + currentSection.attr('id') + ']');
      $('.toc a').removeClass('hilight');
      elementToHilight.addClass('hilight');
      scrollContainerToShowDomElement($('.toc'), elementToHilight);
    }

    $(window).scroll(function() {
      if(!scrollDirty) {
        scrollDirty = true;
        requestAnimationFrame(highlightScrollPositionInTOC);
      }
    });

    $('.toc').on('mousewheel', function(e, d) {
      var toc = $(this);
      if (d > 0 && toc.scrollTop() == 0) {
        e.preventDefault();
      }
      else if (d < 0 && (Math.ceil(toc.scrollTop()) == toc[0].scrollHeight - toc.innerHeight())) {
        e.preventDefault();
      }
    });

    (function() {
        var tagUl = this.find('ul');
        var tagAdder = this.find('.tag-adder');
        var articleSlug = tagAdder.data('article-slug');
        var tagForm = this.find('form');
        var tagInput = this.find('input');
        tagInput.blur(function(e) {
          if(!tagInput.val()) {
            tagForm.hide();
            tagAdder.show();
          }
        });
        tagAdder.click(function(e) {
          e.preventDefault();
          tagAdder.hide();
          tagForm.show();
          tagInput.focus();
        });
        tagForm.submit(function(e) {
          e.preventDefault();
          var tag = tagInput.val();
          $.post('/' + articleSlug + '/add_tag/', {tag: tag}, function(tag) {
            tagAdder.show();
            tagForm.hide();
            tagInput.val('');
            tagUl.append($('<li><a href="/tag/' + tag + '">' + tag + '</a></li>'));
          });
        });
    }).apply($('.tags'));
});

// Stay in web-app on iOS
(function(a,b,c){if(c in b&&b[c]){var d,e=a.location,f=/^(a|html)$/i;a.addEventListener("click",function(a){d=a.target;while(!f.test(d.nodeName))d=d.parentNode;"href"in d&&(d.href.indexOf("http")||~d.href.indexOf(e.host))&&(a.preventDefault(),e.href=d.href)},!1)}})(document,window.navigator,"standalone");

