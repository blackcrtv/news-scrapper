// material-ui
import { Grid } from '@mui/material';
import { gridSpacing } from 'store/constant';

// project imports
import SearchHeader from './SearchHeader';
import MainCard from 'ui-component/cards/MainCard';
import NewsContainer from './NewsContainer';

// ==============================|| SAMPLE PAGE ||============================== //

const Scrappers = () => {

  return (
    <Grid container spacing={gridSpacing} >
      <Grid item xs={12}>
        <MainCard title="Start scrapper">
          <SearchHeader />
        </MainCard>
      </Grid>
      <Grid item xs={12}>
        <MainCard title="Results">
          <NewsContainer />
        </MainCard>
      </Grid>
    </Grid >

  )
};

export default Scrappers;
