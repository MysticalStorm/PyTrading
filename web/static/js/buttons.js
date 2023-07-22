export class TickerButton {
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

    setupEventListeners(currency) {}
}

export class TickerCard {
    constructor(currency) {
        this.currency = currency;
        this.element = this.createCard();
    }

    createCard() {
        const card = $('<div>').addClass('ticker-card').attr('data-currency', this.currency);
        const nameElement = $('<span>').addClass('ticker-name').text(this.currency);
        const priceElement = $('<span>').addClass('ticker-price');
        card.append(nameElement, priceElement)
        return card
    }
}