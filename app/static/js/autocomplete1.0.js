function autocomplete(inp, arr, t9ApiURL) {
    const apiURL = t9ApiURL;
    const textInput = document.getElementById("text");
    const wordsDiv = document.getElementById("t9-words");
    const phrasesDiv = document.getElementById("t9-phrases");
    const phraseLenInput = document.getElementById("phrase-len");
    const firstWordsInput = document.getElementById("first-words");

    let currentFocus;
    let bufferPhrase = "";
    let activeItems;
    // let requestsStack = [];

    function updateLists(t9RenderResponse = false) {
        let wordsContainer, phrasesContainer, wordInput, phraseInput
        let val = textInput.value;
        console.log('updateLists!');
        console.log('arr: ', arr);
        closeAllLists();
        if (!val) {
            return false;
        }
        currentFocus = -1;

        wordsContainer = document.createElement("div");
        wordsContainer.setAttribute("id", "autocomplete-list-words");
        wordsContainer.setAttribute("class", "autocomplete-items");
        wordsDiv.appendChild(wordsContainer);

        phrasesContainer = document.createElement("div");
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
            for (let i = 0; i < (phraseWords.length - 1 < phraseLen ? phraseWords.length - 1 : phraseLen); i++) {
                phrase += (phraseWords[i] + " ");
            }
            if ((phrase.substr(0, value.length).toUpperCase() === value.toUpperCase()) || (value.length = 0) || t9RenderResponse) {

                let valueLength = t9RenderResponse ? 0 : value.length;

                wordInput = document.createElement("div");
                wordInput.className = 'form-control';
                wordInput.style.cursor = "pointer";

                wordInput.innerHTML = "<strong>" + firstWord.substr(0, valueLength) + "</strong>";
                wordInput.innerHTML += firstWord.substr(valueLength);

                wordInput.innerHTML += "<input type='hidden' value='" + firstWord + "'>";

                wordInput.addEventListener("click", function (e) {
                    inp.value = "";
                    for (let i = 0; i < phraseList.length - 1; i++) {
                        inp.value += (phraseList[i] + " ");
                    }
                    let clickedValue = this.getElementsByTagName("input")[0].value;
                    inp.value += clickedValue.substr(0, clickedValue.length - 1);
                    closeAllLists();
                });
                wordsContainer.appendChild(wordInput);

                phraseInput = document.createElement("div");
                phraseInput.className = 'form-control';
                phraseInput.style.cursor = "pointer";

                phraseInput.innerHTML = "<strong>" + phrase.substr(0, valueLength) + "</strong>";
                phraseInput.innerHTML += phrase.substr(valueLength);

                phraseInput.innerHTML += "<input type='hidden' value='" + phrase + "'>";

                phraseInput.addEventListener("click", function (e) {
                    inp.value = "";
                    for (let i = 0; i < phraseList.length - 1; i++) {
                        inp.value += (phraseList[i] + " ");
                    }
                    let clickedValue = this.getElementsByTagName("input")[0].value;
                    inp.value += clickedValue.substr(0, clickedValue.length - 1);
                    closeAllLists();
                });
                phrasesContainer.appendChild(phraseInput);
            }
        }
        changeActiveItems();
    }

    inp.addEventListener("input", function (e) {
        updateLists();
    });

    phraseLenInput.onkeyup = phraseLenInput.onchange = () => {
        updateLists();
    }

    function updateT9Phrases() {
        let val = textInput.value.toString();
        if (val[val.length - 1] === " ") {
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

                    console.log('Make T9 request...');
                    $.post(apiURL, {
                        beginning: bufferPhrase.substr(0, bufferPhrase.length - 1).toLowerCase(),
                        firstWordsCount: wordsCount,
                        phraseLength: phraseLenInput.value,
                    }).done(function (response) {
                        if (response.sentences !== undefined) {
                            arr = response.sentences;
                            console.log('arr: ', arr);
                            updateLists(true);
                        }
                    });
                }
            }
        }
    }

    inp.addEventListener("input", function (e) {
        updateT9Phrases();
    });

    firstWordsInput.onkeyup = firstWordsInput.onchange = () => {
        updateT9Phrases();
    }

    function changeActiveItems() {
        wordsDiv.classList.toggle("hide-element");
        phrasesDiv.classList.toggle("hide-element");
        // console.log();
        if (wordsDiv.classList.contains("hide-element")) {
            // console.log('phrases');
            activeItems = phrasesDiv.children[0];
        } else {
            // console.log('words');
            activeItems = wordsDiv.children[0];
        }
        if (activeItems) activeItems = activeItems.getElementsByTagName("div");
        // console.log('changeActiveItems: ', activeItems);
        // console.log(phrasesDiv.children[0]);
        // console.log(wordsDiv.children[0]);
    }

    inp.addEventListener("keydown", function (e) {
        if (activeItems === undefined) {
            changeActiveItems();
            currentFocus = activeItems.length - 1;
            removeActive(activeItems);
        }
        if (e.keyCode === 39) {
            changeActiveItems();
            currentFocus = activeItems.length - 1;
            removeActive(activeItems);
        } else if (e.keyCode === 40) {
            currentFocus++;
            // console.log('40: ', activeItems);
            // console.log(phrasesDiv.children[0]);
            // console.log(wordsDiv.children[0]);
            addActive(activeItems);
        } else if (e.keyCode === 38) { //up
            currentFocus--;
            // console.log('38: ', activeItems);
            // console.log(phrasesDiv.children[0]);
            // console.log(wordsDiv.children[0]);
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
        // console.log('Before adding active style: ', x[currentFocus].innerHTML);
        x[currentFocus].classList.add("autocomplete-active");
        x[currentFocus].style.backgroundColor = "DodgerBlue";
        // console.log('After adding active style: ', x[currentFocus].innerHTML);
        // console.log('currentFocus: ', currentFocus);
    }

    function removeActive(x) {
        for (let i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
            x[i].style.backgroundColor = "white";
        }
    }

    function closeAllLists(elmnt) {
        const x = document.getElementsByClassName("autocomplete-items");
        for (let item of x) {
            item.remove();
        }
        if (x) {
            for (let item of x) {
                item.remove();
            }
        }
    }

    inp.addEventListener('keyup', function () {
        if (this.scrollTop > 0) {
            this.style.height = this.scrollHeight + "px";
        }
    });

    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}