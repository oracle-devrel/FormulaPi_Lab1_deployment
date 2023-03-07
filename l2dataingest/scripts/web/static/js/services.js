// Fetch Service Status from PI API
fetch('/api/services')
    .then((response) => response.json())
    .then((data) => web(data))

function web(data) {
    //console.log(data);

    document.getElementById('f1store').innerHTML = 'Store: ' + data.f1store.store + "<br> Forward: " + data.f1store.forward + "<br> using " + data.f1store.db + "<br/>";

    if (!data.f1prod.status) {
        content = "F1 Producer not Running<br/>";
    } else {
        content = data.f1prod.service + ": " + data.f1prod.status + "<br/>" + data.f1prod.since + "<br/>";
    }
    content = content + "<textarea style='resize:none; display: block; font-family: monospace; white-space: pre; margin: 1em 0;' readonly='true' rows='10' cols='128'>" + data.f1prod.output + "</textarea>";
    document.getElementById('producer').innerHTML = content;

    if (!data.f1cons.status) {
        content = "F1 Consumer not Running<br/>";
    } else {
        content = data.f1cons.service + ": " + data.f1cons.status + "<br/>" + data.f1cons.since + "<br/>";
    }
    content = content + "<textarea style='resize:none; display: block; font-family: monospace; white-space: pre; margin: 1em 0;' readonly='true' rows='10' cols='128'>" + data.f1cons.output + "</textarea>";
    document.getElementById('consumer').innerHTML = content;

    info = data.info.output.replace(/\n/g, '<br>');
    document.getElementById('info').innerHTML = info;
}
