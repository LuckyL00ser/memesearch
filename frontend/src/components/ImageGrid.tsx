import React from 'react';
import Masonry, { ResponsiveMasonry } from 'react-responsive-masonry';
import { useMemesContext } from '../providers/MemesContext';
import MemeRect from './MemeRect';

interface ImageGridProps {
  onMemeClick: (meme: Meme) => void;
}

export const ImageGrid: React.FC<ImageGridProps> = ({ onMemeClick }) => {
  const { memes } = useMemesContext();

  return (
    <section className="">
      <ResponsiveMasonry columnsCountBreakPoints={{ 350: 1, 550: 2, 900: 3 }}>
        <Masonry gutter="8px">
          {memes.map((m) => (
            <MemeRect meme={m} key={m.id} onClick={() => onMemeClick(m)} />
          ))}
        </Masonry>
      </ResponsiveMasonry>
    </section>
  );
};
