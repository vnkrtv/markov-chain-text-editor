function fillDeleteModal(id) {
    const elemChildren = document.getElementById(id).children;
    const card_id = elemChildren[1].children[0].innerHTML;
    const discount = elemChildren[2].innerHTML;
    document.querySelector('input#del_id').value = card_id;
    document.querySelector('p#del_info').innerHTML = `Are you sure that you want to remove card with discount ${discount * 100}%?` +
        ` This action cannot be canceled.`
}

function fillUpdateModal(id) {
    const elemChildren = document.getElementById(id).children;

    document.querySelectorAll('input#discount.form-control')[1].value = elemChildren[2].innerHTML;
    document.querySelectorAll('input#start_date.form-control')[1].value = elemChildren[3].innerHTML;
    document.querySelectorAll('input#expiration.form-control')[1].value = elemChildren[4].innerHTML;

    document.querySelector('input#upd_id').value = elemChildren[1].children[0].innerHTML;
}