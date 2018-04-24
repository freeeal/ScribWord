const express = require('express');
const app = express();

const bodyParser = require('body-parser')
const path = require('path');
const logger = require('morgan');
const child_process = require('child_process');
const fs = require('fs');

// handle static files
app.use(express.static(path.join(__dirname, 'public')));

app.use(logger('dev'));
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: false }))

app.get('/', (req, res) => res.sendFile('index.html', { root: path.join(__dirname, '') }));
app.get('/history', (req, res) => res.sendFile('history.html', { root: path.join(__dirname, '') }));

app.get('/getHistoricalData', (req, res) => {
  purgeCache('./data.json');
  let historicalData = require('./data.json')
  res.json(historicalData)
  // console.log(historicalData)
});

app.post('/analyze', (req, res) => {
  console.log(req.body);
  let conversationTranscript = req.body;

  // spawn child_process to run topic modeling script
  let spawn = child_process.spawn;
  var py  = spawn('python3', ['topic_modelling/compute_input.py']);
  var dataString = '';

  py.stdout.on('data', function(response){
    dataString += response.toString();
  });
  py.stdout.on('end', function(){
    // console.log('Sum of numbers =', dataString);
    res.send(dataString); // send result as string back to frontend
  });

  py.stdin.write(JSON.stringify(conversationTranscript.text));
  py.stdin.end();

  fs.readFile('data.json', 'utf8', function readFileCallback(err, newData) {
    if (err){
        console.log(err);
    } else {
      obj = JSON.parse(newData); //now its an object
      obj[conversationTranscript.dateTime] = conversationTranscript.text; //add data
      json = JSON.stringify(obj); //convert it back to json
      fs.writeFile('data.json', json, 'utf8', function (err) {
        if (err) {
          return console.log(err);
        }
        console.log("The file was saved!");
      }); // write it back
  }});
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

// Some helper functions
/**
 * Removes a module from the cache
 */
function purgeCache(moduleName) {
    // Traverse the cache looking for the files
    // loaded by the specified module name
    searchCache(moduleName, function (mod) {
        delete require.cache[mod.id];
    });

    // Remove cached paths to the module.
    // Thanks to @bentael for pointing this out.
    Object.keys(module.constructor._pathCache).forEach(function(cacheKey) {
        if (cacheKey.indexOf(moduleName)>0) {
            delete module.constructor._pathCache[cacheKey];
        }
    });
};

/**
 * Traverses the cache to search for all the cached
 * files of the specified module name
 */
function searchCache(moduleName, callback) {
    // Resolve the module identified by the specified name
    var mod = require.resolve(moduleName);

    // Check if the module has been resolved and found within
    // the cache
    if (mod && ((mod = require.cache[mod]) !== undefined)) {
        // Recursively go over the results
        (function traverse(mod) {
            // Go over each of the module's children and
            // traverse them
            mod.children.forEach(function (child) {
                traverse(child);
            });

            // Call the specified callback providing the
            // found cached module
            callback(mod);
        }(mod));
    }
};
