import React, { createContext, useContext, useState, ReactNode } from 'react';

interface PageContextType {
  page: number;
  pagesCount: number;
  setPage: (page: number) => void;
  setPagesCount: (count: number) => void;
}

const PageContext = createContext<PageContextType | undefined>(undefined);

export const PageProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [page, setPage] = useState<number>(0);
  const [pagesCount, setPagesCount] = useState<number>(1);

  return (
    <PageContext.Provider value={{ page, pagesCount, setPage, setPagesCount }}>
      {children}
    </PageContext.Provider>
  );
};

export const usePageContext = (): PageContextType => {
  const context = useContext(PageContext);
  if (!context) {
    throw new Error('usePageContext must be used within a PageProvider');
  }
  return context;
};
