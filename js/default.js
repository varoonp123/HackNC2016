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
        url: 'localhost:80',
        data: query,
        success: function (response)
        {
            console.log(response);
        },
        error: function ()
        {

        }
    })
}