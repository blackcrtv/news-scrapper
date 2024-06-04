import { useEffect, useState } from 'react';

import Grid from '@mui/material/Grid';

import { gridSpacing } from 'store/constant';

const Dashboard = () => {
  const [isLoading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(false);
  }, []);

  return (
    <Grid container spacing={gridSpacing}>
      <Grid item xs={12}>
        <Grid container spacing={gridSpacing}>
          <Grid item lg={4} md={8} sm={6} xs={12}>
          <iframe src="http://localhost:3001/d-solo/adnscrdwznrwgd/dashboard-osint?orgId=1&from=1701720420647&to=1717528020647&panelId=3" width="900" height="300" frameBorder="0"></iframe>
          </Grid>
        </Grid>
      </Grid>
      <Grid item xs={12}>
        <Grid container spacing={gridSpacing}>
          <Grid item xs={12} md={8}>
            <iframe src="http://localhost:3001/d-solo/adnscrdwznrwgd/dashboard-osint?orgId=1&from=1701718544100&to=1717526144100&panelId=1" width="900" height="300" frameBorder="0"></iframe>
          </Grid>
        </Grid>
      </Grid>
      <Grid item xs={12}>
        <Grid container spacing={gridSpacing}>
          <Grid item xs={12} md={8}>
            <iframe src="http://localhost:3001/d-solo/adnscrdwznrwgd/dashboard-osint?orgId=1&from=1701718569285&to=1717526169285&panelId=2" width="900" height="300" frameBorder="0"></iframe>
          </Grid>
        </Grid>
      </Grid>
    </Grid>
  );
};

export default Dashboard;
