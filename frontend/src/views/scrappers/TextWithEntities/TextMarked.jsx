import { Typography } from '@mui/material';
import './style.css';

import Badge from '@mui/material/Badge';

const parseText = (text) => {
    const regex = /\[([^\]]+)\s\((I-[A-Z]+)\)\]/g;
    const parts = [];
    let lastIndex = 0;

    let match;
    while ((match = regex.exec(text)) !== null) {
        const [fullMatch, entityText, entityType] = match;
        const index = match.index;

        // Add the text before the entity
        if (index > lastIndex) {
            parts.push({
                text: text.slice(lastIndex, index),
                type: null,
            });
        }

        // Add the entity
        parts.push({
            text: entityText,
            type: entityType,
        });

        lastIndex = index + fullMatch.length;
    }

    // Add any remaining text after the last entity
    if (lastIndex < text.length) {
        parts.push({
            text: text.slice(lastIndex),
            type: null,
        });
    }

    return parts;
};

const TextOutPut = (text)=>{}

const TextWithEntities = ({ text }) => {
    const parsedText = parseText(text);

    return (
        <Typography>
            {parsedText.map((part, index) => {
                if (part.type) {
                    return (
                        <span key={index} className={`entity-${part.type}`}>
                            {part.text}
                        </span>
                    );
                } else {
                    return part.text;
                }
            })}
        </Typography>
    );
};

export default TextWithEntities;