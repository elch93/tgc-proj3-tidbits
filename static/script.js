$(function () {
    $('#summernote').summernote({
        placeholder: 'Hello Bootstrap 4',
        tabsize: 2,
        height: 100
    });

    $('#sb').click(function(){
        console.log($('#summernote').summernote('code'));
    });
    
    $('#formtoggle').click(function(){
        $('#registerform').toggle()
        $('#loginform').toggle()
    })


}) //jquery end