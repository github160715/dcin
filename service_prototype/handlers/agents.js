var MongoClient = require('mongodb').MongoClient;
var mongoUrl =  'mongodb://localhost:27017/test';

function all(req, res) {
    MongoClient.connect(mongoUrl, function (er1, db) {
            if (er1) {
                res.status(400).json("Mongo connection error");
                return
            }
            db.collection('agents').find({}).toArray(function (er2, docs) {
                if (er2) {
                    res.status(400).send("Mongo search error");
                    return
                }
                res.status(200).json(docs);
            });
        }
    );
}

function agents(req, res) {
    MongoClient.connect(mongoUrl, function (er1, db) {
            if (er1) {
                res.status(400).json("Mongo connection error");
                return
            }
            db.collection('agents').find({}).toArray(function (er2, docs) {
                if (er2) {
                    res.status(400).send("Mongo search error");
                    return
                }
                var data = [];
                for (var i = 0; i < docs.length; i++) {
                    data.push({'_id': docs[i]._id, 'name': docs[i].name});
                }
                res.status(200).json(data);
            });
        }
    );
}

function status(req, res){
    MongoClient.connect(mongoUrl, function (er1, db) {
            if (er1) {
                res.status(400).send("Mongo connection error");
                return;
            }
            db.collection('agents').find({}).toArray(function (er2, docs) {
                if (er2) {
                    res.status(400).send("Mongo search error");
                    return
                }
                var data = [];
                for (var i = 0; i < docs.length; i++) {
                    data.push({'_id': docs[i]._id, 'name': docs[i].name, 'status': docs[i].status});
                }
                res.status(200).json(data);
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
                    }else {data.push(stat[0]);}
                    if (data.length == docs.length) {res.status(200).send(data);}
                });
            }
        });
    });
}

function errf(req, err){
    if (err != null) req.status(500).json({"error" : err.message});
}
function info(req, res){
    var a = req.params.inf, b = req.params.sup;
    MongoClient.connect(mongoUrl, function (err, db){
        errf(req, err);
        db.collection('states').find({time : {$gt: new Date(a), $lt: new Date(b)}}).toArray(
            function (er, docs) {
                errf(res, er);
                res.status(200).json({info : docs});
            }
        );
    });
}
module.exports.agents = agents;
module.exports.status = status;
module.exports.last_info = info_last;
module.exports.info = info;
module.exports.all = all;
