let b = baffle('.testb', {
    speed: 100
});

b.start();
$('.testb').show();
b.reveal(1500);

/* PUBLICATION */

var init = function() {
    bibtexify("#bibtex", "pubTable", {});
};
if (window.addEventListener) {
   window.addEventListener('load', init, false);
} else if (window.attachEvent) {
   window.attachEvent('onload', init);
}

$("#pubTable").on("click", "a", function(e) {
  var $n = $(this),
      text = $n.text().toUpperCase();
  if (text === "X") { return; }
  try {
    _gaq.push(['_trackEvent', "PublicationAction", text]);
} catch(err){ }
  if ($n.attr("href") !== "#") {
    setTimeout(function() {
      document.location.href = $n.attr("href");
    }, 100);
    return false;
  }
});