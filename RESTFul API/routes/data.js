const dataController = require("../controllers/dataController");


const router = require("express").Router();
// add data

router.post("/",dataController.addData);

router.get("/",dataController.getAllData);

router.get("/:id",dataController.getAData);

router.put("/:id",dataController.updateData);

router.delete("/:id",dataController.deleteData);

module.exports = router;


