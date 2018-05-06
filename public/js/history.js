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
        col.className = 'col-sm-12';
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

          cardTopic.addEventListener("click", function() {
            toggleKeywordGraph(cardBody, obj['keywords']);
          });
          cardTopic.innerHTML = topic;
          cardBody.appendChild(cardTopic);
          if (!topics_arr.indexOf(topic) > -1) {
            topics_arr.push(topic);
          }
          // set card id to topic -- for filtering
          card.id = topic;
        });

        let linebreak = document.createElement("br");
        cardBody.appendChild(linebreak);
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

// function to toggle keyword bar chart of selected topic
function toggleKeywordGraph(cardBody, keywordArr) {
  // set the dimensions of the canvas
  var margin = {top: 20, right: 20, bottom: 70, left: 52},
      width = 600 - margin.left - margin.right,
      height = 300 - margin.top - margin.bottom;

  // set the ranges
  var x = d3.scale.ordinal().rangeRoundBands([0, width], .05);

  var y = d3.scale.linear().range([height, 0]);

  // define the axis
  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom")

  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")
      .ticks(10);

  // add the SVG element
  var svg = d3.select(cardBody).append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

  // load the data
  let keywordObj = keywordArr[0];
  let dataArray = [];

  for (let keyword in keywordObj) {
    dataArray.push(
      {
        "Keyword": keyword,
        "Strength": keywordObj[keyword]
      }
    )
  }

  // scale the range of the data
  x.domain(dataArray.map(function(d) { return d.Keyword; }));
  y.domain([0, d3.max(dataArray, function(d) { return d.Strength; })]);

  // add axis
  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
    .selectAll("text")
      .style("text-anchor", "end")
      .attr("dx", "-.8em")
      .attr("dy", "-.55em")
      .attr("transform", "rotate(-90)" )

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left)
      .attr("x",0 - (height / 2))
      .attr("dy", ".71em")
      .style("text-anchor", "middle")
      .text("Keyword Strength");

  // Add bar chart
  svg.selectAll("bar")
      .data(dataArray)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.Keyword); })
      .attr("width", x.rangeBand())
      .attr("y", function(d) { return y(d.Strength); })
      .attr("height", function(d) { return height - y(d.Strength); });
}
