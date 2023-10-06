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
  function search () {
    $.ajax({
      type: 'POST',
      url: 'http://127.0.0.1:5001/api/v1/places_search/',
      contentType: 'application/json',
      data: JSON.stringify({ amenities: Object.values(checked) }),
      success: function (data) {
        $('section.places').empty();
        for (const datum of Object.values(data).sort()) {
          $('section.places').append(`<article>
            <div class="headline">
              <h2>${datum.name}</h2>
              <div class="price_by_night">$${datum.price_by_night}</div>
            </div>
            <div class="information">
              <div class="max_guest">
                <div class="guest_icon"></div>
                <p>${datum.max_guest} Guests</p>
              </div>
              <div class="number_rooms">
                <div class="bed_icon"></div>
                <p>${datum.number_rooms} Bedroom</p>
              </div>
                <div class="number_bathrooms">
                <div class="bath_icon"></div>
                <p>${datum.number_bathrooms} Bathroom</p>
            </div>
            </div>
            <div class="description" style="white-space: pre-wrap;">
              <p>${datum.description}</p>
            </div>
      </article>`);
        }
      }
    });
  }
  $('.filters button').bind('click', search);
  search();
});
