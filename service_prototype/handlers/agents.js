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
function last_info(req, res){
    MongoClient.connect(mongoUrl, function (err, db){
        errf(req, err);
        var collection = db.collection(collectionName);
        collection.find({name : {search : ""}}).toArray(
            function (err, docs) {
                if (err != null) {
                    req.status(500).json({"error" : err.message});
                    return;
                }
                var a = {}, l = docs.length;
                for (var i = 0; i < l; i++) {
                    var t = docs[i].last;
                    a[docs[i].name] = collection.find({time : t});
                }
                res.status(200).json(a);
            }
        );
    })
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