const {Log}= require("../model/model");

const LogController = {
    // ADD data
    addLog: async(req,res)=>{
        try {
            const newLog = new Log(req.body);
            const saLog = await newLog.save();
            res.status(200).json(saLog);
        } catch (error) {
            console.error(error);
            res.status(500).json(error.msg)
        }
    },
    getAllLog: async (req, res) => {
        try {
          const log = await Log.find();
          res.status(200).json(log);
        } catch (err) {
          res.status(500).json(err);
        }
    },
    getALog: async (req, res) => {
        try {
          const log = await Log.findById(req.params.id);
          res.status(200).json(log);
        } catch (err) {
          res.status(500).json(err);
        }
    },
    updateLog: async (req, res) => {
        try {
          const log = await Log.findById(req.params.id);
          await log.updateOne({ $set: req.body });
          const log2 = await Log.findById(req.params.id);
          res.status(200).json(log2);
        } catch (err) {
          res.status(500).json(err);
        }
    },
    updateLogByName: async (req, res) => {
        try {
          const log = await Log.findById(req.params.id);
          await log.updateOne({ $set: req.body });
          res.status(200).json("Updated successfully!");
        } catch (err) {
          res.status(500).json(err);
        }
    },
    deleteLog: async (req, res) => {
        try {
          await Log.findByIdAndDelete(req.params.id);
          res.status(200).json("Deleted successfully!");
        } catch (err) {
          res.status(500).json(err);
        }
    },
};

module.exports = LogController;
//fix bug