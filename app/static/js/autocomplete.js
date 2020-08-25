function autocomplete(inp, arr) {
    const textInput = document.getElementById("text");
    const wordsDiv = document.getElementById("t9-words");
    const phrasesDiv = document.getElementById("t9-phrases");
    const phraseLenInput = document.getElementById("phrase-len");
    const firstWordsInput = document.getElementById("first-words");

    let currentFocus;
    let bufferPhrase = "";
    let activeItems;

    function updateLists() {
        let wordsContainer, phrasesContainer, wordInput, phraseInput
        let val = textInput.value;
        closeAllLists();
        if (!val) { return false;}
        currentFocus = -1;

        wordsContainer = document.createElement("DIV");
        wordsContainer.setAttribute("id", "autocomplete-list-words");
        wordsContainer.setAttribute("class", "autocomplete-items");
        wordsDiv.appendChild(wordsContainer);

        phrasesContainer = document.createElement("DIV");
        phrasesContainer.setAttribute("id", "autocomplete-list-phrases");
        phrasesContainer.setAttribute("class", "autocomplete-items");
        phrasesDiv.appendChild(phrasesContainer);

        let phraseLen = parseInt(phraseLenInput.value);

        for (let i = 0; i < arr.length; i++) {
            let phraseList = val.split(" ");
            let value = phraseList[phraseList.length - 1];
            let phraseWords = arr[i].split(" ");
            let firstWord = phraseWords[0];
            let phrase = '';
            for (let i = 0; i < (phraseWords.length - 1 < phraseLen ? phraseWords.length - 1: phraseLen); i++) {
                phrase += (phraseWords[i] + " ");
            }
            if ((phrase.substr(0, value.length).toUpperCase() === value.toUpperCase()) && (value.length > 0)) {
                wordInput = document.createElement("DIV");
                wordInput.className = 'form-control';
                wordInput.style.cursor = "pointer";

                wordInput.innerHTML = "<strong>" + firstWord.substr(0, value.length) + "</strong>";
                wordInput.innerHTML += firstWord.substr(value.length);

                wordInput.innerHTML += "<input type='hidden' value='" + firstWord + "'>";

                wordInput.addEventListener("click", function(e) {
                    inp.value = "";
                    for (let i = 0; i < phraseList.length - 1; i++) {
                        inp.value += (phraseList[i] + " ");
                    }
                    inp.value += this.getElementsByTagName("input")[0].value;
                    closeAllLists();
                });
                wordsContainer.appendChild(wordInput);

                phraseInput = document.createElement("DIV");
                phraseInput.className = 'form-control';
                phraseInput.style.cursor = "pointer";

                phraseInput.innerHTML = "<strong>" + phrase.substr(0, value.length) + "</strong>";
                phraseInput.innerHTML += phrase.substr(value.length);

                phraseInput.innerHTML += "<input type='hidden' value='" + phrase + "'>";

                phraseInput.addEventListener("click", function(e) {
                    inp.value = "";
                    for (let i = 0; i < phraseList.length - 1; i++) {
                        inp.value += (phraseList[i] + " ");
                    }
                    inp.value += this.getElementsByTagName("input")[0].value;
                    closeAllLists();
                });
                phrasesContainer.appendChild(phraseInput);
            }
        }
        activeItems = document.getElementById("autocomplete-list-phrases").getElementsByTagName("div");
    }

    inp.addEventListener("input", function(e) {
        updateLists();
    });

    phraseLenInput.onkeyup = phraseLenInput.onchange = () => {
        updateLists();
    }

    function updateT9Phrases() {
        console.log('Updating T9...');
        let val = textInput.value.toString();
        // console.log(arr)
        if (val[val.length - 1] === " ") {
            // console.log(val, val[val.length - 1], val.split(" "))
            let phraseList = val.split(" ");
            if (phraseList.length > 1) {
                if (phraseList[phraseList.length - 2] !== bufferPhrase) {
                    let wordsCount = parseInt(firstWordsInput.value);
                    let bufArray = [];
                    for (let i = 0; i < (wordsCount < phraseList.length ? wordsCount : phraseList.length); i++) {
                        bufArray.push(phraseList[phraseList.length - (i + 2)]);
                    }
                    bufferPhrase = '';
                    for (let i = bufArray.length - 1; i >= 0; i--) {
                        bufferPhrase += (bufArray[i] + ' ');
                    }
                    $.post('/t9', {
                        beginning: bufferPhrase.substr(0, bufferPhrase.length - 1).toLowerCase(),
                        first_words_count: wordsCount,
                    }).done(function(response) {
                        arr = response['words']
                    });
                }
            }
        }
    }

    inp.addEventListener("input", function(e) {
        updateT9Phrases();
    });

    firstWordsInput.onkeyup = firstWordsInput.onchange = () => {
        updateT9Phrases();
    }

    function changeActiveItems() {
        if (this.counter === undefined) {
            this.counter = 0;
        }
        this.counter += 1;
        wordsDiv.classList.toggle("hide-element");
        phrasesDiv.classList.toggle("hide-element");

        console.log();
        if (this.counter % 2) {
            console.log('phrases');
            activeItems = phrasesDiv.children[0];
        } else {
            console.log('words');
            activeItems = wordsDiv.children[0];
        }
        if (activeItems) activeItems = activeItems.getElementsByTagName("div");
        console.log(activeItems);
        console.log(phrasesDiv.children[0]);
        console.log(wordsDiv.children[0]);
    }

    inp.addEventListener("keydown", function(e) {
        if (activeItems === undefined) {
            changeActiveItems();
            currentFocus = activeItems.length - 1;
            removeActive(activeItems);
        }
        if (e.keyCode === 37 || e.keyCode === 39) {
            changeActiveItems();
            currentFocus = activeItems.length - 1;
            removeActive(activeItems);
        }
        else if (e.keyCode === 40) {
            currentFocus++;
            addActive(activeItems);
        } else if (e.keyCode === 38) { //up
            currentFocus--;
            addActive(activeItems);
        } else if (e.keyCode === 13) {
            e.preventDefault();
            if (currentFocus > -1) {
                if (activeItems) activeItems[currentFocus].click();
            }
        } else if (e.keyCode === 220) {
            console.log(arr);
        }
    });

    function addActive(x) {
        if (!x) return false;
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        x[currentFocus].classList.add("autocomplete-active");
        x[currentFocus].style.backgroundColor = "DodgerBlue";
    }

    function removeActive(x) {
        for (let i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
            x[i].style.backgroundColor = "white";
        }
    }

    function closeAllLists(elmnt) {
        const x = document.getElementsByClassName("autocomplete-items");
        // console.log();
        // console.log('Before: ', x);
        // console.log();
        for (let item of x) {
            item.remove();
        }
        if (x) {
            for (let item of x) {
                item.remove();
            }
        }
        // console.log();
        // console.log('After: ', x);
    }

    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}