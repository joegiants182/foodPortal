$(function () {
    $('.confirm-on-submit').on("submit", function(event) {
        if(!confirm("Are you sure you want to do that?\nThis action cannot be undone!")) {
            event.preventDefault();
            return false;
        }
    });
    $('[data-toggle="popover"]').popover({
        placement: 'auto'
    });
})
