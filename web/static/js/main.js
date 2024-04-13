const { fromEvent, from, EMPTY } = rxjs;
const { debounceTime, map, switchMap, catchError, distinctUntilChanged, tap, filter } = rxjs.operators;
import { TickerCard, TickerButton } from "./buttons.js";

$(function () {
    let subscribedTickers = new Set();
    let addedTickers = $('#added-tickers');
    let details = $('#details');

    function subscribeOnStream(ticker) {
        let source = new EventSource(`/stream?ticker=${ticker}`);
        let sourcePublisher = fromEvent(source, 'message').pipe(
            map(event => JSON.parse(event.data))
        )

        sourcePublisher.subscribe(data => {
            let dataArray = Object.entries(data).map(([key, value]) => `${key} - ${value?.open}`);

            addedTickers.find('.ticker-button').each(function() {
                let button = $(this);
                let currency= button.attr("data-currency");
                let price= button.find(".ticker-price");
                let open = data[currency]?.open

                if (price.html() !== open) {
                    price.stop().animate({ opacity: 0 }, 200, function() {
                        price.html(open);
                        price.animate({ opacity: 1 }, 200);
                    });
                }
            });
        })
    }

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
                    console.log("Tap: " + details)
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

            fromEvent(this.element, 'click')
            .pipe(
                tap(event => {
                    window.location.href = `/details?currency=${currency}`;
                })
            )
            .subscribe()

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

    $(document).on('click', '#search-trigger', function() {
        $(this).replaceWith('<input id="search-box" type="text" placeholder="Search...">');
        $('#search-box').focus(); // Automatically focus the new input
        initializeSearchBoxEvents();
    });

    function initializeSearchBoxEvents() {
        const searchBox = $('#search-box'); // Make sure this targets the newly created search box
        const searchResults = $('#search-results');
        let documentPublisher = fromEvent(document, 'click');

        let bag = disposedBag("search-box")

        documentPublisher.subscribe( event => {
            // Check if the clicked element is part of the search container or search results
            if (!$(event.target).closest('#search-container').length) {
                // Clicked outside the search container, clear the search box
                searchBox.val('');
                // Hide the search results
                searchResults.hide();
                searchBox.replaceWith('<p id="search-trigger">Search</p>');
            }
        });

        const throttledInput = fromEvent(searchBox, 'keyup').pipe(
            map(event => event.target.value)
        );

        throttledInput.subscribe(text => {
            console.log(text)
            if (text === '') {
                searchResults.hide();
            } else {
                searchResults.show();
            }
        });

        const searchRequest = throttledInput.pipe(
            debounceTime(100),
            distinctUntilChanged(),
            switchMap(text => search(text))
        );

        subscribe(
            searchRequest.subscribe( data => {
                searchResults.empty();
                data.data.forEach(function (currency) {
                    if (!subscribedTickers.has(currency)) {
                        let tickerButton = new AddTickerButton(currency);
                        searchResults.append(tickerButton.element);
                    }
                });
        }), bag);

        throttledInput.subscribe( text => {
            if (text === '') {
                searchResults.hide();
            } else {
                searchResults.show();
            }
        });

        function search(query) {
            if (query === '') return EMPTY

            return from($.ajax({
                url: '/search',
                method: "GET",
                data: { q: query },
            })).pipe();
        }
    }

    function subscribe(observable, bag) {
        bag.add(observable)
    }

    function disposedBag(scope) {
        // Check if the scope exists and has a `unsubscribeAll` method
        if (window[scope] && typeof window[scope].unsubscribeAll === 'function') {
            window[scope].unsubscribeAll();
        } else {
            // If not, create a new composite subscription and assign it to window[scope]
            window[scope] = createCompositeSubscription();
        }
        return window[scope]
    }

    function createCompositeSubscription() {
    const subscriptions = [];
    return {
        add: (subscription) => subscriptions.push(subscription),
        unsubscribeAll: () => {
            subscriptions.forEach(subscription => subscription.unsubscribe());
            subscriptions.length = 0; // Clear the array after unsubscribing
        }
    };
}

});

