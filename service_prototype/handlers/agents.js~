var MongoClient = require('mongodb').MongoClient;
var mongoUrl =  'mongodb://localhost:27017/test';

function all(req, res) {
    MongoClient.connect(mongoUrl, function (er1, db) {
            if (er1) {
                res.status(400).send("Mongo connection error");
                return
            }
            db.collection('agents').find({}).toArray(function (er2, docs) {
                if (er2) {
                    res.status(400).send("Mongo search 'agents' error");
                    return
                }
                res.status(200).send(docs);
            });
        }
    );
}

function info_last(req, res){
    MongoClient.connect(mongoUrl, function (er1, db){
        if (er1) {
            res.status(400).send("Mongo connection error");
            return;
        }
        db.collection('agents').find({}).toArray(function (er2, docs) {
            if (er2) {
                res.status(400).send("Mongo search 'agents' error");
                return;
            }
            var data = [];
            for (var i in docs){
                db.collection('states').find({time: docs[i].last}).toArray(function (er3, stat) {
                    if (er3 && !res._headerSent) {
                        res.status(400).send("Mongo search 'states' error");
                    } else {data.push(stat[0]);}
                    if (data.length == docs.length) {res.status(200).send(data);}
                });
            }
        });
    });
}

function info(req, res){
    var a = req.params.inf, b = req.params.sup;
    MongoClient.connect(mongoUrl, function (er1, db){
        if (er1) {
            res.status(400).send("Mongo connection error");
            return;
        }
        db.collection('states').find({time : {$gt: new Date(a), $lt: new Date(b)}}).toArray(
            function (er2, docs) {
                if (er2) {
                    res.status(400).send("Mongo search 'states' error");
                    return
                }
                res.status(200).send(docs);
            }
        );
    });
}

module.exports.last_info = info_last;
module.exports.info = info;
module.exports.all = all;
