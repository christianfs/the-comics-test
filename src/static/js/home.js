let ns = {};

ns.model = (function() {
    'use strict';

    let CAPTAIN_AMERICA_ID = '1009220'
    let $event_pump = $('body');
    const urlParams = new URLSearchParams(window.location.search);
    const characterId = urlParams.get('characterId') ?? CAPTAIN_AMERICA_ID;
    const url = 'api/character/' + characterId + '/story'

    return {
        'read': function() {
            let ajax_options = {
                type: 'GET',
                url: url,
                accepts: 'application/json',
                dataType: 'json'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_read_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        }
    };
}());

ns.view = (function() {
    'use strict';

    return {
        build_table: function(story) {
            
            let rows = ''

            $('.characters table > tbody').empty();

            if (story) {
                $('.banner').append(`${story.title}`)
                $('.description').append(`${story.description}`)
                for (let i=0, l=story.characters.length; i < l; i++) {
                    rows += `<tr><td class="name">${story.characters[i].name}</td><td class="imageUrl"><img src="${story.characters[i].imageUrl}" alt="${story.characters[i].name}"></td></tr>`;
                }
                $('table > tbody').append(rows);
                $('.attribution').append(`${story.attribution}`)
            }
        },
        error: function(error_msg) {
            $('.error')
                .text(error_msg)
                .css('visibility', 'visible');
            setTimeout(function() {
                $('.error').css('visibility', 'hidden');
            }, 3000)
        }
    };
}());

ns.controller = (function(m, v) {
    'use strict';

    let model = m,
        view = v,
        $event_pump = $('body');

    setTimeout(function() {
        model.read();
    }, 100)

    $event_pump.on('model_read_success', function(e, data) {
        view.build_table(data);
        view.reset();
    });

    $event_pump.on('model_error', function(e, xhr, textStatus, errorThrown) {
        let error_msg = textStatus + ': ' + errorThrown + ' - ' + xhr.responseText;
        view.error(error_msg);
        console.log(error_msg);
    })
}(ns.model, ns.view));

