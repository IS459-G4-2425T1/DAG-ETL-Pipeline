import React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';

const SageMakerTable = () => {
  const data = [
    { id: 1, prediction: 'Positive', confidence: '95%' },
    { id: 2, prediction: 'Negative', confidence: '88%' },
    { id: 3, prediction: 'Neutral', confidence: '76%' },
  ];

  return (
    <Paper elevation={3}>
      <TableContainer component={Paper}>
        <Table aria-label="SageMaker Predictions Table">
          <TableHead>
            <TableRow>
              <TableCell align="center"><Typography variant="h6">ID</Typography></TableCell>
              <TableCell align="center"><Typography variant="h6">Prediction</Typography></TableCell>
              <TableCell align="center"><Typography variant="h6">Confidence</Typography></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((row) => (
              <TableRow key={row.id}>
                <TableCell align="center">{row.id}</TableCell>
                <TableCell align="center">{row.prediction}</TableCell>
                <TableCell align="center">{row.confidence}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
};

export default SageMakerTable;
