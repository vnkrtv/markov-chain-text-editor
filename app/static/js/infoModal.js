function renderInfoModal(title, message) {
    const infoModalTitle = document.getElementById('infoModalTitle');
    const pInfoModal = document.getElementById('pInfoModal');

    infoModalTitle.innerText = title;
    pInfoModal.innerText = message;

    $('#infoModal').modal('show');
}
