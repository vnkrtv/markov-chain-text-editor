function autocomplete(inp, arr) {
    let currentFocus;
    let bufferWord = "";
    let phraseLen = 5;
    let activeItems;

    inp.addEventListener("input", function(e) {
        let wordsContainer, phrasesContainer, wordInput, phraseInput
        let val = this.value;
        closeAllLists();
        if (!val) { return false;}
        currentFocus = -1;

        wordsContainer = document.createElement("DIV");
        wordsContainer.setAttribute("id", "autocomplete-list-words");
        wordsContainer.setAttribute("class", "autocomplete-items");
        document.getElementById("t9-words").appendChild(wordsContainer);

        phrasesContainer = document.createElement("DIV");
        phrasesContainer.setAttribute("id", "autocomplete-list-phrases");
        phrasesContainer.setAttribute("class", "autocomplete-items");
        document.getElementById("t9-phrases").appendChild(phrasesContainer);

        for (let i = 0; i < arr.length; i++) {
            let phraseList = val.split(" ");
            let value = phraseList[phraseList.length - 1];
            let firstWord = arr[i].split(" ")[0];
            if ((arr[i].substr(0, value.length).toUpperCase() === value.toUpperCase()) && (value.length > 0)) {
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

                phraseInput.innerHTML = "<strong>" + arr[i].substr(0, value.length) + "</strong>";
                phraseInput.innerHTML += arr[i].substr(value.length);

                phraseInput.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";

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
    });

    inp.addEventListener("input", function(e) {
        let val = this.value.toString();
        console.log(arr)
        if (val[val.length - 1] === " ") {
            console.log(val, val[val.length - 1], val.split(" "))
            let phraseList = val.split(" ");
            if (phraseList.length > 1) {
                if (phraseList[phraseList.length - 2] !== bufferWord) {
                    bufferWord = phraseList[phraseList.length - 2];
                    $.post('/t9', {
                        word: bufferWord.toLowerCase(),
                    }).done(function(response) {
                        arr = response['words']
                    });
                }
            }
        }
    });

    function changeActiveItems() {
        if (this.counter === undefined) {
            this.counter = 0;
        }
        this.counter += 1;
        document.getElementById("t9-words").classList.toggle("hide-element");
        document.getElementById("t9-phrases").classList.toggle("hide-element");
        if (this.counter % 2) {
            activeItems = document.getElementById("autocomplete-list-phrases");
        } else {
            activeItems = document.getElementById("autocomplete-list-words");
        }
        if (activeItems) activeItems = activeItems.getElementsByTagName("div");
    }

    inp.addEventListener("keydown", function(e) {
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
        for (let i = 0; i < x.length; i++) {
            if (elmnt !== x[i] && elmnt !== inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }

    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}