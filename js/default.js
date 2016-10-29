$(document).ready(function ()
{
    var search = $('input');
    var searchContainer = $('.input-container');
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
        }
    });
});