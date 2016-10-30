var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var PythonShell = require('python-shell');
var cors = require('cors');
var fs = require('fs');
//Converter Class
var Converter = require("csvtojson").Converter;
var converter = new Converter({});


app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));

app.set('view engine', 'ejs');

app.get('/', function (req, res)
{
    res.render('index.ejs');
});

app.get('/query=', function (req, res)
{
    // send req to python, get file
    var csvData = parseCSV('./Python_Script_resources/tst_vals.csv');
    res.header('Access-Control-Allow-Origin', '*');
    res.render('map.ejs', {csvData: csvData});
});

app.use(express.static(__dirname + '/'));

// PythonShell.run('my_script.py', function (err) {
//   if (err) throw err;
//   console.log('finished');
// });

app.listen(8080);

function parseCSV(file)
{
    //end_parsed will be emitted once parsing finished
    converter.on("end_parsed", function (jsonArray)
    {
        return jsonArray; //here is your result jsonarray
    });

    //read from file
    fs.createReadStream(file).pipe(converter);
}