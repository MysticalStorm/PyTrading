const { fromEvent, from, EMPTY } = rxjs;
const { debounceTime, map, switchMap, catchError, distinctUntilChanged, tap, filter } = rxjs.operators;

$(function () {
    // Create a chart
    const chart = LightweightCharts.createChart(document.getElementById('chart'), {
        width: document.getElementById('chart').clientWidth,
        height: 300
    });

    // Add a candlestick series to the chart
    const candleSeries = chart.addCandlestickSeries();

    // Sample data
    const data = [
        { time: '2019-04-11', open: 80.01, high: 96.53, low: 76.64, close: 94.20 },
        { time: '2019-04-12', open: 94.20, high: 114.75, low: 90.01, close: 107.21 },
        // Add more data points here
    ];

    // Set the data for our series
    candleSeries.setData(data);

    // Optionally, you can customize the chart further (e.g., colors, markers)
});