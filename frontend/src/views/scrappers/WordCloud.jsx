import React from 'react';

import WordCloud from 'react-d3-cloud';
import { scaleOrdinal } from 'd3-scale';
import { schemeCategory10 } from 'd3-scale-chromatic';


const WodCloudCustom = ({ data = [] }) => {
    const schemeCategory10ScaleOrdinal = scaleOrdinal(schemeCategory10);

    const processTokenizedData = (tokenizedData) => {
        const wordCount = {};

        tokenizedData.forEach(entry => {
            let concatenatedWord = '';
            entry.tokenized.forEach((token, index) => {
                concatenatedWord += token.word.replace(/▁/g, ''); // Remove special character

                // Check if the next token should be concatenated
                const nextToken = entry.tokenized[index + 1];
                if (nextToken && nextToken.start === token.end) {
                    return; // Continue concatenating
                }

                // Add or update the word count
                if (wordCount[concatenatedWord]) {
                    wordCount[concatenatedWord] += 1;
                } else {
                    wordCount[concatenatedWord] = 1;
                }
                concatenatedWord = ''; // Reset for the next word
            });
        });

        // Convert the word count object to an array of { text, value } objects
        let result =  Object.keys(wordCount).map(word => ({
            text: word,
            value: wordCount[word],
        }));
        console.log(result)
        return result;
    }
    console.log(data)
    return (
        <WordCloud
            data={data}
            width={300}
            height={50}
            font="Times"
            fontStyle="italic"
            fontWeight="bold"
            fontSize={(word) => Math.log2(word.value) * 5}
            spiral="rectangular"
            rotate={(word) => word.value % 360}
            padding={5}
            random={Math.random}
            fill={(d, i) => schemeCategory10ScaleOrdinal(i)}
            onWordClick={(event, d) => {
                console.log(`onWordClick: ${d.text}`);
            }}
            onWordMouseOver={(event, d) => {
                console.log(`onWordMouseOver: ${d.text}`);
            }}
            onWordMouseOut={(event, d) => {
                console.log(`onWordMouseOut: ${d.text}`);
            }}
        />
    );
}

export default WodCloudCustom;
