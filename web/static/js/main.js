const { fromEvent, from, EMPTY } = rxjs;
const { debounceTime, map, switchMap, catchError, distinctUntilChanged, tap, filter } = rxjs.operators;
import { TickerCard, TickerButton } from "./buttons.js";

$(function () {
    let subscribedTickers = new Set();

    let searchBox = $('#search-box');
    let searchResults = $('#search-results');
    let addedTickers = $('#added-tickers');
    let details = $('#details');
    let documentPublisher = fromEvent(document, 'click');

    let source = new EventSource("/stream");
    let sourcePublisher = fromEvent(source, 'message').pipe(
        map(event => JSON.parse(event.data))
    )

    documentPublisher.subscribe( event => {
        // Check if the clicked element is part of the search container or search results
        if (!$(event.target).closest('#search-container').length) {
            // Clicked outside the search container, clear the search box
            $('#search-box').val('');
            // Hide the search results
            $('#search-results').hide();
        }
    });

    sourcePublisher.subscribe(data => {
        let dataArray = Object.entries(data).map(([key, value]) => `${key} - ${value?.open}`);
        $('#number').html(dataArray.join("<br/>")); // joining array elements with break line

        addedTickers.find('.ticker-button').each(function() {
            let button = $(this);
            let currency = button.attr("data-currency");
            let price = button.find(".ticker-price");
            let open = data[currency]?.open

            if (price.html() !== open) {
                price.stop().animate({ opacity: 0 }, 200, function() {
                    price.html(open);
                    price.animate({ opacity: 1 }, 200);
                });
            }
        });
    })

    function search(query) {
        if (query === '') return EMPTY

        return from($.ajax({
            url: '/search',
            method: "GET",
            data: { q: query },
        })).pipe();
    }

    const throttledInput = fromEvent(searchBox, 'keyup').pipe(
        map(event => event.target.value)
    );

    const searchRequest = throttledInput.pipe(
        debounceTime(100),
        distinctUntilChanged(),
        switchMap(text => search(text))
    )

    throttledInput.subscribe( text => {
        if (text === '') {
            searchResults.hide();
        } else {
            searchResults.show();
        }
    })

    searchRequest.subscribe( data => {
        searchResults.empty();
        data.data.forEach(function (currency) {
            if (!subscribedTickers.has(currency)) {
                let tickerButton = new AddTickerButton(currency);
                searchResults.append(tickerButton.element);
            }
        });
    });

    class AddTickerButton extends TickerButton {
        createButtonElement() {
            let button = super.createButtonElement();
            this.addButton = $('<button>').addClass('add-button').text('+');
            button.append(this.addButton)
            return button
        }

        setupEventListeners(currency) {
            super.setupEventListeners(currency);

            fromEvent(this.addButton, 'click')
            .pipe(
                tap( event => event.stopPropagation() ),
                tap(() => this.element.remove()),
                switchMap(() => subscribeToTicker(currency)),
                filter(() => !subscribedTickers.has(currency)),
                tap(() => {
                    subscribedTickers.add(currency);
                    let ticker = new RemoveTickerButton(currency);
                    addedTickers.append(ticker.element);

                    let card = new TickerCard(currency);
                    details.append(card.element);
                    console.log("TEST" + details)
                }),
                catchError(error => {
                    console.error(error);
                    return EMPTY; // You can return an EMPTY observable in case of an error
                })
            )
            .subscribe();
        }
    }

    class RemoveTickerButton extends TickerButton {
        createButtonElement() {
            let button = super.createButtonElement();
            this.removeButton = $('<button>').addClass('remove-button').text('-');
            button.append(this.removeButton);
            return button;
        }

        setupEventListeners(currency) {
            super.setupEventListeners(currency);

            fromEvent(this.removeButton, 'click')
            .pipe(
                tap(() => this.element.remove()),
                switchMap(() => unsubscribeFromTicker(currency)),
                filter(() => subscribedTickers.has(currency)),
                tap(() => {
                    subscribedTickers.delete(currency)
                }),
                catchError(error => {
                    console.error(error);
                    return EMPTY; // You can return an EMPTY observable in case of an error
                })
            )
            .subscribe();
        }
    }

    function subscribeToTicker(symbol) {
        let promise = $.ajax({
            url: "/subscribe",
            method: "POST",
            data: JSON.stringify({ symbol: symbol }),
            contentType: "application/json"
        });

        return from(promise).pipe()
    }

    function unsubscribeFromTicker(symbol) {
        let promise = $.ajax({
            url: "/unsubscribe",
            method: "POST",
            data: JSON.stringify({ symbol: symbol }),
            contentType: "application/json"
        });

        return from(promise).pipe()
    }
});

