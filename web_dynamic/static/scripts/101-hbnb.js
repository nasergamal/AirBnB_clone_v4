$(document).ready(() => {
  const amenities = {};
  const states = {};
  const cities = {};
  $('.popover input').bind('change', (eve) => {
    const target = eve.currentTarget;
    let di;
    if (target.className === 'amenity_input') {
      di = amenities;
    } else if (target.className === 'state_input') {
      di = states;
    } else {
      di = cities;
    }
    if (target.checked) {
      di[target.dataset.name] = target.dataset.id;
    } else {
      delete di[target.dataset.name];
    }
    if (target.className === 'amenity_input') {
      $('.amenities .added_amenities').text(Object.keys(amenities).join(', '));
    } else {
      $('.locations .lo').text(Object.keys(Object.assign({}, states, cities)).join(', '));
    }
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
      data: JSON.stringify({ amenities: Object.values(amenities), states: Object.values(states), cities: Object.values(cities) }),
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
            <div class="description">
              <p>${datum.description}</p>
            </div>
            <div class='reviews'>
              <h2>Reviews</h2>
              <span class="toggle" onclick="review(this)" data-id="${datum.id}">show</span>
              <ul>
              </ul>
            </div>
      </article>`);
        }
      }
    });
  }
  $('.filters button').bind('click', search);
  search();
});
function review (place) {
  if (place.textContent === 'show') {
    place.textContent = 'hide';
    const ur = `http://127.0.0.1:5001/api/v1/places/${place.dataset.id}/reviews`;
    $.ajax({
      type: 'GET',
      url: ur,
      success: function (reviews) {
        $(`*[data-id="${place.dataset.id}"]`).prev().text(reviews.length + ' Reviews');
        for (const rev of reviews) {
          const date = new Date(rev.created_at);
          const day = getOrdinalNum(date.getDate());
          const mon = date.toLocaleString('en', { month: 'long' });
          $.get(`http://127.0.0.1:5001/api/v1/users/${rev.user_id}`, function (data) {
            $(`*[data-id="${place.dataset.id}"]`).next().append(`<li>
                       <h3>From ${data.first_name} ${data.last_name} the ${day} ${mon} ${date.getFullYear()}</h3>
                       <p>${rev.text}</p>
                      </li>`);
          });
        }
      }
    });
  } else {
    place.textContent = 'show';
    $(`*[data-id="${place.dataset.id}"]`).prev().text('Reviews');
    $(`*[data-id="${place.dataset.id}"]`).next().empty();
  }
}
function getOrdinalNum (n) {
  return n + (n > 0 ? ['th', 'st', 'nd', 'rd'][(n > 3 && n < 21) || n % 10 > 3 ? 0 : n % 10] : '');
}
