setTimeout(function() {
  $(document).ready(function () {
    var rating_count = $("div.star-ratings-rating-count span.star-ratings-rating-value").html();
    if(rating_count == "0") {
      var textarea = $("textarea[name='user_rating_comment_text']");
      textarea 
        .attr("disabled","disabled")
        .attr("placeholder", "Please rate before adding comments.");
    }

    $(".star-ratings-rate-action").each(function() {
      $(this).bind("click", function() { window.location.reload(); });
    });
  });
}, 500)
function saveforms(){
  $("#opportunityform").submit();
  $("#commentform").submit();
}

