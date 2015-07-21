var MongoClient = require('mongodb').MongoClient;
var mongoUrl = "mongodb://localhost:27017/TestDB";
var Acollection = "Agents", Icollection = "Info";

function errf(req, err){
    if (err != null) {
        req.status(500).json({"error" : err.message});
        return;
    }
}
function agents(req, res) {
    MongoClient.connect(mongoUrl, function (err, db) {
            errf(req, err);
            var collection = db.collection(Acollection);
            collection.find({name : {search : ""}}).toArray(
                function (err, docs) {
                    if (err != null) {
                        req.status(500).json({"error" : err.message});
                        return;
                    }
                    var a = {}, l = docs.length;
                    for (var i = 0; i < l; i++) {a[i] = docs[i].name;}
                    res.status(200).json(a);
                }
            );

        }
    );
}
function status(req, res){
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
                for (var i = 0; i < l; i++) {a[docs[i].name] = docs[i].stat;}
                res.status(200).json(a);
            }
        );
    })
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