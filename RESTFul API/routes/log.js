const LogController = require("../controllers/logController");

const router = require("express").Router();

router.post("/",LogController.addLog);

router.get("/",LogController.getAllLog);

router.get("/:id",LogController.getALog);

router.put("/:id",LogController.updateLog);

router.delete("/:id",LogController.deleteLog);

module.exports = router;