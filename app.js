var express = require('express');
var app = express();

// respond with "hello world" when a GET request is made to the homepage

app.set('view engine', 'ejs');

app.get('/', function(req, res) {
  res.render('index.ejs');
});

app.use(express.static(__dirname + '/'));

app.listen(8080);