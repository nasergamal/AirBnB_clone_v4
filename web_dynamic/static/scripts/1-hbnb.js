$(document).ready(() => {
  const checked = {};
  $('.amenities .popover input').click(function () {
    if ($(this).is(':checked')) {
      checked[$(this).attr('data-name')] = $(this).attr('data-id');
    } else {
      delete checked[$(this).attr('data-name')];
    }
    $('.amenities .added_amenities').text(Object.keys(checked).join(', '));
  });
});
