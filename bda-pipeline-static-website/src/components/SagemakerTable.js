import React, { useState, useEffect } from 'react';
import { Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, CircularProgress, Alert, Tabs, Tab } from '@mui/material';

const sagemakerURI = process.env.REACT_APP_SAGEMAKER_URI;

const SageMakerTable = () => {
    const [data, setData] = useState([]);
    const [filteredData, setFilteredData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [selectedTab, setSelectedTab] = useState(0);
    const [sortMode, setSortMode] = useState("delayDescending");  // Sort mode state

    // Load data from localStorage when the component mounts
    useEffect(() => {
        const storedData = localStorage.getItem('sagemakerData');
        if (storedData) {
            const parsedData = JSON.parse(storedData);
            setData(parsedData);
            updateFilteredData(parsedData, selectedTab);  // Initialize filteredData based on storedData and selectedTab
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

                // Convert "Estimated delay" to a number for accurate filtering
                const estimatedDelay = item["Estimated delay"] !== undefined ? parseFloat(item["Estimated delay"]) : null;

                return {
                    ...item,
                    dateOfArrival,
                    timeOfArrival: formattedTime,
                    "Estimated delay": estimatedDelay
                };
            });

            setData(processedData);
            updateFilteredData(processedData, selectedTab);  // Update filtered data based on the new data
            localStorage.setItem('sagemakerData', JSON.stringify(processedData));
        } catch (err) {
            console.error('Error fetching predictions:', err);
            setError('Failed to load predictions. Please try again later.');
        } finally {
            setLoading(false);
        }
    };

    // Update filtered data whenever `selectedTab` or `data` changes
    const updateFilteredData = (data, selectedTab) => {
        let newFilteredData;
        
        if (selectedTab === 0) {
            // Show all data
            newFilteredData = data;
        } else if (selectedTab === 1) {
            // No delay (< 0)
            newFilteredData = data.filter(item => item["Estimated delay"] < 0);
        } else if (selectedTab === 2) {
            // Slight delay (0-30 mins)
            newFilteredData = data.filter(item => item["Estimated delay"] >= 0 && item["Estimated delay"] <= 30);
        } else if (selectedTab === 3) {
            // Severe delay (> 30 mins)
            newFilteredData = data.filter(item => item["Estimated delay"] > 30);
        }

        setFilteredData(newFilteredData);
    };

    // Handle tab change
    const handleTabChange = (event, newValue) => {
        setSelectedTab(newValue);
        updateFilteredData(data, newValue);  // Update filteredData based on the selected tab
    };

    // Toggle sorting mode between delay descending and arrival date/time ascending
    const toggleSortMode = () => {
        setSortMode((prevMode) => (prevMode === "delayDescending" ? "arrivalAscending" : "delayDescending"));
    };

    // Sort filtered data based on current sort mode
    const sortedData = [...filteredData].sort((a, b) => {
        if (sortMode === "delayDescending") {
            return (b["Estimated delay"] || 0) - (a["Estimated delay"] || 0);
        } else {
            const dateA = new Date(`${a.dateOfArrival}T${a.timeOfArrival}`);
            const dateB = new Date(`${b.dateOfArrival}T${b.timeOfArrival}`);
            return dateA - dateB;
        }
    });

    return (
        <div>
            <Button variant="contained" color="primary" onClick={fetchPredictions} disabled={loading}>
                {loading ? 'Loading...' : 'Fetch Predictions'}
            </Button>

            <Button variant="outlined" color="secondary" onClick={toggleSortMode} sx={{ ml: 2 }}>
                {sortMode === "delayDescending" ? "Sort by Arrival Time" : "Sort by Delay"}
            </Button>

            {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}

            {loading && <CircularProgress sx={{ mt: 2 }} />}

            {/* Tabs for filtering views */}
            <Tabs value={selectedTab} onChange={handleTabChange} sx={{ mt: 2 }}>
                <Tab label="All" />
                <Tab label="No Delay (< 0min)" />
                <Tab label="Slight Delay (0-30mins)" />
                <Tab label="Severe Delay (> 30mins)" />
            </Tabs>

            {sortedData.length > 0 && (
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
                            {sortedData.map((item, index) => (
                                <TableRow key={index}>
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
