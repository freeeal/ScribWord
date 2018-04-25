function loadData() {
  let historicalData;
  fetch('/getHistoricalData')
    .then(response => response.json())
    .then(json => {
      console.log(json)
      historicalDataArr = json['conversations'];
      let feed = document.getElementById('history-feed');
      historicalDataArr.forEach((obj) => {
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
        cardTitle.innerHTML = new Date(parseInt(obj['dateTime']));
        cardBody.appendChild(cardTitle);

        let cardText = document.createElement('p');
        cardText.className = 'card-text';
        cardText.innerHTML = obj['text'];
        cardBody.appendChild(cardText);

        // append topics
        obj['topics'].forEach((topic) => {
          let cardTopic = document.createElement('a');
          cardTopic.className = 'btn btn-primary';
          cardTopic.innerHTML = topic;
          cardBody.appendChild(cardTopic)
        });

      });
    });
}
