var source = new EventSource("/stream");

source.onmessage = function(event) {
  var numberElement = document.getElementById("number");
  var eventData = JSON.parse(event.data);
  numberElement.innerHTML = eventData.open;

  // Update ticker button with the received price
  var tickerButtons = document.getElementsByClassName("ticker-button");
  for (var i = 0; i < tickerButtons.length; i++) {
    var button = tickerButtons[i];
    var currency = button.getAttribute("data-currency");
    var tickerPriceElement = button.querySelector(".ticker-price");

    if (currency === eventData.symbol) {
      tickerPriceElement.innerHTML = eventData.open;
    }
  }
};

$(function () {
    console.log("DOM LOADED2");
})

$(document).ready(function() {
    console.log("DOM LOADED1");

    var subscribedTickers = new Set();
    var searchBox = $('#search-box');
    var searchResults = $('#search-results');
    var addedTickers = $('#added-tickers');

    searchBox.on('input', function() {
        var query = this.value.toLowerCase();
        if (query === '') {
            searchResults.hide();
            return;
        } else {
            searchResults.show();
        }

        // Clear previous results
        searchResults.empty();

        // Fetch matching tickers from server
        $.ajax({
            url: '/search',
            method: 'GET',
            data: { q: query },
            success: function(data) {
                console.log(data)
                data.data.forEach(function(currency) {
                    let tickerButton = new TickerButton(currency);
                    searchResults.append(tickerButton.element);
                });
            }
        });
    });

    class TickerButton {
      constructor(currency) {
        this.currency = currency;
        this.element = this.createButtonElement();
        this.setupEventListeners();
      }

      createButtonElement() {
        const button = $('<button>').addClass('ticker-button').attr('data-currency', this.currency);
        const nameElement = $('<span>').addClass('ticker-name').text(this.currency);
        const priceElement = $('<span>').addClass('ticker-price');
        const addButton = $('<button>').addClass('add-button').text('+');
        const removeButton = $('<button>').addClass('remove-button').text('-');
        button.append(nameElement, priceElement, addButton);
        return button;
      }

      setupEventListeners() {
        this.element.on('click', '.remove-button', () => {
          this.element.remove();
          // Perform other necessary operations when the remove button is clicked
        });

        this.element.on('click', '.add-button', () => {
          this.element.remove();
          // Perform other necessary operations when the remove button is clicked
        });
      }
    }

/*
    searchResults.on('click', '.add-button', function() {
      var button = $(this).parent();
      var currency = button.data('currency');

      if (!subscribedTickers.has(currency)) {
        subscribedTickers.add(currency);
        subscribeToTicker(currency);

        var tickerButton = new TickerButton(currency);
        addedTickers.append(tickerButton.element);

        button.remove();
      }
    });

    addedTickers.on('click', '.remove-button', function() {
        var button = $(this).parent();
        var currency = button.data('currency');

        // Check if ticker is already subscribed to remove it
        if (subscribedTickers.has(currency)) {
            subscribedTickers.delete(currency);
            unsubscribeFromTicker(currency);

            // Remove this ticker from the "added-tickers" list
            button.remove();
        }
    });
*/

    function subscribeToTicker(symbol) {
        // Send subscription request to the server
        fetch("/subscribe", {
            method: "POST",
            body: JSON.stringify({ symbol: symbol }),
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(function(response) {
            if (response.ok) {
                console.log("Subscription request successful");
            } else {
                console.error("Subscription request failed");
            }
        })
        .catch(function(error) {
            console.error("Error sending subscription request:", error);
        });
    }

    function unsubscribeFromTicker(symbol) {
        // Send unsubscribe request to the server
        fetch("/unsubscribe", {
            method: "POST",
            body: JSON.stringify({ symbol: symbol }),
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(function(response) {
            if (response.ok) {
                console.log("Unsubscription request successful");
            } else {
                console.error("Unsubscription request failed");
            }
        })
        .catch(function(error) {
            console.error("Error sending unsubscription request:", error);
        });
    }
});

