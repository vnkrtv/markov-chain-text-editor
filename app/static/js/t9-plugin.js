function t9Plugin(textInput, phrasesDiv, t9ApiURL, userIndexName, csrfToken) {
    const apiURL = t9ApiURL;
    const csrfTokenStr = csrfToken;

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
        formData.append('modelName', indexName);
        formData.append('beginning', beginning.toLowerCase());
        formData.append('firstWordsCount', wordsCount.toString());
        formData.append('phraseLength', '1');

        // let headers = new Headers();
        // headers.append('Content-Type', 'application/json');
        // headers.append('Access-Control-Allow-Origin', '*');

        $.ajax({
            url: apiURL,
            type: 'post',
            data: formData,
            contentType: false,
            processData: false,
            headers: {
                'X-CSRFToken': csrfTokenStr
            },
            success: (response) => {
                if (response["sentences"] !== undefined) {
                    arr = response["sentences"];
                    console.log('arr: ', arr);
                    updateLists();
                }
            },
            error: (jqXHR, textStatus, errorThrown) => {
                console.log('jqXHR: ', jqXHR);
                console.log('textStatus: ', textStatus);
                console.log('errorThrown: ', errorThrown);
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

function activatePlugin(querySelector, t9ApiURL, indexName, t9CssClassName, csrfToken) {
    for (let textInput of document.querySelectorAll(querySelector)) {
        let phrasesDiv = document.createElement('div');
        textInput.parentNode.insertBefore(phrasesDiv, textInput.nextSibling);

        textInput.classList.add(t9CssClassName);
        phrasesDiv.classList.add(t9CssClassName);

        t9Plugin(textInput, phrasesDiv, t9ApiURL, indexName, csrfToken);
    }
    for (let textInput of document.getElementsByTagName('input')) {
        let phrasesDiv = document.createElement('div');
        textInput.parentNode.insertBefore(phrasesDiv, textInput.nextSibling);

        textInput.classList.add(t9CssClassName);
        phrasesDiv.classList.add(t9CssClassName);

        t9Plugin(textInput, phrasesDiv, t9ApiURL, indexName, csrfToken);
    }
}

function PredictiveInput(querySelectors, t9ApiURL, indexName, csrfToken) {
    const t9CssClassName = 'autocomplete';
    for (let querySelector of querySelectors) {
        activatePlugin(querySelector, t9ApiURL, indexName, t9CssClassName, csrfToken);
    }
};

/*
document.addEventListener('DOMContentLoaded', function () {
    PredictiveInput(
        querySelectors=['textarea', 'input'],
        t9ApiURL='http://serverurl/api/t9',
        indexName='t9-index-606ed615e7c351fd86f46c1e'
    );
}); // end ready
*/