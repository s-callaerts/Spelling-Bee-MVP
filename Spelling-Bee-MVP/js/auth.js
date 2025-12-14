//authorization for teacher
const teachKey = "Kh43($^V";

function validateKey () {
    if (target === teachKey) {
        teacherAuthority = true;
    } else {
        console.error("Teacher key invalid");
        return;
    }
};

//signup

function signup () {
    firebase.auth().createUserWithEmailAndPassword(email, password).then((userCredential) => {
        const uid = userCredential.user.uid;
        db.collection("users").doc(uid).set({
            username: username,
            role: role,
            difficulty: null
        });
    })
    .catch((error) => {
        console.error(error.message);
    });
}

//login

function login(email, password) {
    firebase.auth().signInWithEmailAndPassword(email, password).then((userCredential) => {
        //Redirect based on role
        uid.role === teacher ? window.location.href="./dashboard_teacher.html" : window.location.href="./dashboard_student.html";
    });
}