var http = require('http');
var request = require('request');
var hostname = "influxdb_2";
var url1 = "http://"+hostname+":8086/query?db=collectd&q=SELECT value FROM cpu_value LIMIT 1";
var url2 = "http://"+hostname+":8086/query?db=collectd&q=SELECT value FROM memory_value WHERE type_instance='free' LIMIT 1";
var url3 = "http://"+hostname+":8086/query?db=collectd&q=SELECT value FROM memory_value WHERE type_instance='used' LIMIT 1";
var xxx;
//var dict={};
function parse(res){
    var key = res.substring(res.indexOf('name')+7, res.indexOf('columns')-3);
    var i = res.indexOf('[['), j = res.indexOf(']]');
    var vals = res.slice(i+2, j);
    var x = {  time: vals.substring(1,vals.indexOf(',')-1)  };
    x[key] = vals.substring(vals.indexOf(',')+1, vals.length);
    return x;
}

function cpu(req, res){
    request.get(url1, function (er, re, body){
        var dict = {};
        if (er){console.log('var1');}
        else {
            var parsed = parse(body);
            dict['time'] = parsed.time;
            dict['cpu'] = parsed.cpu_value;
            xxx.status(200).json(dict);
        }
    }).on('error', function (err){
        console.log('var2');
        xxx.status(404).send(err.code);
    });
    xxx = res;
}
function memory(req, res){
    request.get(url2, function (er, re, body){
        var dict = {};
        if (er){/*xxx.status(404).send(er.code);*/}
        else {
            var parsed = parse(body);
            dict['time'] = parsed.time;
            dict['total'] = parsed.memory_value;
            var tmp = request.get(url3, function (er, re, body){
                if (er){xxx.status(404).json(er.code);}
                else {
                    dict['used'] = parseFloat((parse(body)).memory_value);
                    var t = parseFloat(dict['used']) + parseFloat(dict['total']);
                    dict['total'] = t;
                    xxx.status(200).json(dict);
                }
            });
        }
    }).on('error', function (err){
            xxx.status(404).send(err.code);
        });
    xxx = res;
}

module.exports.cpu = cpu;
module.exports.memory = memory;
