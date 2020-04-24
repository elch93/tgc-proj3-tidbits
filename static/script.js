$(function () {
    $('#summernote').summernote({
        placeholder: 'Hello Bootstrap 4',
        tabsize: 2,
        height: 100
    });

    alert('js is working');

    $('#sb').click(function(){
        console.log($('#summernote').summernote('code'));
        alert('clicked')
    });
    

}) //jquery end