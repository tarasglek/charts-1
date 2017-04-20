'use strict';
/*
 This does expiration and other maintance
 TODO: report queue stats
*/
const PgBoss = require('pg-boss');
var restify = require('restify');
var plugins = require('restify-plugins');
var bunyan = require('bunyan');

function encode(str) {
  var b = new Buffer(str);
  return b.toString('base64');
}

function decode(base64) {
  var b = new Buffer(base64, 'base64')
  return b.toString();
}

var masterBoss = Promise.resolve(null)

if (process.env.QUEUE_CONFIG) {
  const master = require("./master.js");
  masterBoss = master.setupBoss(process.env.QUEUE_CONFIG).start().then(boss => {
    console.log("Master Ready")
    return boss
  })
}

const server = restify.createServer({
  name: 'pg-boss-queue',
  version: '1.0.0'
});

server.use(plugins.acceptParser(server.acceptable));
server.use(plugins.queryParser());
server.use(plugins.bodyParser());


function queue2boss(base64) {
  var connectionString = decode(base64)
  if (connectionString == process.env.QUEUE_CONFIG)
    masterBoss
  return new PgBoss(connectionString).connect();
}

server.post('/publish/:queue/:subject/:options', function (req, res, next) {
  var options = req.params.options
  queue2boss(req.params.queue)
    .then(boss => options == '' ? [boss, null] : [boss, JSON.parse(options)])
    .then(([boss, options]) => boss.publish(req.params.subject, req.body, options))
    .then(jobId => {
      res.send({ jobId: jobId });
      next()
    })
    .catch(err => next(err))
});

server.get('/fetch/:queue/:subject', function (req, res, next) {
  queue2boss(req.params.queue)
    .then(boss => boss.fetch(req.params.subject))
    .then(ret => {
      res.send({ job: ret })
      next()
    })
    .catch(err => next(err.stack))
});

server.get('/complete/:queue/:subject', function (req, res, next) {
  queue2boss(req.params.queue)
    .then(boss => boss.complete(req.params.subject))
    .then(() => {
      res.send({})
      next()
    })
    .catch(err => next(err.stack))
});

server.listen(8080, function () {
  console.log('%s listening at %s', server.name, server.url);
});

server.on('after', restify.auditLogger({
  log: bunyan.createLogger({
    name: 'audit',
    stream: process.stdout
  }),
  body: true
}));