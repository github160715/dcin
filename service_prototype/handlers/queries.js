var MongoClient = require('mongodb').MongoClient;
var ObjectID = require('mongodb').ObjectID;
var mongoUrl = 'mongodb://localhost:27017/test';

var check = function(db, col_names, field_names, res) {
    for (var i in col_names) {
        db.collection(col_names[i]).find({$or: field_names}).toArray(
            function (er1, docs) {
                if ((er1 || docs.length > 0) && !res._headerSent) {
                    res.status(400).send("Something went wrong");
                }
            });
    }
};
var add = function (doc, res) {
    //status false
    console.log('adding: ', doc);
    MongoClient.connect(mongoUrl, function (er1, db) {
        if (er1) {
            res.status(301).send('MongoClient connection error');
            return
        }
        check(db, ['agents'], [{"name": doc['name']}, {"http": doc['http']}], res);
        db.collection('add').insertOne(doc, function (er3) {
            if (er3 && !res._headerSent) {
                res.status(302).send('Mongo collection insert error')
            } else {
                if (!res._headerSent) {
                    console.log('add');
                    res.status(200).send('added');
                }
            }
        });
    });
};

var upd = function (params, res) {
  console.log('updating doc with id: ', params['_id']);
    MongoClient.connect(mongoUrl, function (er1, db) {
        if (er1) {
            res.status(301).send('MongoClient connection error');
            return
        }
        //check(db, ['agents', 'add'], [{"name": params['name']}, {"http": params['http']}], res);
        db.collection('upd').findOneAndUpdate(
            {"_id": ObjectID(params['_id'])},
            {$set: {
                "name": params['name'],
                "http": params['http'],
                "period": params['period']}},
            {upsert: true},
            function(er2){
                if (res._headerSent) {return}
                if (er2) {res.status(302).send("Something went wrong"); return }
                res.status(200).send('updated')
            });
    });
};

var del = function(obj, res){
    console.log('deleting doc with id: ', obj['_id']);
    MongoClient.connect(mongoUrl, function (er1, db) {
        if (er1) {
            res.status(301).send('MongoClient connection error');
            return
        }
        db.collection('delete').findOneAndUpdate(
            {'_id' : ObjectID(obj['_id'])},
            {$set: {'_id': ObjectID(obj['_id'])}},
            {upsert: true},
            function(er2){
                if (er2) {res.status(302).send("Something went wrong"); return }
                res.status(200).send('deleted')
            }
        );
    });
};

module.exports.add = add;
module.exports.upd = upd;
module.exports.del = del;
