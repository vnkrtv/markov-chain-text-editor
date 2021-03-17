function autocomplete(inp, arr, t9ApiURL) {
    const apiURL = t9ApiURL;
    const textInput = document.getElementById("text");
    const phrasesDiv = document.getElementById("t9-phrases");
    const phraseLenInput = document.getElementById("phrase-len");
    const firstWordsInput = document.getElementById("first-words");

    let currentFocus;
    let activeItems;

    function updateLists() {
        let phrasesContainer, phraseInput
        let val = textInput.value;
        closeAllLists();
        if (!val) {
            return false;
        }
        currentFocus = -1;

        phrasesContainer = document.createElement("div");
        phrasesContainer.setAttribute("id", "autocomplete-list-phrases");
        phrasesContainer.setAttribute("class", "autocomplete-items");
        phrasesDiv.appendChild(phrasesContainer);

        let phraseLen = parseInt(phraseLenInput.value);

        let phraseList = val.split(" ");
        let wordsCount = parseInt(firstWordsInput.value);
        let bufArray = [];
        let count = (wordsCount < phraseList.length ? wordsCount : phraseList.length);
        for (let i = 0; i < count; i++) {
            bufArray.push(phraseList[phraseList.length - count + i]);
        }
        let beginning = bufArray.join(' ');

        for (let i = 0; i < arr.length; i++) {
            let phraseWords = arr[i].split(" ");
            let phrase = '';
            for (let i = 0; i < (phraseWords.length - 1 < phraseLen ? phraseWords.length - 1 : phraseLen); i++) {
                phrase += (phraseWords[i] + " ");
            }
            if (phrase.substr(0, beginning.length).toLowerCase() === beginning.toLowerCase()) {
                let valueLength = beginning.length;

                phraseInput = document.createElement("div");
                phraseInput.className = 'form-control';
                phraseInput.style.cursor = "pointer";

                phraseInput.innerHTML = "<strong>" + phrase.substr(0, valueLength) + "</strong>";
                phraseInput.innerHTML += phrase.substr(valueLength);

                phraseInput.innerHTML += "<input type='hidden' value='" + phrase + "'>";

                phraseInput.addEventListener("click", function (e) {
                    inp.value = '';
                    for (let i = 0; i < phraseList.length - count; i++) {
                        inp.value += (phraseList[i] + ' ');
                    }
                    let clickedValue = this.getElementsByTagName("input")[0].value;
                    inp.value += clickedValue.substr(0, clickedValue.length - 1);
                    closeAllLists();
                });
                phrasesContainer.appendChild(phraseInput);
            }
        }
        activeItems = phrasesDiv.children[0].getElementsByTagName("div");
    }

    inp.addEventListener("input", (e) => {
        updateLists();
    });

    phraseLenInput.onkeyup = phraseLenInput.onchange = () => {
        updateLists();
    }

    function updateT9Phrases() {
        let val = textInput.value.toString();
        let phraseList = val.split(" ");
        let wordsCount = parseInt(firstWordsInput.value);
        let bufArray = [];
        let count = (wordsCount < phraseList.length ? wordsCount : phraseList.length);
        for (let i = 0; i < count; i++) {
            bufArray.push(phraseList[phraseList.length - count + i]);
        }
        let beginning = bufArray.join(' ');

        $.post(apiURL, {
            beginning: beginning.toLowerCase(),
            firstWordsCount: wordsCount,
            phraseLength: phraseLenInput.value,
        }).done(function (response) {
            if (response.sentences !== undefined) {
                arr = response.sentences;
                console.log('arr: ', arr);
                updateLists();
            }
        });
    }

    inp.addEventListener("input", (e) => {
        updateT9Phrases();
    });

    firstWordsInput.onkeyup = firstWordsInput.onchange = () => {
        updateT9Phrases();
    }

    inp.addEventListener("keydown", (e) => {
        if (e.keyCode === 40) {
            currentFocus++;
            addActive(activeItems);
        } else if (e.keyCode === 38) {
            currentFocus--;
            addActive(activeItems);
        } else if (e.keyCode === 13) {
            e.preventDefault();
            if (currentFocus > -1) {
                if (activeItems) activeItems[currentFocus].click();
            }
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

    function closeAllLists(elem) {
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

    inp.addEventListener('keyup', () => {
        if (this.scrollTop > 0) {
            this.style.height = this.scrollHeight + "px";
        }
    });

    document.addEventListener("click", (e) => {
        closeAllLists(e.target);
    });

}
