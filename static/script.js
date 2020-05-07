function showlform(x) {
    $('#lform').show();
    $('#rform').hide();
    $(x).find('h3').css('border-bottom', '#FBB03B 5px solid');
    $(x).parents('#loginpanel').find('h3').eq(1).css('border-bottom', 'none');
}

function showrform(x) {
    $('#rform').show();
    $('#lform').hide();
    $(x).find('h3').css('border-bottom', '#FBB03B 5px solid');
    $(x).parents('#loginpanel').find('h3').eq(0).css('border-bottom', 'none');
}

function hideforms() {
    $('#loginpanel').fadeToggle(400);
    setTimeout(function () {
        $('#herotext, #notepic, #sharedata').fadeToggle();
    }, 600)
}

// toggle Login/Register Panel
function toggleLoginPanel(x) {
    $('#herotext, #notepic, #sharedata').fadeToggle(400);
    $('#loginpanel').fadeToggle(600);
}

// toggle heart
function likePlus(a) {
    //console.log($(a).parent().text())
    if ($(a).children('i').css('color') == 'rgb(33, 33, 33)') {
        $(a).children('i').css('color', 'rgb(255, 0, 0)')
        newLikes = parseInt($(a).parent().text()) + 1
        $(a).parent().children('span').text(newLikes.toString())
    } else if ($(a).children('i').css('color') == 'rgb(255, 0, 0)') {
        $(a).children('i').css('color', 'rgb(33, 33, 33)')
        newLikes = parseInt($(a).parent().text()) - 1
        $(a).parent().children('span').text(newLikes.toString())
    }

}

// alter topic list in select html
function onSubjChange(a) {
    let chosenSubj = $('#selectsubj' + a).val()
    let physicstopics = ['All', 'Measurement', 'Newtonian Mechanics', 'Thermal Physics', 'Waves', 'Electricity & Magnetism']
    let chemtopics = ['All', 'Experimental Chemistry', 'Atomic Structure & Stoichiometry', 'Chemistry of Reactions', 'Periodicity', 'Atmosphere', 'Organic Chemistry']
    let geogtopics = ['All', 'Our Dynamic Planet', 'Our Changing World']
    let mathtopics = ['All', 'Number & Algebra', 'Geometry & Measurement', 'Statistics & Probablity']

    function appendTopics(subj) {
        for (topic of subj) {
            $('#selecttopics' + a).append(`
            <option value='${topic}'>${topic}</option>
        `)
        }
    }

    $('#selecttopics' + a).empty()
    if (chosenSubj == 'Physics') {
        appendTopics(physicstopics)
    } else if (chosenSubj == 'Chemistry') {
        appendTopics(chemtopics)
    } else if (chosenSubj == 'Math') {
        appendTopics(mathtopics)
    } else if (chosenSubj == 'Geography') {
        appendTopics(geogtopics)
    } else if (chosenSubj == 'All') {
        $('#selecttopics' + a).empty()
    }


}

$(function () {
    // hide login/register panel
    $('#loginpanel').hide()
    $('#rform').hide()
    $('#loginpanel').find('h3').eq(0).css('border-bottom', '#FBB03B 5px solid');


    // summernote
    $('#summernote').summernote({
        placeholder: 'Hello Bootstrap 4',
        tabsize: 2,
        height: 300,
        width: 700,
        toolbar: [
            // [groupName, [list of button]]
            ['style', ['bold', 'italic', 'underline', 'clear']],
            ['font', ['strikethrough', 'superscript', 'subscript']],
            ['fontsize', ['fontsize']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['height', ['height']],
            ['insert', ['table', 'picture']],
            ['view', ['fullscreen']]
        ]
    });





}) //jquery end