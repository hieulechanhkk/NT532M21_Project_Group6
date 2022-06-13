const DeviceController = require("../controllers/deviceController");

const router = require("express").Router();

router.post("/",DeviceController.addDevice);

router.get("/",DeviceController.getAllDevice);

router.get("/:id",DeviceController.getADevice);

router.put("/:id",DeviceController.updateDevice);

router.delete("/:id",DeviceController.deleteDevice);

module.exports = router;