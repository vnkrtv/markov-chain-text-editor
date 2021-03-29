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

function fillEditModal(subjectID) {
    const idInput = document.getElementById('edit-subject-id');
    idInput.value = subjectID;

    const subjectNameH3 = document.getElementById(`subject-name-${subjectID}`)
    const nameInput = document.getElementById('edit-name');
    nameInput.value = subjectNameH3.innerHTML;

    const subjectDescriptionP = document.getElementById(`subject-description-${subjectID}`)
    const descriptionInput = document.getElementById('edit-description');
    descriptionInput.value = subjectDescriptionP.innerHTML;
}