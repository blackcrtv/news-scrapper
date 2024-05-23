import { useState } from 'react';

import { Box } from '@mui/system';
import { Button, FormControl, Grid, TextField } from '@mui/material';

import BasicSelect from 'ui-component/Select';
import { gridSpacing } from 'store/constant';

import { optionsScrappers } from 'mock/scrapper';

const SearchHeader = ({ handleSubmitEvent = console.log }) => {

    const [limitScrapper, setLimitScrapper] = useState(0);
    const [sourceScrapper, setSourceScrapper] = useState("");

    const handleChangeInput = (event) => {
        if (event.target.value > 0) {
            setLimitScrapper(event.target.value)
        }
    }

    const handleChangeSelect = (event) => {
        setSourceScrapper(event.target.value)
    }

    const handleSubmit = () => {
        if(limitScrapper < 0) return;
        if(sourceScrapper < 0) return;
        handleSubmitEvent({
            limit: limitScrapper,
            source: sourceScrapper
        })
    }

    return (
        <Grid container spacing={gridSpacing} justifyContent="flex-start"
            alignItems="center">
            <Grid item xs={3} md={4}>
                <BasicSelect options={optionsScrappers} title='Select source' handleChangeEvent={handleChangeSelect}></BasicSelect>
            </Grid>
            <Grid item xs={2} md={2}>
                <TextField type='number' label='Limit results' value={limitScrapper} onChange={handleChangeInput}></TextField>
            </Grid>
            <Grid item xs={1} md={2}>
                <Button variant="contained" type='submit' onClick={handleSubmit}>Pornire</Button>
            </Grid>
        </Grid>
    )
}

export default SearchHeader