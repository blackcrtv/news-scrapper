
import { Box } from '@mui/system';

import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import AddIcon from '@mui/icons-material/Add';
import TextWithEntities from './TextWithEntities/TextMarked';

const entityTypes = [
    { type: 'I-PER', name: 'Person', color: 'blue' },
    { type: 'I-ORG', name: 'Organization', color: 'green' },
    { type: 'I-LOC', name: 'Location', color: 'red' },
    { type: 'I-MISC', name: 'Miscellaneous', color: 'purple' }
];

const NewsContainer = ({ data = [] }) => {
    return (
        <Box>
            <div style={{
                display: "flex",
                gap: ".25rem",
                justifyContent: "flex-end"
            }}>
                {entityTypes.map((entity) => (
                    <div key={entity.type} style={{ display: 'flex', alignItems: 'center', marginBottom: '8px' }}>
                        <span style={{ color: entity.color, fontWeight: 'bold', marginRight: '8px' }}>■</span>
                        <span>{entity.name}</span>
                    </div>
                ))}
            </div>
            {
                data.map((elem, i) => (
                    <Accordion key={i}>
                        <AccordionSummary
                            expandIcon={<AddIcon />}
                            aria-controls="panel2-content"
                            id="panel2-header"
                        >
                            <TextWithEntities text={elem.marked_entities_text} />
                        </AccordionSummary>
                        <AccordionDetails>
                            {
                                elem.text
                            }
                        </AccordionDetails>
                    </Accordion>
                ))
            }
        </Box>)
}

export default NewsContainer;