import React, { useState } from 'react';
import { ImageGrid } from './ImageGrid';
import { Popup } from './Popup';

export const MemeGallery: React.FC = () => {
  const [selectedMeme, setSelectedMeme] = useState<Meme | null>(null);

  const handleMemeClick = (meme: Meme) => {
    setSelectedMeme(meme);
  };

  const closePopup = () => {
    setSelectedMeme(null);
  };

  return (
    <div>
      <ImageGrid onMemeClick={handleMemeClick} />
      {selectedMeme && (
        <Popup meme={selectedMeme} onClose={closePopup} />
      )}
    </div>
  );
};