
import { Grid } from '@mui/material';
import { gridSpacing } from 'store/constant';
import { useState } from 'react';

import WodCloudCustom from './WordCloud';

import toast from 'react-hot-toast';
import SearchHeader from './SearchHeader';
import MainCard from 'ui-component/cards/MainCard';
import NewsContainer from './NewsContainer';

const Scrappers = () => {

  const [data, setData] = useState([]);
  const [news, setNews] = useState([]);

  const fetchApi = async ({ limit, source }) => {
    try {
      const result = await fetch(`localhost:5000/api/start-scrapping`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          limit, site_text: source
        })
      });
      if (!result.ok) throw new Error('Eroare api!');
      const resultJson = await result.json();
      const processedNews = processData(resultJson)
      setNews(resultJson);
      setData(processedNews);
    } catch (error) {
      console.log(error);
      toast.error('Eroare server!')
    }
  }

  const processData = (apiResponse) => {
    const allTokens = [];
    const wordCounts = {};
    const processedData = [];

    const prepositions = [
      'de', 'la', 'pe', 'pentru', 'contra', 'a', 'în', 'spre', 'cu', 'pe', 'din', 'spre', 'prin', 'între', 'sub', 'peste',
      'fără', 'de-a lungul', 'departe de', 'aproape de', 'deasupra', 'dedesubt', 'în jurul', 'în fața', 'în spatele', 'până la',
      'dincolo de', 'printre', 'alături de', 'împotriva', 'în favoarea', 'în detrimentul', 'în baza', 'în conformitate cu',
      'în ciuda', 'din cauza', 'datorită', 'grație', 'conform', 'potrivit', 'contrar', 'față de', 'în comparație cu', 'și'
    ];
    const shortWordsFilter = 2;

    for (const item of apiResponse) {
      const itemTokens = item.tokenized.map(token => token.word).join(' ');
      allTokens.push(itemTokens);
    }

    for (const tokens of allTokens) {
      const words = tokens.split(' ');
      for (const word of words) {
        if (word.length < shortWordsFilter || prepositions.includes(word.toLowerCase()) || word === '') {
          continue;
        }

        if (wordCounts[word]) {
          wordCounts[word]++;
        } else {
          wordCounts[word] = 1;
        }
      }
    }

    for (const word in wordCounts) {
      const processedItem = {
        text: word,
        value: wordCounts[word]
      };
      processedData.push(processedItem);
    }
    console.log(processedData)
    return processedData;
  }

  return (
    <Grid container spacing={gridSpacing} >
      <Grid item xs={12}>
        <MainCard title="Start scrapper">
          <SearchHeader handleSubmitEvent={fetchApi} />
        </MainCard>
      </Grid>
      <Grid item xs={12}>
        <MainCard title="Results">
          <NewsContainer data={news} />
        </MainCard>
      </Grid>
      <Grid item xs={12}>
        <MainCard title="Word Cloud">
          <WodCloudCustom data={data} />
        </MainCard>
      </Grid>
    </Grid >

  )
};

export default Scrappers;
