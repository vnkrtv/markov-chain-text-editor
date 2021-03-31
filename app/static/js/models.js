function renderModels() {
    const getAllModelsApiUrl = modelsApiUrl.replace('model_id', 'all');
    const modelsTBody = document.getElementById('modelsTBody');
    $.get(getAllModelsApiUrl)
        .done((response) => {
            if (response.error) {
                renderInfoModal('Error', response.error);
            } else {
                modelsTBody.innerHTML = '';
                for (let idx = 0; idx < response.length; idx++) {
                    let model = response[idx];
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <tr>
                            <th scope="row">${model.id}</th>
                            <td id="row_${idx}">
                                <img
                                    id="delImg${idx}" alt="Del" 
                                    title="Delete" src="${iconUrls.delete}" 
                                    style="display: none; cursor: pointer;" 
                                    data-toggle="modal" 
                                    data-target="#deleteModelModal" 
                                    onclick='fillDeleteModal(${model.id}, "${model.name}")'
                                 >     
                                <img 
                                    id="updImg${idx}" alt="Edit"
                                    title="Update" src="${iconUrls.update}" 
                                    style="display: none; cursor: pointer;" 
                                    data-toggle="modal" 
                                    data-target="#updateModelModal" 
                                    onclick='fillEditModal(${model.id}, "${model.name}")'
                                >
                            </td>
                            <td>${model.name}</t>
                            <td>${model.index_name}</td>
                            <td>${model.doc_count}</td>
                            <td>${model.size}</td>
                        </tr>
                    `;
                    tr.setAttribute('onmouseover', `showImages(${idx})`);
                    tr.setAttribute('onmouseout', `hideImages(${idx})`);
                    modelsTBody.appendChild(tr);
                }
            }
        });
}

function selectFolder(e) {
    let theFiles = e.target.files;
    let relativePath = theFiles[0].webkitRelativePath;
    let folder = relativePath.split("/");
    let filesStr = '';
    for (let filePath of theFiles) {
        filesStr += (filePath.name.split('.')[0] + '<separator>');
    }
    document.getElementById('files_names').value = filesStr.substr(0, filesStr.length - 11);
    document.getElementById('load-subject-name-label').children[1].value = folder[0];
}


function showImages(rowIdx) {
    document.getElementById(`delImg${rowIdx}`).style.display = "";
    document.getElementById(`updImg${rowIdx}`).style.display = "";
}

function hideImages(rowIdx) {
    document.getElementById(`delImg${rowIdx}`).style.display = "none";
    document.getElementById(`updImg${rowIdx}`).style.display = "none";
}

function fillEditModal(modelID, modelName) {
    // const idInput = document.getElementById('edit-subject-id');
    // idInput.value = subjectID;
    //
    // const subjectNameH3 = document.getElementById(`subject-name-${subjectID}`)
    // const nameInput = document.getElementById('edit-name');
    // nameInput.value = subjectNameH3.innerHTML;
    //
    // const subjectDescriptionP = document.getElementById(`subject-description-${subjectID}`)
    // const descriptionInput = document.getElementById('edit-description');
    // descriptionInput.value = subjectDescriptionP.innerHTML;
}

function fillDeleteModal(modelID, modelName) {
    const pDelete = document.getElementById('pDelete');
    pDelete.innerText = `Are you sure what you want to delete model '${modelName}'? This action can't be canceled.`;

    const deleteModelID = document.getElementById('idModelDelete');
    deleteModelID.value = `${modelID}`;

    const deleteModelButton = document.getElementById('deleteModelButton');
    deleteModelButton.onclick = () => {
        $.ajax({
            url: modelsApiUrl.replace('model_id', modelID),
            type: 'DELETE',
            success: function (response) {
                if (response.success) {
                    renderInfoModal('Model was deleted', response.success);
                    renderModels();
                } else {
                    renderInfoModal('Error', response.error);
                }
            }
        });
    }
}