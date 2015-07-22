var assert = require('assert');
var MongoClient = require('mongodb').MongoClient;
var mongoUrl =  'mongodb://localhost:27017/test';
var Acollection = "agents", Icollection = "states";


var find_agents = function(db, callback) {
    var cursor =db.collection(Acollection).find( ).toArray(function (err, docs) {
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
    var cursor =db.collection(Acollection).find().toArray(function (err, docs) {
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




module.exports.agents = agents;
module.exports.status = status;
module.exports.last_info = last_info;
module.exports.info = info;
