function postRequest(url, data = {}, callback) {
    const csrfToken = getValue(object("#csrf_token"));
    data.csrf_token = csrfToken;
    url = "posts/" + url;
    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json().then(data => callback(data, response.status)))
        .catch(error => {
            console.error('Hata:', error);
            callback(null, null);
        });
}

function object(name) {
    const a = name[0];
    if (a === "#") {
        return document.getElementById(name.slice(1));
    } else if (a === ".") {
        return document.getElementsByClassName(name.slice(1));
    } else {
        return document.getElementsByTagName(name);
    }
}

function onclick(object, events) {
    let elements = object;
    if (elements.length) {
        Array.from(elements).forEach(element => {
            element.addEventListener("click", events);
        });
    } else {
        elements.addEventListener("click", events);
    }
}

function getValue(object) {
    return object.value || object.textContent || object.innerHTML;
}

function replace() {
    window.location.replace();
}

function redirectTo(url) {
    window.location.href = url;
}


function setValue(object, data) {
    if (object.value !== undefined) {
        object.value = data;
    } else if (object.textContent !== undefined) {
        object.textContent = data;
    } else {
        object.innerHTML = data;
    }
}

function getText(object) {
    return object.textContent || object.innerText;
}

function setText(object, data) {
    if (object.textContent !== undefined) {
        object.textContent = data;
    } else {
        object.innerText = data;
    }
}