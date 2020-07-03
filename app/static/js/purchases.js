function fillDeleteModal(id) {
    const elemChildren = document.getElementById(id).children;
    const purchase_id = elemChildren[1].children[0].innerHTML;
    document.querySelector('input#del_id').value = purchase_id;
    document.querySelector('p#del_info').innerHTML = `Are you sure that you want to remove purchase with ID ${purchase_id}?` +
        ` This action cannot be canceled.`
}

function fillUpdateModal(id) {
    const elemChildren = document.getElementById(id).children;

    document.querySelectorAll('input#quantity.form-control')[1].value = elemChildren[5].innerHTML;
    document.querySelectorAll('input#date.form-control')[1].value = elemChildren[6].innerHTML;
    document.querySelectorAll('input#total_cost.form-control')[1].value = elemChildren[7].innerHTML;

    document.querySelector('input#upd_id').value = elemChildren[1].children[0].innerHTML;

    let val = elemChildren[2].innerHTML;
    let sel = document.querySelectorAll('select#product_id.form-control')[1];
    let opts = sel.options;

    for (let j = 0;; j++) {
        if (opts[j].innerHTML === val) {
            sel.selectedIndex = j;
            break;
        }
    }

	val = elemChildren[3].innerHTML;
    sel = document.querySelectorAll('select#worker_id.form-control')[1];
    opts = sel.options;

    for (let j = 0;; j++) {
        if (opts[j].innerHTML === val) {
            sel.selectedIndex = j;
            break;
        }
    }

    val = elemChildren[4].innerHTML;
    sel = document.querySelectorAll('select#customer_id.form-control')[1];
    opts = sel.options;

    for (let j = 0;; j++) {
        if (opts[j].innerHTML === val) {
            sel.selectedIndex = j;
            break;
        }
    }

}