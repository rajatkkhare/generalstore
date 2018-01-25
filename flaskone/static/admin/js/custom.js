function validate() {
    var email = $('#email');
    var password = $('#password');
    var err = 0;

    if (email.val() == '') {
        email.addClass('error-border');
        err = 1;
    } else email.removeClass('error-border');
    if (password.val() == '') {
        password.addClass('error-border');
        err = 1;
    } else password.removeClass('error-border');

    if (err) return false;
}
