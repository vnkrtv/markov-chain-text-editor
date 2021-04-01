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
                            <td id="row_${idx}">
                                <img
                                    id="delImg${idx}" alt="Del" 
                                    title="Delete" src="${iconUrls.delete}" 
                                    style="display: none; cursor: pointer;" 
                                    data-toggle="modal" 
                                    data-target="#deleteModelModal" 
                                    onclick='fillDeleteModal("${model.id}", "${model.name}")'
                                 >     
                                <img 
                                    id="updImg${idx}" alt="Edit"
                                    title="Update" src="${iconUrls.update}" 
                                    style="display: none; cursor: pointer;" 
                                    data-toggle="modal" 
                                    data-target="#updateModelModal" 
                                    onclick='fillEditModal("${model.id}", "${model.name}")'
                                >
                            </td>
                            <th>${model.id}</th>
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
    const filesNamesInput = document.getElementById('filesNames');
    const selectedFilesP = document.getElementById('selectedFiles');

    let filesStr = '';
    selectedFilesP.innerText = '\nSelected files:\n';
    for (let file of e.target.files) {
        filesStr += (file.name.split('.')[0] + '<separator>');
        selectedFilesP.innerText += ` - ${file.name}\n`
    }
    filesNamesInput.value = filesStr.substr(0, filesStr.length - 11);

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

function fillAddModal() {
    const addModelModalTitle = document.getElementById('addModelModalTitle');
    addModelModalTitle.innerHTML = 'Add model';
    const addModelButton = document.getElementById('addModelButton');
    addModelButton.onclick = () => {
        const modelName = document.getElementById('name');
        const dataSource = document.getElementById("dataSourceOptionSelect");

        let formData = new FormData();
        formData.append('name', modelName.value);

        if (dataSource.selectedIndex === 0) { // single file
            formData.append('data_source', 'file');
            const trainFile = document.getElementById('trainFile');
            formData.append('train_file', trainFile.files[0]);

        } else if (dataSource.selectedIndex === 1) { // folder with text files
            formData.append('data_source', 'folder');
            const trainFiles = document.getElementById('trainFiles');
            for (let file of trainFiles.files) {
                formData.append(file.name, file);
            }

        } else if (dataSource.selectedIndex === 2) { // postgresql
            formData.append('data_source', 'postgres');
            const pgHost = document.getElementById('pgHost');
            const pgPort = document.getElementById('pgPort');
            const pgUser = document.getElementById('pgUser');
            const pgPassword = document.getElementById('pgPassword');
            const pgDBName = document.getElementById('pgDBName');
            const pgQuery = document.getElementById('pgQuery');

            formData.append('pg_host', pgHost.value);
            formData.append('pg_port', pgPort.value);
            formData.append('pg_user', pgUser.value);
            formData.append('pg_password', pgPassword.value);
            formData.append('pg_dbname', pgDBName.value);
            formData.append('sql_query', pgQuery.value);
        }
        for (let key of formData) {
            console.log(key, formData[key]);
        }

        $.ajax({
            url: modelsApiUrl.replace('model_id', 'new'),
            type: 'post',
            data: formData,
            contentType: false,
            processData: false,
            success: (response) => {
                if (response.success) {
                    renderModels();
                    renderInfoModal("New model", response.success);
                } else {
                    renderInfoModal("Error", response.error);
                }
            }
        });

    };

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