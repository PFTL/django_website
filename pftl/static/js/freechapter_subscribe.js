$(document).ready(function () {
  $('#free-chapter').submit(function (event) {
    event.preventDefault();
    var data = $(this).serialize();
    $.ajax({
        type: "POST",
        url: "/free_chapter/",
        data: data,
        beforeSend: function () {
          $("#send").prop("disabled", true);
          $("#send").text("Sending");
        },
        success: function (data) {
          $("#newsletter_feedback").html('<div class="alert alert-primary" role="alert">Thanks for signing up to our newsletter!</div>');
        },
        error: function (data) {
          $("#newsletter_feedback").html('<div class="alert alert-danger" role="alert">An error ocurred, please try again!</div>');
        }
       });
  });
});
