
import { Box } from '@mui/system';
import { news } from 'mock/scrapper';

import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import AddIcon from '@mui/icons-material/Add';
import TextWithEntities from './TextWithEntities/TextMarked';

const NewsContainer = ({ data = [] }) => {
    return (<Box>
        {
            news.map((elem, i) => (
                <Accordion key={i}>
                    <AccordionSummary
                        expandIcon={<AddIcon />}
                        aria-controls="panel2-content"
                        id="panel2-header"
                    >
                        <TextWithEntities text={elem.marked_entities_text}/>
                    </AccordionSummary>
                    <AccordionDetails>
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse
                        malesuada lacus ex, sit amet blandit leo lobortis eget.
                    </AccordionDetails>
                </Accordion>
            ))
        }
    </Box>)
}

export default NewsContainer;