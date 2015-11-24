function change_iframe_src(selected_option, element_to_change) {
    if (selected_option != '') {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (xhttp.readyState == 4 && xhttp.status == 200) {
                var response = JSON.parse(xhttp.responseText);
                var src_string = 'https://calendar.google.com/calendar/embed?src='+ response['vet_email'] + '&ctz=Asia/Manila;'
                element_to_change.attr('src' , src_string.replace('@', '%40'))
                element_to_change.show();
            }
        };
        xhttp.open('GET', element_to_change.attr('geturl') + '?vet_id=' + selected_option, true);
        xhttp.send()
    } else {
        element_to_change.attr('src' , '')
        element_to_change.hide();
    }
}