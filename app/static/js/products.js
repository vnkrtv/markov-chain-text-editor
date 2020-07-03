function fillDeleteModal(id) {
    const elemChildren = document.getElementById(id).children;
    const product_id = elemChildren[1].children[0].innerHTML;
    const name = elemChildren[2].innerHTML;
    document.querySelector('input#del_id').value = product_id;
    document.querySelector('p#del_info').innerHTML = `Are you sure that you want to remove ${name}?` +
        ` This action cannot be canceled.`
}

function fillUpdateModal(id) {
    const elemChildren = document.getElementById(id).children;

    document.querySelectorAll('input#name.form-control')[1].value = elemChildren[2].innerHTML;
    document.querySelectorAll('input#quantity.form-control')[1].value = elemChildren[4].innerHTML;
    document.querySelectorAll('input#price.form-control')[1].value = elemChildren[6].innerHTML;
    document.querySelectorAll('input#promotion.form-control')[1].value = elemChildren[7].innerHTML;

    document.querySelector('input#upd_id').value = elemChildren[1].children[0].innerHTML;

    let val = elemChildren[3].innerHTML;
    let sel = document.querySelectorAll('select#producer.form-control')[1];
    let opts = sel.options;

    for (let j = 0;; j++) {
        if (opts[j].innerHTML === val) {
            sel.selectedIndex = j;
            break;
        }
    }

	val = elemChildren[5].innerHTML;
    sel = document.querySelectorAll('select#supplier.form-control')[1];
    opts = sel.options;

    for (let j = 0;; j++) {
        if (opts[j].innerHTML === val) {
            sel.selectedIndex = j;
            break;
        }
    }

}