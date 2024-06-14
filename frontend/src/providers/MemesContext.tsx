import React, { createContext, useContext, useState, ReactNode } from 'react';

interface MemesContextType {
  memes: Meme[];
  setMemes: (memes: Meme[]) => void;
}

const MemesContext = createContext<MemesContextType | undefined>(undefined);

export const MemesProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [memes, _setMemes] = useState<Meme[]>([]);

  const setMemes = (memes: Meme[]) => {
    _setMemes(memes)
  }

  return (
    <MemesContext.Provider value={{ memes, setMemes }}>
      {children}
    </MemesContext.Provider>
  );
};

export const useMemesContext = (): MemesContextType => {
  const context = useContext(MemesContext);
  if (!context) {
    throw new Error('useMemesContext must be used within a MemesProvider');
  }
  return context;
};
