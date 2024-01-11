// import Jsondata from '../certificate.json'
import { Button } from '@mui/material'
// import axios from 'axios';
import { useEffect , useState} from 'react';

// React table component
function Table() {   
    const [certvalue, setValue] = useState([{
        servername: "",
        thumbprint:"",
        noofdays: "",
        status: ""
    }]);  

// Function to renew or create certificate
const [certvalues, setcert] = useState("Cert Created")
const handleClick = (e: any) => {
    fetch("http://127.0.0.1:5000/")
    .then((res) => res.json())
    .then((jsonRes) => setcert(jsonRes));
    console.log(e)
    alert('Your certificate renewed successfully!');
};

// Fetch data from mogo DB
useEffect(() => {
      fetch("http://localhost:3001/")
      .then((res) => res.json())
      .then((jsonRes) => setValue(jsonRes));      
    }, []); 

    useEffect(() => {
        console.log(certvalue);
        
    }, [certvalue])
    
//   Get data from json and display
  const DisplayData=certvalue.map(
    (info:any)=>{
        return(
            <tr>
                <td>{info.servername}</td>
                <td>{info.thumbprint}</td>
                <td>{info.noofdays}</td>
                <td>{info.status}</td>
                <td><Button variant="contained" onClick = {(e:any) => handleClick(e.preventDefault)} 
                disabled={info.status == "Not Expired"}>Renew</Button></td>
                </tr>
        )
    }
)

return(
  <div>
      <table className="table table-striped">
          <thead>
              <tr>
              <th>Server Name</th>
              <th>Thumb Print</th>
              <th>Days to Expire</th>
              <th>Status</th>
              <th>Actions</th>
              </tr>
          </thead>
          <tbody>
              {DisplayData}
          </tbody>
      </table>
  </div>
)
}

export default Table;
