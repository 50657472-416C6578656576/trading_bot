import { useState, useEffect } from 'react'
import axios from "axios";
import logo from './logo.svg';
import './App.css';

function App() {

  const [Data, setData] = useState(null)

  function getData() {
    axios({
      method: "GET",
      url:"/home",
    })
    .then((response) => {
      const res = response.data
      setData(({
        data: res.data
      }))
    }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
        }
    })}

  useEffect(() => {
    getData()
  }, [])

  return (
    <div className="App">
        {Data && <div>
              <p>Profile name: {Data.data}</p>
            </div>
        }
    </div>
  );
}

export default App;