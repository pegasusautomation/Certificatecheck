require("dotenv").config()

const express= require("express");
const cors = require("cors");
const mongoose = require("mongoose");
const app = express();

// Midleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
// // Database
// const certificates = [
//     {
//         "CertificateName": "Google Cert",
//         "DaysToExpire":290,
//         "Status": "Not Expired"
//       },
//       {
//         "CertificateName": "Yahoo Cert",
//         "DaysToExpire":0,
//         "Status": "Expired"
//       },
//       {
//         "CertificateName": "Facebook Cert",
//         "DaysToExpire":7,
//         "Status": "Not Expired"
//       },
//       {
//         "CertificateName": "Niscraft Cert",
//         "DaysToExpire":1,
//         "Status": "Not Expired"
//       }
//     ]

// Connect to mongoose
mongoose.connect(process.env.MONOGO_URI)

// Create schema
const certschema = new mongoose.Schema({
    servername: String,
    thumbprint: String,
    noofdays: Number,
    status: String
});

// Create model
const certmodel = mongoose.model("cert", certschema);

// // insert into db
// certificates.forEach((cert) =>{
//     const newcert = new certmodel({
//         certname : cert.CertificateName,
//         noofdays : cert.DaysToExpire,
//         status : cert.Status
//     });
//     newcert.save();
// });

app.get("/", (req, res) => {
    certmodel.find({}).then(
        items => res.json(items)
    ).catch(err => console.log(err))
});

app.listen(3001, function()  {
console.log("Server is running");
});