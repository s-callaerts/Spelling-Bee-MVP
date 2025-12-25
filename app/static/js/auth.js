// grab info from register sheet and send to backend

const submitBtn = document.getElementById("submit");
const registrationForm = document.getElementById("registrationForm");

registrationForm.addEventListener("submit", e.preventDefault());

function validateName() {
    const name = document.getElementById('name');
    if (!name) {
        console.error('名前が必要です。');
        return;
    }
}

function validateEmail() {
    const email = document.getElementById('email');
    const regexp = /\w+@\w+\./;

    if (!regexp.test(email)) {
        console.error('メールのフォーマットは間違っている。');
        return;
    }
}

submitBtn.addEventListener("click", function () {
    validateName();
    validateEmail();

    const data = {
    name: document.getElementById("name").value,
    password: document.getElementById("password").value,
    email: document.getElementById("email"),
    grade: document.getElementById("grade") 
    };

    const userdata = JSON.stringify(data);

    const URL = ""

    fetch(URL, {
        method: POST,
        headers: {"content-type": "application/json"},
        body: userdata
    })
    .then(response => response.json())
    .then(data => console.log("success"))
    .catch((error) => {
        console.error("Error", error);
    })
})