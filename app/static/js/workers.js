function fillDeleteModal(id) {
    const elemChildren = document.getElementById(id).children;
    const worker_id = elemChildren[1].children[0].innerHTML;
    const fullname = elemChildren[2].innerHTML;
    document.querySelector('input#del_id').value = worker_id;
    document.querySelector('p#del_info').innerHTML = `Are you sure that you want to remove ${fullname}?` +
        ` This action cannot be canceled.`
}

function fillUpdateModal(id) {
    const elemChildren = document.getElementById(id).children;

    document.querySelectorAll('input#fullname.form-control')[1].value = elemChildren[2].innerHTML;
    document.querySelectorAll('input#salary.form-control')[1].value = elemChildren[3].innerHTML;
    document.querySelectorAll('input#job.form-control')[1].value = elemChildren[4].innerHTML;
    document.querySelectorAll('input#address.form-control')[1].value = elemChildren[5].innerHTML;
    document.querySelectorAll('input#email.form-control')[1].value = elemChildren[8].innerHTML;
    document.querySelectorAll('input#telephone.form-control')[1].value = elemChildren[7].innerHTML;
    document.querySelectorAll('input#passport_number.form-control')[1].value = elemChildren[6].innerHTML;

    document.querySelector('input#upd_id').value = elemChildren[1].children[0].innerHTML;
}