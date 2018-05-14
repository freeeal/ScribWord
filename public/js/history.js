const navbar_element = document.getElementById('filter-navbar');
let topics_arr = [];

function reloadFilteredTopics(topic) {
  let all_card_elements = document.getElementsByClassName('card');
  for (i = 0; i < all_card_elements.length; i++) {
    let thisEle = all_card_elements[i];
    if (topic !== 'all') {
      if (thisEle.id.includes(topic)) {
        thisEle.style.display = "block";
      } else {
        thisEle.style.display = "none";
      }
    } else {
      thisEle.style.display = "block";
    }
  }
}

function reloadFilterButtons(topic) {
  let all_filter_buttons = document.querySelectorAll(".topic-btn");
  all_filter_buttons.forEach((button) => {
    t = button.innerHTML;
    if (t==topic){
      button.classList.remove('btn-secondary');
      button.classList.add('btn-primary');
    }else{
      button.classList.remove('btn-primary');
      button.classList.add('btn-secondary');
    }
  });
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
        card.id = '';
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
        obj['topTopics'].forEach((topic, i) => {
          let cardTopic = document.createElement('button');
          cardTopic.className = 'btn btn-primary';
          cardTopic.innerHTML = topic;
          cardTopic.addEventListener("click", function() {
            toggleKeywordGraph(cardBody, obj['keywords'][i]);
          });

          cardBody.appendChild(cardTopic);
          if (!topics_arr.includes(topic)) {
            topics_arr.push(topic);
            console.log(topics_arr)
          }
          // set card id to topic -- for filtering
          card.id += topic + ' ';
        });

        let compareTopicButton = document.createElement('copyButton');
        compareTopicButton.className = 'btn btn-info';
        compareTopicButton.innerHTML = 'Compare Topics';
        compareTopicButton.setAttribute('style', 'float:right');
        compareTopicButton.addEventListener("click", function() {
          toggleCompareGraph(cardBody, obj['allTopics'], obj['likelihoods']);
        });

        cardBody.appendChild(compareTopicButton);
      });

      // load initial navbar
      topics_arr.forEach((topic) => {
        let filterButton = document.createElement('button');
        filterButton.className = "btn btn-secondary topic-btn";
        filterButton.innerHTML = topic;
        filterButton.addEventListener("click", function() {
          reloadFilteredTopics(topic);
          reloadFilterButtons(topic);
        });
        filterButton.id = "topic" + topic;
        navbar_element.appendChild(filterButton);
      })
  });
}

// function to toggle keyword bar chart of selected topic
function toggleKeywordGraph(cardBody, keywordObj) {
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

  // toggle functionality
  let svgExists = false;
  for (i = 0; i < cardBody.childNodes.length; i++) {
    let childNode = cardBody.childNodes[i];
    if (childNode.nodeName === "svg") {
      svgExists = true;
    }
  }

  if (!svgExists) {
    // add the SVG element
    var svg = d3.select(cardBody).append("svg")
        .attr("id", "keyword")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

    // load the data
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
    
    // Scroll svg into view
    cardBody.scrollIntoView({behavior: "smooth"});
  } else {
    console.log(cardBody.lastChild);
    cardBody.removeChild(cardBody.lastChild);
    toggleKeywordGraph(cardBody, keywordObj)
  }

}

// function to toggle keyword bar chart of selected topic
function toggleCompareGraph(cardBody, allTopics, allLikelihoods) {
  console.log(allTopics);
  console.log(allLikelihoods);
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

  // toggle functionality
  let svgExists = false;
  for (i = 0; i < cardBody.childNodes.length; i++) {
    let childNode = cardBody.childNodes[i];
    if (childNode.nodeName === "svg") {
      svgExists = true;
    }
  }

  if (!svgExists) {
    // add the SVG element
    var svg = d3.select(cardBody).append("svg")
        .attr("id", "compare")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

    // load the data
    let topics = allTopics;
    let likelihoods = allLikelihoods;
    let dataArray = [];

    for (let i=0; i<topics.length; i++) {
      dataArray.push(
        {
          "Topic": topics[i],
          "Likelihood": likelihoods[i]
        }
      )
    }

    // scale the range of the data
    x.domain(dataArray.map(function(d) { return d.Topic; }));
    y.domain([0, d3.max(dataArray, function(d) { return d.Likelihood; })]);

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
        .text("Topic Likelihood");

    // Add bar chart
    svg.selectAll("bar")
        .data(dataArray)
      .enter().append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return x(d.Topic); })
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(d.Likelihood); })
        .attr("height", function(d) { return height - y(d.Likelihood); });

    // Scroll graph into view
    cardBody.scrollIntoView({behavior: "smooth"});
  } else {
    console.log(cardBody.lastChild);
    console.log(cardBody.lastChild.id)
    cardBody.removeChild(cardBody.lastChild);
    toggleCompareGraph(cardBody, allTopics, allLikelihoods);
  }

}

// processSpeech(transcript);
//  Is called anytime speech is recognized by the Web Speech API
// Input:
//    transcript, a string of possibly multiple words that were recognized
// Output:
//    processed, a boolean indicating whether the system reacted to the speech or not
var processSpeech = function(transcript) {
  // Helper function to detect if any commands appear in a string
  console.log("processing...");
  var userSaid = function(str, commands) {
    for (var i = 0; i < commands.length; i++) {
      if (str.indexOf(commands[i]) > -1)
        return true;
    }
    return false;
  };

  var processed = false;
  console.log(transcript);

  topics_arr.forEach((topic) => {
    console.log(transcript)
    if (userSaid(transcript.toLowerCase(),['display ' + topic.toLowerCase()])) {
      console.log('displaying ' + topic)
      document.getElementById('topic' + topic).click();
      processed = true;
    }
  })

  if (userSaid(transcript.toLowerCase(),['display all'])) {
    console.log('displaying All')
    document.getElementById('topicAll').click();
    processed = true;
  }

  return processed;
};
