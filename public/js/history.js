function loadData() {
  let historicalData;
  fetch('/getHistoricalData')
    .then(response => response.json())
    .then(json => {
      console.log(json)
      historicalData = json
      let feed = document.getElementById('history-feed');
      for (let dateTime in historicalData) {
        let col = document.createElement('div');
        col.className = 'col-sm-6';
        feed.appendChild(col);

        let card = document.createElement('div');
        card.className = 'card';
        col.appendChild(card);

        let cardBody = document.createElement('div');
        cardBody.className = 'card-body';
        card.appendChild(cardBody);

        let cardTitle = document.createElement('h5');
        cardTitle.className = 'card-title';
        cardTitle.innerHTML = new Date(parseInt(dateTime));
        cardBody.appendChild(cardTitle);

        let cardText = document.createElement('p');
        cardText.className = 'card-text';
        cardText.innerHTML = historicalData[dateTime];
        cardBody.appendChild(cardText);

        // append topics
      }
    });
}
