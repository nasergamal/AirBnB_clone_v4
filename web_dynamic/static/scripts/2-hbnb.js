$(document).ready(() => {
  const checked = {};
  $('.amenities .popover input').click(function () {
    if (this.checked) {
      checked[this.dataset.name] = this.dataset.id;
    } else {
      delete checked[this.dataset.name];
    }
    $('.amenities .added_amenities').text(Object.keys(checked).join(', '));
  });
  $.getJSON('http://127.0.0.1:5001/api/v1/status/', function (data) {
    if (data.status === 'OK') {
      $('div#api_status').addClass('available');
    } else {
      $('div#api_status').removeClass('available');
    }
  });
});
