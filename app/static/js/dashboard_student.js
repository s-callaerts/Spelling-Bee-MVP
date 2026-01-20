const makeTestBtn = document.getElementById("make-test-btn");
const testContentSelect = document.getElementById("test-content-select");
const gradeChoice = document.getElementById("grade");
const chapterChoice = document.getElementById("chapter");
const startTestBtn = document.getElementById("start-test-btn");
const testDisplay = document.getElementById("test-display");
const question = document.getElementById("question");
const answer = document.getElementById("answer");
const submitAnswerBtn = document.getElementById("submit-answer");
const noticeBox = document.getElementById("notice-box");
const closeNoticeBtn = document.getElementById("close-notice");

makeTestBtn.addEventListener("click", () => {
    makeTestBtn.classList.toggle("hidden");
    testContentSelect.classList.toggle("hidden");
})

startTestBtn.addEventListener("click", () => {
    const payload = {grade: gradeChoice.value, chapter: chapterChoice.value};
    postJSON('/test', (payload))
    .then(validateResponse)
    .then((data) => {
        console.log(data);
        testContentSelect.classList.toggle("hidden");
        testDisplay.classList.toggle("hidden");
        question.textContent = data.question;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
})

submitAnswerBtn.addEventListener("click", () => {
    const payload = {answer: answer.value};
    postJSON('/inserturlhere', (payload))
    .then(validateResponse)
    .then((data) => {
        console.log(data);
        noticeBox.classList.toggle("hidden");
        noticeBox.textContent = data.message;
        question.innerText = data.question;
        answer.value = '';
    })
    .catch((error) => {
        console.error('Error:', error);
    });
})

closeNoticeBtn.addEventListener("click", () => {
    noticeBox.classList.toggle("hidden");
})

async function validateResponse(response) {
    const data = await response.json();
    console.log(data);
    if (!response.ok) {
        throw data;
    }
    return data;
}

function postJSON(url, payload) {
    console.log(payload);
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload),
    })
}