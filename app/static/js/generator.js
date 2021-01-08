function getSampleDiv(phrase, idx) {
    const phraseDiv = document.createElement('div');
    phraseDiv.classList.add('jumbotron');

    const phraseH3 = document.createElement('h3');
    phraseH3.innerText = `Sample ${idx}`;

    const phraseP = document.createElement('p');
    phraseP.innerText = phrase

    phraseDiv.appendChild(phraseH3);
    phraseDiv.appendChild(phraseP);

    return phraseDiv;
}

function renderSamples(samples, outputDiv) {
    outputDiv.innerHTML = '';
    for (let i = 0; i < samples.length; i++) {
        outputDiv.appendChild(getSampleDiv(samples[i], i + 1))
    }
}

function generateSamples(generatorAPIRef) {
    const loadingDiv = document.getElementById("loadingContainer");
    const outputH3 = document.getElementById("outputH3");
    const outputDiv = document.getElementById("outputDiv");
    const phraseInput = document.getElementById("phraseInput");
    const samplesNum = document.getElementById("samplesNum");
    const modelSelect = document.getElementById("modelSelect");

    let params = {
        phrase: phraseInput.value,
        samplesNum: parseInt(samplesNum.value),
        modelID: parseInt(modelSelect.value)
    }

    loadingDiv.style.display = '';
    outputH3.style.display = 'none';
    outputDiv.style.display = 'none';
    $.post(generatorAPIRef, params)
        .done((response) => {
            renderSamples(response['samples'], outputDiv);
            outputH3.style.display = '';
            outputDiv.style.display = '';
            loadingDiv.style.display = 'none'
        });
}
