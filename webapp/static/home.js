$(document).ready(function() {
    addFormEventListener();
});

function addFormEventListener(){
    $('#bully-form').on('submit', function(e) {
        e.preventDefault();
        const sentence = $('#input-sentence').val();
        $.post( "/get_sentence_result", {
            text: sentence,
        }).done(function(data) {
            const selector = data.bullying ? '.sad' : '.happy';
            $(selector).css('display', 'block');
            $('.row').css('opacity', '0.4');
            let interval = setInterval(function(){
            $(selector).css('display', 'none');
            $('.row').css('opacity', '1');
            clearInterval(interval);
            }, 2000);
        });
    })
}