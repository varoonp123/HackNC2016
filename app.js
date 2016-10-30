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
    var kwd = req.params.kwd;

    PythonShell.run('test.py', {args:[kwd]}, function(err, result)
    {
        if (err) throw error;
        fs.readFile(result[0], function(err, data) {
            if (err) {
                throw error;
            }
            console.log(JSON.parse(data));
            res.render('map', {jsonData: data, thingVar: kwd});
        });
   });
    
});


app.use(express.static(__dirname + '/'));


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