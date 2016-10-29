$(document).ready(function ()
{
    var search = $('input');
    var searchButton = $('#search');
    var defaultVal = 'Enter map query';

    search.val(defaultVal);

    search.on({
        focusin: function ()
        {
            if (search.val() == defaultVal)
                search.val('');
        },
        focusout: function ()
        {
            if (search.val() == '')
                search.val(defaultVal);
        },
        keyup: function (e)
        {
            if (e.which == 13)
            {
                getMapData(search.val());
            }
        }
    });

    searchButton.on({
        click: function ()
        {
            getMapData(search.val());
        }
    });
});

function getMapData(query)
{
    $.get({
        url: 'http://127.0.0.1:8080/getTweet/',
        data: query,
        success: function (response)
        {
            $('.map').html(response);
        },
        error: function ()
        {

        }
    })
}