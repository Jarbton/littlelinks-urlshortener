$('#id_orig_url').keyup(function(){
    getUrlValid();
});

function getUrlValid(){
    console.log("Function has been called")
    var output = document.getElementById('output');
    var url = document.getElementById('id_orig_url').value;
    var valImg = new Image();
    var invImg = new Image();

    valImg.src = '../static/littlelinksite/img/correct.svg';
    invImg.src = '../static/littlelinksite/img/incorrect.svg';

    console.log("Input URL:")
    console.log(url);

    if (isValidUrl(url)){
        output.innerHTML = '<img id="val-img" src="'+valImg.src+'" />';
    } else {
        output.innerHTML = '<img id="val-img" src="'+invImg.src+'" />';
    }
}

function isValidUrl(url){
    var inUrl = url;
    var pattern = new RegExp('^(?:(?:https?|ftp):\/\/)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/\S*)?$');
    console.log("Regex result:");
    console.log(pattern.test(inUrl));
    return pattern.test(inUrl);
 }