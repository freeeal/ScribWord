const navbar_element = document.getElementById('filter-navbar');
let topics_arr = [];

function reloadFilteredTopics(topic) {
  let all_card_elements = document.getElementsByClassName('card');
  console.log(all_card_elements)
  for (i = 0; i < all_card_elements.length; i++) {
    let thisEle = all_card_elements[i];
    if (topic !== 'all') {
      if (thisEle.id === topic) {
        thisEle.style.display = "block";
      } else {
        thisEle.style.display = "none";
      }
    } else {
      thisEle.style.display = "block";
    }
  }
}

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
        card.className = 'card bg-light';
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
          let cardTopic = document.createElement('button');
          cardTopic.className = 'btn btn-primary';
          // cardTopic.style.color = 'black';
          cardTopic.innerHTML = topic;
          cardBody.appendChild(cardTopic);
          if (!topics_arr.indexOf(topic) > -1) {
            topics_arr.push(topic);
          }
          // set card id to topic -- for filtering
          card.id = topic;
        });

      });
      // load initial navbar
      topics_arr.forEach((topic) => {
        let filterButton = document.createElement('button');
        filterButton.className = "btn btn-primary";
        filterButton.innerHTML = topic;
        filterButton.addEventListener("click", function() {
          reloadFilteredTopics(topic);
        });
        navbar_element.appendChild(filterButton);
      })
  });
}
