//for both login and signup pages
const submitBtn = document.getElementById('submit-btn');
const loginBtn = document.getElementById('login-btn');

function validateResponse(response) {
    if (response.ok) {
        return response.json()
    } else {
        throw new Error('Invalid JSON data');
    }
}

function postJSON(url, payload) {
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload),
    })
    .then(validateResponse)
}

function setResponse(message) {
    document.getElementById('response_message').innerText = message;
}

function reroute(url) {
    setTimeout(() => windcow.location.href = url, 2000);
}

function handleLoginData(data) {
    if(data.status == 'teacher') {
        console.log('Success', data.message);
        setResponse(data.message);
        reroute('dashboard_teacher.html');
    } else if (data.status == 'student') {
        console.log('Success', data.message);
        setResponse(data.message);
        reroute('dashboard_student.html');
    } else {
        console.error('error', data);
        setResponse(data.message);
        return
    }
}

function handleSignupData(data) {
    if (data.status == 'success') {
        console.log('success', data);
        setResponse(data.message);
        reroute('login.html')
    } else {
        console.error('error', data);
        setResponse(data.message);
        return
    }
}

function attemptSignup() {
    const userName = validateName(document.getElementById('username').value);
    const userEmail = validateEmail(document.getElementById('email').value);
    const userPassword = validatePassword(document.getElementById('password').value);
    const userGrade = validateGrade(document.getElementById('grade').value);

    const dataToSend = {
        name: userName,
        email: userEmail,
        password: userPassword,
        grade: userGrade
    };

    postJSON('/signup', dataToSend)
    .then(data => handleSignupData(data))
    .catch((error) => {
        console.error('Error:', error);
        setResponse('An error occurred.');
    });
}

if (submitBtn) {
    submitBtn.addEventListener('click', (event) => {
        event.preventDefault();
        attemptSignup();
    })
}

function attemptLogin() {
    const name = validateName(document.getElementById('name').value);
    const password = validatePassword(document.getElementById('password').value)
    const dataToSend = {username: name, password: password};

    postJSON('/login', dataToSend)
    .then(data => handleLoginData(data))
    .catch((error) => {
        console.error('Error:', error);
        setResponse('Something went wrong');
    });
}

if (loginBtn) {
    loginBtn.addEventListener('click', (event) => {
        event.preventDefault();
        attemptLogin();
    })
}

function validateName(name) {
    const japaneseCheck = /^[\p{scx=Hiragana}\p{scx=Katakana}\p{scx=Han}\u3005\u3007\u3000-\u303F]+$/u;
    if (!name) {
        console.error('need a name');
        return
    } else if (!japaneseCheck.test(name)) {
        console.error('wrong characters');
        return
    }
    return name;
}

function validateEmail(email) {
    const emailRegex = /\w+@\w+.\[a-z]+/i;
    if (!email) {
        console.error('need email');
        return;
    } else if (!emailRegex.test(email)) {
        console.error('wrong format');
        return;
    }
    return email;
}

function validatePassword(password) {
    const passwordRegex = /.@\$#!\?[0-9]/;
    if (!password) {
        console.error('need password');
        return;
    } else if (!passwordRegex.test(password)) {
        console.error('include at least one number and special symbol (? @ # $ . !)');
        return;
    } else if (password.length > 8) {
        console.error('password should be at least 8 characters');
        return;
    }
    return password;
}

function validateGrade(grade) {
    console.log(typeof grade);
    return grade;
}