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
const noticeMessage = document.getElementById("message");

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
        question.textContent = data.message;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
})

submitAnswerBtn.addEventListener("click", () => {
    const payload = {answer: answer.value};
    postJSON('/answer', (payload))
    .then(validateResponse)
    .then((data) => {
        console.log(data);

        if(data.status === 'False' || data.status === 'Error') {
            reset();
            setNoticeBox(data.message);
        } else if(data.status === 'Complete') {
            userScore = data.summary['score'];
            total = data.summary['total'];
            reset();
            setNoticeBox(`Test Complete! You answered ${userScore}/${total} questions correctly.`)
        } else if(data.status === 'In Progress') {
            if (data.correct) {
                setNoticeBox("Correct!");
            } else {
                setNoticeBox(`Incorrect. The correct answer was: ${data.correct_answer}`);
            }
        question.innerText = data.next_question;
        answer.value = '';
        }  
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

function setNoticeBox(message) {
    noticeBox.classList.remove("hidden");
    noticeMessage.textContent = message;
}

function reset() {
    testDisplay.classList.toggle("hidden");
    makeTestBtn.classList.toggle("hidden");
    question.textContent = '';
    answer.value = '';
}