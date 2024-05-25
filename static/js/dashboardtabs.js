$(document).ready(function() {
    $('.tab-button').click(function() {
        var tab_id = $(this).attr('data-tab');
        $('.tab-button').removeClass('active');
        $('.tab-content').removeClass('active');
        $(this).addClass('active');
        $('#' + tab_id).addClass('active');
    });
    $('.tab-button').first().click();
});
