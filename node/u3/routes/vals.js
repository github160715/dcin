var express = require('express');
var router = express.Router();
var handlers = require("../handlers/vals");

router.get('/memory', handlers.memory);
router.get('/cpu', handlers.cpu);

module.exports = router;