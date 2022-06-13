const {Data}= require("../model/model");

const dataController = {
    // ADD data
    addData: async(req,res)=>{
        try {
            const newData = new Data(req.body);
            const savedData = await newData.save();
            res.status(200).json(savedData);
        } catch (error) {
            console.error(error);
            res.status(500).json(error.msg)
        }
    },
    getAllData: async (req, res) => {
        try {
          const datas = await Data.find();
          res.status(200).json(datas);
        } catch (err) {
          res.status(500).json(err);
        }
    },
    getAData: async (req, res) => {
        try {
          const data = await Data.findById(req.params.id);
          res.status(200).json(data);
        } catch (err) {
          res.status(500).json(err);
        }
    },
    updateData: async (req, res) => {
        try {
          const data = await Data.findById(req.params.id);
          await data.updateOne({ $set: req.body });
          const data2 = await Data.findById(req.params.id);
          res.status(200).json(data2);
        } catch (err) {
          res.status(500).json(err);
        }
    },
    deleteData: async (req, res) => {
        try {
          await Data.findByIdAndDelete(req.params.id);
          res.status(200).json("Deleted successfully!");
        } catch (err) {
          res.status(500).json(err);
        }
    },
};

module.exports = dataController;