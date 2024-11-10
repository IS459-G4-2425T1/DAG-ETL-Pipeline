import React, { useState, useEffect } from 'react';
import { Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, CircularProgress, Alert } from '@mui/material';

const sagemakerURI = process.env.REACT_APP_SAGEMAKER_URI;
console.log("API Base URL:", process.env.REACT_APP_SAGEMAKER_URI);

const SageMakerTable = () => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Load data from localStorage when the component mounts
    useEffect(() => {
        const storedData = localStorage.getItem('sagemakerData');
        if (storedData) {
            setData(JSON.parse(storedData));  // Load the data if available
        }
    }, []);

    // Function to fetch data from the API
    const fetchPredictions = async () => {
      setLoading(true);
      setError(null);
  
      try {
          const response = await fetch(`${sagemakerURI}`, {
              method: 'POST',
          });
  
          if (!response.ok) {   
              throw new Error('Failed to fetch predictions');
          }
  
          const result = await response.json();
  
          // Process each item to split `crsarrival` into date and time
          const processedData = result.map((item) => {
              const [dateOfArrival, timeOfArrival] = item.crsarrival.split('T');
              const formattedTime = timeOfArrival ? timeOfArrival.slice(0, 5) : ''; // Extract HH:MM from the time part
              return {
                  ...item,
                  dateOfArrival,
                  timeOfArrival: formattedTime
              };
          });
  
          console.log('Processed Predictions:', processedData);
          setData(processedData);  // Set the processed data
          localStorage.setItem('sagemakerData', JSON.stringify(processedData));  // Save processed data to localStorage
      } catch (err) {
          console.error('Error fetching predictions:', err);
          setError('Failed to load predictions. Please try again later.');
      } finally {
          setLoading(false);
      }
  };

    return (
        <div>
            <Button variant="contained" color="primary" onClick={fetchPredictions} disabled={loading}>
                {loading ? 'Loading...' : 'Fetch Predictions'}
            </Button>

            {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}

            {loading && <CircularProgress sx={{ mt: 2 }} />}

            {data.length > 0 && (
                <TableContainer component={Paper} sx={{ mt: 2 }}>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>Flight Number</TableCell>
                                <TableCell>Origin</TableCell>
                                <TableCell>Destination</TableCell>
                                <TableCell>Carrier</TableCell>
                                <TableCell>Scheduled Date of Arrival</TableCell>
                                <TableCell>Scheduled Time of Arrival</TableCell>
                                <TableCell>Predicted Delay (Minutes)</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {data.map((item) => (
                                <TableRow key={`${item.flightnum}-${item.origin}-${item.dests}-${item.uniquecarrier}`}>
                                    <TableCell>{item.flightnum}</TableCell>
                                    <TableCell>{item.origin}</TableCell>
                                    <TableCell>{item.dests}</TableCell>
                                    <TableCell>{item.uniquecarrier}</TableCell>
                                    <TableCell>{item.dateOfArrival}</TableCell>
                                    <TableCell>{item.timeOfArrival}</TableCell>
                                    <TableCell>{item["Estimated delay"] !== undefined ? item["Estimated delay"].toFixed(2) : "N/A"}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            )}
        </div>
    );
};

export default SageMakerTable;
