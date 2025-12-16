// grab info from register sheet and send to backend

const submitBtn = document.getElementById("submit");
const registrationForm = document.getElementById("registrationForm");

registrationForm.addEventListener("submit", e.preventDefault());

submitBtn.addEventListener("click", function () {
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