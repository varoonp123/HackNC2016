var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var PythonShell = require('python-shell');
var cors = require('cors');

app.use(cors());
app.use(bodyParser.json());  
app.use(bodyParser.urlencoded({ extended: false }));

// respond with "hello world" when a GET request is made to the homepage

app.set('view engine', 'ejs');

// app.get('*', function(req, res) {
//   console.log(req);
//   next();
// });

app.get('/', function(req, res) {
  res.render('index.ejs');
});

app.get('/getTweet/', function(req, res) {
  res.render('map.ejs');
});

app.use(express.static(__dirname + '/'));

// PythonShell.run('my_script.py', function (err) {
//   if (err) throw err;
//   console.log('finished');
// });



app.listen(8080);
