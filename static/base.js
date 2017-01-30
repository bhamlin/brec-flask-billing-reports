
function bloop() {
    var stype = $('select#inputIdType').val();
    var sid = $('input#inputIdentifier').val();
    var sdstart = $('input#inputDateStart').val();
    var sdend = $('input#inputDateEnd').val();
    console.log(sid);
    
    if( sid === '' ) {
        $('input#inputIdentifier')[0].focus();
        alert('You must provide an identifier.');
    } else {
        console.log(stype);
        console.log(sdstart);
        console.log(sdend);
        
        var newUrl = [window.location.href, ['chart', stype, sid, 'start', sdstart, 'end', sdend].join('/')].join('');
        console.log(newUrl);
    }
}

$('button#generateChart').click(bloop);
