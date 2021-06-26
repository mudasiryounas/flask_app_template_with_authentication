function show_loading(selector) {
    $(selector).LoadingOverlay("show", {
        fade: [50, 1000]
    });
}

function hide_loading(selector) {
    $(selector).LoadingOverlay("hide", {
        fade: [50, 1000]
    });
}

function show_reload_msg() {
    Swal(500, 'Something went wrong, please reload the page and try again!', 'error');
}

function Swal(title, html, type, timer = 10000, show_close_button = true, split_lines = false) {
    if (split_lines) {
        html = html.replace(/(?:\r\n|\r|\n)/g, '<br>');
    }
    swal({
        position: 'bottom-end',
        html: html,
        type: type,
        showConfirmButton: false,
        showCloseButton: show_close_button,
        timer: timer,
        footer: '<img src="/static/img/logo/mfm-logo.png" style="width:80px;height:24px;" />',
    });
}

function swal_confirm(callback, title = "Are you sure?", confirmButtonText = 'Delete') {
    swal({
        type: 'warning',
        title: title,
        html: '',
        customClass: 'swal-wide',
        showCancelButton: true,
        showCloseButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: confirmButtonText
    }).then((result) => {
        if (result.value) {
            callback();
        }
    });

    $('.swal-wide').attr('style', 'display: flex;width: 720px !important;');
}