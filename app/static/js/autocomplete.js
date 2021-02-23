function getT9Hashtable(apiURL) {
    let t9Dict = {};
    $.get(apiURL).done((response) => {
        if (response.words) {
            for (let word of response.words) {
                let firstLetter = word[0];
                if (t9Dict[firstLetter]) {
                    t9Dict[firstLetter].push(word);
                } else {
                    t9Dict[firstLetter] = [word];
                }
            }
            for (let key in t9Dict) {
                t9Dict[key].sort();
            }
            return t9Dict;
        }
    });
}

function autocomplete(inp, t9Hashtable) {
    const textInput = document.getElementById("text");
    const wordsDiv = document.getElementById("t9-words");

    let currentFocus;
    let activeItems;

    function updateLists() {
        let wordsContainer, wordInput;
        let val = textInput.value;
        let inputWords = val.split(" ");
        let inputWord = inputWords[inputWords.length - 1];
        console.log('inputWord: ', inputWord);

        closeAllLists();
        if (!inputWord.length) {
            return false;
        }
        let arr = t9Hashtable[inputWord[0]];
        currentFocus = -1;

        wordsContainer = document.createElement("div");
        wordsContainer.setAttribute("id", "autocomplete-list-words");
        wordsContainer.setAttribute("class", "autocomplete-items");
        wordsDiv.appendChild(wordsContainer);

        for (let i = 0; i < arr.length; i++) {
            let word = arr[i];
            if (word.substr(0, inputWord.length).toUpperCase() === inputWord.toUpperCase()) {

                wordInput = document.createElement("div");
                wordInput.className = 'form-control';
                wordInput.style.cursor = "pointer";

                wordInput.innerHTML = "<strong>" + word.substr(0, inputWord.length) + "</strong>";
                wordInput.innerHTML += word.substr(inputWord.length);

                wordInput.innerHTML += "<input type='hidden' value='" + word + "'>";

                wordInput.addEventListener("click", function (e) {
                    inp.value = "";
                    for (let i = 0; i < inputWords.length - 1; i++) {
                        inp.value += (inputWords[i] + " ");
                    }
                    let clickedValue = this.getElementsByTagName("input")[0].value;
                    inp.value += clickedValue.substr(0, clickedValue.length);
                    closeAllLists();
                });
                wordsContainer.appendChild(wordInput);
            }
        }
        changeActiveItems();
    }

    inp.addEventListener("input", function (e) {
        updateLists();
    });

    function changeActiveItems() {
        wordsDiv.classList.remove("hide-element");
        activeItems = wordsDiv.children[0];
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