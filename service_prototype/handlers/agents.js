var assert = require('assert');
var MongoClient = require('mongodb').MongoClient;
var mongoUrl =  'mongodb://localhost:27017/test';
var Acollection = "agents", Icollection = "states";


var find_agents = function(db, callback) {
    var cursor =db.collection('agents').find( ).toArray(function (err, docs) {
        var data = [];
        assert.equal(null, err);
        for (var i = 0; i < docs.length; i++) {
            data.push(docs[i].name);
            console.log(docs[i].name);
        }
        callback(data);
    });
};


function agents(req, res) {
    MongoClient.connect(mongoUrl, function (err, db) {
            if (err != null) {
                res.status(200).json("error");
            }
            find_agents(db, function(data) {
                db.close();
                res.status(200).json(data);
            });
        }
    );
}

function find_status(db, callback) {
    var cursor =db.collection('agents').find().toArray(function (err, docs) {
        var data = {};
        assert.equal(null, err);
        for (var i = 0; i < docs.length; i++) {
            data[docs[i].name] = docs[i].status;
        }
        callback(data);
    });
}
function status(req, res){
    MongoClient.connect(mongoUrl, function (err, db) {
            if (err != null) {
                res.status(200).json("error");
            }
            find_status(db, function(data) {
                db.close();
                res.status(200).json(data);
            });
        }
    );
}
function get_last(db, callback) {
    var data = {}, ttt = 0;
    db.collection('agents').find({}).each(function (err, docs){
        if (docs == null) {
            console.log(data);
            return;
        }
        ttt++;
        var r = db.collection('states').find({time : docs.last}).toArray(function (er, ds){
            data[docs.name] = ds;
            if (--ttt == 0) callback(data);
        });
    });
}
function last_info(req, res){
    MongoClient.connect(mongoUrl, function (err, db){
        errf(res, err);
        get_last(db, function(data) {
            db.close();
            res.status(200).json(data);
        });
    });
}
var inf, sup;
function info(req, res){
    MongoClient.connect(mongoUrl, function (err, db){
        errf(req, err);
        var collection = db.collection(collectionName);
        collection.find({time : {$gt: inf, $lt: sup}}).toArray(
            function (err, docs) {
                if (err != null) {
                    req.status(500).json({"error" : err.message});
                    return;
                }
                res.status(200).json(docs);
            }
        );
    })
}
module.exports.agents = agents;
module.exports.status = status;
module.exports.last_info = last_info;
module.exports.info = info;
