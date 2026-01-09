//for both login and signup pages
const submitBtn = document.getElementById('submit-btn');
const loginBtn = document.getElementById('login-btn');

async function validateResponse(response) {
    const data = await response.json();
    console.log(data);
    if (!response.ok) {
        throw data;
    }
    return data;
}

function postJSON(url, payload) {
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload),
    })
}

function setResponse(message) {
    document.getElementById('response_message').innerText = message;
}

function reroute(url) {
    setTimeout(() => window.location.href = url, 2000);
}

function handleLoginData(data) {
    if(data.status == 'teacher') {
        console.log('Success', data.message);
        setResponse(data.message);
        reroute('/dashboard_teacher');
    } else if (data.status == 'student') {
        console.log('Success', data.message);
        setResponse(data.message);
        reroute('/dashboard_student');
    } else {
        console.error('error', data);
        setResponse(data.message);
        return
    }
}

function handleSignupData(data) {
    console.log('data put into handlesignup:', data);
    if (data.status == 'success') {
        console.log('success', data);
        setResponse(data.message);
        reroute('/login_page')
    } else {
        console.error('error', data);
        setResponse(data.message);
        throw new Error(`What went wrong: ${data}`)
    }
}

function attemptSignup() {
    console.log('signup attempt fired');
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

    postJSON('/auth/signup', dataToSend)
    .then(validateResponse)
    .then(handleSignupData)
    .catch((error) => {
        console.error('Error:', error);
        setResponse('An error occurred.');
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('registrationForm');  
    
    if (!form) {
        return;
    }

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        console.log('form submit intercepted');
        attemptSignup();
    })
});

function attemptLogin() {
    const name = validateName(document.getElementById('name').value);
    const password = validatePassword(document.getElementById('password').value)
    const dataToSend = {username: name, password: password};

    postJSON('/auth/login', dataToSend)
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
    const japaneseCheck = /^[\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Han}\u3005\u3007\u3000-\u303F]+$/u;
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
    const emailRegex = /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i;
    if (!email) {
        throw new Error('need email');
    } else if (!emailRegex.test(email)) {
        throw new Error('wrong format');
    }
    return email;
}

function validatePassword(password) {
    const passwordRegex = /(?=.*[0-9])(?=.*[@#$!.?])/;
    if (!password) {
        throw new Error('need password');
    } else if (!passwordRegex.test(password)) {
        throw new Error('include at least one number and special symbol (? @ # $ . !)');
    } else if (password.length < 8) {
        throw new Error('password should be at least 8 characters');
    }
    return password;
}

function validateGrade(grade) {
    console.log(typeof grade);
    const parsed = parseInt(grade, 10);
    if (Number.isNaN(parsed)) {
        throw new Error('wrong grade')
    }
    return parsed;
}