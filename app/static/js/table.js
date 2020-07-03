function main() {
    const table = document.getElementById('table');

    for (let i = 1; i <= table.rows.length; i++) {
        document.getElementById(`del_img_${i}`).style.display = "none";
        document.getElementById(`upd_img_${i}`).style.display = "none";
    }
}

function showImages(row_index) {
    document.getElementById(`del_img_${row_index}`).style.display = "";
    document.getElementById(`upd_img_${row_index}`).style.display = "";
}

function hideImages(row_index) {
    document.getElementById(`del_img_${row_index}`).style.display = "none";
    document.getElementById(`upd_img_${row_index}`).style.display = "none";
}

function tableSearch(input_id, table_id) {
    const phrase = document.getElementById(input_id);
    const table = document.getElementById(table_id);
    const regPhrase = new RegExp(phrase.value, 'i');
    let flag = false;
    for (let i = 1; i < table.rows.length; i++) {
        flag = false;
        for (let j = table.rows[i].cells.length - 1; j >= 0; j--) {
            flag = regPhrase.test(table.rows[i].cells[j].innerHTML);
            if (flag) break;
        }
        if (flag) {
            table.rows[i].style.display = "";
        } else {
            table.rows[i].style.display = "none";
        }
    }
}

function sortTableByNums(table_id, column_num, has_child) {
    const table = document.getElementById(table_id);
    let rows, i, x, y, shouldSwitch;
    let switchCount = 0;
    let switching = true;
    let dir = "asc";

    while (switching) {
        switching = false;
        rows = table.rows;

        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;

            x = rows[i].getElementsByTagName("TD")[column_num];
            if (has_child) {
                x = x.firstChild;
            }
            y = rows[i + 1].getElementsByTagName("TD")[column_num];
            if (has_child) {
                y = y.firstChild;
            }
            if (dir === "asc") {
                if (Number(x.innerHTML) > Number(y.innerHTML)) {
                    shouldSwitch = true;
                    break;
                }
            } else if (dir === "desc") {
                if (Number(x.innerHTML) < Number(y.innerHTML)) {
                    shouldSwitch = true;
                    break;
                }
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchCount ++;
        } else {
            if (switchCount === 0 && dir === "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}

function sortTable(table_id, column_num) {
    const table = document.getElementById(table_id);
    let rows, i, x, y, shouldSwitch;
    let switchCount = 0;
    let switching = true;
    let dir = "asc";

    while (switching) {
        switching = false;
        rows = table.rows;

        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;

            x = rows[i].getElementsByTagName("TD")[column_num];
            y = rows[i + 1].getElementsByTagName("TD")[column_num];
            if (dir === "asc") {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                  shouldSwitch = true;
                  break;
                }
            } else if (dir === "desc") {
            if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                shouldSwitch = true;
                break;
                }
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchCount ++;
        } else {
            if (switchCount === 0 && dir === "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}
