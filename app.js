var bodyParser = require('body-parser');
var cors = require('cors');
var express = require('express');
var fs = require('fs');
var PythonShell = require('python-shell');

var app = express();

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
    var options = {
        pythonPath: '/usr/bin/python2',
        args: [kwd]
    };

    if (kwd == 'hillary clinton' || kwd == 'donald trump' || kwd == 'microsoft')
    {
        var file;
        switch (kwd)
        {
            case 'hillary clinton':
                file = 'json/hillary.json';
                break;
            case 'donald trump':
                file = 'json/trump.json';
                break;
            case 'microsoft':
                file = 'json/microsoft.json';
                break;
            default:
                break;
        }

        fs.readFile(file, function (err, data)
        {
            if (err) throw error;
            res.render('map', {jsonData: data, thingVar: kwd});
        })
    } else
    {
        PythonShell.run('test.py', options, function (err, result)
        {
            if (err) throw error;
            fs.readFile(result[0], function (err, data)
            {
                if (err) throw error;
                res.render('map', {jsonData: data, thingVar: kwd});
            });
        });
    }
});

app.use(express.static(__dirname + '/'));

app.listen(80);