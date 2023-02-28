//DOM selections
const micElt = document.getElementById("micro");
const recordElt = document.getElementById("record");
const mainElt = document.querySelector(".main");
const cardElt = document.querySelector(".card")
const answerElt = document.getElementById("answer");
const arrowElt = document.getElementById("arrow")
const sliderElt = document.getElementById("slider")
const flags = document.querySelectorAll('.flag')
const imgElt = document.getElementById("valentin")

//variable declaration
const PATH = "/static/img/"
let selectedLanguage = "france"

//events listener
recordElt.addEventListener("click", record)
arrowElt.addEventListener("click", reset)

//simulate hesitation
function loader(bool) {
    if (bool) {
        interval = setInterval(() => {
            answerElt.textContent += '.';
            if (answerElt.textContent === '....') {
                answerElt.textContent = ''
            }
        }, 500)
    } else {
        clearInterval(interval);
        answerElt.innerHTML = '';
    }
}

// Speaking in mic and displaying Valentin
function record() {
    sliderElt.setAttribute("disabled", "true");
    sliderElt.style.cursor = "default";
    recordElt.classList.add("active");
    recordElt.removeEventListener("click", record);
    micElt.src = PATH + "microphone.gif";
    loader(true);

    fetch('/listen').then(function (response) {
        return response.json();
    })
        .then(function (data) {
            mainElt.style.display = "none";
            cardElt.style.display = "block";
            console.log(data.query);
            askBot(data.query)
        })
}

//Ask to the bot and display text answer
function askBot(query) {
    const formData = new FormData();
    formData.append('temperature', sliderElt.value);
    fetch('/answer/' + query, {
        method: 'POST',
        body: formData
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            console.log(data);
            loader(false);
            answer = data.answer.replace('?', '');
            printLetterByLetter(answer, 60);
            fetch('/speech/' + answer + '?language=' + selectedLanguage);
        })
}

// Fill page like first display
function reset() {
    answerElt.innerHTML = '';
    arrowElt.style.display = "none";
    mainElt.style.display = "block";
    cardElt.style.display = "none";
    micElt.src = PATH + "microphone-base.png";
    recordElt.classList.remove("active");
    recordElt.addEventListener("click", record);
    sliderElt.removeAttribute("disabled");
    sliderElt.style.cursor = "pointer";
}

// Display letters one by one
function printLetterByLetter(message, speed) {
    let i = 0;
    let interval = setInterval(function () {
        answerElt.innerHTML += message.charAt(i);
        i++;
        if (i > message.length) {
            arrowElt.style.display = "block"
            clearInterval(interval);
        }
    }, speed);
}

// Flag selection
function activeLink() {
    flags.forEach((flag) =>
        flag.classList.remove('selected')
    )
    this.classList.add('selected')
    selectedLanguage = this.getAttribute("alt")
    if (this.getAttribute("alt") === "inde") {
        imgElt.src = PATH + "lakhbir.png";
    }
    else {
        imgElt.src = PATH + "valentin.jpg";
    }
}

flags.forEach((flag) =>
    flag.addEventListener("click", activeLink)
)
