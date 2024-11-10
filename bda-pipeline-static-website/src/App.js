import React, { useEffect, useState } from 'react';
import QuickSightEmbed from './components/QuickSightEmbed';
import SageMakerTable from './components/SagemakerTable';
import { getQuickSightEmbedUrl } from './services/api';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import CircularProgress from '@mui/material/CircularProgress';
import Alert from '@mui/material/Alert';
import CssBaseline from '@mui/material/CssBaseline';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import useMediaQuery from '@mui/material/useMediaQuery';
import { useTheme } from '@mui/material/styles';

const dashboardId1 = process.env.REACT_APP_QUICKSIGHT_DASHBOARD_ID_1;
const dashboardId2 = process.env.REACT_APP_QUICKSIGHT_DASHBOARD_ID_2;
const dashboardId3 = process.env.REACT_APP_QUICKSIGHT_DASHBOARD_ID_3;

function App() {
  const [currentTab, setCurrentTab] = useState(0);
  const [embedUrls, setEmbedUrls] = useState({ dashboard1: '', dashboard2: '', dashboard3: '' });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));

  useEffect(() => {
    refetchEmbedUrl(currentTab);
  }, [currentTab]);

  const handleTabChange = (event, newValue) => {
    setCurrentTab(newValue);

    if (newValue === 3) {
      setError(null);
    } else {
      const dashboardKey = newValue === 0 ? 'dashboard1' : newValue === 1 ? 'dashboard2' : 'dashboard3';
      setEmbedUrls((prev) => ({
        ...prev,
        [dashboardKey]: '',
      }));
      refetchEmbedUrl(newValue);
    }
  };

  const refetchEmbedUrl = async (tabIndex) => {
    try {
      setLoading(true);
      let dashboardId;
      
      if (tabIndex === 0) {
        dashboardId = dashboardId1;
      } else if (tabIndex === 1) {
        dashboardId = dashboardId2;
      } else if (tabIndex === 2) {
        dashboardId = dashboardId3;
      } else {
        setLoading(false);
        return;
      }

      console.log("Requesting embed URL for Dashboard ID:", dashboardId);

      const embedUrl = await getQuickSightEmbedUrl(dashboardId);
      setEmbedUrls((prev) => ({
        ...prev,
        [tabIndex === 0 ? 'dashboard1' : tabIndex === 1 ? 'dashboard2' : 'dashboard3']: embedUrl,
      }));
      setError(null);
    } catch (err) {
      console.error('Error fetching QuickSight embed URL:', err);
      setError('Failed to load QuickSight dashboard. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <CssBaseline />

      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div">
            Big Data Pipeline Dashboard Analytics and Prediction
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Tabs
          value={currentTab}
          onChange={handleTabChange}
          variant={isMobile ? "scrollable" : "standard"}
          scrollButtons="auto"
          allowScrollButtonsMobile
          centered={!isMobile}
          sx={{ scrollBehavior: 'smooth' }}
        >
          <Tab label="Pipeline 1 QuickSight Dashboard" />
          <Tab label="Pipeline 2 QuickSight Dashboard" />
          <Tab label="Pipeline 3 QuickSight Dashboard" />
          <Tab label="Airline Delay Predictions" />
        </Tabs>

        <Box sx={{ mt: 4 }}>
          {loading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '600px' }}>
              <CircularProgress />
            </Box>
          ) : error && (currentTab === 0 || currentTab === 1 || currentTab === 2) ? (
            <Alert severity="error">{error}</Alert>
          ) : (
            <>
              {currentTab === 0 && (
                embedUrls.dashboard1 ? (
                  <QuickSightEmbed embedUrl={embedUrls.dashboard1} />
                ) : (
                  <Alert severity="warning">QuickSight Dashboard 1 is not ready for viewing or has an invalid ID.</Alert>
                )
              )}
              {currentTab === 1 && (
                embedUrls.dashboard2 ? (
                  <QuickSightEmbed embedUrl={embedUrls.dashboard2} />
                ) : (
                  <Alert severity="warning">QuickSight Dashboard 2 is not ready for viewing or has an invalid ID.</Alert>
                )
              )}
              {currentTab === 2 && (
                embedUrls.dashboard3 ? (
                  <QuickSightEmbed embedUrl={embedUrls.dashboard3} />
                ) : (
                  <Alert severity="warning">QuickSight Dashboard 3 is not ready for viewing or has an invalid ID.</Alert>
                )
              )}
              {currentTab === 3 && (
                <Box sx={{ mt: 4 }}>
                  <Typography variant="h5" gutterBottom>
                    SageMaker Predictions
                  </Typography>
                  <SageMakerTable />
                </Box>
              )}
            </>
          )}
        </Box>
      </Container>

      <Box
        component="footer"
        sx={{
          py: 3,
          px: 2,
          mt: 'auto',
          backgroundColor: (theme) =>
            theme.palette.mode === 'light' ? theme.palette.grey[200] : theme.palette.grey[800],
        }}
      >
        <Container maxWidth="sm">
          <Typography variant="body1">
            AWS QuickSight Dashboard and SageMaker Predictions Application
          </Typography>
        </Container>
      </Box>
    </>
  );
}

export default App;
