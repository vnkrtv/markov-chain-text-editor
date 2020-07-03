function fillDeleteModal(id) {
    const elemChildren = document.getElementById(id).children;
    const customer_id = elemChildren[1].children[0].innerHTML;
    const fullname = elemChildren[2].innerHTML;
    document.querySelector('input#del_id').value = customer_id;
    document.querySelector('p#del_info').innerHTML = `Are you sure that you want to remove ${fullname}?` +
        ` This action cannot be canceled.`
}

function fillUpdateModal(id) {
    const elemChildren = document.getElementById(id).children;

    document.querySelectorAll('input#fullname.form-control')[1].value = elemChildren[2].innerHTML;
    document.querySelectorAll('input#address.form-control')[1].value = elemChildren[4].innerHTML;
    document.querySelectorAll('input#email.form-control')[1].value = elemChildren[5].innerHTML;
    document.querySelectorAll('input#telephone.form-control')[1].value = elemChildren[6].innerHTML;

    document.querySelector('input#upd_id').value = elemChildren[1].children[0].innerHTML;

    const val = elemChildren[3].innerHTML;
    const sel = document.querySelectorAll('select#card_id.form-control')[1];
    const opts = sel.options;

    for (let j = 0;; j++) {
        if (opts[j].innerHTML === val) {
            sel.selectedIndex = j;
            break;
        }
    }

}