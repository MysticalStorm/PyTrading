let source = new EventSource("/stream");
const { fromEvent, from } = rxjs;
const { debounceTime, map, switchMap, catchError, distinctUntilChanged } = rxjs.operators;


source.onmessage = function(event) {
  let numberElement = document.getElementById("number");
  let eventData = JSON.parse(event.data);
  numberElement.innerHTML = eventData.open;

  // Update ticker button with the received price
  let tickerButtons = document.getElementsByClassName("ticker-button");
  for (let i = 0; i < tickerButtons.length; i++) {
    let button = tickerButtons[i];
    let currency = button.getAttribute("data-currency");
    let tickerPriceElement = button.querySelector(".ticker-price");

    if (currency === eventData.symbol) {
      tickerPriceElement.innerHTML = eventData.open;
    }
  }
};

$(function () {
    let subscribedTickers = new Set();
    let searchBox = $('#search-box');
    let searchResults = $('#search-results');
    let addedTickers = $('#added-tickers');

    function searchWikipedia(query) {
        return from($.ajax({
            url: '/search',
            method: "GET",
            data: { q: query },
        })).pipe();
    }

    let throttledInput = fromEvent(searchBox, 'keyup').pipe(
        map(event => event.target.value),
        debounceTime(500),
        distinctUntilChanged(),
        switchMap(text => searchWikipedia(text))
    )

    throttledInput.subscribe( data => {
        data.data.forEach(function (currency) {
                let tickerButton = new AddTickerButton(currency);
                searchResults.append(tickerButton.element);
        });
    });

 /*
    searchBox.on('input', function() {
        let query = this.value.toLowerCase();
        if (query === '') {
            searchResults.hide();
            return;
        } else {
            searchResults.show();
        }

        function search(data) {
            searchResults.empty();
            data.data.forEach(function (currency) {
                let tickerButton = new AddTickerButton(currency);
                searchResults.append(tickerButton.element);
            });
        }

        // Fetch matching tickers from server
        $.ajax({
            url: '/search',
            method: 'GET',
            data: { q: query },
            success: search
        });
    });

  */

    class TickerButton {
      constructor(currency) {
        this.currency = currency;
        this.element = this.createButtonElement();
        this.setupEventListeners(currency);
      }

      createButtonElement() {
        const button = $('<button>').addClass('ticker-button').attr('data-currency', this.currency);
        const nameElement = $('<span>').addClass('ticker-name').text(this.currency);
        const priceElement = $('<span>').addClass('ticker-price');
        button.append(nameElement, priceElement);
        return button;
      }

      setupEventListeners(currency) {
        this.element.on('click', '.remove-button', () => {
          this.element.remove();
          if (subscribedTickers.has(currency)) {
              subscribedTickers.delete(currency);
              unsubscribeFromTicker(currency);
          }
        });

        this.element.on('click', '.add-button', () => {
          this.element.remove();
          if (!subscribedTickers.has(currency)) {
            subscribedTickers.add(currency)
            subscribeToTicker(currency)
          }
        });
      }
    }

    class AddTickerButton extends TickerButton {
        createButtonElement() {
            let button = super.createButtonElement();
            const addButton = $('<button>').addClass('add-button').text('+');
            button.append(addButton)
            return button
        }
    }

    class RemoveTickerButton extends TickerButton {
        createButtonElement() {
            let button = super.createButtonElement();
            const removeButton = $('<button>').addClass('remove-button').text('-');
            button.append(removeButton)
            return button
        }
    }

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
                let ticker = new RemoveTickerButton(symbol)
                addedTickers.append(ticker.element)
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

