import React from 'react';
import Paper from '@mui/material/Paper';

const QuickSightEmbed = ({ embedUrl }) => {
  return (
    <Paper elevation={3} sx={{ height: '600px', overflow: 'hidden' }}>
      <iframe
        src={embedUrl}
        title="QuickSight Dashboard"
        width="100%"
        height="100%"
        frameBorder="0"
        allowFullScreen
        allow="fullscreen"
        style={{ border: 'none' }}
      ></iframe>
    </Paper>
  );
};

export default QuickSightEmbed;
