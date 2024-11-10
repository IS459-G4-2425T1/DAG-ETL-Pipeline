import React, { useState } from 'react';
import { Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, CircularProgress, Alert } from '@mui/material';

const sagemakerURI = process.env.REACT_APP_SAGEMAKER_URI;

const SageMakerTable = () => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Function sto fetch data from the API
    const fetchPredictions = async () => {
        setLoading(true);
        setError(null);

        try {
            const response = await fetch(sagemakerURI, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('Failed to fetch predictions');
            }

            const result = await response.json();
            setData(result);  // Set the fetched data
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
                                <TableCell>Predicted Delay</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {data.map((item) => (
                                <TableRow key={item.flightnum}>
                                    <TableCell>{item.flightnum}</TableCell>
                                    <TableCell>{item.orgin}</TableCell>
                                    <TableCell>{item.destination}</TableCell>
                                    <TableCell>{item.carrier}</TableCell>
                                    <TableCell>{item.predicted_delay.toFixed(2)}</TableCell>
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
