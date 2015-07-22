var express = require('express');
var router = express.Router();
var handlers = require('../handlers/agents');

router.get('/agents', handlers.agents);
router.get('/status', handlers.status);
router.get('/last_info', handlers.last_info);
router.get('/info/:inf/:sup', handlers.info);

module.exports = router;
