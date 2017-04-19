'use strict';
/*
 This does expiration and other maintance
 TODO: report queue stats
*/
const PgBoss = require('pg-boss');
/*
 This does expiration and other maintance
 TODO: report queue stats
*/
function onError(x) {
  console.error(x.stack)
  process.exit(1)
}

function setupBoss() {
  var options
  if (process.env.QUEUE_CONFIG) {
    options = process.env.QUEUE_CONFIG
  } else {
    console.error(`need env variable QUEUE_CONFIG=postgres://user:pass@host/database`)
    process.exit(1)
  }
  const boss = new PgBoss(options);

  boss.on('error', x => console.error(x.stack));
  return boss
}

setupBoss().start().then(() => console.log("Ready")).catch(onError)
