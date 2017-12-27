$(document).ready(function() {
    console.log('Loaded')
    var smallRedLoader = ' <div class="preloader-wrapper active small">\n' +
        '    <div class="spinner-layer spinner-red-only">\n' +
        '      <div class="circle-clipper left">\n' +
        '        <div class="circle"></div>\n' +
        '      </div><div class="gap-patch">\n' +
        '        <div class="circle"></div>\n' +
        '      </div><div class="circle-clipper right">\n' +
        '        <div class="circle"></div>\n' +
        '      </div>\n' +
        '    </div>\n' +
        '  </div>';
    var bigRedLoader = '<div class="preloader-wrapper active big big-loader">\n' +
        '    <div class="spinner-layer spinner-red-only">\n' +
        '      <div class="circle-clipper left">\n' +
        '        <div class="circle"></div>\n' +
        '      </div><div class="gap-patch">\n' +
        '        <div class="circle"></div>\n' +
        '      </div><div class="circle-clipper right">\n' +
        '        <div class="circle"></div>\n' +
        '      </div>\n' +
        '    </div>\n' +
        '  </div>';
    $('select').material_select();
    // Sends chosen class and format to the server and which generate
    // and returns a deck which is rendered using jQuery
    $('#deck-data').on('submit', function () {
        event.preventDefault();
        console.log('Clicked');
        document.getElementById('deck-content').innerHTML = bigRedLoader;
        $.ajax({
            url: 'deck',
            data: {
                'hero' : $('#id_hero').val(),
                'format' : $('#id_deck_format').val()
            },
            dataType: 'html',
            success: function (data) {
                console.log('Loading html');
                // document.getElementById('big-loader').innerHTML = "";
                $('#deck').html(data)

            }

        })
    });

    $('#import-collection').on('submit', function () {
        event.preventDefault();
        console.log('Importing collection');
        document.getElementById('import-response').innerHTML = "Importing collection...";
        document.getElementById('import-loader').innerHTML = smallRedLoader;
        $.ajax({
            url: 'import_collection',
            data: {
                'name':  $('#id_name').val()
            },
            dataType: 'json',
            success: function (data) {
                document.getElementById('import-loader').innerHTML = "";
                document.getElementById('import-response').innerHTML = data['response']
            }
        })
    });
    $(document).on('click','#copyButton', function () {
        copyToClipboard(document.getElementById("deckstring"));
    });
});

// Taken from https://stackoverflow.com/questions/22581345/click-button-copy-to-clipboard-using-jquery


function copyToClipboard(elem) {
	  // create hidden text element, if it doesn't already exist
    console.log("Copying");
    var targetId = "_hiddenCopyText_";
    var isInput = elem.tagName === "INPUT" || elem.tagName === "TEXTAREA";
    var origSelectionStart, origSelectionEnd;
    if (isInput) {
        // can just use the original source element for the selection and copy
        target = elem;
        origSelectionStart = elem.selectionStart;
        origSelectionEnd = elem.selectionEnd;
    } else {
        // must use a temporary form element for the selection and copy
        target = document.getElementById(targetId);
        if (!target) {
            var target = document.createElement("textarea");
            target.style.position = "absolute";
            target.style.left = "-9999px";
            target.style.top = "0";
            target.id = targetId;
            document.body.appendChild(target);
        }
        target.textContent = elem.textContent;
    }
    // select the content
    var currentFocus = document.activeElement;
    target.removeAttribute("disabled");
    target.focus();
    target.setSelectionRange(0, target.value.length);
    target.setAttribute("disabled", "disabled");
    // copy the selection
    var succeed;
    try {
    	  succeed = document.execCommand("copy");
    } catch(e) {
        succeed = false;
    }
    // restore original focus
    if (currentFocus && typeof currentFocus.focus === "function") {
        currentFocus.focus();
    }

    if (isInput) {
        // restore prior selection
        elem.setSelectionRange(origSelectionStart, origSelectionEnd);
    } else {
        // clear temporary content
        target.textContent = "";
    }
    return succeed;
}

