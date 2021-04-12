function t9Plugin(textInput, phrasesDiv, t9ApiURL, userIndexName) {
    const apiURL = t9ApiURL;

    let indexName = userIndexName;
    let arr = [];

    let currentFocus;
    let activeItems;


    function updateLists() {
        let phrasesContainer, phraseInput;
        let cursorPosition = textInput['selectionStart'];
        let val = textInput.value.substr(0, cursorPosition);
        let ending = textInput.value.substr(cursorPosition);
        closeAllLists();
        if (!val) {
            return false;
        }
        currentFocus = -1;

        phrasesContainer = document.createElement("div");
        phrasesContainer.setAttribute("id", "autocomplete-list-phrases");
        phrasesContainer.setAttribute("class", "autocomplete-items");
        phrasesDiv.appendChild(phrasesContainer);

        let phraseLen = 1;

        let phraseList = val.split(" ");
        let isNewWord = (phraseList[phraseList.length - 1] === '')
        if (isNewWord) {
            phraseList = phraseList.slice(0, phraseList.length - 1);
        }
        let wordsCount = 1;
        let bufArray = [];
        let count = (wordsCount < phraseList.length ? wordsCount : phraseList.length);
        for (let i = 0; i < count; i++) {
            bufArray.push(phraseList[phraseList.length - count + i]);
        }
        let beginning = bufArray.join(' ');

        let phraseSet = new Set();
        for (let i = 0; i < arr.length; i++) {
            let phraseWords = arr[i].split(" ");
            let phrase = '';
            let startIdx = (isNewWord ? 1 : 0);
            let endIdx = (phraseWords.length - 1 < phraseLen ? phraseWords.length - 1 : phraseLen) + startIdx;
            for (let i = startIdx; i < endIdx; i++) {
                phrase += (phraseWords[i] + " ");
            }
            if (phraseSet.has(phrase) || phrase.length === 0) {
                continue
            }
            phraseSet.add(phrase);
            if ((phrase.substr(0, beginning.length).toLowerCase() === beginning.toLowerCase()) || isNewWord) {
                let valueLength = isNewWord ? 0 : beginning.length;

                phraseInput = document.createElement("div");
                phraseInput.className = 'form-control';
                phraseInput.style.cursor = "pointer";

                phraseInput.innerHTML = "<strong>" + phrase.substr(0, valueLength) + "</strong>";
                phraseInput.innerHTML += phrase.substr(valueLength);

                phraseInput.innerHTML += "<input type='hidden' value='" + phrase + "'>";

                phraseInput.addEventListener("click", function (e) {
                    textInput.value = '';
                    for (let i = 0; i < phraseList.length - count + (isNewWord ? 1 : 0); i++) {
                        textInput.value += (phraseList[i] + ' ');
                    }
                    let clickedValue = this.getElementsByTagName("input")[0].value;
                    textInput.value += clickedValue.substr(0, clickedValue.length - 1);
                    let selectionStart = textInput.value.length;
                    textInput.value += ending;
                    closeAllLists();
                    textInput.setSelectionRange(selectionStart, selectionStart);
                });
                phrasesContainer.appendChild(phraseInput);
            }
        }
        activeItems = phrasesDiv.children[0].getElementsByTagName("div");
    }

    textInput.addEventListener("input", function (e) {
        updateLists();
    });


    function updateT9Phrases() {
        let cursorPosition = textInput['selectionStart'];
        let val = textInput.value.substr(0, cursorPosition);
        let phraseList = val.split(" ");
        if (phraseList[phraseList.length - 1] === '') {
            phraseList = phraseList.slice(0, phraseList.length - 1);
        }
        let wordsCount = 1;
        let bufArray = [];
        let count = (wordsCount < phraseList.length ? wordsCount : phraseList.length);
        for (let i = 0; i < count; i++) {
            bufArray.push(phraseList[phraseList.length - count + i]);
        }
        let beginning = bufArray.join(' ');
        console.debug('count: ', count);
        console.debug('phraseList: ', phraseList);
        console.debug('bufArray: ', bufArray);
        console.debug('beginning: ', beginning);

        let formData = new FormData();
        formData.append('indexName', indexName);
        formData.append('beginning', beginning.toLowerCase());
        formData.append('firstWordsCount', wordsCount.toString());
        formData.append('phraseLength', '1');

        $.ajax({
            url: apiURL,
            type: 'post',
            data: formData,
            contentType: false,
            processData: false,
            // headers: {
            //     'Content-Type': 'application/json',
            //     "Access-Control-Allow-Origin": "*"
            // },
            success: (response) => {
                if (response["sentences"] !== undefined) {
                    arr = response["sentences"];
                    console.log('arr: ', arr);
                    updateLists();
                }
            }
        });
    }

    textInput.addEventListener("input", function (e) {
        updateT9Phrases();
    });

    textInput.addEventListener("keydown", function (e) {
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
        } else if (e.keyCode === 17) {
            currentFocus++;
            addActive(activeItems);
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
        for (let item of x) {
            item.remove();
        }
        if (x) {
            for (let item of x) {
                item.remove();
            }
        }
    }

    textInput.addEventListener('keyup', function () {
        if (this.scrollTop > 0) {
            this.style.height = this.scrollHeight + "px";
        }
    });

    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}

function activatePlugin(t9ApiURL, indexName, t9CssClassName) {
    for (let textInput of document.getElementsByTagName('textarea')) {
        let phrasesDiv = document.createElement('div');
        textInput.parentNode.insertBefore(phrasesDiv, textInput.nextSibling);

        textInput.classList.add(t9CssClassName);
        phrasesDiv.classList.add(t9CssClassName);

        t9Plugin(textInput, phrasesDiv, t9ApiURL, indexName);
    }
    for (let textInput of document.getElementsByTagName('input')) {
        let phrasesDiv = document.createElement('div');
        textInput.parentNode.insertBefore(phrasesDiv, textInput.nextSibling);

        textInput.classList.add(t9CssClassName);
        phrasesDiv.classList.add(t9CssClassName);

        t9Plugin(textInput, phrasesDiv, t9ApiURL, indexName);
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const t9ApiURLHiddenInput = document.createElement('input');
    t9ApiURLHiddenInput.setAttribute('id', 't9ApiURLHiddenInput');
    t9ApiURLHiddenInput.setAttribute('type', 'hidden');
    t9ApiURLHiddenInput.setAttribute('value', '/api/t9');

    const indexNameHiddenInput = document.createElement('input');
    indexNameHiddenInput.setAttribute('id', 'indexNameHiddenInput');
    indexNameHiddenInput.setAttribute('type', 'hidden');
    indexNameHiddenInput.setAttribute('value', 't9-index-606ed615e7c351fd86f46c1e');

    const t9ApiURL = t9ApiURLHiddenInput.value;
    const indexName = indexNameHiddenInput.value;
    const t9CssClassName = 'autocomplete';

    activatePlugin(t9ApiURL, indexName, t9CssClassName);

    indexNameHiddenInput.onchange = () => {
        const t9ApiURL = t9ApiURLHiddenInput.value;
        const indexName = indexNameHiddenInput.value;
        activatePlugin(t9ApiURL, indexName, t9CssClassName);
    }
}); // end ready