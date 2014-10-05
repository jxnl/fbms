var express = require('express')
  , mongoskin = require('mongoskin')
  , bodyParser = require('body-parser')

var app = express()
app.use(bodyParser())
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');
app.use("/", express.static(__dirname + '/public'));

var db = mongoskin.db('mongodb://marksweep:pennapps@ds035300.mongolab.com:35300/marksweep', {safe:true});

app.param('collectionName', function(req, res, next, collectionName){
  req.collection = db.collection(collectionName)
  return next()
})
app.get('/', function(req, res) {
  res.render("index");
})

app.get('/collections/:collectionName', function(req, res) {
  req.collection.find({},{limit:50, sort: [['_id',-1]]}).toArray(function(e, results){
    if (e) return next(e)
    res.send(results)
  })
})

app.listen(3000)