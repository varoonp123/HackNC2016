var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var PythonShell = require('python-shell');
var cors = require('cors');
var fs = require('fs');
//Converter Class
var Converter = require("csvtojson").Converter;
var converter = new Converter({
  constructResult:true,
  workerNum:4,
  noheader:true
});
// var csvData;


app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));

app.set('view engine', 'ejs');

app.get('/', function (req, res)
{
    res.render('index.ejs');
});

app.get("/query/:kwd", function (req, res)
{
    // send req to python, get file
    var kwd = req.params.kwd;
    // var csvData = parseCSV("./test.csv");
    // console.log("This is the returned jsonArray" + csvData);
    // res.header('Access-Control-Allow-Origin', '*');
    fs.readFile("test.json", function(err, data) {
        if (err) {
            throw error;
        }
        console.log(JSON.parse(data));
        res.render('map', {jsonData: data, thingVar: kwd});
    });
});

// app.get("/query/:keyword", function(req, res){
//   var keyword = req.params.keyword;
//   res.render("map", {thingVar: keyword});
// });


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
        console.log(jsonArray);
        // csvData = jsonArray;
        return jsonArray; //here is your result jsonArray
    });

    //read from file
    fs.createReadStream(file).pipe(converter);
}