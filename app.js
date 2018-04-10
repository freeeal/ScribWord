const express = require('express');
const bodyParser = require('body-parser')
const path = require('path');
const child_process = require('child_process');
// const fs = require('fs');

const app = express();

// handle static files
app.use(express.static(path.join(__dirname, 'public')));

// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: false }))

// parse application/json
app.use(bodyParser.json())

app.get('/', (req, res) => res.sendFile('index.html', { root: path.join(__dirname, '') }));

app.post('/analyze', (req, res) => {
  console.log(req.body);
  let conversationTranscript = req.body;

  // spawn child_process to run topic modeling script
  let spawn = child_process.spawn;
  var py  = spawn('python3', ['topic_modelling/compute_input.py']);
  var data = [1,2,3,4,5,6,7,8,9];
  var dataString = '';

  py.stdout.on('data', function(response){
    dataString += response.toString();
  });
  py.stdout.on('end', function(){
    console.log('Sum of numbers =', dataString);
    res.send(dataString); // send result as string back to frontend
  });

  py.stdin.write(JSON.stringify(conversationTranscript.text));
  py.stdin.end();

  // fs.readFile('data.json', 'utf8', function readFileCallback(err, data){
  //     if (err){
  //         console.log(err);
  //     } else {
  //       obj = JSON.parse(data); //now its an object
  //       obj.table.push(newConversation); //add some data
  //       json = JSON.stringify(obj); //convert it back to json
  //       fs.writeFile('data.json', json, 'utf8', callback); // write it back
  // }});
});

// 404 route
app.use((req, res, next) => {
  const err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// route error handler
app.use((err, req, res, next) => {
  res.status(err.status || 500);
  res.send({
    status: err.status,
    message: err.message,
  });
});

app.listen(8000, () => console.log('App listening on port 8000...'))
