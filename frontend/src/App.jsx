import { useState,useEffect } from 'react'
import './App.css'

function App() {
  const [firmsData, setFirmsData] = useState([]);

  useEffect(() => {
    // Connect to WebSocket
    const socket = new WebSocket("ws://localhost:8000/ws");

    socket.onopen = () => {
      console.log("Connected to WebSocket");
    };

    socket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      if (message.event === "new_data") {
        setFirmsData((prevData) => [...prevData, ...JSON.parse(message.data)]);
      }
    };

    socket.onclose = () => {
      console.log("WebSocket connection closed");
    };

    // Cleanup on unmount
    return () => {
      socket.close();
    };
  }, []);

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>FIRMS Data Viewer</h1>
      <p>Displaying real-time FIRMS data updates:</p>
      <ul>
        {firmsData.map((row, index) => (
          <li key={index}>
            Latitude: {row.latitude}, Longitude: {row.longitude}, Date: {row.acq_date}, Time:{row.acq_time}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
