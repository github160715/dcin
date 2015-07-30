var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var mongodb = require('mongodb');
var MongoClient = require('mongodb').MongoClient;

var routes = require('./routes/index');
var users = require('./routes/users');
var handlers = require('./routes/handlers');

var app = express();
var mongoUrl = 'mongodb://localhost:27017/test';

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(function (req, res, next) {

    // Website you wish to allow to connect
    res.setHeader('Access-Control-Allow-Origin', '*');
    // Request methods you wish to allow
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');
    // Request headers you wish to allow
    res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');
    // Set to true if you need the website to include cookies in the requests sent
    // to the API (e.g. in case you use sessions)
    res.setHeader('Access-Control-Allow-Credentials', true);
    // Pass to next layer of middleware
    next();
});
// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.static(__dirname + '/script'));


//app.use('/', routes);
app.get('/',function(req,res){
    res.sendFile(path.join(__dirname+'/webapp/index.html'));
    //__dirname : It will resolve to your project folder.
});
app.get('/about.html',function(req,res){
    res.sendFile(path.join(__dirname+'/webapp/about.html'));
});

app.get('/control.html',function(req,res){
    res.sendFile(path.join(__dirname+'/webapp/control.html'));
});
app.get('/history.html',function(req,res){
    res.sendFile(path.join(__dirname+'/webapp/history.html'));
});
app.get('/home.html',function(req,res){
    res.sendFile(path.join(__dirname+'/webapp/home.html'));
});
app.get('/last_info.html',function(req,res){
    res.sendFile(path.join(__dirname+'/webapp/last_info.html'));
});
app.use('/users', users);
app.use('/handlers', handlers);

var queries = require('./handlers/queries');

app.post('/add', function (req, res) {
    queries.add(req.body, res);
});
app.post('/upd', function (req, res) {
    queries.upd(req.body, res);
});
app.post('/del', function (req, res) {
    queries.del(req.body, res);
});

// catch 404 and forward to error handler
app.use(function (req, res, next) {
    var err = new Error('Not Found');
    err.status = 404;
    next(err);
});

// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
    app.use(function (err, req, res, next) {
        res.status(err.status || 500);
        res.render('error', {
            message: err.message,
            error: err
        });
    });
}

// production error handler
// no stacktraces leaked to user
app.use(function (err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
        message: err.message,
        error: {}
    });
});


module.exports = app;
