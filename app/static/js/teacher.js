db.collection("users").where("role", "==", "student").get().then(snapshot => {
    snapshot.forEach(doc => {
        const student = doc.data();
        console.log(student.username, student.difficulty);
    });
});