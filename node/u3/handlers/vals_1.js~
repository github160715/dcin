var http = require('http');
var request = require('request');
var hostname = "influxdb";
var url1 = "http://"+hostname+":8086/query?db=collectd&q=SELECT value FROM cpu_value LIMIT 1";
var url2 = "http://"+hostname+":8086/query?db=collectd&q=SELECT value FROM memory_value LIMIT 1";
var xxx;
function parse(res){
    var key = res.substring(res.indexOf('name')+7, res.indexOf('columns')-3);
    var i = res.indexOf('[['), j = res.indexOf(']]');
    var vals = res.slice(i+2, j);
    var x = {  time: vals.substring(1,vals.indexOf(',')-1)  };
    x[key] = vals.substring(vals.indexOf(',')+1, vals.length);
    return x;
}
function logger(er, re, body) {
    if (er){
        console.log(er);
    }else {
        console.log(body);
        xxx.status(200).json(parse(body));
    }
}
function cpu(req, res){
    request.get(url1, logger);
    xxx = res;
}
function memory(req, res){
    request.get(url2, logger);
    xxx = res;
}

module.exports.cpu = cpu;
module.exports.memory = memory;

