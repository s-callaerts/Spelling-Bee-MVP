// load words from JSON
fetch('data/words.json').then(response => response.json()).then(data => {
    const difficulty = "shou 5 / 6";
    const words = data[difficulty];
    const word = words[Math.floor(Math.random()*words.length)];
    console.log(word.english, word.japanese);
});