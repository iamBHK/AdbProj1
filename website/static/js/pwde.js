$(document).on('click', '.toggle-pwd', function() {

    $(this).toggleClass("fa-eye fa-eye-slash");
    
    var input = $("#pwd");
    input.attr('type') === 'password' ? input.attr('type','text') : input.attr('type','password')
});
$(document).on('click', '.toggle-npwd', function() {

    $(this).toggleClass("fa-eye fa-eye-slash");
    
    var input = $("#npwd");
    input.attr('type') === 'password' ? input.attr('type','text') : input.attr('type','password')
});
$(document).on('click', '.toggle-cnpwd', function() {

    $(this).toggleClass("fa-eye fa-eye-slash");
    
    var input = $("#cnpwd");
    input.attr('type') === 'password' ? input.attr('type','text') : input.attr('type','password')
});