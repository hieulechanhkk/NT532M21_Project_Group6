const {Device}= require("../model/model");

const DeviceController = {
    // ADD data
    addDevice: async(req,res)=>{
        try {
            const newDevice = new Device(req.body);
            const savedDevice = await newDevice.save();
            res.status(200).json(savedDevice);
        } catch (error) {
            console.error(error);
            res.status(500).json(error.msg)
        }
    },
    getAllDevice: async (req, res) => {
        try {
          const devices = await Device.find();
          res.status(200).json(devices);
        } catch (err) {
          res.status(500).json(err);
        }
    },
    getADevice: async (req, res) => {
        try {
          const device = await Data.findById(req.params.id);
          res.status(200).json(device);
        } catch (err) {
          res.status(500).json(err);
        }
    },
    updateDevice: async (req, res) => {
        try {
          const device = await Device.findById(req.params.id);
          await device.updateOne({ $set: req.body });
          const device2 = await Device.findById(req.params.id);
          res.status(200).json(device2);
        } catch (err) {
          res.status(500).json(err);
        }
    },
    updateDevicenByName: async (req, res) => {
        try {
          const device = await Device.findById(req.params.id);
          await device.updateOne({ $set: req.body });
          res.status(200).json("Updated successfully!");
        } catch (err) {
          res.status(500).json(err);
        }
    },
    deleteDevice: async (req, res) => {
        try {
          await Device.findByIdAndDelete(req.params.id);
          res.status(200).json("Deleted successfully!");
        } catch (err) {
          res.status(500).json(err);
        }
    },
};

module.exports = DeviceController;