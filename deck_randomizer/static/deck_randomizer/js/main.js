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
    var bigRedLoader = '<div class="preloader-wrapper active big">\n' +
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
        document.getElementById('deck').innerHTML = bigRedLoader;
        $.ajax({
            url: 'deck',
            data: {
                'hero' : $('#id_hero').val(),
                'format' : $('#id_deck_format').val()
            },
            dataType: 'html',
            success: function (data) {
                console.log('Loading html');
                document.getElementById('deck').innerHTML = "";
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
});


