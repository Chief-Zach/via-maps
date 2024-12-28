import React, { useState } from "react";

const TrainInfo = () => {
  const [trainNumber, setTrainNumber] = useState("");
  const [date, setDate] = useState("");
  const [trainData, setTrainData] = useState(null); // Data for the train cars
  const [scheduleData, setScheduleData] = useState(null); // Data for the schedule
  const [message, setMessage] = useState(""); // Display dynamic train info

  // Handle form submission for train info
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!trainNumber || !date) {
      alert("Please enter both the train number and date.");
      return;
    }

    try {
      // Fetch train cars info
      const response = await fetch(
        `http://localhost:8000/trains?number=${trainNumber}&date=${date}`
      );
      const data = await response.json();
      setTrainData(data);
      setMessage(`Train ${trainNumber} on ${date} from ${data.origin} to ${data.destination}`);
    } catch (error) {
      console.error("Error fetching train data:", error);
      alert("Failed to fetch train data. Please try again.");
    }

    // Fetch train schedule info
    try {
      const scheduleResponse = await fetch(`http://localhost:8000/${trainNumber}`);
      if (!scheduleResponse.ok) {
        throw new Error("Schedule not found.");
      }
      const scheduleHtml = await scheduleResponse.text(); // API returns raw HTML
      setScheduleData(scheduleHtml);
    } catch (error) {
      console.error("Error fetching schedule:", error);
      alert("Failed to fetch schedule data. Please try again.");
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "row" }}>
      {/* Left Column - Train Info */}
      <div style={{ flex: 1, padding: "20px" }}>
        <h1>VIA Car Info</h1>
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="trainNumber">Train Number:</label>
            <input
              type="text"
              id="trainNumber"
              value={trainNumber}
              onChange={(e) => setTrainNumber(e.target.value)}
            />
          </div>
          <div>
            <label htmlFor="date">Date:</label>
            <input
              type="date"
              id="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
            />
          </div>
          <button type="submit">Submit</button>
        </form>

        {message && <h2>{message}</h2>}

        {trainData && (
          <ul>
            {trainData.cars.map((car, index) => (
              <li key={index}>
                Car {car.number} - {car.type} ({car.class})
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* Right Column - Train Schedule */}
      <div style={{ flex: 1, padding: "20px", borderLeft: "1px solid #ccc" }}>
        <h1>Schedule</h1>
        {scheduleData ? (
          <div
            dangerouslySetInnerHTML={{ __html: scheduleData }}
            style={{ overflow: "auto" }}
          />
        ) : (
          <p>No schedule data available. Please enter a train number.</p>
        )}
      </div>
    </div>
  );
};

export default TrainInfo;
