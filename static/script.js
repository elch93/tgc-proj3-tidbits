$(function () {
    
    // get started button displayes an overlay
    $('#getstarted').click(function(){
        $('#getstarted').hide();
        $('#loginbg').css('transform','scale(1000)');
        $("#loginpanel").fadeToggle(800);
    })

  















    // $('#summernote').summernote({
    //     placeholder: 'Hello Bootstrap 4',
    //     tabsize: 2,
    //     height: 100
    // });

    // $('#sb').click(function(){
    //     console.log($('#summernote').summernote('code'));
    // });
    
    // $('#formtoggle').click(function(){
    //     $('#registerform').toggle()
    //     $('#loginform').toggle()
    // })


}) //jquery end