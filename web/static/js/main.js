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

document.addEventListener("DOMContentLoaded", function() {
    var tickerButtons = document.getElementsByClassName("ticker-button");
    var subscribedTickers = new Set();

    for (var i = 0; i < tickerButtons.length; i++) {
        (function() {
            var button = tickerButtons[i];
            var currency = button.getAttribute("data-currency");

            button.addEventListener("click", function() {
                var isSubscribed = subscribedTickers.has(currency);
                console.log(subscribedTickers)
                if (isSubscribed) {
                    // Unsubscribe logic
                    subscribedTickers.delete(currency);
                    this.classList.remove("subscribed");
                    unsubscribeFromTicker(currency);
                } else {
                    // Subscribe logic
                    subscribedTickers.add(currency);
                    this.classList.add("subscribed");
                    subscribeToTicker(currency);
                }
            });
        })();
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

