function sleep(ms) {
    return new Promise((resolve) => {
        setTimeout(resolve, 4000);
    });
}

window.exportedContactsStorage = new Set();
window.scroller = document.querySelectorAll('.ZvpjBb.C8Dkz')[0].parentElement.parentElement.parentElement.parentElement.parentElement;
while (scroller.scrollHeight - scroller.scrollTop > 1000) {
    for (let element of document.querySelectorAll('.ZvpjBb.C8Dkz')[0].querySelectorAll('.XXcuqd')) {
        if (element.firstChild.childNodes.length == 1) {
            break;
        }
        let name = element.firstChild.childNodes[1].innerText;
        let bu_email = element.firstChild.childNodes[2].innerText;
        let job_title = element.firstChild.childNodes[4].innerText;
        window.exportedContactsStorage.add(JSON.stringify({'name': name, 'bu_email': bu_email, 'job_title': job_title}));
    }
    scroller.scrollTo({
        top: scroller.scrollTop + 1000,
        behavior: 'smooth'
    });
    console.log(
        (scroller.scrollTop / scroller.scrollHeight * 100).toString() + '%'
    );
    await sleep(4000);
}

// And to extract the variable to a file, use 
JSON.stringify(Array.from(exportedContactsStorage))

// This is better
function download(content, fileName, contentType) {
  var a = document.createElement("a");
  var file = new Blob([content], { type: contentType });
  a.href = URL.createObjectURL(file);
  a.download = fileName;
  a.click();
}
download(Array.from(exportedContactsStorage), "json.txt", "text/plain");