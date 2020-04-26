function showlform() {
    $('#lform').show();
    $('#rform').hide();
    $("#login").css('border-bottom', 'gold 5px solid');
    $("#register").css('border-bottom', 'none');
}

function showrform() {
    $('#rform').show();
    $('#lform').hide();
    $("#login").css('border-bottom', 'none');
    $("#register").css('border-bottom', 'gold 5px solid');
}

function hideforms() {
    $('#loginbg').css('transform', 'scale(1)');
    $("#loginpanel").fadeToggle(400);
    setTimeout(function () {
        $('#getstarted').fadeToggle();
        $('#herotxt').fadeToggle();
    }, 800)
}

function showPanel(panelname) {
    for (let i = 0; i < $('.mycarousel').length; i++) {
        $('.mycarousel').eq(i).hide();
    }
    $('#' + panelname).fadeToggle();
}






$(function () {
    // get started button displayes an overlay
    $('#getstarted').click(function () {
        $('#getstarted').fadeToggle();
        $('#herotxt').fadeToggle();
        $('#loginbg').css('transform', 'scale(100)');
        setTimeout(function () {
            $("#loginpanel").fadeToggle();
        }, 600)
        $("#register").css('border-bottom', 'none');
        $("#login").css('border-bottom', 'gold 5px solid');

    })



    // summernote
    $('#summernote').summernote({
        placeholder: 'Hello Bootstrap 4',
        tabsize: 2,
        height: 300,
        width: 500
    });



    // create a carousel in CRUD panel
    for (let i = 1; i < $('.mycarousel').length; i++) {
        $('.mycarousel').eq(i).hide();
    }









}) //jquery end