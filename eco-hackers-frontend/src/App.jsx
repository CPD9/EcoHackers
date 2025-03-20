import React from 'react';
import { Box, Container, Grid, Paper, Typography, AppBar, Toolbar } from '@mui/material';
import HeatmapChart from './components/HeatmapChart';
// Import other visualization components

function App() {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Eco-Hackers Energy Valve Dashboard
          </Typography>
        </Toolbar>
      </AppBar>
      <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
        <Grid container spacing={3}>
          {/* Heatmap */}
          <Grid item xs={12} md={12} lg={12}>
            <Paper
              sx={{
                p: 2,
                display: 'flex',
                flexDirection: 'column',
                height: 600,
              }}
            >
              <HeatmapChart />
            </Paper>
          </Grid>
          
          {/* Add Grid items for other visualizations */}
        </Grid>
      </Container>
    </Box>
  );
}

export default App;