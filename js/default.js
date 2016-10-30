$(document).ready(function ()
{
    var search = $('input');
    var searchButton = $('#search');
    var searchContainer = $('.input-container');
    var demos = $('.demos');
    var defaultVal = 'Enter a search term';

    // move the search box to the around the middle of the page
    searchContainer.css('margin-top', $(window).height() / 3);

    // hide and then fade in the demos
    demos.hide();
    demos.fadeIn(1500);

    $('#hillary').on({
        click: function ()
        {
            var val = 'hillary clinton';
            search.val(val);
            getMapData(val);
        }
    });

    $('#trump').on({
        click: function ()
        {
            var val = 'donald trump';
            search.val(val);
            getMapData(val);
        }
    });

    $('#microsoft').on({
        click: function ()
        {
            var val = 'microsoft';
            search.val(val);
            getMapData(val);
        }
    });

    // set the search bar to the default value
    search.val(defaultVal);

    // search events
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
                getMapData(search.val().trim().toLowerCase());
        }
    });

    searchButton.on({
        click: function ()
        {
            getMapData(search.val().trim().toLowerCase());
        }
    });

    /**
     * Queries the server for map info based on the given query, then inserts it into the webpage.
     * @param query - The query on which to search.
     */
    function getMapData(query)
    {
        $.get({
            url: 'http://localhost:8080/query/' + query,
            success: function (response)
            {
                demos.fadeOut(500, function ()
                {
                    // move the search box to the upper portion of the page
                    searchContainer.animate({'margin-top': $('.navbar').height()}, 1000, function ()
                    {
                        var map = $('.map');
                        map.html(response);
                    });
                });
            },
            error: function (xhr, status, error)
            {
                console.log('Error: ' + error.message);
            }
        })
    }
});