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

// toggle heart
function likePlus(a) {
    //console.log($(a).parent().text())
    if ($(a).children('i').css('color') == 'rgb(33, 33, 33)') {
        $(a).children('i').css('color','rgb(255, 0, 0)')
        newLikes = parseInt($(a).parent().text()) + 1
        $(a).parent().children('span').text(newLikes.toString())
    }

    else if ($(a).children('i').css('color') == 'rgb(255, 0, 0)') {
        $(a).children('i').css('color','rgb(33, 33, 33)')
        newLikes = parseInt($(a).parent().text()) - 1
        $(a).parent().children('span').text(newLikes.toString())
    }
    
}

// alter topic list in select html
function onSubjChange(a) {
    let chosenSubj = $('#selectsubj' + a).val()
    let physicstopics = ["Measurement", "Newtonian Mechanics", "Thermal Physics", "Waves", "Electricity & Magnetism"]
    let chemtopics = ['Experimental Chemistry','Atomic Structure & Stoichiometry','Chemistry of Reactions', 'Periodicity', 'Atmosphere', 'Organic Chemistry']
    let geogtopics = ['Our Dynamic Planet', 'Our Changing World', 'Geographical Skills & Investigations']
    let mathtopics = ['Number & Algebra','Geometry & Measurement','Statistics & Probablity']
    
    function appendTopics(subj){
        for (topic of subj) {
            $('#selecttopics' + a).append(`
            <option value="${topic}">${topic}</option>
        `)
        }
    }

    $('#selecttopics' + a).empty()
    if (chosenSubj == 'Physics') {
        appendTopics(physicstopics)
    }
    else if (chosenSubj == 'Chemistry') {
        appendTopics(chemtopics)
    }
    else if (chosenSubj == 'Math') {
        appendTopics(mathtopics)
    }
    else if (chosenSubj == 'Geography') {
        appendTopics(geogtopics)
    }

    
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
        width: 700
    });





}) //jquery end