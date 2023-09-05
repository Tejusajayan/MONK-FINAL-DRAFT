$(document).ready(function() {
    $('.add-btn').click(function(e) {
        e.preventDefault();
        var itemId = $(this).data('item-id');
        window.location.href='/product/'+itemId+'/'
    })      
});